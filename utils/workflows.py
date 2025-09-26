"""Definiciones centralizadas de los ciclos de vida de tarjetas.

Este módulo contiene únicamente datos (sin lógica) que describen el
orden y la descripción de cada paso involucrado en los flujos de
*Tarjetas nominadas* y *Tarjetas innominadas*. Al mantener la
información en un único lugar, los tests y los Page Objects pueden
consumirla sin duplicar cadenas o códigos de módulo.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence, Tuple


@dataclass(frozen=True)
class WorkflowStep:
    """Representa un paso atómico dentro de un flujo del CMS."""

    code: str
    description: str

    def label(self) -> str:
        """Etiqueta conveniente para reportes o parametrizaciones."""

        return f"{self.code} — {self.description}"


TARJETA_NOMINADA_WORKFLOW: Tuple[WorkflowStep, ...] = (
    WorkflowStep(
        "CM01",
        "Solicitud de tarjeta - Ciclo vida Tarjeta nominada",
    ),
    WorkflowStep(
        "CM10",
        "Emisión de tarjetas - Ciclo vida Tarjeta nominada",
    ),
    WorkflowStep(
        "CM07",
        "Recepción de tarjetas - Ciclo vida Tarjeta nominada",
    ),
    WorkflowStep(
        "CM03",
        "Entrega de tarjetas - Ciclo vida Tarjeta nominada",
    ),
    WorkflowStep(
        "CM02",
        "Solicitud de tarjeta adicional - Ciclo vida Tarjeta nominada",
    ),
)
"""Pasos oficiales del ciclo de vida de tarjetas nominadas."""


TARJETA_INNOMINADA_WORKFLOW: Tuple[WorkflowStep, ...] = (
    WorkflowStep(
        "CM83",
        "Cupos por oficina - Ciclo vida Tarjeta innominada",
    ),
    WorkflowStep(
        "CM70",
        "Solicitud de tarjetas innominadas - Ciclo vida Tarjeta innominada",
    ),
    WorkflowStep(
        "CM10",
        "Emisión de tarjetas - Ciclo vida Tarjeta innominada",
    ),
    WorkflowStep(
        "CM07",
        "Recepción de tarjetas - Ciclo vida Tarjeta innominada",
    ),
    WorkflowStep(
        "CM06",
        "Mantenimiento de tarjetas - Ciclo vida Tarjeta innominada",
    ),
)
"""Pasos oficiales del ciclo de vida de tarjetas innominadas."""


def workflow_to_pytest_params(workflow: Sequence[WorkflowStep]) -> List[Tuple[str, str]]:
    """Convierte un flujo en parámetros `(código, descripción)` para pytest."""

    return [(step.code, step.description) for step in workflow]
