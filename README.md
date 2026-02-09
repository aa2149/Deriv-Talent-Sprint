# Deriv Self-Service HR Operations Platform

**Deriv AI Talent Sprint 2026 · HR & Operations Challenge**

> An AI-powered self-service platform where contracts generate themselves, queries answer themselves, and HR operations become invisible.

🌐 **Live Demo:** https://deriv-hr-platform-520393715152.africa-south1.run.app

---

## What This Does

An AI agent built with Google Gemini that automates HR operations across 3 phases:

| Phase | Capability |
|-------|-----------|
| 🛡 **Compliance Intelligence** | Autonomous compliance scanning across jurisdictions (UAE, Malaysia, Malta) with risk assessment and financial projection |
| 📄 **Document Generation** | Generates employment contracts, offer letters, NDAs, and equity grants with jurisdiction-specific legal clauses |
| 💬 **HR Policy Assistant** | Answers employee queries instantly using RAG over HR knowledge base |

**The Problem:** Deriv operates across 3 countries with different labor laws. HR teams spend hours on manual contract creation, field repetitive policy questions, and track compliance in spreadsheets. Past incidents cost $24,400 and averaged 18 days to resolve.

**The Solution:** This platform automates all three areas using Gemini 2.5 Flash with 12 specialized tools.

---

## Quick Start

### Prerequisites

- Python 3.9+
- Google Gemini API key — get yours at https://aistudio.google.com/apikey

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd finallll/deriv_hr_platform

# Create virtual environment
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
# .venv\Scripts\activate        # Windows

# Install dependencies
pip install -r requirements.txt
```

### Configuration

```bash
# Copy the example environment file
cd hr_agent
cp .env.example .env
```

Edit `hr_agent/.env` and add your API key:
```
GOOGLE_API_KEY=your_api_key_here
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

### Run the Platform

```bash
# From deriv_hr_platform/ directory
cd ..
python server.py
```

Open your browser to: **http://localhost:8080**

---

## Project Structure

```
deriv_hr_platform/
├── server.py                   # FastAPI server - START HERE
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Cloud Run deployment config
│
├── frontend/
│   └── index.html              # Dashboard with live chat interface
│
├── hr_agent/                   # AI agent package
│   ├── agent.py                # 12 tools across 3 phases
│   ├── .env.example            # Environment template
│   ├── data/                   # Compliance data (employees, visas, certs)
│   └── docs/                   # Knowledge base (HR policies, templates)
│
└── slack_bot/                  # Optional Slack integration
    ├── bot.py
    └── .env.example
```

---

## Features

**12 AI Tools:**

- `generate_employment_contract` - Jurisdiction-aware contracts (UAE/Malaysia/Malta)
- `generate_offer_letter` - Role-specific offer letters
- `generate_nda` - Non-disclosure agreements
- `generate_equity_grant` - Equity grant documents
- `generate_complete_onboarding_package` - Full onboarding package
- `lookup_hr_policy` - RAG-based policy search
- `get_employee_info` - Employee data retrieval
- `process_hr_request` - General HR query handling
- `scan_all_compliance_data` - Autonomous compliance scanning
- `get_employee_deep_dive` - Detailed employee compliance check
- `get_organizational_risk_data` - Organization-wide risk analysis
- `simulate_future_risk` - Future risk projection

**Key Capabilities:**

- Jurisdiction-aware legal clause generation (UAE probation law, MOHRE, WPS vs Malaysia EPF vs Malta GDPR)
- Cross-correlation of compliance risks (visa + certification + department sensitivity)
- Financial exposure projection based on historical incident costs
- Real-time conversational HR assistant

---

## Architecture

```
Frontend (index.html)
    ↓ HTTP
FastAPI Server (server.py)
    ↓ /api/chat
ADK Agent (hr_agent/agent.py)
    ↓
Gemini 2.5 Flash API
    ↓
Tools → Data (CSV) + Docs (TXT)
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Agent Offline" in dashboard | Check `hr_agent/.env` has valid `GOOGLE_API_KEY` |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` in activated venv |
| Server won't start | Ensure you're in `deriv_hr_platform/` when running `python server.py` |
| Chat returns errors | Verify API key at https://aistudio.google.com/apikey |

---

**Built with Google ADK + Gemini 2.5 Flash** · Live deployment on Cloud Run
