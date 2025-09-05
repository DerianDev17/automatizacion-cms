"""
Prueba end‑to‑end del módulo CM21 – Consulta de Clave.
Consulta la clave asociada a un identificador y valida la respuesta.
"""

import pytest

from cms_automation.pages.cm21_clave_page import CM21ClavePage


@pytest.mark.cm21
def test_cm21_reporte_consultas_clave(page, login):
    menu = login()
    cm21 = CM21ClavePage(page)
    cm21.open_from_menu(menu)
    cm21.consultar_clave("IDENT123")