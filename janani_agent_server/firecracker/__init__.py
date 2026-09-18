"""
janani_agent_server/firecracker package

Firecracker MicroVM isolated execution engine for Janani Setu.
Enables secure, lightweight sandboxed processing for sensitive maternal health
workloads (PHI scrubbing, clinical risk assessment, prescription verification).
"""

from .sandbox import (
    FirecrackerMicroVMRunner,
    execute_in_microvm,
    get_microvm_status,
)
from .sensitive_tasks import (
    isolated_clinical_triage,
    isolated_phi_redaction,
    isolated_contraindication_check,
)

__all__ = [
    "FirecrackerMicroVMRunner",
    "execute_in_microvm",
    "get_microvm_status",
    "isolated_clinical_triage",
    "isolated_phi_redaction",
    "isolated_contraindication_check",
]
