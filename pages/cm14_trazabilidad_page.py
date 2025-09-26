"""
Page Object para el módulo **CM14 – Trazabilidad de Tarjetas**.
Según la guía operativa, este módulo permite rastrear la historia de cada
tarjeta emitida, consultando eventos como emisión, renovación, reimpresión o
suspensión【547172095933312†L194-L204】. La automatización de este módulo
incluye la apertura desde el menú principal, la búsqueda de una tarjeta
mediante su número y la validación de que se presentan resultados en la
tabla.
"""

from playwright.sync_api import Page, expect
import csv
from pathlib import Path


class CM14TrazabilidadPage:
    """Modela la pantalla CM14 – Trazabilidad de Tarjetas."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def open_from_menu(self, menu_page) -> None:
        """Utiliza el `MenuPage` para abrir este módulo."""
        menu_page.open_cm14()
        # Esperar a que el iframe de CM14 esté visible
        expect(self.page.locator("iframe[name='iframe_CM14']")).to_be_visible()

    def _get_frame(self):
        """Retorna el frame interno del módulo CM14 (o lanza si no existe)."""
        iframe_el = self.page.wait_for_selector("iframe[name='iframe_CM14']", timeout=30_000)
        frame = iframe_el.content_frame()
        if frame is None:
            raise RuntimeError("No se pudo obtener el frame de CM14")
        return frame

    def buscar_por_numero_en_frame(self, numero_tarjeta: str) -> None:
        """Busca la tarjeta dentro del iframe usando el campo y postback del CMS."""
        frame = self._get_frame()
        # selectores específicos del CM14 (actualizar si cambia la UI)
        frame.fill("#ctl00_maincontent_TxtTarjeta", numero_tarjeta)
        # disparar postback que la aplicación espera
        frame.evaluate("__doPostBack('ctl00$maincontent$TxtTarjeta','');")
        frame.wait_for_timeout(2_000)

    def imprimir_y_capturar_report(self, screenshot_report_path: str, screenshot_result_path: str) -> None:
        """Hace click en imprimir, captura el popup PDF y la pantalla final.

        - captura `screenshot_report_path` del popup que contiene el PDF
        - captura `screenshot_result_path` con la leyenda "Fin del Reporte"
        """
        frame = self._get_frame()
        btn_imprimir = frame.locator("#ctl00_maincontent_BtnImprimir:not([disabled])")
        btn_imprimir.wait_for(state="visible", timeout=30_000)

        with self.page.expect_popup() as popup_info:
            btn_imprimir.click()
        report = popup_info.value
        report.wait_for_load_state("load")
        report.wait_for_timeout(1_000)
        report.screenshot(path=screenshot_report_path, full_page=True)
        report.close()
        # volver al tab principal
        self.page.bring_to_front()

        # volver a hacer click para que aparezca “Fin del Reporte” y capturar
        btn_imprimir.click()
        frame.wait_for_selector("text=Fin del Reporte", timeout=30_000)
        self.page.wait_for_timeout(1_000)
        self.page.screenshot(path=screenshot_result_path, full_page=True)

    def buscar_por_numero(self, numero_tarjeta: str) -> None:
        """Ingresa el número de tarjeta y dispara la búsqueda.

        Este método debe ajustar los selectores a la interfaz real del CMS:
        - Ubicar el campo de búsqueda (p. ej., placeholder 'Número de Tarjeta').
        - Ingresar el número y pulsar el botón de buscar/consultar.
        """
        # TODO: Actualizar con selectors específicos (data‑testid) una vez conocidos.
        self.page.fill("input[placeholder='Número de Tarjeta']", numero_tarjeta)
        self.page.click("button:has-text('Buscar')")
        # Esperar a que la tabla cargue (podría usarse un spinner o contador de filas)
        expect(self.page.locator("table tr")).to_have_count(at_least=1)

    def validar_resultados(self, min_rows: int = 1) -> None:
        """Valida que la tabla de resultados contenga al menos `min_rows` filas."""
        rows = self.page.locator("table tr")
        expect(rows).to_have_count(at_least=min_rows)

    # --- Encapsulación de flujo de prueba completa ---
    def load_cards_from_csv(self, csv_path: str | None = None) -> list:
        """Carga la lista de tarjetas desde `csv_path`.

        - Por defecto busca `cms_automation/tests/data/cards.csv`.
        """
        if csv_path is None:
            default = Path(__file__).resolve().parent.parent / "tests" / "data" / "cards.csv"
            csv_path = str(default)
        csv_file = Path(csv_path)
        if not csv_file.exists():
            raise FileNotFoundError(f"CSV de tarjetas no encontrado: {csv_file}")

        cards = []
        with open(csv_file, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'card_number' in row and row['card_number'].strip():
                    cards.append(row['card_number'].strip())
        return cards

    def run_for_card(self, numero_tarjeta: str) -> None:
        """Ejecuta la búsqueda e impresión/captura para una tarjeta.

        Usa los métodos existentes para buscar dentro del iframe y capturar
        el PDF y la vista final con 'Fin del Reporte'.
        """
        self.buscar_por_numero_en_frame(numero_tarjeta)
        from pathlib import Path
        evid = Path(__file__).resolve().parent.parent / "evidencias"
        evid.mkdir(parents=True, exist_ok=True)
        report_path = evid / f"screenshot_cm14_report_{numero_tarjeta}.png"
        result_path = evid / f"screenshot_cm14_result_{numero_tarjeta}.png"
        self.imprimir_y_capturar_report(str(report_path), str(result_path))

    def run_all_from_csv(self, csv_path: str | None = None) -> None:
        """Carga las tarjetas del CSV y ejecuta `run_for_card` para cada una.

    Si ocurre un error en una tarjeta se propaga la excepción para que el
    test falle, dejando evidencia parcial en `evidencias/` o en el working dir.
        """
        cards = self.load_cards_from_csv(csv_path)
        if not cards:
            raise RuntimeError("No se encontraron tarjetas en el CSV")
        for c in cards:
            self.run_for_card(c)