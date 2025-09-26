"""Esqueleto de pruebas para el ciclo de vida de Tarjetas nominadas."""

import pytest

from cms_automation.utils.workflows import (
    TARJETA_NOMINADA_WORKFLOW,
    workflow_to_pytest_params,
)

pytestmark = [
    pytest.mark.ciclo_nominada,
    pytest.mark.skip(reason="pendiente implementación"),
]


@pytest.mark.parametrize(
    "codigo, descripcion",
    workflow_to_pytest_params(TARJETA_NOMINADA_WORKFLOW),
    ids=lambda param: param[0],
)
def test_ciclo_tarjeta_nominada(codigo: str, descripcion: str) -> None:
    """Cada paso se implementará cuando el flujo end-to-end esté listo."""

    pass
