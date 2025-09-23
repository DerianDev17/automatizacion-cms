"""
Prueba end‑to‑end del módulo CM60 – Reporte de Tarjetas Canceladas.
Busca tarjetas canceladas en un rango de fechas y valida resultados.
"""

import pytest

from cms_automation.pages.cm60_canceladas_page import CM60CanceladasPage
from datetime import date, timedelta


@pytest.mark.cm60
def test_cm60_reporte_tarjetas_canceladas(page, login):
    menu = login()
    cm60 = CM60CanceladasPage(page)
    cm60.open_from_menu(menu)
    # usar el page-object para fijar fechas, filtros y generar/capturar evidencia
    cm60.set_date_range_days(15)
    cm60.set_filters(por="Oficina Origen", oficina="Todas", motivo="Todos")
    cm60.generate_and_capture(screenshot_report="screenshot_cm60_report.png", screenshot_result="screenshot_cm60_result.png")