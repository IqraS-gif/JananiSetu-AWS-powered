"""
janani_agent_server/main.py

FastAPI server powering the Janani AI chatbot with:
  - AWS Strands Agents SDK  (AI orchestration)
  - OpenSearch              (RAG: health knowledge retrieval)
  - Cedar                   (Authorization: Mother / ASHA / Doctor access control)

All running LOCALLY — no AWS account, no card, no bill.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Literal
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

from agent import create_janani_agent
from cedar_auth import (
    check_tool_permission,
    is_action_allowed,
    ROLE_PERMISSIONS_SUMMARY,
    Role,
)

# ── App setup ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Janani Setu AI Agent",
    description=(
        "Janani maternal health AI — powered by:\n"
        "- AWS Strands Agents SDK (AI orchestration)\n"
        "- OpenSearch (health knowledge RAG)\n"
        "- Cedar (role-based access control)\n"
        "- Ollama / Amazon Bedrock (LLM)"
    ),
    version="3.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Session store (in-memory for dev) ─────────────────────────────────────────
session_store: dict = {}

# ── Request / Response models ─────────────────────────────────────────────────

class ChatMessage(BaseModel):
    role: str   # 'user' or 'ai'
    text: str


class ChatRequest(BaseModel):
    message:    str
    history:    Optional[List[ChatMessage]] = []
    language:   Optional[str]  = "hi"
    session_id: Optional[str]  = "default"
    user_id:    Optional[str]  = None
    # Cedar: who is making this request?
    user_role:  Optional[str]  = "Mother"   # 'Mother' | 'ASHA' | 'Doctor'


class ChatResponse(BaseModel):
    response:   str
    session_id: str
    role_used:  str
    cedar_decision: str   # 'cedar_permit' | 'cedar_forbid' | 'dev_mode_allow_all'


class PermissionsResponse(BaseModel):
    role: str
    can: List[str]
    cannot: List[str]


class VitalsLogRequest(BaseModel):
    bp_systolic: int
    bp_diastolic: int
    blood_glucose_mg_dl: float
    pregnancy_week: int
    notes: Optional[str] = ""
    recorded_by: Optional[str] = "Mother"


class MicroVMTriageRequest(BaseModel):
    bp_systolic: int
    bp_diastolic: int
    blood_glucose_mg_dl: float
    pregnancy_week: int
    symptoms: Optional[List[str]] = []
    hemoglobin_g_dl: Optional[float] = None
    medications: Optional[List[str]] = []
    user_role: Optional[str] = "Mother"
    user_id: Optional[str] = "user_001"


class PHIRedactRequest(BaseModel):
    text: str


# ── Helpers ───────────────────────────────────────────────────────────────────

LANG_NAMES = {
    "hi": "Hindi (Devanagari script)",
    "en": "English",
    "bilingual": "Hinglish (mixed Hindi-English)",
    "bn": "Bengali", "gu": "Gujarati", "mr": "Marathi",
    "te": "Telugu",  "ta": "Tamil",   "kn": "Kannada",
    "ml": "Malayalam", "pa": "Punjabi", "or": "Odia",
}

CEDAR_DENIED_MESSAGES = {
    "hi": "क्षमा करें, आपको इस जानकारी तक पहुंचने की अनुमति नहीं है।",
    "en": "Sorry, you do not have permission to access this information.",
}


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/architecture", response_class=HTMLResponse)
@app.get("/", response_class=HTMLResponse)
async def get_architecture_page():
    """Serves the interactive AWS Architecture & Services Map webpage."""
    html_path = os.path.join(os.path.dirname(__file__), "architecture.html")
    if not os.path.exists(html_path):
        # Check parent folder
        html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "janani-aws-architecture.html")
    
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Janani Setu Architecture Page</h1><p>architecture.html not found</p>")


@app.get("/health")
async def health():
    dynamo_status = "unreachable"
    try:
        from dynamodb.client import get_dynamodb_client
        client = get_dynamodb_client()
        client.list_tables()
        dynamo_status = "connected"
    except Exception:
        pass

    return {
        "status": "ok",
        "agent": "Janani Strands Agent v3.2",
        "features": [
            "strands-agents",
            "opensearch-rag",
            "cedar-auth",
            "dynamodb-local",
            "firecracker-microvm",
        ],
        "dynamodb": dynamo_status,
        "firecracker": "ready",
    }


@app.get("/permissions/{role}", response_model=PermissionsResponse)
async def get_permissions(role: str):
    """Return what a given role is allowed to do (for UI display)."""
    perms = ROLE_PERMISSIONS_SUMMARY.get(role)
    if not perms:
        raise HTTPException(status_code=404, detail=f"Unknown role: {role}")
    return PermissionsResponse(role=role, can=perms["can"], cannot=perms["cannot"])


@app.get("/patients/{user_id}")
async def get_patient_endpoint(user_id: str):
    """Fetch patient profile from DynamoDB Local."""
    try:
        from dynamodb.client import get_patient
        patient = get_patient(user_id)
        if not patient:
            raise HTTPException(status_code=404, detail=f"Patient {user_id} not found")
        return patient
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/patients/{user_id}/visits")
async def get_patient_visits_endpoint(user_id: str, limit: int = 10):
    """Fetch ANC checkup visits and vitals history from DynamoDB Local."""
    try:
        from dynamodb.client import get_visits
        visits = get_visits(user_id, limit=limit)
        return {"user_id": user_id, "visits": visits}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/patients/{user_id}/vitals")
async def log_patient_vitals_endpoint(user_id: str, req: VitalsLogRequest):
    """Log new ANC vitals for a patient into DynamoDB Local."""
    try:
        from dynamodb.client import log_visit
        bp_risk = "CRITICAL" if (req.bp_systolic >= 160 or req.bp_diastolic >= 110) else \
                  "HIGH" if (req.bp_systolic >= 140 or req.bp_diastolic >= 90) else \
                  "ELEVATED" if (req.bp_systolic >= 130 or req.bp_diastolic >= 80) else "LOW"
                  
        diabetes_risk = "HIGH" if req.blood_glucose_mg_dl >= 180 else \
                        "MODERATE" if req.blood_glucose_mg_dl >= 140 else "LOW"

        visit_data = {
            "pregnancy_week": req.pregnancy_week,
            "bp_systolic": req.bp_systolic,
            "bp_diastolic": req.bp_diastolic,
            "blood_glucose_mg_dl": req.blood_glucose_mg_dl,
            "bp_risk": bp_risk,
            "diabetes_risk": diabetes_risk,
            "notes": req.notes,
            "recorded_by": req.recorded_by,
        }
        visit_id = log_visit(user_id, visit_data)
        if not visit_id:
            raise HTTPException(status_code=500, detail="Failed to persist visit to DynamoDB Local")
        return {
            "success": True,
            "visit_id": visit_id,
            "user_id": user_id,
            "bp_risk": bp_risk,
            "diabetes_risk": diabetes_risk,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Firecracker MicroVM Endpoints ─────────────────────────────────────────────

@app.get("/sandbox/status")
async def sandbox_status():
    """Return Firecracker microVM engine telemetry and configuration."""
    from firecracker.sandbox import get_microvm_status
    return get_microvm_status()


@app.post("/sandbox/clinical-triage")
async def isolated_triage_endpoint(req: MicroVMTriageRequest):
    """
    Run sensitive clinical triage and drug safety screening inside an
    isolated Firecracker microVM sandbox.
    """
    from firecracker.sandbox import execute_in_microvm
    from firecracker.sensitive_tasks import (
        isolated_clinical_triage,
        isolated_contraindication_check,
    )

    # Cedar check
    allowed, cedar_reason = is_action_allowed(
        role=req.user_role or "Mother",
        principal_id=req.user_id or "user_001",
        action="ExecuteMicroVM",
        resource="OwnData" if req.user_role != "ASHA" else "AssignedPatientData",
    )
    if not allowed:
        raise HTTPException(status_code=403, detail="Cedar policy denied microVM execution for this role.")

    def _workload():
        triage = isolated_clinical_triage(
            bp_systolic=req.bp_systolic,
            bp_diastolic=req.bp_diastolic,
            blood_glucose_mg_dl=req.blood_glucose_mg_dl,
            pregnancy_week=req.pregnancy_week,
            symptoms=req.symptoms,
            hemoglobin_g_dl=req.hemoglobin_g_dl,
        )
        contra = isolated_contraindication_check(
            medications=req.medications or [],
            pregnancy_week=req.pregnancy_week,
        ) if req.medications else {"is_safe": True, "contraindications": []}

        return {
            "triage": triage,
            "medication_safety": contra,
        }

    res = execute_in_microvm(
        task_name="isolated_clinical_triage_and_drug_safety",
        task_fn=_workload,
    )
    return res


@app.post("/sandbox/redact-phi")
async def isolated_phi_redact_endpoint(req: PHIRedactRequest):
    """
    Strip sensitive identifiers (Phone, Aadhaar, MCP ID) inside the microVM
    sandbox before sending text to external LLMs.
    """
    from firecracker.sandbox import execute_in_microvm
    from firecracker.sensitive_tasks import isolated_phi_redaction

    res = execute_in_microvm(
        task_name="isolated_phi_redaction",
        task_fn=isolated_phi_redaction,
        raw_text=req.text,
    )
    return res


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Main chat endpoint.
    1. Cedar checks if this role can Chat → denies if not.
    2. Builds prompt from history + language.
    3. Strands Agent responds (using OpenSearch RAG tool + other tools).
    4. Returns response with Cedar decision logged.
    """
    session_id  = req.session_id or "default"
    user_role   = req.user_role  or "Mother"
    principal   = req.user_id    or "anonymous"
    lang        = req.language   or "hi"
    lang_name   = LANG_NAMES.get(lang, "Hindi")

    # ── Step 1: Cedar authorization check ─────────────────────────────────────
    allowed, cedar_reason = is_action_allowed(
        role=user_role,
        principal_id=principal,
        action="Chat",
        resource="AIChat",
    )

    if not allowed:
        denied_msg = CEDAR_DENIED_MESSAGES.get(lang, CEDAR_DENIED_MESSAGES["en"])
        return ChatResponse(
            response=denied_msg,
            session_id=session_id,
            role_used=user_role,
            cedar_decision="cedar_forbid",
        )

    # ── Step 2: Build context-aware prompt ────────────────────────────────────
    history_text = ""
    if req.history:
        for msg in req.history[-10:]:
            speaker = "User" if msg.role == "user" else "Janani"
            history_text += f"{speaker}: {msg.text}\n"

    # Inject role context so agent knows who is asking
    role_context = {
        "Mother": "The user is the pregnant patient herself asking about her own health.",
        "ASHA":   "The user is an ASHA worker asking on behalf of an assigned patient.",
        "Doctor": "The user is a licensed doctor with full access to patient medical information.",
    }.get(user_role, "")

    full_prompt = ""
    if history_text:
        full_prompt += f"[Conversation History]\n{history_text}\n"
    if req.user_id:
        full_prompt += f"[Patient ID: {req.user_id}]\n"

    full_prompt += (
        f"[Requester Role: {user_role}] {role_context}\n"
        f"[Language: {lang_name}]\n"
        f"User: {req.message}\n\n"
        f"Respond ONLY in {lang_name}. Use plain text (no markdown). "
        f"Be warm, brief, and empathetic."
    )

    # ── Step 3: Run Strands Agent ──────────────────────────────────────────────
    try:
        agent  = create_janani_agent(language=lang, user_id=req.user_id)
        result = agent(full_prompt)
        response_text = str(result).strip() if result else "Something went wrong. Please try again."

        # Store session
        session_store.setdefault(session_id, [])
        session_store[session_id].append({
            "user": req.message,
            "agent": response_text,
            "role": user_role,
        })

        return ChatResponse(
            response=response_text,
            session_id=session_id,
            role_used=user_role,
            cedar_decision=cedar_reason,
        )

    except Exception as e:
        print(f"[Agent Error] {e}")
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


@app.delete("/session/{session_id}")
async def clear_session(session_id: str):
    session_store.pop(session_id, None)
    return {"cleared": session_id}


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    # Auto-initialize DynamoDB tables if DynamoDB is running
    try:
        from dynamodb.client import create_tables_if_not_exist
        create_tables_if_not_exist()
    except Exception:
        pass

    print(f"\n🌸 Janani Agent Server v3.2 starting on http://{host}:{port}")
    print("   Stack: Strands Agents + OpenSearch RAG + Cedar Auth + DynamoDB Local + Firecracker MicroVM")
    print("   Find your IP: run 'ipconfig' on Windows (IPv4 Address)")
    print("   Set EXPO_PUBLIC_STRANDS_AGENT_URL=http://<YOUR_IP>:8000 in maa-app/.env\n")
    uvicorn.run("main:app", host=host, port=port, reload=True)
