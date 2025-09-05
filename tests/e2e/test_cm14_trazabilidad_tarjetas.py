"""
Prueba end‑to‑end del módulo CM14 – Trazabilidad de Tarjetas.
Busca la trazabilidad de una tarjeta específica y valida que se muestren resultados.
"""

import pytest
from cms_automation.pages.cm14_trazabilidad_page import CM14TrazabilidadPage

CARD_NUMBER = "4281502050002267"


@pytest.mark.cm14
def test_cm14_trazabilidad_tarjetas(page, login):
    menu = login()
    cm14 = CM14TrazabilidadPage(page)
    cm14.open_from_menu(menu)

    # Entrar al iframe CM14
    iframe_el = page.wait_for_selector("iframe[name='iframe_CM14']", timeout=30_000)
    frame = iframe_el.content_frame()

    # Ingresar tarjeta y disparar postback
    frame.fill("#ctl00_maincontent_TxtTarjeta", CARD_NUMBER)
    frame.evaluate("__doPostBack('ctl00$maincontent$TxtTarjeta','');")
    frame.wait_for_timeout(2_000)

    # Click en “Imprimir” para abrir popup PDF
    btn_imprimir = frame.locator("#ctl00_maincontent_BtnImprimir:not([disabled])")
    btn_imprimir.wait_for(state="visible", timeout=30_000)

    # Capturar el popup con el PDF
    with page.expect_popup() as popup_info:
        btn_imprimir.click()
    report = popup_info.value
    report.wait_for_load_state("load")
    report.wait_for_timeout(1_000)
    report.screenshot(path="screenshot_cm14_report.png", full_page=True)

    # Cerrar el popup y volver al tab principal
    report.close()
    page.bring_to_front()

    # Volver a hacer click para que aparezca “Fin del Reporte”
    btn_imprimir.click()
    frame.wait_for_selector("text=Fin del Reporte", timeout=30_000)

    # Captura de la pantalla con “Fin del Reporte”
    page.wait_for_timeout(1_000)
    page.screenshot(path="screenshot_cm14_result.png", full_page=True)