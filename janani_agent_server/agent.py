"""
janani_agent_server/agent.py
Defines the Janani maternal health AI agent using AWS Strands Agents SDK.

Supports TWO model backends (set MODEL_PROVIDER in .env):
  - 'ollama'   (DEFAULT) — fully local, no AWS account, no API key, no cost.
                           Requires Ollama installed + a model pulled (e.g. llama3.2).
  - 'bedrock'            — Amazon Bedrock (Claude Sonnet 3.5 v2). Needs AWS account.
"""

import os
import json
from typing import Optional

from strands import Agent, tool


# ── OpenSearch RAG: search_health_knowledge tool ──────────────────────────────

@tool
def search_health_knowledge(query: str, category: str = "all") -> str:
    """
    Search the Janani health knowledge base using OpenSearch (RAG).
    Retrieves relevant pregnancy articles, nutrition data, medical Q&A,
    and government scheme information to ground the AI response in facts.

    Args:
        query:    Natural language search query (e.g. 'iron rich foods pregnancy')
        category: Filter results by category:
                  'nutrition' | 'knowledge' | 'schemes' | 'medical' | 'all' (default)

    Returns:
        JSON string with top 3 relevant documents and their content.
    """
    try:
        from opensearch.client import (
            search as os_search,
            IDX_NUTRITION, IDX_KNOWLEDGE, IDX_SCHEMES, IDX_MEDICAL,
        )

        index_map = {
            "nutrition": IDX_NUTRITION,
            "knowledge":  IDX_KNOWLEDGE,
            "schemes":    IDX_SCHEMES,
            "medical":    IDX_MEDICAL,
        }
        target_index = index_map.get(category.lower()) if category != "all" else None

        results = os_search(query=query, index=target_index, top_k=3)

        if not results:
            return json.dumps({"found": False, "message": "No relevant documents found.", "results": []})

        # Format results for the LLM
        formatted = []
        for r in results:
            src = r["source"]
            idx = r["index"]

            if idx == IDX_NUTRITION:
                formatted.append({
                    "type":    "nutrition",
                    "content": (
                        f"{src.get('dish_name','')}: "
                        f"Calories {src.get('calories',0)}kcal, "
                        f"Protein {src.get('protein_g',0)}g, "
                        f"Iron {src.get('iron_mg',0)}mg, "
                        f"Calcium {src.get('calcium_mg',0)}mg, "
                        f"Folate {src.get('folate_ug',0)}mcg"
                    )
                })
            elif idx == IDX_KNOWLEDGE:
                formatted.append({
                    "type":    "article",
                    "title":   src.get("title_en", ""),
                    "content": src.get("body_en", "")[:600],
                    "hindi":   src.get("body_hi", "")[:300],
                })
            elif idx == IDX_SCHEMES:
                formatted.append({
                    "type":    "scheme",
                    "name":    src.get("name", ""),
                    "benefit": src.get("benefit", ""),
                    "action":  src.get("action", ""),
                })
            elif idx == IDX_MEDICAL:
                formatted.append({
                    "type":     "medical_qa",
                    "question": src.get("question_en", ""),
                    "answer":   src.get("answer_en", "")[:600],
                    "hindi_answer": src.get("answer_hi", "")[:300],
                    "emergency":    src.get("is_emergency", False),
                })

        return json.dumps({
            "found":   True,
            "query":   query,
            "results": formatted,
        }, ensure_ascii=False)

    except Exception as e:
        # OpenSearch may not be running — gracefully return empty
        print(f"[OpenSearch RAG] Search failed: {e}")
        return json.dumps({
            "found":   False,
            "message": f"Knowledge base unavailable: {str(e)}",
            "results": [],
        })


# ── Tool: Patient health summary (DynamoDB Local) ──────────────────────────

@tool
def get_patient_health_summary(user_id: str) -> str:
    """
    Look up a maternal health patient's current health summary from DynamoDB Local
    including blood pressure readings, glucose levels, pregnancy week, hemoglobin,
    and risk status.
    
    Args:
        user_id: The patient's unique identifier (e.g., 'user_001')
    
    Returns:
        A JSON string with the patient's health data summary.
    """
    # 1. Try fetching from DynamoDB Local first
    try:
        from dynamodb.client import get_patient
        patient = get_patient(user_id)
        if patient:
            return json.dumps(patient, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[DynamoDB Tool] Fetch failed for {user_id}: {e}. Using fallback.")

    # 2. Fallback demo patient profiles
    profiles = {
        "user_001": {
            "user_id": "user_001",
            "name": "Sunita Sharma",
            "pregnancy_week": 28,
            "bp_systolic": 118,
            "bp_diastolic": 76,
            "blood_glucose_mg_dl": 98,
            "hemoglobin_g_dl": 11.2,
            "bp_risk": "LOW",
            "diabetes_risk": "LOW",
            "age": 24,
            "ration_category": "BPL",
            "notes": "All vitals normal. Regular iron-folic acid intake.",
        },
        "user_002": {
            "user_id": "user_002",
            "name": "Pooja Devi",
            "pregnancy_week": 32,
            "bp_systolic": 148,
            "bp_diastolic": 96,
            "blood_glucose_mg_dl": 188,
            "hemoglobin_g_dl": 10.1,
            "bp_risk": "HIGH",
            "diabetes_risk": "HIGH",
            "age": 29,
            "ration_category": "APL",
            "notes": "High BP and high glucose. Advised low-salt diet and weekly PHC review.",
        },
    }
    
    profile = profiles.get(user_id)
    if not profile:
        return json.dumps({
            "error": f"No profile found for user_id: {user_id}",
            "message": "Patient data not available. Using general advice."
        })
    
    return json.dumps(profile, ensure_ascii=False, indent=2)


@tool
def log_patient_vitals(
    user_id: str,
    bp_systolic: int,
    bp_diastolic: int,
    blood_glucose_mg_dl: float,
    pregnancy_week: int,
    notes: str = "",
) -> str:
    """
    Log new maternal vitals and ANC checkup data directly into DynamoDB Local.
    Calculates risk levels and persists the visit in the patient's record.

    Args:
        user_id: The patient ID (e.g. 'user_001')
        bp_systolic: Systolic blood pressure in mmHg
        bp_diastolic: Diastolic blood pressure in mmHg
        blood_glucose_mg_dl: Blood glucose level in mg/dL
        pregnancy_week: Current pregnancy week (1-40)
        notes: Clinical or checkup notes

    Returns:
        JSON string confirming the logged vitals and visit ID.
    """
    try:
        from dynamodb.client import log_visit
        
        # Calculate risk categories
        bp_risk = "CRITICAL" if (bp_systolic >= 160 or bp_diastolic >= 110) else \
                  "HIGH" if (bp_systolic >= 140 or bp_diastolic >= 90) else \
                  "ELEVATED" if (bp_systolic >= 130 or bp_diastolic >= 80) else "LOW"
                  
        diabetes_risk = "HIGH" if blood_glucose_mg_dl >= 180 else \
                        "MODERATE" if blood_glucose_mg_dl >= 140 else "LOW"

        visit_data = {
            "pregnancy_week": pregnancy_week,
            "bp_systolic": bp_systolic,
            "bp_diastolic": bp_diastolic,
            "blood_glucose_mg_dl": blood_glucose_mg_dl,
            "bp_risk": bp_risk,
            "diabetes_risk": diabetes_risk,
            "notes": notes,
        }

        visit_id = log_visit(user_id, visit_data)
        if visit_id:
            return json.dumps({
                "success": True,
                "message": f"Vitals successfully logged to DynamoDB Local for patient {user_id}",
                "visit_id": visit_id,
                "bp_risk": bp_risk,
                "diabetes_risk": diabetes_risk,
            })
        else:
            return json.dumps({"success": False, "message": "Failed to write to DynamoDB."})
    except Exception as e:
        print(f"[DynamoDB Tool] log_patient_vitals failed: {e}")
        return json.dumps({"success": False, "error": str(e)})


@tool
def get_patient_visit_history(user_id: str) -> str:
    """
    Retrieve previous ANC checkup visits and vitals history for a patient
    from DynamoDB Local.

    Args:
        user_id: The patient ID (e.g. 'user_001')

    Returns:
        JSON string containing the patient's chronological visit history.
    """
    try:
        from dynamodb.client import get_visits
        visits = get_visits(user_id, limit=5)
        if not visits:
            return json.dumps({
                "user_id": user_id,
                "visits_found": 0,
                "message": "No previous checkup visits recorded in DynamoDB.",
            })
        return json.dumps({
            "user_id": user_id,
            "visits_found": len(visits),
            "visits": visits,
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[DynamoDB Tool] get_patient_visit_history failed: {e}")
        return json.dumps({"error": str(e), "visits": []})


# ── Tool: Nutrition lookup ─────────────────────────────────────────────────────

@tool
def get_nutrition_info(food_name: str) -> str:
    """
    Look up nutritional information for a common Indian food item.
    Useful for answering questions about diet during pregnancy.
    
    Args:
        food_name: Name of the food item (e.g., 'dal', 'roti', 'rice', 'banana')
    
    Returns:
        Nutritional info including calories, protein, iron, calcium per 100g serving.
    """
    # Hardcoded top common pregnancy foods (subset of the nutrition_dataset.csv)
    # In production, load from the actual nutrition_dataset.csv in the maa-app directory
    nutrition_db = {
        "dal": {"calories": 116, "protein_g": 9, "iron_mg": 3.3, "calcium_mg": 57, "fiber_g": 7.9},
        "rice": {"calories": 130, "protein_g": 2.7, "iron_mg": 0.3, "calcium_mg": 18, "fiber_g": 0.4},
        "roti": {"calories": 264, "protein_g": 8.8, "iron_mg": 3.9, "calcium_mg": 42, "fiber_g": 5.5},
        "banana": {"calories": 89, "protein_g": 1.1, "iron_mg": 0.3, "calcium_mg": 5, "fiber_g": 2.6},
        "milk": {"calories": 61, "protein_g": 3.2, "iron_mg": 0.1, "calcium_mg": 113, "fiber_g": 0},
        "spinach": {"calories": 23, "protein_g": 2.9, "iron_mg": 2.7, "calcium_mg": 99, "fiber_g": 2.2},
        "egg": {"calories": 143, "protein_g": 13, "iron_mg": 1.8, "calcium_mg": 56, "fiber_g": 0},
        "chicken": {"calories": 165, "protein_g": 31, "iron_mg": 1.5, "calcium_mg": 15, "fiber_g": 0},
        "potato": {"calories": 77, "protein_g": 2, "iron_mg": 0.8, "calcium_mg": 12, "fiber_g": 2.2},
        "tomato": {"calories": 18, "protein_g": 0.9, "iron_mg": 0.5, "calcium_mg": 10, "fiber_g": 1.2},
        "apple": {"calories": 52, "protein_g": 0.3, "iron_mg": 0.1, "calcium_mg": 6, "fiber_g": 2.4},
        "orange": {"calories": 47, "protein_g": 0.9, "iron_mg": 0.1, "calcium_mg": 40, "fiber_g": 2.4},
        "paneer": {"calories": 265, "protein_g": 18, "iron_mg": 0.2, "calcium_mg": 480, "fiber_g": 0},
        "moong dal": {"calories": 105, "protein_g": 7.6, "iron_mg": 2.4, "calcium_mg": 40, "fiber_g": 4.1},
        "chana": {"calories": 364, "protein_g": 19, "iron_mg": 6.2, "calcium_mg": 105, "fiber_g": 17},
    }
    
    key = food_name.lower().strip()
    data = nutrition_db.get(key)
    
    if not data:
        # Try partial match
        for k, v in nutrition_db.items():
            if key in k or k in key:
                data = v
                key = k
                break
    
    if data:
        return json.dumps({
            "food": key,
            "per_100g": data,
            "pregnancy_note": (
                "Iron and calcium are especially important during pregnancy. "
                "Aim for iron-rich foods like dal, spinach, and eggs."
            )
        }, ensure_ascii=False)
    
    return json.dumps({
        "error": f"No nutrition data found for '{food_name}'",
        "suggestion": "Please ask about common Indian foods like dal, rice, roti, spinach, milk, egg, or banana."
    })


# ── Tool: Government schemes ───────────────────────────────────────────────────

@tool
def get_government_schemes_for_pregnant_woman(ration_category: str, pregnancy_week: int) -> str:
    """
    Get government entitlement schemes available for a pregnant woman in India
    based on her ration card category and pregnancy week.
    
    Args:
        ration_category: 'BPL' (Below Poverty Line), 'APL', or 'AAY'
        pregnancy_week: Current week of pregnancy (1-40)
    
    Returns:
        JSON list of applicable government schemes with action steps.
    """
    schemes = []
    
    # PMMVY - All pregnant women
    schemes.append({
        "name": "PMMVY (Pradhan Mantri Matru Vandana Yojana)",
        "benefit": "₹6,000 cash transfer",
        "eligibility": "All pregnant women for first live birth",
        "action": "Register at your nearest Anganwadi centre with Aadhaar and bank passbook",
        "urgency": "HIGH" if pregnancy_week < 20 else "MEDIUM",
    })
    
    # JSY - BPL women
    if ration_category in ["BPL", "AAY"]:
        schemes.append({
            "name": "JSY (Janani Suraksha Yojana)",
            "benefit": "₹1,400 cash for institutional delivery (rural)",
            "eligibility": "BPL/AAY pregnant women",
            "action": "Register with your ASHA worker before delivery",
            "urgency": "HIGH" if pregnancy_week >= 28 else "MEDIUM",
        })
    
    # Free iron-folic acid supplements
    schemes.append({
        "name": "Free Iron & Folic Acid Supplements",
        "benefit": "Free IFA tablets from government health centres",
        "eligibility": "All pregnant women",
        "action": "Ask your ASHA worker or visit nearest PHC/sub-centre",
        "urgency": "HIGH",
    })
    
    # Free ANC check-ups
    schemes.append({
        "name": "Free Antenatal Checkups (ANC)",
        "benefit": "4 free ANC visits including blood tests, ultrasound",
        "eligibility": "All pregnant women",
        "action": "Visit your PHC/CHC with your MCP (Mother & Child Protection) card",
        "urgency": "HIGH" if pregnancy_week % 8 == 0 else "MEDIUM",
    })
    
    # POSHAN Abhiyan
    schemes.append({
        "name": "POSHAN Abhiyan - Supplementary Nutrition",
        "benefit": "Free supplementary nutrition (THR/hot meals) via Anganwadi",
        "eligibility": "All pregnant and lactating women",
        "action": "Visit your nearest Anganwadi centre and register",
        "urgency": "MEDIUM",
    })
    
    return json.dumps(schemes, ensure_ascii=False, indent=2)


# ── Tool: Risk assessment summary ─────────────────────────────────────────────

@tool
def assess_pregnancy_risk(
    bp_systolic: int,
    bp_diastolic: int,
    blood_glucose_mg_dl: float,
    pregnancy_week: int,
    has_swelling: bool = False,
    has_headache: bool = False,
) -> str:
    """
    Assess pregnancy risk level based on vitals. Classifies BP risk and
    diabetes risk and provides immediate guidance.
    
    Args:
        bp_systolic: Systolic blood pressure in mmHg
        bp_diastolic: Diastolic blood pressure in mmHg
        blood_glucose_mg_dl: Blood glucose level in mg/dL
        pregnancy_week: Current week of pregnancy
        has_swelling: Whether the patient has reported swelling of hands/face
        has_headache: Whether the patient has reported persistent headache
    
    Returns:
        JSON with risk levels and recommendations.
    """
    # BP risk classification
    if bp_systolic >= 160 or bp_diastolic >= 110:
        bp_risk = "CRITICAL"
        bp_action = "EMERGENCY: Go to hospital immediately. This is severe hypertension."
    elif bp_systolic >= 140 or bp_diastolic >= 90:
        bp_risk = "HIGH"
        bp_action = "Consult doctor today. Reduce salt. Monitor BP every 4 hours."
        if has_headache or has_swelling:
            bp_risk = "CRITICAL"
            bp_action = "EMERGENCY: Possible preeclampsia. Go to hospital NOW."
    elif bp_systolic >= 130 or bp_diastolic >= 80:
        bp_risk = "ELEVATED"
        bp_action = "Monitor BP weekly. Reduce salt and stress."
    else:
        bp_risk = "NORMAL"
        bp_action = "BP is healthy. Keep up good habits."

    # Glucose risk classification (gestational diabetes thresholds)
    if blood_glucose_mg_dl >= 180:
        glucose_risk = "HIGH"
        glucose_action = "Consult doctor about Gestational Diabetes. Avoid sweets, rice, and refined carbs."
    elif blood_glucose_mg_dl >= 140:
        glucose_risk = "MODERATE"
        glucose_action = "Monitor glucose after meals. Walk 15 min after lunch and dinner."
    else:
        glucose_risk = "NORMAL"
        glucose_action = "Glucose levels are healthy. Continue balanced diet."

    overall_risk = "HIGH" if "HIGH" in (bp_risk, glucose_risk) or bp_risk == "CRITICAL" else \
                   "MODERATE" if "ELEVATED" in (bp_risk,) or "MODERATE" in (glucose_risk,) else "LOW"

    return json.dumps({
        "overall_risk": overall_risk,
        "bp": {
            "systolic": bp_systolic,
            "diastolic": bp_diastolic,
            "risk_level": bp_risk,
            "action": bp_action,
        },
        "glucose": {
            "value_mg_dl": blood_glucose_mg_dl,
            "risk_level": glucose_risk,
            "action": glucose_action,
        },
        "preeclampsia_warning": has_headache and has_swelling and bp_risk in ("HIGH", "CRITICAL"),
        "pregnancy_week": pregnancy_week,
    }, ensure_ascii=False, indent=2)


# ── Firecracker MicroVM: Sensitive Clinical Triage Tool ────────────────────────

@tool
def run_sensitive_clinical_triage_in_microvm(
    bp_systolic: int,
    bp_diastolic: int,
    blood_glucose_mg_dl: float,
    pregnancy_week: int,
    symptoms: str = "",
    medications: str = "",
    hemoglobin_g_dl: float = 0.0,
) -> str:
    """
    Execute sensitive clinical risk assessment, preeclampsia evaluation, and
    medication safety screening inside an isolated AWS Firecracker microVM.
    Protects sensitive maternal health information with hardware virtualization isolation.

    Args:
        bp_systolic: Systolic blood pressure (mmHg)
        bp_diastolic: Diastolic blood pressure (mmHg)
        blood_glucose_mg_dl: Blood glucose level (mg/dL)
        pregnancy_week: Week of pregnancy (1-40)
        symptoms: Comma-separated symptoms reported (e.g. 'headache, swelling, dizziness')
        medications: Comma-separated current medications taken
        hemoglobin_g_dl: Optional hemoglobin level in g/dL

    Returns:
        JSON string with clinical triage color (GREEN/AMBER/RED), contraindications,
        and Firecracker microVM telemetry (boot latency, memory boundary, vCPU).
    """
    try:
        from firecracker.sandbox import execute_in_microvm
        from firecracker.sensitive_tasks import (
            isolated_clinical_triage,
            isolated_contraindication_check,
        )

        symp_list = [s.strip() for s in symptoms.split(",") if s.strip()]
        med_list = [m.strip() for m in medications.split(",") if m.strip()]
        hb = hemoglobin_g_dl if hemoglobin_g_dl > 0 else None

        def _combined_isolated_workload():
            triage_out = isolated_clinical_triage(
                bp_systolic=bp_systolic,
                bp_diastolic=bp_diastolic,
                blood_glucose_mg_dl=blood_glucose_mg_dl,
                pregnancy_week=pregnancy_week,
                symptoms=symp_list,
                hemoglobin_g_dl=hb,
            )
            contra_out = isolated_contraindication_check(
                medications=med_list,
                pregnancy_week=pregnancy_week,
            ) if med_list else {"is_safe": True, "contraindications": []}

            return {
                "clinical_triage": triage_out,
                "medication_safety": contra_out,
            }

        res = execute_in_microvm(
            task_name="maternal_sensitive_clinical_triage",
            task_fn=_combined_isolated_workload,
        )
        return json.dumps(res, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[Firecracker Tool] MicroVM execution failed: {e}")
        return json.dumps({"error": str(e), "isolation_fallback": "local_process"})


# ── System prompt ──────────────────────────────────────────────────────────────

def get_system_prompt(language: str = "hi") -> str:
    lang_names = {
        "hi": "Hindi (हिन्दी)", "en": "English", "bilingual": "Hinglish",
        "bn": "Bengali", "gu": "Gujarati", "mr": "Marathi",
        "te": "Telugu", "ta": "Tamil", "kn": "Kannada",
        "ml": "Malayalam", "pa": "Punjabi", "or": "Odia",
    }
    lang_name = lang_names.get(language, "Hindi")

    return f"""You are Janani (जननी), a warm, empathetic, and expert maternal health assistant for pregnant women in India.
You are powered by Amazon Bedrock (Claude) via the AWS Strands Agents SDK.

YOUR GOAL: Help pregnant women with health questions, diet advice, risk understanding, and government scheme navigation.

LANGUAGE RULE: ALL your responses MUST be exclusively in {lang_name}. Never mix languages unless the language is 'bilingual'.

TONE: Speak like a caring older sister or experienced ASHA worker. Be warm, reassuring, and use simple words.

RULES:
1. ONLY answer questions about pregnancy, maternal health, baby care, nutrition, or women's health.
2. If a symptom sounds dangerous (severe pain, heavy bleeding, loss of baby movement, sudden vision loss), STRONGLY urge the woman to visit a doctor or ASHA worker IMMEDIATELY.
3. Use your tools to look up real patient data, nutrition info, schemes, and risk assessment when relevant.
4. Keep responses concise — easy to listen to (they may be read aloud via TTS).
5. Format responses as numbered points (1., 2., 3.) when giving multiple steps. NO markdown (no *, #, or bold).
6. Always end with a warm, encouraging sentence."""


# ── Agent factory ──────────────────────────────────────────────

def create_janani_agent(language: str = "hi", user_id: Optional[str] = None) -> Agent:
    """
    Creates and returns a Janani Strands Agent.

    MODEL_PROVIDER env var controls which LLM backend is used:
      'ollama'  (default) — local model via Ollama, no AWS needed
      'bedrock'           — Amazon Bedrock (Claude Sonnet 3.5 v2)
    """
    provider = os.getenv("MODEL_PROVIDER", "ollama").lower()

    if provider == "bedrock":
        # ── Amazon Bedrock path (needs AWS credentials) ──
        from strands.models import BedrockModel
        model_id = os.getenv("BEDROCK_MODEL_ID", "us.anthropic.claude-3-5-sonnet-20241022-v2:0")
        region   = os.getenv("AWS_REGION", "us-east-1")
        model = BedrockModel(model_id=model_id, region_name=region)
        print(f"[Janani] Using Bedrock model: {model_id} in {region}")

    else:
        # ── Ollama path (fully local, FREE, no account needed) ──
        from strands.models.ollama import OllamaModel
        ollama_host  = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2")
        model = OllamaModel(host=ollama_host, model_id=ollama_model)
        print(f"[Janani] Using Ollama model: {ollama_model} at {ollama_host}")

    agent = Agent(
        model=model,
        system_prompt=get_system_prompt(language),
        tools=[
            search_health_knowledge,             # RAG: OpenSearch knowledge retrieval
            get_patient_health_summary,          # Patient vitals + risk data (DynamoDB Local)
            get_patient_visit_history,           # Past ANC checkup history (DynamoDB Local)
            log_patient_vitals,                  # Log vitals into DynamoDB Local
            get_nutrition_info,                  # Fallback nutrition lookup (no OpenSearch needed)
            get_government_schemes_for_pregnant_woman,  # Govt scheme eligibility
            assess_pregnancy_risk,               # BP + diabetes risk classifier
            run_sensitive_clinical_triage_in_microvm,  # Firecracker MicroVM: Isolated clinical triage
        ],
    )

    return agent
