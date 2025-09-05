"""
Prueba end‑to‑end del módulo CM18 – Tarjetas por Opción.
Selecciona una opción de clasificación y genera el reporte【547172095933312†L194-L203】.
"""

import pytest

from cms_automation.pages.cm18_opcion_page import CM18OpcionPage


@pytest.mark.cm18
def test_cm18_tarjetas_por_opcion(page, login):
    menu = login()
    cm18 = CM18OpcionPage(page)
    cm18.open_from_menu(menu)
    cm18.seleccionar_opcion("Opción 1")  # TODO: actualizar con opción real
    cm18.generar_reporte()
    cm18.validar_resultados()