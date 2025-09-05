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
    cm85.buscar("2021-01-01", "2021-12-31")
    cm85.exportar_excel()