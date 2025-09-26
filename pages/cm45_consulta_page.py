"""
Page Object para el módulo **CM45 – Consulta de Tarjetas**. Permite
consultar el estado de las tarjetas emitidas, suspendidas o canceladas
mediante diferentes filtros (número de tarjeta, cliente, fecha, etc.).
"""

from playwright.sync_api import Page, expect


class CM45ConsultaPage:
    """Modela la pantalla CM45 – Consulta de Tarjetas."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def open_from_menu(self, menu_page) -> None:
        menu_page.open_cm45()
        # Esperar al iframe del módulo en vez del texto
        self.page.wait_for_selector("iframe[name='iframe_CM45']", timeout=30_000)

    def _get_frame(self):
        iframe_el = self.page.wait_for_selector("iframe[name='iframe_CM45']", timeout=30_000)
        frame = iframe_el.content_frame()
        if frame is None:
            raise RuntimeError("No se pudo obtener el frame de CM45")
        return frame

    def buscar(self, criterio: str, valor: str) -> None:
        """Realiza una búsqueda por un criterio específico.

        Por ejemplo:
        - criterio='tarjeta', valor='5353…1234'
        - criterio='cliente', valor='Cédula/Nombre'
        """
        # TODO: Implementar selección de criterio y campo dinámico
        selector_campo = f"input[placeholder='{criterio}']"
        self.page.fill(selector_campo, valor)
        self.page.click("button:has-text('Buscar')")
        expect(self.page.locator("table tr")).to_have_count(at_least=1)

    def buscar_por_tarjeta(self, card_number: str) -> None:
        frame = self._get_frame()
        frame.fill("#ctl00_maincontent_TxtTarjeta", card_number)
        frame.evaluate("__doPostBack('ctl00$maincontent$TxtTarjeta','');")
        # esperar que se enmascare o que haya un pequeño delay
        try:
            frame.wait_for_selector("#ctl00_maincontent_TxtTarjeta[value*='XXXX']", timeout=15_000)
        except Exception:
            frame.wait_for_timeout(2_000)

    def continuar(self) -> None:
        frame = self._get_frame()
        continuar = frame.locator("#ctl00_maincontent_UpdatePanel3 #ctl00_maincontent_BtnContinuar:not([disabled])")
        continuar.wait_for(state="visible", timeout=20_000)
        continuar.click()
        frame.wait_for_timeout(2_000)

    def obtener_identificacion(self) -> str:
        frame = self._get_frame()
        id_input = frame.wait_for_selector("//td[normalize-space()='Identificacion:']/following-sibling::td//input", timeout=10_000)
        return id_input.input_value().strip()

    def esperar_boton_salir(self, timeout: int = 10_000) -> None:
        """Espera a que el botón 'Salir' (Cancelar) esté visible en la pantalla del iframe.

        Selector usado: `#ctl00_maincontent_BtnCancelar` (referencia del usuario).
        """
        frame = self._get_frame()
        frame.wait_for_selector("#ctl00_maincontent_BtnCancelar", timeout=timeout)

    def validar_resultados(self, min_rows: int = 1) -> None:
        expect(self.page.locator("table tr")).to_have_count(at_least=min_rows)

    def run_for_card_and_capture(self, card_number: str, evidencias_dir: str | None = None) -> None:
        """Busca tarjeta en el iframe, continúa, espera boton Salir y captura screenshot en 'evidencias'."""
        frame = self._get_frame()
        self.buscar_por_tarjeta(card_number)
        self.continuar()
        self.esperar_boton_salir(timeout=15_000)
        # crear directorio evidencias si se pidió
        from pathlib import Path
        if evidencias_dir is None:
            evidencias_dir = Path(__file__).resolve().parent.parent / "evidencias"
        evidencias_dir = Path(evidencias_dir)
        evidencias_dir.mkdir(parents=True, exist_ok=True)
        target = evidencias_dir / f"screenshot_cm45.png"
        # Capturar en el directorio de evidencias
        self.page.screenshot(path=str(target), full_page=True)

    def run_all_from_csv(self, csv_path: str | None = None) -> None:
        import csv
        from pathlib import Path
        if csv_path is None:
            default = Path(__file__).resolve().parent.parent / "tests" / "data" / "cards.csv"
            csv_path = str(default)
        csv_file = Path(csv_path)
        if not csv_file.exists():
            raise FileNotFoundError(f"CSV de tarjetas no encontrado: {csv_file}")
        with open(csv_file, newline='') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                card = row.get('card_number')
                if card:
                    self.run_for_card_and_capture(card.strip())