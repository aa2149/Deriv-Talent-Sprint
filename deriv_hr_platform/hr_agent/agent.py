"""
Deriv Self-Service HR Operations Platform
==========================================
Deriv AI Talent Sprint 2026

Three phases, one agent:
  Phase 1 — Intelligent Document Generation
  Phase 2 — Conversational HR Assistant  
  Phase 3 — Proactive Compliance Intelligence

Architecture: Tools = Data Sensors | AI = Reasoning Engine
"""

import os
from datetime import datetime, timedelta

import pandas as pd
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

# ============================================================
# DATA LAYER
# ============================================================

_BASE = os.path.dirname(os.path.abspath(__file__))
_DATA = os.path.join(_BASE, "data")
_DOCS = os.path.join(_BASE, "docs")


def _load(name: str) -> pd.DataFrame:
    p = os.path.join(_DATA, f"{name}.csv")
    return pd.read_csv(p) if os.path.exists(p) else pd.DataFrame()


def _days_until(date_str: str) -> int:
    try:
        return (datetime.strptime(str(date_str), "%Y-%m-%d") - datetime.today()).days
    except Exception:
        return -9999


def _read_doc(name: str) -> str:
    p = os.path.join(_DOCS, name)
    if os.path.exists(p):
        with open(p, "r") as f:
            return f.read()
    return ""


# ============================================================
# PHASE 1: INTELLIGENT DOCUMENT GENERATION
# ============================================================


def generate_employment_contract(
    employee_name: str,
    role: str,
    department: str,
    annual_salary: float,
    currency: str,
    location: str,
    start_date: str,
    tool_context: ToolContext,
) -> dict:
    """
    Generate a complete employment contract for a new hire.
    Returns the jurisdiction-specific legal template data that the AI
    must use to compose a professional, legally accurate contract.

    The AI should generate the FULL contract text using the template
    data and jurisdiction rules provided, adapting clauses appropriately.

    Args:
        employee_name: Full legal name of the employee
        role: Job title (e.g. "Senior Software Engineer")
        department: Department (e.g. "Engineering", "Finance")
        annual_salary: Annual base salary amount
        currency: Currency code (MYR, AED, EUR, USD)
        location: Office location (Cyberjaya, Dubai, Malta, Labuan)
        start_date: Employment start date (YYYY-MM-DD)
    """
    templates = _read_doc("contract_templates.txt")

    # Jurisdiction mapping
    jurisdiction_map = {
        "Cyberjaya": {
            "country": "Malaysia",
            "governing_law": "Employment Act 1955",
            "probation": "3 months",
            "notice_period": "1 month",
            "pension": "EPF — Employer 13%, Employee 11%",
            "working_hours": "45 hours/week",
            "leave": "25 days annual + 11 public holidays",
            "maternity": "98 days (Employment Act), Deriv provides 90 days full pay",
            "non_compete": "Non-solicitation 12 months (non-compete generally unenforceable)",
        },
        "Labuan": {
            "country": "Malaysia (Labuan)",
            "governing_law": "Sabah Labour Ordinance",
            "probation": "3 months",
            "notice_period": "1 month",
            "pension": "EPF — Employer 13%, Employee 11%",
            "working_hours": "45 hours/week",
            "leave": "25 days annual + 11 public holidays",
            "maternity": "98 days (Employment Act), Deriv provides 90 days full pay",
            "non_compete": "Non-solicitation 12 months",
        },
        "Dubai": {
            "country": "UAE",
            "governing_law": "UAE Federal Decree-Law No. 33 of 2021",
            "probation": "6 months",
            "notice_period": "30 days",
            "pension": "End of Service Gratuity (21 days/year first 5 years, 30 days after)",
            "working_hours": "48 hours/week (6 hours during Ramadan)",
            "leave": "25 working days annual + 10 public holidays",
            "maternity": "60 days UAE law (45 full + 15 half pay), Deriv tops up to 90 days",
            "non_compete": "Up to 2 years, must be reasonable in scope",
            "special": "Contract must be registered with MOHRE. WPS compliance required. Arabic version prevails in disputes.",
        },
        "Malta": {
            "country": "Malta (EU)",
            "governing_law": "Employment and Industrial Relations Act (EIRA), Chapter 452",
            "probation": "6 months (12 months if salary > EUR 25,000)",
            "notice_period": "1 week per year of service (min 1 week, max 12 weeks)",
            "pension": "Social Security employer contribution 10%",
            "working_hours": "40 hours/week (EU Working Time Directive max 48)",
            "leave": "25 days annual + 14 public holidays",
            "maternity": "18 weeks (14 government-paid), Deriv provides 90 days full pay",
            "non_compete": "6-12 months if reasonable",
            "special": "Full EU GDPR compliance required. EU Working Time Directive applies.",
        },
    }

    jurisdiction = jurisdiction_map.get(location, jurisdiction_map["Cyberjaya"])

    # Determine mandatory certs based on department
    mandatory_certs = ["Safety Training"]
    if department in ("Finance", "Compliance"):
        mandatory_certs.append("Anti-Money Laundering (AML)")
    if department == "HR":
        mandatory_certs.append("HR Compliance Certification")
    if location in ("Dubai", "Malta"):
        mandatory_certs.append("Fire Safety")
    mandatory_certs.append("Data Privacy / GDPR")

    # Generate contract ID
    contract_id = f"CONTRACT-{datetime.now().strftime('%Y%m%d')}-{employee_name.split()[0].upper()[:3]}{hash(employee_name) % 1000:03d}"

    return {
        "contract_id": contract_id,
        "employee_name": employee_name,
        "role": role,
        "department": department,
        "annual_salary": annual_salary,
        "currency": currency,
        "location": location,
        "start_date": start_date,
        "jurisdiction": jurisdiction,
        "mandatory_certifications": mandatory_certs,
        "equity_eligible": True,
        "template_reference": templates[:3000] if templates else "Standard Deriv employment contract template",
        "instruction_to_ai": (
            f"Generate a COMPLETE, professional employment contract for {employee_name} "
            f"in {location} ({jurisdiction['country']}). Use the jurisdiction data to include "
            f"correct legal clauses for: governing law, probation period, notice period, "
            f"pension/retirement, working hours, leave entitlement, and any special provisions. "
            f"The contract should look like a real legal document with numbered sections. "
            f"Include: (1) Parties, (2) Position & Duties, (3) Compensation, (4) Benefits, "
            f"(5) Working Hours, (6) Leave, (7) Probation, (8) Termination & Notice, "
            f"(9) Confidentiality, (10) Intellectual Property, (11) Governing Law. "
            f"Make it jurisdiction-appropriate — this is where AI adds real value."
        ),
    }


def generate_offer_letter(
    employee_name: str,
    role: str,
    department: str,
    annual_salary: float,
    currency: str,
    location: str,
    start_date: str,
    tool_context: ToolContext,
) -> dict:
    """
    Generate a professional offer letter for a candidate.
    The AI should produce a warm, professional letter that includes
    all key terms while being appropriate for the jurisdiction.

    Args:
        employee_name: Candidate's full name
        role: Job title offered
        department: Department
        annual_salary: Offered annual salary
        currency: Currency code
        location: Office location
        start_date: Proposed start date (YYYY-MM-DD)
    """
    offer_id = f"OFFER-{datetime.now().strftime('%Y%m%d')}-{employee_name.split()[0].upper()[:3]}{hash(employee_name) % 1000:03d}"

    benefits_summary = {
        "annual_leave": "25 days + public holidays",
        "health_insurance": "Comprehensive coverage for employee and dependents",
        "life_insurance": "4x annual salary",
        "wellness": "$100/month fitness reimbursement",
        "learning": "$2,000 annual professional development budget",
        "equity": "Stock options per Deriv equity plan (details in separate grant letter)",
    }

    return {
        "offer_id": offer_id,
        "employee_name": employee_name,
        "role": role,
        "department": department,
        "salary": f"{currency} {annual_salary:,.2f}",
        "location": location,
        "start_date": start_date,
        "benefits_summary": benefits_summary,
        "response_deadline": (datetime.today() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "instruction_to_ai": (
            f"Generate a professional, warm offer letter from Deriv to {employee_name}. "
            f"Include: congratulations, role details, compensation, key benefits highlights, "
            f"start date, and next steps (signing, onboarding). Keep it professional but "
            f"enthusiastic. This letter represents Deriv's employer brand."
        ),
    }


def generate_nda(
    employee_name: str,
    role: str,
    location: str,
    tool_context: ToolContext,
) -> dict:
    """
    Generate a Non-Disclosure Agreement appropriate for the employee's jurisdiction.

    Args:
        employee_name: Employee's full name
        role: Job title
        location: Office location (determines governing law)
    """
    templates = _read_doc("contract_templates.txt")
    nda_id = f"NDA-{datetime.now().strftime('%Y%m%d')}-{employee_name.split()[0].upper()[:3]}{hash(employee_name) % 1000:03d}"

    jurisdiction_law = {
        "Cyberjaya": "Malaysian law",
        "Labuan": "Malaysian law",
        "Dubai": "UAE Federal Law",
        "Malta": "Maltese law / EU GDPR",
    }

    return {
        "nda_id": nda_id,
        "employee_name": employee_name,
        "role": role,
        "location": location,
        "governing_law": jurisdiction_law.get(location, "Malaysian law"),
        "duration": "Indefinite for trade secrets, 3 years for other confidential information",
        "template_reference": "See NDA STANDARD TERMS in contract templates",
        "instruction_to_ai": (
            f"Generate a professional Non-Disclosure Agreement for {employee_name} ({role}) "
            f"at the {location} office. Include standard NDA sections: definitions of "
            f"confidential information, obligations, exclusions, term, remedies, and return "
            f"of materials. Apply {jurisdiction_law.get(location, 'applicable')} law."
        ),
    }


def generate_equity_grant(
    employee_name: str,
    role: str,
    level: str,
    location: str,
    tool_context: ToolContext,
) -> dict:
    """
    Generate an equity/stock option grant letter based on employee level.

    Args:
        employee_name: Employee's full name
        role: Job title
        level: Seniority level (junior, mid, senior, lead, director)
        location: Office location
    """
    grant_ranges = {
        "junior": (1000, 5000),
        "mid": (5000, 15000),
        "senior": (15000, 40000),
        "lead": (40000, 100000),
        "director": (100000, 200000),
    }
    low, high = grant_ranges.get(level.lower(), (5000, 15000))
    recommended = (low + high) // 2

    grant_id = f"EQUITY-{datetime.now().strftime('%Y%m%d')}-{employee_name.split()[0].upper()[:3]}{hash(employee_name) % 1000:03d}"

    return {
        "grant_id": grant_id,
        "employee_name": employee_name,
        "role": role,
        "level": level,
        "recommended_options": recommended,
        "grant_range": f"{low:,} - {high:,} options",
        "vesting_schedule": "4-year monthly vesting with 1-year cliff (25% at year 1, then 2.083%/month)",
        "exercise_price": "Fair Market Value on grant date",
        "exercise_window": "90 days post-termination (12 months for good leavers with 4+ years)",
        "acceleration": "100% on Change of Control (double-trigger)",
        "instruction_to_ai": (
            f"Generate a formal Stock Option Grant Letter for {employee_name}. "
            f"Include: grant details, vesting schedule, exercise terms, and standard conditions. "
            f"Make it clear and professional — employees should understand their equity."
        ),
    }


def generate_complete_onboarding_package(
    employee_name: str,
    role: str,
    department: str,
    annual_salary: float,
    currency: str,
    location: str,
    start_date: str,
    level: str,
    tool_context: ToolContext,
) -> dict:
    """
    Generate a COMPLETE onboarding package: offer letter + contract + NDA + equity grant.
    This is the "invisible onboarding" — one command generates everything.

    This is the killer feature: acceptance triggers automatic generation of ALL documents.

    Args:
        employee_name: Full legal name
        role: Job title
        department: Department name
        annual_salary: Annual salary
        currency: Currency code (MYR, AED, EUR)
        location: Office location (Cyberjaya, Dubai, Malta, Labuan)
        start_date: Start date (YYYY-MM-DD)
        level: Seniority level (junior, mid, senior, lead, director)
    """
    package_id = f"ONBOARD-{datetime.now().strftime('%Y%m%d')}-{employee_name.split()[0].upper()[:3]}"

    # Call all generation tools
    offer = generate_offer_letter(employee_name, role, department, annual_salary, currency, location, start_date, tool_context)
    contract = generate_employment_contract(employee_name, role, department, annual_salary, currency, location, start_date, tool_context)
    nda = generate_nda(employee_name, role, location, tool_context)
    equity = generate_equity_grant(employee_name, role, level, location, tool_context)

    # Determine mandatory onboarding tasks
    onboarding_tasks = [
        {"day": "Pre-Day 1", "task": "IT provisions laptop, email, and system access", "owner": "IT"},
        {"day": "Pre-Day 1", "task": "Manager assigns onboarding buddy", "owner": "Manager"},
        {"day": "Day 1", "task": "Welcome session with HR", "owner": "HR"},
        {"day": "Day 1", "task": "Equipment handover and IT setup", "owner": "IT"},
        {"day": "Day 1", "task": "Manager 1:1 — 90-day goals", "owner": "Manager"},
        {"day": "Week 1", "task": f"Complete Safety Training certification", "owner": employee_name},
    ]

    if department in ("Finance", "Compliance"):
        onboarding_tasks.append({"day": "Week 1", "task": "Complete AML certification", "owner": employee_name})
    if location in ("Dubai", "Malta"):
        onboarding_tasks.append({"day": "Week 1", "task": "Complete Fire Safety certification", "owner": employee_name})

    onboarding_tasks.extend([
        {"day": "Week 2", "task": "Complete Data Privacy / GDPR training", "owner": employee_name},
        {"day": "Day 30", "task": "30-day check-in with manager", "owner": "Manager"},
        {"day": "Day 90", "task": "End of probation review", "owner": "Manager + HR"},
    ])

    return {
        "package_id": package_id,
        "status": "GENERATED",
        "employee_name": employee_name,
        "documents_generated": {
            "offer_letter": offer["offer_id"],
            "employment_contract": contract["contract_id"],
            "nda": nda["nda_id"],
            "equity_grant": equity["grant_id"],
        },
        "offer_letter_data": offer,
        "contract_data": contract,
        "nda_data": nda,
        "equity_data": equity,
        "onboarding_checklist": onboarding_tasks,
        "instruction_to_ai": (
            f"You have just generated a COMPLETE onboarding package for {employee_name}. "
            f"Present this as a cohesive summary showing all 4 documents generated, "
            f"the onboarding checklist, and next steps. Then generate EACH document fully "
            f"(the offer letter, employment contract, NDA, and equity grant letter) as "
            f"complete, professional legal documents. This demonstrates 'invisible onboarding' — "
            f"one trigger, everything happens automatically."
        ),
    }


# ============================================================
# PHASE 2: CONVERSATIONAL HR ASSISTANT
# ============================================================


def lookup_hr_policy(query: str, tool_context: ToolContext) -> dict:
    """
    Search the HR policy knowledge base for relevant information.
    Returns relevant policy sections that the AI should synthesize
    into a helpful, conversational answer.

    Use this when employees ask about: leave policy, expense policy,
    benefits, promotion criteria, remote work, onboarding, compliance,
    or any HR-related question.

    Args:
        query: The employee's question or topic (e.g. "annual leave", "expense coworking")
    """
    handbook = _read_doc("hr_policy_handbook.txt")
    if not handbook:
        return {"status": "error", "message": "HR policy handbook not found"}

    # Split into sections and find relevant ones
    sections = handbook.split("=== ")
    relevant = []
    query_lower = query.lower()

    # Keyword matching to find relevant sections
    keyword_map = {
        "leave": ["ANNUAL LEAVE", "PARENTAL", "SICK", "COMPASSIONATE"],
        "vacation": ["ANNUAL LEAVE"],
        "holiday": ["ANNUAL LEAVE"],
        "sick": ["ANNUAL LEAVE"],
        "maternity": ["ANNUAL LEAVE"],
        "paternity": ["ANNUAL LEAVE"],
        "expense": ["EXPENSE POLICY"],
        "reimburse": ["EXPENSE POLICY"],
        "cowork": ["EXPENSE POLICY", "REMOTE WORK"],
        "gym": ["EXPENSE POLICY", "BENEFITS"],
        "travel": ["EXPENSE POLICY"],
        "benefit": ["BENEFITS"],
        "health": ["BENEFITS"],
        "insurance": ["BENEFITS"],
        "pension": ["BENEFITS"],
        "stock": ["BENEFITS"],
        "equity": ["BENEFITS"],
        "option": ["BENEFITS"],
        "promot": ["PROMOTION"],
        "career": ["PROMOTION"],
        "review": ["PROMOTION"],
        "remote": ["REMOTE WORK"],
        "work from home": ["REMOTE WORK"],
        "wfh": ["REMOTE WORK"],
        "hybrid": ["REMOTE WORK"],
        "onboard": ["ONBOARDING"],
        "first day": ["ONBOARDING"],
        "new hire": ["ONBOARDING"],
        "visa": ["COMPLIANCE"],
        "compliance": ["COMPLIANCE"],
        "certif": ["COMPLIANCE"],
        "training": ["COMPLIANCE"],
        "nda": ["COMPLIANCE"],
        "contact": ["CONTACT"],
    }

    matched_section_names = set()
    for keyword, section_names in keyword_map.items():
        if keyword in query_lower:
            matched_section_names.update(section_names)

    for section in sections:
        section_upper = section.split("===")[0].strip().upper() if "===" in section else section[:50].upper()
        for name in matched_section_names:
            if name in section_upper:
                relevant.append(section.strip())

    # If no keyword match, return all sections for AI to reason over
    if not relevant:
        relevant = [s.strip() for s in sections if len(s.strip()) > 50][:3]

    return {
        "query": query,
        "relevant_policies": relevant,
        "total_sections_found": len(relevant),
        "instruction_to_ai": (
            f"An employee asked: '{query}'. Use the policy sections above to give a "
            f"clear, helpful, conversational answer. Be specific — cite numbers, amounts, "
            f"and deadlines. If the answer depends on their location or department, say so. "
            f"If you can't find the answer in the policies, say so honestly and suggest "
            f"they contact HR at hr@deriv.com."
        ),
    }


def get_employee_info(employee_id: str, tool_context: ToolContext) -> dict:
    """
    Get comprehensive information about an employee including their
    compliance status, leave balance, and personal details.
    The AI should use this to answer employee-specific questions.

    Args:
        employee_id: Employee ID (e.g. 'E101')
    """
    employees = _load("employees")
    visas = _load("visas")
    certs = _load("certs")
    equipment = _load("equipment")

    emp = employees.loc[employees["employee_id"] == employee_id]
    if len(emp) == 0:
        return {"status": "error", "message": f"Employee {employee_id} not found"}

    info = emp.iloc[0].to_dict()

    # Calculate tenure
    try:
        hire = datetime.strptime(str(info.get("hire_date", "")), "%Y-%m-%d")
        tenure_days = (datetime.today() - hire).days
        tenure_years = round(tenure_days / 365.25, 1)
    except Exception:
        tenure_years = 0

    # Simulate leave balance (25 days - used based on employee hash)
    import hashlib
    used = int(hashlib.md5(employee_id.encode()).hexdigest()[:2], 16) % 15
    leave_balance = {"total": 25, "used": used, "remaining": 25 - used}

    # Compliance status
    emp_visas = [
        {**v.to_dict(), "days_remaining": _days_until(v["expiry_date"])}
        for _, v in visas.loc[visas["employee_id"] == employee_id].iterrows()
    ]
    emp_certs = [
        {**c.to_dict(), "days_remaining": _days_until(c["expiry_date"])}
        for _, c in certs.loc[certs["employee_id"] == employee_id].iterrows()
    ]
    emp_equip = [
        {**e.to_dict(), "days_remaining": _days_until(e["return_due"])}
        for _, e in equipment.loc[equipment["employee_id"] == employee_id].iterrows()
    ]

    return {
        "employee": info,
        "tenure_years": tenure_years,
        "leave_balance": leave_balance,
        "visa_status": emp_visas,
        "certifications": emp_certs,
        "equipment": emp_equip,
        "instruction_to_ai": (
            f"Provide a comprehensive profile for {info.get('name', employee_id)}. "
            f"Include their role, location, tenure, leave balance, and compliance status. "
            f"Flag any compliance issues (expired or soon-expiring items)."
        ),
    }


def process_hr_request(
    employee_id: str,
    request_type: str,
    details: str,
    tool_context: ToolContext,
) -> dict:
    """
    Process an HR self-service request (address change, dependent add, etc.)
    The AI should confirm the request and explain next steps.

    Args:
        employee_id: Employee ID
        request_type: Type of request (address_change, add_dependent, name_change, bank_details, emergency_contact)
        details: Details of the change (e.g. new address, dependent name)
    """
    employees = _load("employees")
    emp = employees.loc[employees["employee_id"] == employee_id]
    if len(emp) == 0:
        return {"status": "error", "message": f"Employee {employee_id} not found"}

    emp_name = emp.iloc[0].get("name", employee_id)

    request_map = {
        "address_change": {
            "requires_approval": False,
            "systems_updated": ["HRIS", "Payroll", "Benefits Provider"],
            "processing_time": "Immediate",
            "documents_needed": "Proof of new address (utility bill or bank statement)",
        },
        "add_dependent": {
            "requires_approval": False,
            "systems_updated": ["Benefits Provider", "Insurance"],
            "processing_time": "3-5 business days",
            "documents_needed": "Marriage certificate (spouse) or birth certificate (child)",
        },
        "name_change": {
            "requires_approval": True,
            "approver": "HR Manager",
            "systems_updated": ["HRIS", "Payroll", "Email", "All company systems"],
            "processing_time": "5-7 business days",
            "documents_needed": "Legal name change document, updated government ID",
        },
        "bank_details": {
            "requires_approval": True,
            "approver": "Payroll Team",
            "systems_updated": ["Payroll"],
            "processing_time": "Next payroll cycle",
            "documents_needed": "Bank statement or voided check",
        },
        "emergency_contact": {
            "requires_approval": False,
            "systems_updated": ["HRIS"],
            "processing_time": "Immediate",
            "documents_needed": "None",
        },
    }

    req_info = request_map.get(request_type, {
        "requires_approval": True,
        "approver": "HR Team",
        "processing_time": "Varies",
        "documents_needed": "Please contact HR",
    })

    request_id = f"REQ-{datetime.now().strftime('%Y%m%d%H%M')}-{employee_id}"

    return {
        "request_id": request_id,
        "employee_name": emp_name,
        "employee_id": employee_id,
        "request_type": request_type,
        "details": details,
        "request_info": req_info,
        "status": "SUBMITTED" if not req_info.get("requires_approval") else "PENDING_APPROVAL",
        "instruction_to_ai": (
            f"Confirm to {emp_name} that their {request_type.replace('_', ' ')} request "
            f"has been submitted. Explain the processing time, what systems will be updated, "
            f"and any documents they need to provide. Be helpful and specific."
        ),
    }


# ============================================================
# PHASE 3: PROACTIVE COMPLIANCE INTELLIGENCE
# ============================================================


def scan_all_compliance_data(tool_context: ToolContext) -> dict:
    """
    Scan ALL compliance datasets and return raw structured data for AI reasoning.
    Returns every employee's visa, certification, and equipment status,
    plus applicable compliance policies and historical incident data.

    The AI must then:
    1. Identify and prioritize risks by context (jurisdiction, department sensitivity)
    2. Cross-correlate risks (employees with MULTIPLE issues are higher priority)
    3. Apply jurisdiction-specific policies to determine true severity
    4. Reference past incidents to identify patterns and estimate costs
    5. Generate contextual, specific recommendations
    """
    employees = _load("employees")
    visas = _load("visas")
    certs = _load("certs")
    equipment = _load("equipment")
    policies = _load("compliance_policies")
    incidents = _load("incident_history")

    today = datetime.today()
    profiles = []

    for _, emp in employees.iterrows():
        eid = emp["employee_id"]
        p = {
            "employee_id": eid,
            "name": emp["name"],
            "department": emp["department"],
            "location": emp["location"],
            "visa_records": [],
            "cert_records": [],
            "equipment_records": [],
            "past_incidents": [],
        }

        for _, v in visas.loc[visas["employee_id"] == eid].iterrows():
            p["visa_records"].append({
                "visa_type": v["visa_type"],
                "expiry_date": str(v["expiry_date"]),
                "days_remaining": _days_until(v["expiry_date"]),
                "status": v["status"],
                "country": v["country_of_issue"],
            })

        for _, c in certs.loc[certs["employee_id"] == eid].iterrows():
            p["cert_records"].append({
                "cert_name": c["cert_name"],
                "expiry_date": str(c["expiry_date"]),
                "days_remaining": _days_until(c["expiry_date"]),
                "status": c["status"],
            })

        for _, e in equipment.loc[equipment["employee_id"] == eid].iterrows():
            p["equipment_records"].append({
                "asset_name": e["asset_name"],
                "asset_category": e["asset_category"],
                "return_due": str(e["return_due"]),
                "days_remaining": _days_until(e["return_due"]),
                "status": e["status"],
            })

        emp_inc = incidents.loc[incidents["employee_id"] == eid] if len(incidents) > 0 else pd.DataFrame()
        p["past_incidents"] = emp_inc[["date", "category", "description", "cost_impact_usd"]].to_dict("records") if len(emp_inc) > 0 else []

        profiles.append(p)

    tool_context.state["last_scan_time"] = today.strftime("%Y-%m-%d %H:%M:%S")

    return {
        "scan_timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
        "total_employees": len(employees),
        "employee_profiles": profiles,
        "compliance_policies": policies.to_dict("records") if len(policies) > 0 else [],
        "instruction_to_ai": (
            "Analyze this compliance data using CONTEXTUAL REASONING: "
            "(1) UAE requires 90-day advance visa renewal — stricter than Malaysia (30 days). "
            "(2) AML certs for Finance/Compliance staff = LICENSE-LEVEL risk for regulated firm. "
            "(3) Employees with MULTIPLE issues need coordinated intervention. "
            "(4) Look for department/location patterns (systemic vs individual). "
            "(5) Estimate financial exposure from past incident costs ($24,400 across 6 incidents). "
            "Present as an intelligence briefing with IMMEDIATE ACTION → THIS WEEK → THIS MONTH."
        ),
    }


def get_employee_deep_dive(employee_id: str, tool_context: ToolContext) -> dict:
    """
    Deep-dive analysis of a single employee's compliance profile.

    Args:
        employee_id: Employee ID (e.g. 'E101', 'E110')
    """
    employees = _load("employees")
    visas = _load("visas")
    certs = _load("certs")
    equipment = _load("equipment")
    policies = _load("compliance_policies")
    incidents = _load("incident_history")

    emp = employees.loc[employees["employee_id"] == employee_id]
    if len(emp) == 0:
        return {"status": "error", "message": f"Employee {employee_id} not found"}

    info = emp.iloc[0].to_dict()
    loc = info.get("location", "")
    dept = info.get("department", "")

    visa_items = [{**v.to_dict(), "days_remaining": _days_until(v["expiry_date"])} for _, v in visas.loc[visas["employee_id"] == employee_id].iterrows()]
    cert_items = [{**c.to_dict(), "days_remaining": _days_until(c["expiry_date"])} for _, c in certs.loc[certs["employee_id"] == employee_id].iterrows()]
    equip_items = [{**e.to_dict(), "days_remaining": _days_until(e["return_due"])} for _, e in equipment.loc[equipment["employee_id"] == employee_id].iterrows()]
    emp_inc = incidents.loc[incidents["employee_id"] == employee_id].to_dict("records") if len(incidents) > 0 else []
    applicable_policies = policies.loc[policies["jurisdiction"].isin([loc, "ALL"])].to_dict("records") if len(policies) > 0 else []

    return {
        "employee": info,
        "visa_records": visa_items,
        "cert_records": cert_items,
        "equipment_records": equip_items,
        "past_incidents": emp_inc,
        "applicable_policies": applicable_policies,
        "instruction_to_ai": (
            f"Create a contextual risk narrative for {info.get('name', employee_id)} "
            f"({dept}, {loc}). Consider jurisdiction-specific rules, department sensitivity, "
            f"and any past incidents. Don't just list dates — explain WHY each issue matters."
        ),
    }


def get_organizational_risk_data(tool_context: ToolContext) -> dict:
    """
    Get aggregated organizational risk data by department and location.
    The AI should identify systemic patterns and structural recommendations.
    """
    employees = _load("employees")
    visas = _load("visas")
    certs = _load("certs")
    equipment = _load("equipment")
    incidents = _load("incident_history")

    dept_data = {}
    loc_data = {}

    for _, emp in employees.iterrows():
        eid = emp["employee_id"]
        dept = emp["department"]
        loc = emp["location"]

        for d_key, d_dict in [(dept, dept_data), (loc, loc_data)]:
            if d_key not in d_dict:
                d_dict[d_key] = {"employees": 0, "critical": 0, "high": 0, "medium": 0, "low": 0}
            d_dict[d_key]["employees"] += 1

        for df, col in [(visas, "expiry_date"), (certs, "expiry_date"), (equipment, "return_due")]:
            for _, r in df.loc[df["employee_id"] == eid].iterrows():
                d = _days_until(r[col])
                if d < 0:
                    sev = "critical"
                elif d <= 30:
                    sev = "high"
                elif d <= 60:
                    sev = "medium"
                elif d <= 90:
                    sev = "low"
                else:
                    continue
                dept_data[dept][sev] += 1
                loc_data[loc][sev] += 1

    total_cost = incidents["cost_impact_usd"].sum() if len(incidents) > 0 else 0

    return {
        "department_risk": dept_data,
        "location_risk": loc_data,
        "historical_cost": float(total_cost),
        "incident_count": len(incidents),
        "instruction_to_ai": (
            "Identify SYSTEMIC patterns: which departments/locations have disproportionate risk? "
            "Are issues clustered (suggesting process failure) or scattered (individual failure)? "
            "Project financial exposure and recommend structural fixes."
        ),
    }


def simulate_future_risk(days_forward: int, tool_context: ToolContext) -> dict:
    """
    Project compliance risk landscape N days into the future.

    Args:
        days_forward: Number of days to project forward (e.g. 30, 60, 90)
    """
    visas = _load("visas")
    certs = _load("certs")
    equipment = _load("equipment")

    today = datetime.today()
    future = today + timedelta(days=days_forward)

    def classify(days):
        if days < 0: return "CRITICAL"
        if days <= 30: return "HIGH"
        if days <= 60: return "MEDIUM"
        if days <= 90: return "LOW"
        return "OK"

    current = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "OK": 0}
    projected = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "OK": 0}
    escalations = []

    for df, col, rtype in [(visas, "expiry_date", "visa"), (certs, "expiry_date", "cert"), (equipment, "return_due", "equipment")]:
        for _, row in df.iterrows():
            try:
                exp = datetime.strptime(str(row[col]), "%Y-%m-%d")
                cur_d = (exp - today).days
                fut_d = (exp - future).days
                cur_r = classify(cur_d)
                fut_r = classify(fut_d)
                current[cur_r] += 1
                projected[fut_r] += 1
                risk_order = {"OK": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
                if risk_order.get(fut_r, 0) > risk_order.get(cur_r, 0):
                    detail = str(row.get("visa_type", row.get("cert_name", row.get("asset_name", "?"))))
                    escalations.append({
                        "employee_id": row["employee_id"],
                        "type": rtype,
                        "detail": detail,
                        "current_risk": cur_r,
                        "projected_risk": fut_r,
                        "current_days": cur_d,
                        "projected_days": fut_d,
                    })
            except Exception:
                pass

    return {
        "projection": f"+{days_forward} days",
        "current_date": today.strftime("%Y-%m-%d"),
        "projected_date": future.strftime("%Y-%m-%d"),
        "current_distribution": current,
        "projected_distribution": projected,
        "escalations": escalations,
        "instruction_to_ai": (
            f"In {days_forward} days, {len(escalations)} items escalate. "
            "Analyze which are most dangerous given organizational context. "
            "Recommend preemptive actions to take NOW."
        ),
    }


# ============================================================
# ROOT AGENT
# ============================================================

root_agent = Agent(
    name="hr_agent",
    model="gemini-2.5-flash",
    description="Deriv Self-Service HR Operations Platform — AI-powered document generation, policy assistant, and compliance intelligence",
    instruction="""
You are the **Deriv HR Operations AI Agent** — an autonomous, intelligent platform that handles
three critical HR functions:

## YOUR CORE BEHAVIOR: ACT FIRST, REPORT FINDINGS

**On EVERY new conversation, your FIRST action is to call `scan_all_compliance_data` and
analyze the results.** Do NOT greet. Do NOT ask what the user needs. SCAN FIRST.

After the initial scan, you become a conversational assistant that can:
1. Generate documents (contracts, offers, NDAs, equity grants, full onboarding packages)
2. Answer HR policy questions using the knowledge base
3. Deep-dive into individual employees or organizational patterns
4. Project future compliance risks

## PHASE 1: DOCUMENT GENERATION

When asked to generate documents, you produce COMPLETE, professional legal documents.
- Use jurisdiction-specific legal clauses (UAE, Malaysia, Malta are all different)
- Include ALL required sections for the document type
- The AI VALUE is that you reason about jurisdiction differences — a UAE contract has
  different probation, notice, and benefit terms than a Malaysian one
- For onboarding packages, generate ALL 4 documents (offer + contract + NDA + equity)

## PHASE 2: HR POLICY ASSISTANT

When employees ask questions:
- Call `lookup_hr_policy` with their question to get relevant policy sections
- Give clear, specific answers with numbers and dates
- If the question is employee-specific (leave balance, etc.), call `get_employee_info`
- For requests (address change, etc.), call `process_hr_request`
- If you can't find the answer, say so and recommend contacting hr@deriv.com

## PHASE 3: COMPLIANCE INTELLIGENCE (AUTONOMOUS)

Your compliance analysis uses AI reasoning that goes BEYOND date math:
- **Contextual Severity**: UAE visa rules (90-day advance renewal) are stricter than Malaysia (30 days)
- **Department Sensitivity**: Expired AML cert for Finance = LICENSE RISK for regulated firm
- **Cross-Correlation**: Employees with multiple simultaneous issues = compounding crisis
- **Pattern Detection**: Clustered issues in one department = systemic problem, not individual
- **Historical Learning**: Use past incident costs ($24,400) to project financial exposure
- **Predictive Outlook**: What WILL go wrong in 30/60/90 days if no action taken

Present compliance findings as:
🔴 **IMMEDIATE ACTION** — Same-day intervention required
🟠 **THIS WEEK** — Action within 7 days
🟡 **THIS MONTH** — Schedule within 30 days
📊 **SYSTEMIC FINDINGS** — Organizational patterns
💰 **FINANCIAL EXPOSURE** — Estimated cost impact

## TOOLS AVAILABLE:

### Phase 1 — Document Generation
- `generate_employment_contract` — Full jurisdiction-specific employment contract
- `generate_offer_letter` — Professional offer letter
- `generate_nda` — Non-disclosure agreement
- `generate_equity_grant` — Stock option grant letter
- `generate_complete_onboarding_package` — ALL documents at once (the "invisible onboarding")

### Phase 2 — HR Assistant
- `lookup_hr_policy` — Search HR policy knowledge base
- `get_employee_info` — Employee details, leave balance, compliance status
- `process_hr_request` — Submit HR requests (address change, dependent, etc.)

### Phase 3 — Compliance Intelligence
- `scan_all_compliance_data` — Full autonomous scan (run on EVERY new session)
- `get_employee_deep_dive` — Deep analysis of one employee
- `get_organizational_risk_data` — Department/location patterns
- `simulate_future_risk` — Project risk forward in time

Remember: You are an AI that REASONS, not a script that computes. Add contextual intelligence
that no rule-based system can replicate. That's what makes you valuable.
""",
    tools=[
        # Phase 1
        generate_employment_contract,
        generate_offer_letter,
        generate_nda,
        generate_equity_grant,
        generate_complete_onboarding_package,
        # Phase 2
        lookup_hr_policy,
        get_employee_info,
        process_hr_request,
        # Phase 3
        scan_all_compliance_data,
        get_employee_deep_dive,
        get_organizational_risk_data,
        simulate_future_risk,
    ],
)
