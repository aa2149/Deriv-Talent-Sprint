"""
Deriv HR Platform — Server
===========================
Single server that:
  1. Runs the ADK agent (all 12 tools, 3 phases)
  2. Serves the frontend dashboard
  3. Exposes /api/chat for live agent interaction
  4. Deploys to Google Cloud Run (PORT env var)
"""

import asyncio
import os
import sys
import traceback
import uuid

from dotenv import load_dotenv

# Load env before importing agent
_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_dir, "hr_agent", ".env"))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Deriv HR Operations Platform")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── ADK Agent ────────────────────────────────────────────
runner = None
session_service = None
AGENT_OK = False

try:
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types as genai_types
    from hr_agent.agent import root_agent

    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="hr_agent",
        session_service=session_service,
    )
    AGENT_OK = True
    print("[SERVER] ✓ ADK agent loaded — 12 tools across 3 phases")
except Exception as e:
    print(f"[SERVER] ✗ Agent failed to load: {e}")
    traceback.print_exc()

_sessions: dict[str, str] = {}          # user_id -> session_id


# ── Health ───────────────────────────────────────────────

@app.get("/api/health")
async def health():
    return {"status": "ok", "agent": AGENT_OK, "tools": 12, "model": "gemini-2.5-flash"}


# ── Chat ─────────────────────────────────────────────────

@app.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    message = body.get("message", "").strip()
    user_id = body.get("user_id", "demo")

    if not message:
        return JSONResponse({"response": "Please type a message.", "ok": False})
    if not AGENT_OK:
        return JSONResponse({
            "response": "Agent not available — check GOOGLE_API_KEY in hr_agent/.env",
            "ok": False,
        })

    try:
        # Create session once per user
        if user_id not in _sessions:
            s = await session_service.create_session(
                app_name="hr_agent", user_id=user_id
            )
            _sessions[user_id] = s.id

        content = genai_types.Content(
            role="user",
            parts=[genai_types.Part.from_text(message)],
        )

        text_parts = []
        async for event in runner.run_async(
            user_id=user_id,
            session_id=_sessions[user_id],
            new_message=content,
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    for p in event.content.parts:
                        if hasattr(p, "text") and p.text:
                            text_parts.append(p.text)

        return JSONResponse({
            "response": "\n".join(text_parts) or "(No response from agent.)",
            "ok": True,
        })

    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"response": f"Error: {e}", "ok": False})


@app.post("/api/reset")
async def reset(request: Request):
    body = await request.json()
    uid = body.get("user_id", "demo")
    _sessions.pop(uid, None)
    return JSONResponse({"status": "reset"})


# ── Serve frontend (keep LAST so /api routes take priority) ──

_fe = os.path.join(_dir, "frontend")
if os.path.isdir(_fe):
    app.mount("/", StaticFiles(directory=_fe, html=True))
    print(f"[SERVER] ✓ Frontend: {_fe}")


# ── Run ──────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    print(f"\n  Deriv HR Platform → http://localhost:{port}\n")
    uvicorn.run(app, host="0.0.0.0", port=port)
