"""
Prueba end‑to‑end del módulo CM22 – Reporte de Tarjetas por Procesos【547172095933312†L221-L224】.
Selecciona un proceso y genera el reporte.
"""

import pytest

from cms_automation.pages.cm22_procesos_page import CM22ProcesosPage


@pytest.mark.cm22
def test_cm22_reporte_procesos(page, login):
    menu = login()
    cm22 = CM22ProcesosPage(page)
    cm22.open_from_menu(menu)
    cm22.seleccionar_proceso("Emisión")  # TODO: proceso real
    cm22.generar_reporte()
    cm22.validar_resultados()