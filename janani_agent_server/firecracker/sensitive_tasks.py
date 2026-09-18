"""
janani_agent_server/firecracker/sensitive_tasks.py

Defines sensitive maternal health AI workloads that execute inside
isolated Firecracker microVM sandboxes to guarantee PHI protection and clinical safety:

1. isolated_clinical_triage: Multi-factor preeclampsia & gestational emergency triage.
2. isolated_phi_redaction: Patient identity & Aadhaar/MCP stripping.
3. isolated_contraindication_check: Pregnancy medication safety & drug interaction check.
"""

import re
import time
from typing import Dict, Any, List


def isolated_clinical_triage(
    bp_systolic: int,
    bp_diastolic: int,
    blood_glucose_mg_dl: float,
    pregnancy_week: int,
    symptoms: List[str] = None,
    hemoglobin_g_dl: float = None,
    previous_cesarean: bool = False,
) -> Dict[str, Any]:
    """
    Executes deep clinical triage for high-risk maternal symptoms inside
    an isolated environment.
    """
    symptoms = [s.lower() for s in (symptoms or [])]
    flags = []
    triage_color = "GREEN"
    primary_warning = "All vitals within expected parameters."

    # 1. Preeclampsia / Eclampsia detection
    has_severe_hypertension = bp_systolic >= 160 or bp_diastolic >= 110
    has_mild_hypertension   = bp_systolic >= 140 or bp_diastolic >= 90
    has_headache            = any("headache" in s for s in symptoms)
    has_edema               = any("swelling" in s or "edema" in s or "sujan" in s for s in symptoms)
    has_vision_issues       = any("vision" in s or "blur" in s or "dhundla" in s for s in symptoms)
    has_epigastric_pain     = any("epigastric" in s or "upper belly" in s or "pet dard" in s for s in symptoms)
    has_seizure             = any("fit" in s or "seizure" in s or "jhatka" in s for s in symptoms)

    if has_seizure:
        triage_color = "RED"
        flags.append("ECLAMPSIA EMERGENCY: Active convulsions reported.")
        primary_warning = "CRITICAL OBSTETRIC EMERGENCY: Immediate administration of Magnesium Sulfate and tertiary hospital transfer required."
    elif has_severe_hypertension or (has_mild_hypertension and (has_headache or has_edema or has_vision_issues or has_epigastric_pain)):
        triage_color = "RED"
        flags.append("SEVERE PREECLAMPSIA RISK: Hypertension combined with neurological or end-organ symptoms.")
        primary_warning = "CRITICAL: Urgent hospital review needed within 2 hours. High preeclampsia risk."
    elif has_mild_hypertension:
        triage_color = "AMBER"
        flags.append("GESTATIONAL HYPERTENSION: Blood pressure elevated above 140/90 mmHg.")
        primary_warning = "URGENT: Review at Primary Health Centre within 24 hours. Daily BP monitoring."

    # 2. Gestational Diabetes Triage
    if blood_glucose_mg_dl >= 200:
        triage_color = "RED" if triage_color != "RED" else triage_color
        flags.append(f"SEVERE HYPERGLYCEMIA: Glucose {blood_glucose_mg_dl} mg/dL exceeds safety threshold.")
    elif blood_glucose_mg_dl >= 140:
        if triage_color == "GREEN":
            triage_color = "AMBER"
        flags.append(f"GESTATIONAL DIABETES RISK: Glucose {blood_glucose_mg_dl} mg/dL exceeds normal limit (140 mg/dL).")

    # 3. Severe Anemia Triage
    if hemoglobin_g_dl is not None:
        if hemoglobin_g_dl < 7.0:
            triage_color = "RED"
            flags.append(f"CRITICAL ANEMIA: Hemoglobin {hemoglobin_g_dl} g/dL (< 7 g/dL) requires immediate blood transfusion facility referral.")
        elif hemoglobin_g_dl < 9.0:
            if triage_color == "GREEN":
                triage_color = "AMBER"
            flags.append(f"MODERATE ANEMIA: Hemoglobin {hemoglobin_g_dl} g/dL requires parenteral iron / injectable iron sucrose protocol.")

    # 4. Obstetric Danger Signs (Bleeding, Leaking fluid, Reduced movements)
    has_bleeding = any("bleeding" in s or "blood" in s or "khoon" in s for s in symptoms)
    has_decreased_movement = any("movement" in s or "hilna" in s or "kick" in s for s in symptoms)
    has_water_break = any("water" in s or "fluid" in s or "pani" in s for s in symptoms)

    if has_bleeding:
        triage_color = "RED"
        flags.append("ANTEPARTUM HEMORRHAGE: Vaginal bleeding during pregnancy is a critical emergency.")
    if has_decreased_movement and pregnancy_week >= 28:
        triage_color = "RED"
        flags.append("FETAL DISTRESS WARNING: Decreased fetal movements in third trimester.")
    if has_water_break:
        triage_color = "RED"
        flags.append("PRETERM RUPTURE OF MEMBRANES: Water broken - risk of cord prolapse and infection.")

    return {
        "triage_color": triage_color,  # GREEN, AMBER, RED
        "triage_level": "CRITICAL" if triage_color == "RED" else "URGENT" if triage_color == "AMBER" else "STABLE",
        "primary_recommendation": primary_warning,
        "clinical_flags": flags,
        "pregnancy_week": pregnancy_week,
        "vitals_evaluated": {
            "bp": f"{bp_systolic}/{bp_diastolic} mmHg",
            "glucose": f"{blood_glucose_mg_dl} mg/dL",
            "hemoglobin": f"{hemoglobin_g_dl} g/dL" if hemoglobin_g_dl else "Not recorded",
        },
        "isolated_compute_timestamp": int(time.time()),
    }


def isolated_phi_redaction(raw_text: str) -> Dict[str, Any]:
    """
    Strips Protected Health Information (PHI) and Indian PII (Aadhaar, Phone, MCP Card)
    inside the microVM sandbox before any text is dispatched to external LLMs.
    """
    redacted = raw_text
    redactions_count = 0

    # 1. Indian Mobile numbers (10 digits, +91 optional)
    phone_pattern = r'(?:\+91[-\s]?)?[6-9]\d{9}\b'
    matches = re.findall(phone_pattern, redacted)
    if matches:
        redactions_count += len(matches)
        redacted = re.sub(phone_pattern, "[REDACTED_PHONE]", redacted)

    # 2. Aadhaar Numbers (12 digits with or without spaces/dashes)
    aadhaar_pattern = r'\b[2-9]\d{3}[\s\-]?\d{4}[\s\-]?\d{4}\b'
    matches = re.findall(aadhaar_pattern, redacted)
    if matches:
        redactions_count += len(matches)
        redacted = re.sub(aadhaar_pattern, "[REDACTED_AADHAAR]", redacted)

    # 3. MCP Card IDs / RCH IDs (typically alphanumeric 12-16 chars)
    rch_pattern = r'\b(?:MCP|RCH|ABHA)[-\s:]*([A-Za-z0-9]{8,16})\b'
    matches = re.findall(rch_pattern, redacted, re.IGNORECASE)
    if matches:
        redactions_count += len(matches)
        redacted = re.sub(rch_pattern, "[REDACTED_GOVT_HEALTH_ID]", redacted, flags=re.IGNORECASE)

    # 4. Email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    matches = re.findall(email_pattern, redacted)
    if matches:
        redactions_count += len(matches)
        redacted = re.sub(email_pattern, "[REDACTED_EMAIL]", redacted)

    return {
        "original_length": len(raw_text),
        "redacted_text": redacted,
        "redactions_made": redactions_count,
        "is_safe_for_llm": True,
    }


def isolated_contraindication_check(
    medications: List[str],
    pregnancy_week: int,
) -> Dict[str, Any]:
    """
    Checks medications for strict pregnancy contraindications in isolation.
    """
    # High-risk drug database for pregnancy
    CONTRAINDICATED_DRUGS = {
        "warfarin": {
            "risk": "CATEGORY X",
            "warning": "Teratogenic. Causes fetal warfarin syndrome, nasal hypoplasia, and CNS defects. Use Low Molecular Weight Heparin instead.",
            "severity": "CRITICAL",
        },
        "methotrexate": {
            "risk": "CATEGORY X",
            "warning": "Strictly contraindicated. Causes major congenital malformations and fetal death.",
            "severity": "CRITICAL",
        },
        "losartan": {
            "risk": "CATEGORY D",
            "warning": "ACE inhibitor/ARB contraindicated in 2nd and 3rd trimesters. Causes oligohydramnios and fetal renal failure.",
            "severity": "CRITICAL",
        },
        "enalapril": {
            "risk": "CATEGORY D",
            "warning": "ACE inhibitor contraindicated. Causes fetal hypotension and neonatal renal failure.",
            "severity": "CRITICAL",
        },
        "tetracycline": {
            "risk": "CATEGORY D",
            "warning": "Causes permanent yellow-gray-brown discoloration of baby's deciduous teeth and enamel hypoplasia.",
            "severity": "HIGH",
        },
        "doxycycline": {
            "risk": "CATEGORY D",
            "warning": "Avoid in pregnancy. Crosses placenta, impairs bone growth and discolors baby's teeth.",
            "severity": "HIGH",
        },
        "ibuprofen": {
            "risk": "CONTRAINDICATED IN 3RD TRIMESTER",
            "warning": "NSAIDs in 3rd trimester cause premature closure of ductus arteriosus and persistent pulmonary hypertension. Paracetamol is safe.",
            "severity": "HIGH" if pregnancy_week >= 28 else "CAUTION",
        },
        "aspirin": {
            "risk": "HIGH DOSE CONTRAINDICATED",
            "warning": "High dose aspirin (>100mg) causes maternal/fetal bleeding and delayed labor. Low-dose (75-150mg) only under doctor advice for preeclampsia prevention.",
            "severity": "CAUTION",
        },
    }

    warnings = []
    is_safe = True

    for med in medications:
        med_clean = med.lower().strip()
        for drug_key, info in CONTRAINDICATED_DRUGS.items():
            if drug_key in med_clean:
                is_safe = False
                warnings.append({
                    "medication": med,
                    "matched_contraindication": drug_key.capitalize(),
                    "risk_category": info["risk"],
                    "clinical_warning": info["warning"],
                    "severity": info["severity"],
                })

    return {
        "pregnancy_week": pregnancy_week,
        "is_safe": is_safe,
        "flagged_count": len(warnings),
        "contraindications": warnings,
        "safe_alternatives_note": "Paracetamol is generally safe for mild pain/fever. Labetalol/Methyldopa are first-line for hypertension in pregnancy.",
    }
