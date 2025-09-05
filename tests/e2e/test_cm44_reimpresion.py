"""
Prueba end‑to‑end del módulo CM44 – Reimpresión de Solicitudes.
Verifica la capacidad de buscar solicitudes de reimpresión y de descargar el
reporte correspondiente【547172095933312†L194-L202】.
"""

import pytest

from cms_automation.pages.cm44_reimpresion_page import CM44ReimpresionPage


@pytest.mark.cm44
def test_cm44_reimpresion(page, login):
    menu = login()
    cm44 = CM44ReimpresionPage(page)
    cm44.open_from_menu(menu)
    cm44.buscar_por_solicitud("SOLIC123")  # TODO: reemplazar con un identificador válido
    cm44.descargar_reporte()