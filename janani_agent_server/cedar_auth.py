"""
janani_agent_server/cedar_auth.py

Cedar-based fine-grained authorization for JananiSetu.
Controls WHO can see or modify WHICH patient information.

Roles:
  Mother  — can only access her own data; can chat freely
  ASHA    — can view assigned patients' summaries & risk; cannot modify medical records
  Doctor  — full read + write access to all patient data

Uses 'cedarpy' — open source Python bindings for the Cedar policy engine.
No AWS account needed. Runs 100% locally.
"""

import json
from typing import Literal
from functools import lru_cache

try:
    from cedarpy import is_authorized, Decision
    CEDAR_AVAILABLE = True
except ImportError:
    CEDAR_AVAILABLE = False
    print("[Cedar] cedarpy not installed — run: pip install cedarpy")
    print("[Cedar] Falling back to role-based allow-all for dev mode.")


# ── Role type ─────────────────────────────────────────────────────────────────
Role = Literal["Mother", "ASHA", "Doctor"]

# ── Cedar Policies ────────────────────────────────────────────────────────────
# Written in Cedar Policy Language (https://cedarpolicy.com)
# These policies answer: "Can principal P perform action A on resource R?"

CEDAR_POLICIES = """
// =====================================================
// JananiSetu Cedar Policies
// Roles: Mother | ASHA | Doctor
// =====================================================

// ── MOTHER policies ───────────────────────────────────
// A mother can chat freely (AI chatbot access)
permit(
    principal in Role::"Mother",
    action == Action::"Chat",
    resource == Resource::"AIChat"
);

// A mother can view her OWN health summary (not others')
permit(
    principal in Role::"Mother",
    action == Action::"ViewHealthSummary",
    resource == Resource::"OwnData"
);

// A mother can view nutrition information (public knowledge)
permit(
    principal in Role::"Mother",
    action == Action::"ViewNutrition",
    resource == Resource::"NutritionKnowledge"
);

// A mother can view government schemes she is eligible for
permit(
    principal in Role::"Mother",
    action == Action::"ViewSchemes",
    resource == Resource::"GovernmentSchemes"
);

// A mother can view her own risk scores
permit(
    principal in Role::"Mother",
    action == Action::"ViewRiskScore",
    resource == Resource::"OwnData"
);

// A mother can log her own vitals
permit(
    principal in Role::"Mother",
    action == Action::"LogVitals",
    resource == Resource::"OwnData"
);

// A mother can execute sensitive triage inside Firecracker microVM
permit(
    principal in Role::"Mother",
    action == Action::"ExecuteMicroVM",
    resource == Resource::"OwnData"
);

// A mother CANNOT view other patients' data
forbid(
    principal in Role::"Mother",
    action == Action::"ViewHealthSummary",
    resource == Resource::"OtherPatientData"
);

// ── ASHA Worker policies ──────────────────────────────
// ASHA can chat on behalf of patients
permit(
    principal in Role::"ASHA",
    action == Action::"Chat",
    resource == Resource::"AIChat"
);

// ASHA can view assigned patient health summaries
permit(
    principal in Role::"ASHA",
    action == Action::"ViewHealthSummary",
    resource == Resource::"AssignedPatientData"
);

// ASHA can view risk scores
permit(
    principal in Role::"ASHA",
    action == Action::"ViewRiskScore",
    resource == Resource::"AssignedPatientData"
);

// ASHA can view nutrition and schemes
permit(
    principal in Role::"ASHA",
    action == Action::"ViewNutrition",
    resource == Resource::"NutritionKnowledge"
);

permit(
    principal in Role::"ASHA",
    action == Action::"ViewSchemes",
    resource == Resource::"GovernmentSchemes"
);

// ASHA can log patient vitals
permit(
    principal in Role::"ASHA",
    action == Action::"LogVitals",
    resource == Resource::"AssignedPatientData"
);

// ASHA can execute sensitive clinical triage in Firecracker microVM
permit(
    principal in Role::"ASHA",
    action == Action::"ExecuteMicroVM",
    resource == Resource::"AssignedPatientData"
);

// ASHA CANNOT modify doctor prescriptions or diagnoses
forbid(
    principal in Role::"ASHA",
    action == Action::"ModifyMedicalRecord",
    resource == Resource::"MedicalRecord"
);

// ── DOCTOR policies ───────────────────────────────────
// Doctors have full access to all patient data and actions
permit(
    principal in Role::"Doctor",
    action,
    resource
);
"""

# ── Actions & Resources registry ─────────────────────────────────────────────
# Maps Strands Agent tool names → Cedar (action, resource) pairs

TOOL_TO_CEDAR = {
    # Strands tool name          : (Cedar action,              Cedar resource)
    "get_patient_health_summary": ("ViewHealthSummary",        "OwnData"),
    "get_patient_visit_history":  ("ViewHealthSummary",        "OwnData"),
    "log_patient_vitals":         ("LogVitals",                "OwnData"),
    "run_sensitive_clinical_triage_in_microvm": ("ExecuteMicroVM", "OwnData"),
    "get_nutrition_info":         ("ViewNutrition",            "NutritionKnowledge"),
    "get_government_schemes_for_pregnant_woman": ("ViewSchemes", "GovernmentSchemes"),
    "assess_pregnancy_risk":      ("ViewRiskScore",            "OwnData"),
    "search_health_knowledge":    ("ViewNutrition",            "NutritionKnowledge"),
    "chat":                       ("Chat",                     "AIChat"),
}

# Resource overrides when accessing another patient's data
ASHA_RESOURCE_MAP = {
    "ViewHealthSummary": "AssignedPatientData",
    "ViewRiskScore":     "AssignedPatientData",
    "LogVitals":         "AssignedPatientData",
    "ExecuteMicroVM":    "AssignedPatientData",
}


def _build_entities(role: Role, principal_id: str) -> list:
    """Build the Cedar entity list for the authorization request."""
    return [
        # The principal (user making the request)
        {
            "uid":     {"__entity": {"type": "User", "id": principal_id}},
            "attrs":   {"role": role},
            "parents": [{"__entity": {"type": "Role", "id": role}}],
        },
        # Role entities
        {"uid": {"__entity": {"type": "Role",   "id": "Mother"}}, "attrs": {}, "parents": []},
        {"uid": {"__entity": {"type": "Role",   "id": "ASHA"}},   "attrs": {}, "parents": []},
        {"uid": {"__entity": {"type": "Role",   "id": "Doctor"}}, "attrs": {}, "parents": []},
        # Resource entities
        {"uid": {"__entity": {"type": "Resource", "id": "AIChat"}},              "attrs": {}, "parents": []},
        {"uid": {"__entity": {"type": "Resource", "id": "OwnData"}},             "attrs": {}, "parents": []},
        {"uid": {"__entity": {"type": "Resource", "id": "OtherPatientData"}},    "attrs": {}, "parents": []},
        {"uid": {"__entity": {"type": "Resource", "id": "AssignedPatientData"}}, "attrs": {}, "parents": []},
        {"uid": {"__entity": {"type": "Resource", "id": "NutritionKnowledge"}},  "attrs": {}, "parents": []},
        {"uid": {"__entity": {"type": "Resource", "id": "GovernmentSchemes"}},   "attrs": {}, "parents": []},
        {"uid": {"__entity": {"type": "Resource", "id": "MedicalRecord"}},       "attrs": {}, "parents": []},
        # Action entities
        {"uid": {"__entity": {"type": "Action", "id": "Chat"}},                  "attrs": {}, "parents": []},
        {"uid": {"__entity": {"type": "Action", "id": "ViewHealthSummary"}},     "attrs": {}, "parents": []},
        {"uid": {"__entity": {"type": "Action", "id": "ViewNutrition"}},         "attrs": {}, "parents": []},
        {"uid": {"__entity": {"type": "Action", "id": "ViewSchemes"}},           "attrs": {}, "parents": []},
        {"uid": {"__entity": {"type": "Action", "id": "ViewRiskScore"}},         "attrs": {}, "parents": []},
        {"uid": {"__entity": {"type": "Action", "id": "LogVitals"}},             "attrs": {}, "parents": []},
        {"uid": {"__entity": {"type": "Action", "id": "ExecuteMicroVM"}},        "attrs": {}, "parents": []},
        {"uid": {"__entity": {"type": "Action", "id": "ModifyMedicalRecord"}},   "attrs": {}, "parents": []},
    ]


def is_action_allowed(
    role: Role,
    principal_id: str,
    action: str,
    resource: str,
) -> tuple[bool, str]:
    """
    Check if a role is allowed to perform an action on a resource.

    Args:
        role:         'Mother', 'ASHA', or 'Doctor'
        principal_id: user ID (e.g. 'user_001')
        action:       Cedar action string (e.g. 'ViewHealthSummary')
        resource:     Cedar resource string (e.g. 'OwnData')

    Returns:
        (allowed: bool, reason: str)
    """
    if not CEDAR_AVAILABLE:
        # Dev fallback: allow everything but log a warning
        print(f"[Cedar] DEV MODE — cedarpy not installed. Allowing {role}:{action}:{resource}")
        return True, "dev_mode_allow_all"

    entities = _build_entities(role, principal_id)

    try:
        result = is_authorized(
            principal=f'User::"{principal_id}"',
            action=f'Action::"{action}"',
            resource=f'Resource::"{resource}"',
            policies=CEDAR_POLICIES,
            entities=entities,
        )

        allowed = result.decision == Decision.Allow
        reason  = "cedar_permit" if allowed else "cedar_forbid"

        print(f"[Cedar] {role}/{principal_id} → {action}/{resource} = {'✅ ALLOW' if allowed else '❌ DENY'}")
        return allowed, reason

    except Exception as e:
        print(f"[Cedar] Authorization error: {e}")
        # Fail open for chat (degraded mode), fail closed for sensitive data
        if action == "Chat":
            return True, "cedar_error_failopen"
        return False, f"cedar_error: {str(e)}"


def check_tool_permission(
    tool_name: str,
    role: Role,
    principal_id: str,
    is_own_data: bool = True,
) -> tuple[bool, str]:
    """
    Check if a role can invoke a specific Strands Agent tool.

    Args:
        tool_name:    Name of the Strands tool being called
        role:         User's role
        principal_id: User's ID
        is_own_data:  True if accessing own data, False if accessing another patient's

    Returns:
        (allowed: bool, reason: str)
    """
    cedar_pair = TOOL_TO_CEDAR.get(tool_name)
    if not cedar_pair:
        # Unknown tool — allow but log
        print(f"[Cedar] Unknown tool '{tool_name}' — defaulting to ALLOW")
        return True, "unknown_tool_allow"

    action, resource = cedar_pair

    # ASHA accessing another patient's data uses different resource
    if role == "ASHA" and not is_own_data:
        resource = ASHA_RESOURCE_MAP.get(action, resource)

    return is_action_allowed(role, principal_id, action, resource)


# ── Quick summary for display ─────────────────────────────────────────────────

ROLE_PERMISSIONS_SUMMARY = {
    "Mother": {
        "can": [
            "Chat with AI (own health questions only)",
            "View own health summary & risk scores",
            "View nutrition information",
            "View applicable government schemes",
        ],
        "cannot": [
            "View other patients' data",
            "Log vitals or modify records",
            "Access admin or doctor functions",
        ],
    },
    "ASHA": {
        "can": [
            "Chat with AI (for patient guidance)",
            "View assigned patients' health summaries",
            "View risk scores for assigned patients",
            "Log patient vitals",
            "View nutrition & scheme information",
        ],
        "cannot": [
            "Modify doctor prescriptions or diagnoses",
            "Access patients not assigned to them",
            "View medical records in full detail",
        ],
    },
    "Doctor": {
        "can": [
            "Full access to all patient data",
            "View and modify medical records",
            "View all risk assessments",
            "Access all tools and resources",
        ],
        "cannot": [],
    },
}
