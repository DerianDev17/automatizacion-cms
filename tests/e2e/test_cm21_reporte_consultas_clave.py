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
with open(CSV_PATH, newline="") as f:
    reader = csv.DictReader(f)
    CARDS = [row["card_number"] for row in reader]


@pytest.mark.cm21
@pytest.mark.parametrize("card_number", CARDS)
def test_cm21_reporte_consultas_clave(page: Page, login, card_number):
    # calcular fechas: fecha_fin = hoy, fecha_inicio = hoy - 15 dias
    fecha_fin = date.today()
    fecha_inicio = fecha_fin - timedelta(days=15)

    # formato esperado por la UI: yyyy/mm/dd
    formato = "%Y/%m/%d"
    fecha_fin_str = fecha_fin.strftime(formato)
    fecha_inicio_str = fecha_inicio.strftime(formato)

    # Usar la fixture login con el usuario 'admin' (ya configurado en config/qa.yaml)
    menu = login("admin")

    # Abrir CM21 y ejecutar el flujo usando el Page Object
    cm21 = CM21ClavePage(page)
    cm21.open_from_menu(menu)
    cm21.set_fechas(fecha_inicio_str, fecha_fin_str)
    cm21.consultar_clave(card_number)
    cm21.imprimir_y_capturar_report()