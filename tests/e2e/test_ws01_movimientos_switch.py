"""
Test end-to-end para el módulo WS01 - Reporte de Movimientos Switch.
Verifica la generación de reportes detallados de movimientos.
"""

import pytest
from datetime import datetime
from cms_automation.pages.ws01_movimientos_page import WS01MovimientosPage


@pytest.mark.ws01
def test_ws01_reporte_movimientos_switch(page, login):
    """Verifica la generación del reporte de movimientos switch con detalles."""
    menu = login()
    ws01 = WS01MovimientosPage(page)
    ws01.open_from_menu(menu)
    ws01.set_fechas(datetime.now())  # Fecha fin = hoy, inicio = hoy - 15 días
    ws01.seleccionar_detalle()
    ws01.generar_y_capturar_reporte()