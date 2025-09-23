"""
Page Object para el módulo **CM19 – Historial de Tarjetas**. Permite
consultar el historial de transacciones o estados de una tarjeta a lo
largo del tiempo【547172095933312†L204-L208】.
"""

from playwright.sync_api import Page, expect
from datetime import date, timedelta
import csv
from pathlib import Path


class CM19HistorialPage:
    """Modela la pantalla CM19 – Historial de Tarjetas."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.frame = None

    def open_from_menu(self, menu_page) -> None:
        menu_page.open_cm19()
        # Esperar al iframe de CM19 y guardar el frame
        expect(self.page.locator("iframe[name='iframe_CM19']")).to_be_visible()
        iframe_el = self.page.wait_for_selector("iframe[name='iframe_CM19']", timeout=30_000)
        self.frame = iframe_el.content_frame()
        if self.frame is None:
            raise RuntimeError("No se pudo obtener el frame de CM19")

    def _get_frame(self):
        """Retorna el frame interno del módulo CM19 (o lanza si no existe)."""
        if self.frame is not None:
            return self.frame
        iframe_el = self.page.wait_for_selector("iframe[name='iframe_CM19']", timeout=30_000)
        frame = iframe_el.content_frame()
        if frame is None:
            raise RuntimeError("No se pudo obtener el frame de CM19")
        self.frame = frame
        return frame


    def buscar_por_numero(self, numero_tarjeta: str) -> None:
        """Ingresa el número de tarjeta dentro del iframe y dispara el postback que carga el panel."""
        frame = self._get_frame()
        # Selector real conocido en CM19
        frame.fill("#ctl00_maincontent_TxtTarjeta", numero_tarjeta)
        # Disparar el postback que la aplicación espera
        frame.evaluate("__doPostBack('ctl00$maincontent$TxtTarjeta','');")
        frame.wait_for_timeout(2_000)

        # Esperar a que el campo se enmascare (contenga XXXX)
        frame.wait_for_selector("#ctl00_maincontent_TxtTarjeta[value*='XXXX']", timeout=10_000)

    def set_fechas(self, fecha_inicio: str, fecha_fin: str) -> None:
        """Rellena las fechas de inicio y fin dentro del iframe del CM19.

        Los selectores usados son los observados en la UI: `FecInicial` y
        `FecFinal`. Las fechas deben venir en el formato aceptado por la UI.
        """
        frame = self._get_frame()
        frame.fill("#ctl00_maincontent_FecInicial", fecha_inicio)
        frame.fill("#ctl00_maincontent_FecFinal", fecha_fin)
        # Pequeña espera para que la UI procese los cambios
        frame.wait_for_timeout(500)

    def imprimir_y_capturar_report(self, screenshot_report_path: str = "screenshot_cm19_report.png", screenshot_result_path: str = "screenshot_cm19_main.png") -> None:
        """Hace click en imprimir/generar, captura el popup PDF y toma una captura del panel.

        Guarda por defecto `screenshot_cm19_report.png` y `screenshot_cm19_main.png`.
        """
        frame = self._get_frame()
        btn_imprimir = frame.locator("#ctl00_maincontent_BtnImprimir:not([disabled])")
        btn_imprimir.wait_for(state="visible", timeout=30_000)

        with self.page.expect_popup() as popup_info:
            btn_imprimir.click()
        report = popup_info.value
        report.wait_for_load_state("load")
        report.wait_for_timeout(1_000)
        try:
            report.screenshot(path=screenshot_report_path, full_page=True)
        except Exception:
            pass
        report.close()

        # volver al tab principal y capturar estado del panel
        self.page.bring_to_front()
        try:
            btn_imprimir.click()
        except Exception:
            pass
        self.page.wait_for_timeout(1_000)
        try:
            self.page.screenshot(path=screenshot_result_path, full_page=True)
        except Exception:
            pass


    def validar_resultados(self, min_rows: int = 1) -> None:
        """Valida que la tabla de resultados dentro del frame tenga al menos `min_rows` filas."""
        frame = self._get_frame()
        rows = frame.locator("table tr")
        frame.wait_for_timeout(500)
        count = rows.count()
        assert count >= min_rows, f"Se esperaban al menos {min_rows} filas, pero se encontraron {count}"

    # --- Encapsulación de flujo de prueba completa ---
    def load_cards_from_csv(self, csv_path: str | None = None) -> list:
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

    def run_for_card(self, numero_tarjeta: str, days: int = 15) -> None:
        """Ejecuta el flujo completo para una tarjeta: buscar, fijar fechas, imprimir y validar."""
        # calcular fechas
        fecha_fin = date.today()
        fecha_inicio = fecha_fin - timedelta(days=days)
        fmt = lambda d: d.strftime("%Y/%m/%d")
        fecha_fin_str = fmt(fecha_fin)
        fecha_inicio_str = fmt(fecha_inicio)

        # ejecutar pasos
        self.buscar_por_numero(numero_tarjeta)
        self.set_fechas(fecha_inicio_str, fecha_fin_str)
        self.imprimir_y_capturar_report(screenshot_report_path=f"screenshot_cm19_report_{numero_tarjeta}.png",
                                        screenshot_result_path=f"screenshot_cm19_main_{numero_tarjeta}.png")
        # validar que existan resultados en el frame
        try:
            self.validar_resultados(min_rows=1)
        except AssertionError:
            # dejar evidencia aunque falle
            try:
                self.page.screenshot(path=f"screenshot_cm19_error_{numero_tarjeta}.png", full_page=True)
            except Exception:
                pass
            raise

    def run_all_from_csv(self, csv_path: str | None = None, days: int = 15) -> None:
        cards = self.load_cards_from_csv(csv_path)
        if not cards:
            raise RuntimeError("No se encontraron tarjetas en el CSV")
        for c in cards:
            self.run_for_card(c, days=days)