"""
Pruebas esqueleto para los módulos del CMS que aún no tienen
automatización implementada. Estas pruebas verifican simplemente que la
navegación al módulo sea posible mediante el menú. Cuando se
implemente cada módulo, se deben reemplazar estas pruebas con casos
concretos que interactúen con los formularios y validen salidas.
"""

import pytest

from cms_automation.pages.placeholders import (
    CM87HistoriaOficinaPage,
    CMA4EmitidasProductoPage,
    CM88AnuladasSuspendidasPage,
    CM17CostosPage,
    CM89VencerPage,
    CM97BinPage,
    MD16AutorizacionesPage,
)


@pytest.mark.parametrize(
    "placeholder_class",
    [
        CM87HistoriaOficinaPage,
        CMA4EmitidasProductoPage,
        CM88AnuladasSuspendidasPage,
        CM17CostosPage,
        CM89VencerPage,
        CM97BinPage,
        MD16AutorizacionesPage,
    ],
)
def test_placeholder_navegacion(page, login, placeholder_class):
    """
    Verifica que se pueda abrir el módulo placeholder desde el menú y que la
    clase placeholder indique que falta la implementación.
    """
    menu = login()
    placeholder = placeholder_class(page)
    # Navega a la página
    placeholder.open_from_menu(menu)
    # La siguiente llamada debería lanzar NotImplementedError
    with pytest.raises(NotImplementedError):
        placeholder.not_implemented()