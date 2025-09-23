"""
Prueba end‑to‑end del módulo CM46 – Reporte de Lotes Pendientes.
Genera el reporte y valida la descarga.
"""

import pytest

from cms_automation.pages.cm46_lotes_pendientes_page import CM46LotesPendientesPage


@pytest.mark.cm46
def test_cm46_reporte_lotes_pendientes(page, login):
    menu = login()
    cm46 = CM46LotesPendientesPage(page)
    cm46.open_from_menu(menu)
    cm46.generar_y_capturar()
    cm46.descargar_excel()