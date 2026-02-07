# Deriv Self-Service HR Operations Platform

**Team: We Are Builders**  
**Event:** Deriv AI Talent Sprint 2026 · HR & Operations Challenge

> *AI-powered self-service platform where contracts generate themselves, queries answer themselves, and HR operations become invisible.*

---

## 🚨 Problem Statement

HR teams at Deriv face repeated operational overhead:

- Manual creation of contracts, offer letters, NDAs, and equity docs per hire.
- Repetitive employee queries interrupt work daily.
- Compliance tracked via spreadsheets is error-prone.

**Impact:**  
6 past compliance incidents cost **$24,400** and averaged **18 days** to resolve. Expanding to new jurisdictions multiplies this complexity.

---

## 🛠 Our Solution

A **3-phase AI platform** that automates HR operations, built on Google ADK + Gemini AI:

| Phase | What it does | Key AI Feature |
|-------|-------------|----------------|
| **📄 Phase 1** | Auto-generates contracts, offer letters, NDAs, and equity grants | Jurisdiction-aware clause generation (UAE ≠ Malaysia ≠ Malta) |
| **💬 Phase 2** | Slack bot answers HR queries instantly | RAG over HR handbook using Gemini File Search |
| **🛡 Phase 3** | Autonomous compliance agent monitors operations | Cross-correlates risk, applies jurisdiction severity, projects financial exposure |

**Before vs After:**

| Function | Before | After |
|----------|-------|------|
| Document generation | Hours per hire | Seconds, jurisdiction-correct |
| Policy questions | HR interrupted 100x/month | Slack bot responds instantly |
| Compliance monitoring | Monthly spreadsheets | Autonomous real-time scanning |
| Risk assessment | Isolated issues | AI cross-correlates multiple risks |
| Incident cost | $24,400 | ~80% reduction via proactive alerts |

---

## ⚡ Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/<your-org>/deriv_hr_platform.git
cd deriv_hr_platform

python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
pip install --upgrade pip
pip install -r requirements.txt
