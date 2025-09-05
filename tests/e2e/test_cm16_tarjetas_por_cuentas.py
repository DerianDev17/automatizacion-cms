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

    # Entrar al iframe CM16
    iframe_el = page.wait_for_selector("iframe[name='iframe_CM16']", timeout=30_000)
    frame = iframe_el.content_frame()

    # Seleccionar tipo de cuenta y rellenar número de cuenta
    frame.locator("select#ctl00_maincontent_CboTipoCuenta").select_option(label="AH")
    frame.locator("input#ctl00_maincontent_TxtCuenta").fill("020101166985")

    # Click en "Aceptar" y esperar el popup PDF
    with page.expect_popup() as popup_info:
        frame.get_by_role("button", name="Aceptar").click()
    report_page = popup_info.value

    # Esperar a que el PDF cargue completamente
    report_page.wait_for_load_state("load")
    report_page.wait_for_timeout(1_000)

    # Screenshot del reporte
    report_page.screenshot(path="screenshot_cm16_report.png", full_page=True)

    # Volver al menú principal
    page.bring_to_front()
    page.wait_for_selector("input[placeholder='Opción']")