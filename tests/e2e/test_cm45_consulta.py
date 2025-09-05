"""
Prueba end‑to‑end del módulo CM45 – Consulta de Tarjetas.
Realiza una búsqueda por número de tarjeta y valida que existan resultados
en la tabla【547172095933312†L194-L202】.
"""

import pytest

from cms_automation.pages.cm45_consulta_page import CM45ConsultaPage


@pytest.mark.cm45
def test_cm45_consulta_tarjetas(page, login):
    menu = login()
    cm45 = CM45ConsultaPage(page)
    cm45.open_from_menu(menu)
    cm45.buscar("tarjeta", "5353********1234")
    cm45.validar_resultados()