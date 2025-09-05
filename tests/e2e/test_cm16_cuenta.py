"""
Prueba end‑to‑end del módulo CM16 – Tarjeta por Cuenta.
Busca las tarjetas asociadas a una cuenta específica y valida resultados【547172095933312†L214-L220】.
"""

import pytest

from cms_automation.pages.cm16_cuenta_page import CM16CuentaPage


@pytest.mark.cm16
def test_cm16_tarjeta_por_cuenta(page, login):
    menu = login()
    cm16 = CM16CuentaPage(page)
    cm16.open_from_menu(menu)
    cm16.buscar_por_cuenta("1234567890")  # TODO: cuenta de pruebas
    cm16.validar_resultados()