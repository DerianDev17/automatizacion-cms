"""
Prueba end‑to‑end del módulo CM60 – Reporte de Tarjetas Canceladas.
Busca tarjetas canceladas en un rango de fechas y valida resultados.
"""

import pytest

from cms_automation.pages.cm60_canceladas_page import CM60CanceladasPage


@pytest.mark.cm60
def test_cm60_reporte_tarjetas_canceladas(page, login):
    menu = login()
    cm60 = CM60CanceladasPage(page)
    cm60.open_from_menu(menu)
    cm60.buscar("2021-01-01", "2021-12-31")
    cm60.validar_resultados()