"""Utilidades compartidas del paquete `cms_automation`."""

from .workflows import (
    WorkflowStep,
    TARJETA_INNOMINADA_WORKFLOW,
    TARJETA_NOMINADA_WORKFLOW,
    workflow_to_pytest_params,
)

__all__ = [
    "WorkflowStep",
    "TARJETA_INNOMINADA_WORKFLOW",
    "TARJETA_NOMINADA_WORKFLOW",
    "workflow_to_pytest_params",
]
