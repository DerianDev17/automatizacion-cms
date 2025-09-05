"""
Prueba end‑to‑end del módulo CM19 – Historial de Tarjetas de Débito.
Consulta el historial de una tarjeta de débito determinada.
"""

import pytest

from cms_automation.pages.cm19_historial_page import CM19HistorialPage


@pytest.mark.cm19
def test_cm19_historial_tarjetas_debito(page, login):
    menu = login()
    cm19 = CM19HistorialPage(page)
    cm19.open_from_menu(menu)
    cm19.buscar_por_numero("5353********1234")
    cm19.validar_resultados()