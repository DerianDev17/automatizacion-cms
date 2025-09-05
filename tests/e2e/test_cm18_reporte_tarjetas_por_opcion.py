"""
Prueba end‑to‑end del módulo CM18 – Reporte de Tarjetas por Opción.
Selecciona una opción y genera el reporte.
"""

import pytest

from cms_automation.pages.cm18_opcion_page import CM18OpcionPage


@pytest.mark.cm18
def test_cm18_reporte_tarjetas_por_opcion(page, login):
    menu = login()
    cm18 = CM18OpcionPage(page)
    cm18.open_from_menu(menu)
    cm18.seleccionar_opcion("Opción 1")
    cm18.generar_reporte()
    cm18.validar_resultados()