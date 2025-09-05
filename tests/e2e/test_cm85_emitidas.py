"""
Prueba end‑to‑end del módulo CM85 – Reporte de Tarjetas Emitidas【547172095933312†L211-L213】.
Genera el reporte para un rango de fechas y valida la exportación a Excel.
"""

import pytest

from cms_automation.pages.cm85_emitidas_page import CM85EmitidasPage


@pytest.mark.cm85
def test_cm85_tarjetas_emitidas(page, login):
    menu = login()
    cm85 = CM85EmitidasPage(page)
    cm85.open_from_menu(menu)
    cm85.buscar("2021-01-01", "2021-12-31")
    cm85.exportar_excel()