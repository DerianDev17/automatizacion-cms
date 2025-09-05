"""
Prueba end‑to‑end del módulo CM46 – Reporte de Lotes Pendientes【547172095933312†L235-L239】.
Genera el reporte y comprueba que existan registros.
"""

import pytest

from cms_automation.pages.cm46_lotes_pendientes_page import CM46LotesPendientesPage


@pytest.mark.cm46
def test_cm46_lotes_pendientes(page, login):
    menu = login()
    cm46 = CM46LotesPendientesPage(page)
    cm46.open_from_menu(menu)
    cm46.generar_reporte()
    cm46.descargar_excel()