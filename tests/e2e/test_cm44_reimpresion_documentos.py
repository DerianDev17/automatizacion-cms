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
    # buscar por tarjeta y descargar reporte; el número puede venir de datos/fixture
    cm44.buscar_por_tarjeta(CARD_NUMBER)
    cm44.descargar_reporte()