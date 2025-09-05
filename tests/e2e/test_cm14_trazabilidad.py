"""
Prueba end‑to‑end del módulo CM14 – Trazabilidad de Tarjetas.

Este test verifica que un usuario pueda consultar la trazabilidad de una tarjeta
específica y que el sistema despliegue resultados. La tarjeta utilizada debe
existir en el entorno de pruebas o puede ser un número ficticio si el
sistema permite búsquedas sin resultados. Las referencias a la guía
operativa se encuentran en la lista de módulos【547172095933312†L194-L204】.
"""

import pytest

from cms_automation.pages.cm14_trazabilidad_page import CM14TrazabilidadPage


@pytest.mark.cm14
def test_cm14_trazabilidad(page, login):
    """Ejecuta la búsqueda de trazabilidad para una tarjeta y valida resultados."""
    menu = login()
    cm14 = CM14TrazabilidadPage(page)
    cm14.open_from_menu(menu)
    cm14.buscar_por_numero("5353********1234")  # TODO: reemplazar con un número válido
    cm14.validar_resultados(min_rows=1)