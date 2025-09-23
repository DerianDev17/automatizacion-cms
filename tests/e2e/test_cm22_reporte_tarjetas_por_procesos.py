"""
Prueba end‑to‑end del módulo CM22 – Reporte de Tarjetas por Procesos.
Selecciona un proceso y genera el reporte.
"""

import pytest
from datetime import date, timedelta

from cms_automation.pages.cm22_procesos_page import CM22ProcesosPage


@pytest.mark.cm22
def test_cm22_reporte_tarjetas_por_procesos(page, login):
    menu = login()
    cm22 = CM22ProcesosPage(page)
    cm22.open_from_menu(menu)
    cm22.run_and_capture()
    cm22.validar_resultados()