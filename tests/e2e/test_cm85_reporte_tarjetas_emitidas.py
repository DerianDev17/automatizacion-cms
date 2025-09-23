"""
Prueba end‑to‑end del módulo CM85 – Reporte de Tarjetas Emitidas.
Genera y exporta el reporte en un rango de fechas.
"""

import pytest

from cms_automation.pages.cm85_emitidas_page import CM85EmitidasPage


@pytest.mark.cm85
def test_cm85_reporte_tarjetas_emitidas(page, login):
    menu = login()
    cm85 = CM85EmitidasPage(page)
    cm85.open_from_menu(menu)

    # según la captura, la fecha de emisión requerida es 9/17/2025 -> formato YYYY/MM/DD
    emission_date = "2025/09/17"

    # seleccionar BIN, desmarcar checks, elegir modelo y fijar fecha
    cm85.set_bin("423216")
    cm85.uncheck_modelo_oficina()
    cm85.set_modelo("VISA CLASICA")
    cm85.set_fecha_emision(emission_date)

    # procesar y capturar el PDF resultante
    cm85.procesar_and_capture(screenshot_report="screenshot_cm85_report.png")