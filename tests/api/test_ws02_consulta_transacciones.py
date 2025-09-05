"""
Prueba de integración para el servicio WS02 – Consulta de Transacciones del Switch.
Al igual que el caso WS01, esta prueba se deja como esqueleto hasta que
exista un endpoint real. Una vez implementado el servicio, realiza la
consulta con parámetros adecuados y comprueba que la respuesta coincide
con el esquema esperado.
"""

import pytest


@pytest.mark.ws02
def test_ws02_consulta_transacciones():
    pytest.skip("WS02 todavía no se ha implementado.")