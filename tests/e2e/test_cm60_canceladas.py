"""
Prueba end‑to‑end del módulo CM60 – Tarjetas Canceladas【547172095933312†L219-L220】.
Filtra por rango de fechas y valida que se obtienen resultados.
"""

import pytest

from cms_automation.pages.cm60_canceladas_page import CM60CanceladasPage


@pytest.mark.cm60
def test_cm60_tarjetas_canceladas(page, login):
    menu = login()
    cm60 = CM60CanceladasPage(page)
    cm60.open_from_menu(menu)
    cm60.buscar("2021-01-01", "2021-12-31")  # TODO: ajustar fechas al entorno
    cm60.validar_resultados()