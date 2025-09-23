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
    cm22.seleccionar_proceso()
    # establecer fechas específicas dentro del frame
    if cm22.frame is not None:
        hoy = date.today()
        inicio = hoy - timedelta(days=15)
        fmt = lambda d: d.strftime("%Y/%m/%d")
        cm22.frame.fill("#ctl00_maincontent_FecInicial", fmt(inicio))
        cm22.frame.fill("#ctl00_maincontent_FecFinal", fmt(hoy))

    cm22.seleccionar_detallado()
    cm22.imprimir_y_capturar_report()
    cm22.validar_resultados()