# Deriv Self-Service HR Operations Platform

**Deriv AI Talent Sprint 2026 · HR & Operations Challenge**

> *An AI-powered self-service platform where contracts generate themselves, queries answer themselves, and HR operations become invisible.*

🌐 **Live Demo:** https://deriv-hr-platform-520393715152.africa-south1.run.app

---

## The Problem

Deriv operates across **4 offices in 3 countries** (Malaysia, UAE, Malta) — each with different labor laws, visa rules, and compliance requirements.

**Today, every hire is a manual ordeal:** HR spends hours drafting jurisdiction-specific contracts, employees ask the same policy questions hundreds of times a month, and compliance is tracked in spreadsheets that no one checks until audit time.

**Cost of inaction:** 6 past compliance incidents cost **$24,400** and averaged **18 days** to resolve — after the damage was already done.

---

## What We Built

| Phase | What it does | AI Reasoning (not replaceable by rules) |
|-------|-------------|----------------------------------------|
| 🛡 **Compliance Intelligence** | Autonomous scan on every session — no prompting needed | Jurisdiction severity (UAE 90-day vs Malaysia 30-day), department sensitivity (AML + Finance = license risk), cross-correlation, pattern detection, financial projection |
| 📄 **Document Generation** | One command → offer + contract + NDA + equity grant | Adapts legal clauses per jurisdiction (UAE probation, MOHRE, WPS vs Malaysia EPF vs Malta GDPR) |
| 💬 **HR Policy Assistant** | Instant answers from HR knowledge base | RAG retrieval + synthesis — conversational answers with specific numbers, not document dumps |

---

## ⚡ Quick Start — Local Demo

### Prerequisites

- **Python 3.9+**
- **Google Gemini API key** — free at https://aistudio.google.com/apikey

### 1. Extract & Setup

```bash
unzip deriv_hr_platform.zip
cd deriv_hr

python -m venv .venv
source .venv/bin/activate       # macOS/Linux
# .venv\Scripts\activate        # Windows

pip install -r requirements.txt
```

### 2. Add Your API Key

```bash
cd hr_agent
cp .env.example .env
```

Edit `hr_agent/.env` — paste your key:
```
GOOGLE_API_KEY=AIzaSy...your_key_here
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

### 3. Run the Platform

```bash
cd ..   # back to deriv_hr/
python server.py
```

### 4. Open in Browser

```
http://localhost:8080
```

**That's it.** The frontend connects to the agent. Click any demo prompt or type a question.

---

## ☁️ Deploy to Google Cloud Run

### Prerequisites

- Google Cloud account with a project
- `gcloud` CLI installed (`brew install google-cloud-sdk` or https://cloud.google.com/sdk/docs/install)
- Google Gemini API key from https://aistudio.google.com/apikey

### Deploy with Cloud Build

```bash
# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build the Docker image
gcloud builds submit --tag REGION-docker.pkg.dev/YOUR_PROJECT_ID/cloud-run-source-deploy/deriv-hr-platform:latest

# Deploy to Cloud Run with environment variables
gcloud run deploy deriv-hr-platform \
  --image REGION-docker.pkg.dev/YOUR_PROJECT_ID/cloud-run-source-deploy/deriv-hr-platform:latest \
  --platform managed \
  --region REGION \
  --allow-unauthenticated \
  --set-env-vars "GOOGLE_API_KEY=YOUR_API_KEY,GEMINI_API_KEY=YOUR_API_KEY" \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300
```

**🔒 IMPORTANT: Secure Your API Key**

After deployment, immediately add API restrictions:

1. Go to https://console.cloud.google.com/apis/credentials
2. Find your API key → Click Edit
3. Under "API restrictions" → Select "Restrict key"
4. Check ONLY: **Generative Language API**
5. Save

This prevents your API key from being used for other Google services if exposed.

### Live Production Deployment

Our production deployment is live at:
- **URL:** https://deriv-hr-platform-520393715152.africa-south1.run.app
- **Region:** africa-south1
- **Resources:** 2Gi memory, 2 CPU
- **Features:** All 3 phases, 12 tools, full frontend

---

## Slack Bot Setup (Phase 2)

The Slack bot is a separate process that uses Gemini + File Search RAG.

### 1. Create a Slack App

1. https://api.slack.com/apps → **Create New App** → **From scratch**
2. Name: `Deriv HR Bot` → pick your workspace → **Create**

### 2. Enable Socket Mode

1. **Settings → Socket Mode → Toggle ON**
2. Token name: `socket-token` → **Generate**
3. Copy the token → this is your `SLACK_APP_TOKEN` (starts with `xapp-`)

### 3. Add Bot Scopes

**OAuth & Permissions → Bot Token Scopes** → add:

`app_mentions:read` · `chat:write` · `im:history` · `im:read` · `im:write`

### 4. Subscribe to Events

**Event Subscriptions → Enable → Subscribe to bot events** → add:

`app_mention` · `message.im` → **Save**

### 5. Install & Run

1. **Install App → Install to Workspace → Allow**
2. Copy the **Bot User OAuth Token** → `SLACK_BOT_TOKEN` (starts with `xoxb-`)

```bash
cd deriv_hr/slack_bot
cp .env.example .env
# Edit .env with your 3 tokens: SLACK_BOT_TOKEN, SLACK_APP_TOKEN, GEMINI_API_KEY

python bot.py
```

Test in Slack:
```
@Deriv HR Bot How many leave days do I get?
@Deriv HR Bot Can I expense a coworking space?
```

---

## 🎬 Demo Script (5 minutes)

### Opening — 30 sec

> *"We built a complete HR operations platform — all 3 phases. Contracts generate themselves, queries answer themselves, compliance monitors itself. This is a live agent running on Gemini 2.5 Flash with 12 AI tools. Let me show you."*

### 🛡 Phase 3 — Lead with autonomy (90 sec)

Click **"Compliance Scan"** on the dashboard. The agent runs a full scan.

> *"I didn't tell it what to look for. It autonomously analyzed 20 employees across 3 jurisdictions. Look at the reasoning — it's not just 'visa expires in X days.' It knows a UAE visa with 20 days left is CRITICAL because UAE law requires 90-day advance renewal. It knows an expired AML certification in the Finance department is a LICENSE RISK for a regulated fintech."*

Then click **"Simulate: what happens in 30 days?"**

> *"It projects forward — items that were yellow become red, and it estimates financial exposure based on our past $24,400 in incident costs."*

### 📄 Phase 1 — Invisible onboarding (60 sec)

Click **"Generate Onboarding (Dubai)"**

> *"One command — the agent generates an offer letter, employment contract, NDA, and equity grant. The contract has UAE-specific clauses: 6-month probation per Federal Decree-Law 33/2021, MOHRE registration, Wages Protection System. If I change the location to Malta, it uses EU GDPR clauses and different notice periods. It's reasoning about jurisdiction — not filling templates."*

### 💬 Phase 2 — HR assistant (60 sec)

Click **"What is the leave policy?"** or **"Can I expense coworking?"**

> *"Instant answer with specific numbers from our HR knowledge base. $300/month coworking limit, submit via Concur within 30 days. This is RAG — Gemini retrieves relevant policy sections and synthesizes a conversational answer. In Slack, employees just @mention the bot."*

### Close — 30 sec

> *"Three phases, all working, all deployed. The AI does 5 types of reasoning no rule-based system can replicate. That's our solution."*

---

## Architecture

```
┌──────────────────────────────────────────────┐
│              Frontend (index.html)             │
│    Dashboard + Live Chat → /api/chat          │
└───────────────────┬──────────────────────────┘
                    │ HTTP
┌───────────────────▼──────────────────────────┐
│              server.py (FastAPI)               │
│    /api/chat → ADK Runner → Gemini 2.5 Flash  │
│    /api/health, /api/reset                     │
└───────────────────┬──────────────────────────┘
                    │
┌───────────────────▼──────────────────────────┐
│         hr_agent/agent.py — 12 tools          │
│                                                │
│  Phase 1: generate_employment_contract         │
│           generate_offer_letter                │
│           generate_nda                         │
│           generate_equity_grant                │
│           generate_complete_onboarding_package  │
│                                                │
│  Phase 2: lookup_hr_policy                     │
│           get_employee_info                    │
│           process_hr_request                   │
│                                                │
│  Phase 3: scan_all_compliance_data             │
│           get_employee_deep_dive               │
│           get_organizational_risk_data         │
│           simulate_future_risk                 │
└───────────────────┬──────────────────────────┘
                    │
     ┌──────────────┼──────────────┐
     │              │              │
  data/*.csv    docs/*.txt    Gemini API
  (employees,   (HR handbook,  (reasoning)
   visas,        contract
   certs...)     templates)
```

---

## Project Structure

```
deriv_hr/
├── server.py               ← START HERE: python server.py
├── Dockerfile              ← Cloud Run deployment
├── .dockerignore
├── requirements.txt
├── README.md
│
├── frontend/
│   └── index.html          ← Live dashboard + agent chat
│
├── hr_agent/               ← ADK agent package
│   ├── __init__.py
│   ├── agent.py            ← 12 tools, 3 phases
│   ├── .env.example        ← Copy to .env, add API key
│   ├── data/               ← Synthetic compliance data
│   │   ├── employees.csv
│   │   ├── visas.csv
│   │   ├── certs.csv
│   │   ├── equipment.csv
│   │   ├── compliance_policies.csv
│   │   ├── incident_history.csv
│   │   └── audit_docs.csv
│   └── docs/               ← RAG knowledge base
│       ├── hr_policy_handbook.txt
│       └── contract_templates.txt
│
└── slack_bot/              ← Phase 2 Slack integration
    ├── bot.py
    └── .env.example
```

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Agent Offline` in dashboard header | Check `hr_agent/.env` has a valid `GOOGLE_API_KEY` |
| `ModuleNotFoundError: google.adk` | Run `pip install -r requirements.txt` in your venv |
| `ModuleNotFoundError: deprecated` | Update `requirements.txt` to include `Deprecated>=1.2.14` and reinstall |
| Server won't start | Make sure you run `python server.py` from `deriv_hr/` directory |
| Agent returns errors | Verify your Gemini API key at https://aistudio.google.com |
| `403 PERMISSION_DENIED` | API key is leaked/restricted. Create a new key at https://aistudio.google.com/apikey |
| Cloud Run deploy fails | Ensure `gcloud` is authenticated and project ID is correct |
| Chat returns JSON serialization error | Telemetry issue with bytes - ensure `OTEL_SDK_DISABLED=true` is set or use the patched `server.py` |
| Slack bot doesn't respond | Check tokens in `slack_bot/.env`, ensure bot is added to channel |

## Technical Notes

### Security Best Practices
- Never commit `.env` files to git (already in `.gitignore`)
- Always add API key restrictions immediately after creating a key
- For production, use Google Secret Manager instead of environment variables
- Rotate API keys every 90 days

### Deployment Architecture
- **Runtime:** Python 3.11 on Cloud Run
- **AI Model:** Google Gemini 2.5 Flash via ADK (Agent Development Kit)
- **Session Management:** In-memory sessions (suitable for demo/small scale)
- **Frontend:** Single-page dashboard with live chat interface
- **Backend:** FastAPI server with `/api/chat`, `/api/health` endpoints

### Dependencies Fixed During Development
- Added `Deprecated>=1.2.14` for ADK telemetry compatibility
- Monkey-patched `json.dumps` to handle bytes serialization in telemetry
- Fixed async/await session creation (ADK Runner compatibility)
- Updated `Part` API usage from `Part.from_text()` to `Part(text=...)`

---

**Deriv AI Talent Sprint 2026** · All 3 Phases · Live Agent Demo · Cloud Run Ready
