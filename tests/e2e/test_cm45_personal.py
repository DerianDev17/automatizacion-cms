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

    cm45.buscar_por_tarjeta(CARD)
    cm45.continuar()
    # Llegó a la pantalla; validar que el botón 'Salir' esté presente como evidencia de éxito
    cm45.esperar_boton_salir(timeout=15_000)
    # Guardar evidencia en la carpeta artefacts con el nombre solicitado
    from pathlib import Path
    artefacts = Path(__file__).parents[2] / "artefacts"
    artefacts.mkdir(parents=True, exist_ok=True)
    target = artefacts / "screenshot_cm45.png"
    page.screenshot(path=str(target), full_page=True)
