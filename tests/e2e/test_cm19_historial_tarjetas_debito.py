"""
Prueba end‑to‑end del módulo CM19 – Historial de Tarjetas de Débito.
Consulta el historial de una tarjeta de débito determinada.
"""

from datetime import date, timedelta
import csv
from pathlib import Path
import pytest

from cms_automation.pages.cm19_historial_page import CM19HistorialPage


# Cargar tarjetas desde CSV en tiempo de colección (igual que CM14)
DATA_DIR = Path(__file__).parent.parent / "data"
CSV_PATH = DATA_DIR / "cards.csv"
with open(CSV_PATH, newline="") as f:
    reader = csv.DictReader(f)
    CARDS = [row["card_number"] for row in reader]


@pytest.mark.cm19
@pytest.mark.parametrize("card_number", CARDS)
def test_cm19_historial_tarjetas_debito(page, login, card_number):
    # calcular fechas: fecha_fin = hoy, fecha_inicio = hoy - 15 dias
    fecha_fin = date.today()
    fecha_inicio = fecha_fin - timedelta(days=15)

    # formato esperado por la UI: yyyy/mm/dd
    formato = "%Y/%m/%d"
    fecha_fin_str = fecha_fin.strftime(formato)
    fecha_inicio_str = fecha_inicio.strftime(formato)

    menu = login()
    cm19 = CM19HistorialPage(page)
    cm19.open_from_menu(menu)
    cm19.buscar_por_numero(card_number)
    cm19.set_fechas(fecha_inicio_str, fecha_fin_str)
    cm19.imprimir_y_capturar_report()
    cm19.validar_resultados(min_rows=1)