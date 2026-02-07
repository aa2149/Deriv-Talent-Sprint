"""
Phase 2: Slack HR Assistant Bot
================================
Uses Gemini + File Search (RAG) for policy questions.
Connects to the same data layer as the ADK agent.

Setup: See README.md for Slack app creation steps.
Run:   python bot.py
"""

import os
import sys
import time
import mimetypes
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from google import genai
from google.genai import types

load_dotenv()

# ── Clients ──────────────────────────────────────────────
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
client = genai.Client()

# ── Knowledge Base Setup (File Search) ───────────────────
DOCS_FOLDER = os.path.join(os.path.dirname(__file__), "..", "hr_agent", "docs")


def setup_knowledge_base():
    """Upload HR policy docs to Gemini File Search store for RAG."""
    store_name = "Deriv-HR-Knowledge-Base"
    target_store = None

    for store in client.file_search_stores.list():
        if store.display_name == store_name:
            target_store = store
            break

    if not target_store:
        print("[KB] Creating new knowledge base store...")
        target_store = client.file_search_stores.create(
            config={"display_name": store_name}
        )

    # Check existing files to avoid duplicates
    existing_files = set()
    try:
        for doc in client.file_search_stores.documents.list(parent=target_store.name):
            existing_files.add(doc.display_name)
    except Exception as e:
        print(f"[KB] Note: {e}")

    # Upload docs
    if os.path.exists(DOCS_FOLDER):
        for filename in os.listdir(DOCS_FOLDER):
            if filename in existing_files:
                print(f"[KB] Skipping {filename} — already uploaded")
                continue
            filepath = os.path.join(DOCS_FOLDER, filename)
            if os.path.isfile(filepath):
                mime_type, _ = mimetypes.guess_type(filepath)
                if not mime_type:
                    mime_type = "text/plain"
                print(f"[KB] Uploading {filename} ({mime_type})...")
                with open(filepath, "rb") as f:
                    op = client.file_search_stores.upload_to_file_search_store(
                        file=f,
                        file_search_store_name=target_store.name,
                        config={"display_name": filename, "mime_type": mime_type},
                    )
                while not op.done:
                    time.sleep(2)
                    op = client.operations.get(op)
                print(f"[KB] ✓ {filename} uploaded")
    else:
        print(f"[KB] Warning: docs folder not found at {DOCS_FOLDER}")

    return target_store.name


print("[BOOT] Setting up knowledge base...")
STORE_ID = setup_knowledge_base()
print(f"[BOOT] Knowledge base ready: {STORE_ID}")

# ── System Prompt ────────────────────────────────────────
SYSTEM_PROMPT = """You are the Deriv HR Assistant, available in Slack. You help employees with:

1. **Policy Questions** — Use the knowledge base to answer questions about leave, expenses, benefits, promotions, remote work, compliance, and onboarding. Always give specific numbers and cite the policy.

2. **Common Requests** — Guide employees through self-service processes:
   - Leave balance inquiries
   - Expense policy questions
   - Benefits information
   - Onboarding questions for new hires

3. **Compliance Awareness** — If an employee asks about visas, certifications, or equipment, remind them of deadlines and renewal processes.

Guidelines:
- Be concise and friendly — this is Slack, not a formal letter.
- Use bullet points for clarity when listing multiple items.
- If you can't find the answer in the knowledge base, say so and recommend contacting hr@deriv.com.
- Never make up policy information. Only cite what's in the knowledge base.
- For sensitive requests (salary changes, complaints), direct to HR directly.

You represent Deriv's employer brand — be helpful, professional, and warm.
"""

# ── Event Handlers ───────────────────────────────────────


@app.event("app_mention")
def handle_mention(body, say):
    """Respond when @mentioned in a channel."""
    event = body["event"]
    thread_ts = event.get("thread_ts", event["ts"])
    user_query = event.get("text", "").strip()

    # Remove the bot mention from the query
    if "<@" in user_query:
        user_query = user_query.split(">", 1)[-1].strip()

    if not user_query:
        say(text="Hi! I'm the Deriv HR Assistant. Ask me about leave policy, expenses, benefits, or anything HR-related!", thread_ts=thread_ts)
        return

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_query,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=[STORE_ID]
                        )
                    )
                ],
                system_instruction=SYSTEM_PROMPT,
            ),
        )
        say(text=response.text, thread_ts=thread_ts)

    except Exception as e:
        print(f"[ERROR] {e}")
        say(
            text="I'm having trouble right now. Please try again or contact hr@deriv.com for urgent matters.",
            thread_ts=thread_ts,
        )


@app.event("message")
def handle_dm(body, say):
    """Respond to direct messages."""
    event = body["event"]

    # Skip bot messages, message_changed events, etc.
    if event.get("subtype"):
        return
    if event.get("bot_id"):
        return

    # Only respond to DMs (channel type "im")
    if event.get("channel_type") != "im":
        return

    user_query = event.get("text", "").strip()
    if not user_query:
        return

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_query,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=[STORE_ID]
                        )
                    )
                ],
                system_instruction=SYSTEM_PROMPT,
            ),
        )
        say(text=response.text)

    except Exception as e:
        print(f"[ERROR] {e}")
        say(text="I'm having trouble right now. Please try again or contact hr@deriv.com.")


# ── Main ─────────────────────────────────────────────────
if __name__ == "__main__":
    print("[BOOT] Starting Deriv HR Slack Bot...")
    print("[BOOT] Listening for @mentions and DMs...")
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()
