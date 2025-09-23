"""
Prueba end‑to‑end del módulo CM14 – Trazabilidad de Tarjetas.
Busca la trazabilidad de una tarjeta específica y valida que se muestren resultados.
"""

import pytest
from cms_automation.pages.cm14_trazabilidad_page import CM14TrazabilidadPage


@pytest.mark.cm14
def test_cm14_trazabilidad_tarjetas(page, login):
    menu = login()
    cm14 = CM14TrazabilidadPage(page)
    cm14.open_from_menu(menu)

    # delegar la ejecución completa al page-object (carga CSV y procesado)
    cm14.run_all_from_csv()