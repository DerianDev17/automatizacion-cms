import pytest
from cms_automation.pages.ws02_transacciones_page import WS02TransaccionesPage

@pytest.mark.ws02
def test_ws02_consulta_transacciones_switch(page, login):
    menu = login()
    ws02 = WS02TransaccionesPage(page)
    ws02.open_from_menu(menu)

    # Rango solicitado: hasta hoy, desde 7 días antes
    ws02.set_rango_ultimos_dias(dias=5)

    ws02.consultar_y_capturar()
