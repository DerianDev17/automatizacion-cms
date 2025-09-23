"""
Prueba end‑to‑end del módulo CM44 – Reimpresión de Documentos de Solicitud.
Busca una solicitud y descarga el reporte de reimpresión.
"""

import pytest
from cms_automation.pages.cm44_reimpresion_page import CM44ReimpresionPage


CARD_NUMBER = "4281502050002267"


@pytest.mark.cm44
def test_cm44_reimpresion_documentos(page, login):
    menu = login()
    cm44 = CM44ReimpresionPage(page)
    cm44.open_from_menu(menu)
    # delegar ejecución al page-object (usa CSV por defecto)
    cm44.run_all_from_csv()