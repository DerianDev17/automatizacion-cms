"""
Page Object para el módulo **CM44 – Reimpresión de Solicitudes**. Este
módulo permite consultar solicitudes de tarjetas y gestionar su
reimpresión【547172095933312†L194-L202】. La interacción típica
consiste en abrir el módulo desde el menú, filtrar por número de
solicitud o tarjeta y descargar el reporte.
"""

from playwright.sync_api import Page, expect


class CM44ReimpresionPage:
    """Modela la pantalla CM44 – Reimpresión de Solicitudes."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def open_from_menu(self, menu_page) -> None:
        menu_page.open_cm44()
        # El botón de texto puede estar oculto; esperar directamente al iframe del módulo
        self.page.wait_for_selector("iframe[name='iframe_CM44']", timeout=30_000)

    def _get_frame(self):
        iframe_el = self.page.wait_for_selector("iframe[name='iframe_CM44']", timeout=30_000)
        frame = iframe_el.content_frame()
        if frame is None:
            raise RuntimeError("No se pudo obtener el frame de CM44")
        return frame

    def buscar_por_solicitud(self, numero_solicitud: str) -> None:
        """Busca una solicitud para reimpresión mediante su número."""
        # TODO: Ajustar selector al campo real
        self.page.fill("input[placeholder='Solicitud']", numero_solicitud)
        self.page.click("button:has-text('Buscar')")
        expect(self.page.locator("table tr")).to_have_count(at_least=1)

    def buscar_por_tarjeta(self, card_number: str) -> None:
        """Busca una solicitud por número de tarjeta dentro del iframe y espera el postback."""
        frame = self._get_frame()
        frame.fill("#ctl00_maincontent_TxtTarjeta", card_number)
        frame.evaluate("__doPostBack('ctl00$maincontent$TxtTarjeta','');")
        frame.wait_for_selector("#ctl00_maincontent_TxtTarjeta[value*='XXXX']", timeout=10_000)

    def descargar_reporte(self, screenshot_confirmation: str = "screenshot_cm44_confirmation.png", screenshot_report: str = "screenshot_cm44_report.png") -> None:
        """Realiza el flujo de selección e impresión dentro del iframe y captura popup/report y confirmación."""
        frame = self._get_frame()

        # Continuar
        cont = frame.locator("#ctl00_maincontent_BtnContinuar:not([disabled])")
        cont.wait_for(state="visible", timeout=15_000)
        cont.click()
        frame.wait_for_timeout(1_000)

        # Seleccionar tipo de documento
        try:
            frame.select_option("#ctl00_maincontent_CboTipoDoc", label="Solicitud Tarjeta")
        except Exception:
            pass

        # Preparar imprimir
        imprimir = frame.locator("#ctl00_maincontent_BtnImprimir:not([disabled])")
        imprimir.wait_for(state="visible", timeout=15_000)

        # Capturar popup al hacer clic
        with self.page.expect_popup() as popup_info:
            imprimir.click()
        popup = popup_info.value

        # Esperar y verificar el mensaje de confirmación en la vista principal
        frame.wait_for_selector("text=Impresion se realizo Correctamente", timeout=30_000)
        self.page.wait_for_timeout(1_000)
        from pathlib import Path
        evid = Path(__file__).resolve().parent.parent / "evidencias"
        evid.mkdir(parents=True, exist_ok=True)
        conf_path = evid / screenshot_confirmation
        # Capturar la confirmación en la vista principal
        self.page.screenshot(path=str(conf_path), full_page=True)

        # Esperar a que el PDF cargue y tomar screenshot del popup
        popup.wait_for_load_state("load")
        popup.wait_for_timeout(1_000)
        try:
            rpt_path = evid / screenshot_report
            popup.screenshot(path=str(rpt_path), full_page=True)
        except Exception:
            pass

        # Regresar al menú (traer al frente)
        self.page.bring_to_front()

    
    def load_cards_from_csv(self, csv_path: str | None = None) -> list:
        import csv
        from pathlib import Path
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

    def run_for_card(self, card_number: str) -> None:
        self.buscar_por_tarjeta(card_number)
        self.descargar_reporte()

    def run_all_from_csv(self, csv_path: str | None = None) -> None:
        cards = self.load_cards_from_csv(csv_path)
        if not cards:
            raise RuntimeError("No se encontraron tarjetas en el CSV")
        for c in cards:
            self.run_for_card(c)

