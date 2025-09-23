"""
Prueba end‑to‑end del módulo CM21 – Consulta de Clave.
Flujo adaptado: login manual con credenciales del snippet, apertura de CM21,
relleno de fechas, búsqueda por tarjeta, y captura del reporte.
"""

from datetime import date, timedelta
import csv
from pathlib import Path
from playwright.sync_api import Page
import pytest

from cms_automation.pages.menu_page import MenuPage
from cms_automation.pages.cm21_clave_page import CM21ClavePage


# Cargar tarjetas desde CSV en tiempo de colección (igual que CM14/CM19)
DATA_DIR = Path(__file__).parent.parent / "data"
CSV_PATH = DATA_DIR / "cards.csv"

 
@pytest.mark.cm21
def test_cm21_reporte_consultas_clave(page, login):
    menu = login("admin")
    cm21 = CM21ClavePage(page)
    cm21.open_from_menu(menu)
    cm21.run_all_from_csv()