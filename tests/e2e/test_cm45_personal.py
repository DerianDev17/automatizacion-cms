"""
Prueba CM45 - Pestaña Personal: busca una tarjeta, continúa y valida el campo Identificación.
"""

import pytest

import csv
from pathlib import Path

from cms_automation.pages.cm45_consulta_page import CM45ConsultaPage


# Leer la primera tarjeta desde tests/data/cards.csv
DATA_DIR = Path(__file__).parents[1] / "data"
CARDS_FILE = DATA_DIR / "cards.csv"
_CARD = None
if CARDS_FILE.exists():
    with CARDS_FILE.open(newline='') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            if row.get('card_number'):
                _CARD = row['card_number'].strip()
                break

CARD = _CARD or "4232162290117332"


@pytest.mark.cm45
def test_consulta_cm45_pestana_personal(page, login):
    menu = login()
    cm45 = CM45ConsultaPage(page)
    cm45.open_from_menu(menu)
    # delegar la ejecución al page-object (usa CSV por defecto o la tarjeta en el CSV)
    cm45.run_all_from_csv()
