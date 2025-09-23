"""
Prueba end‑to‑end del módulo CM16 – Tarjetas por Cuentas.
Consulta las tarjetas asociadas a una cuenta bancaria y valida resultados.
"""

import pytest

from cms_automation.pages.cm16_cuenta_page import CM16CuentaPage


@pytest.mark.cm16
def test_cm16_tarjetas_por_cuentas(page, login):
    menu = login()
    cm16 = CM16CuentaPage(page)
    cm16.open_from_menu(menu)
    # delegar la operación al page-object
    cm16.procesar_and_capture(cuenta="020101166985", tipo_cuenta="AH", screenshot_report="screenshot_cm16_report.png")