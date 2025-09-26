from playwright.sync_api import Page
from datetime import date, datetime, timedelta
from pathlib import Path
import re

class WS02TransaccionesPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def open_from_menu(self, menu_page) -> None:
        menu_page.open_ws02()
        self.page.wait_for_selector("iframe[name='iframe_WS02']", timeout=30_000)

    def _get_frame(self):
        iframe_el = self.page.wait_for_selector("iframe[name='iframe_WS02']", timeout=30_000)
        frame = iframe_el.content_frame()
        if frame is None:
            raise RuntimeError("No se pudo obtener el frame de WS02")
        return frame

    # ---------- helpers de fecha ----------
    def _detect_strftime_pattern(self, frame, selector: str) -> str:
        """Detecta formato de fecha por placeholder/value del input."""
        el = frame.locator(selector)
        ph = (el.get_attribute("placeholder") or "").strip()
        val = (el.input_value() or "").strip()

        sample = ph or val
        # dd/MM/yyyy
        if re.search(r"\b\d{2}/\d{2}/\d{4}\b", sample):
            return "%d/%m/%Y"
        # yyyy/MM/dd
        if re.search(r"\b\d{4}/\d{2}/\d{2}\b", sample):
            return "%Y/%m/%d"
        # fallback seguro (la mayoría de CMS locales usan dd/MM/yyyy)
        return "%d/%m/%Y"

    def _fmt(self, d: date | datetime, pattern: str) -> str:
        if isinstance(d, datetime):
            d = d.date()
        return d.strftime(pattern)

    def _fill_and_blur(self, frame, selector: str, value: str) -> None:
        el = frame.locator(selector)
        el.click()
        # limpiar por si queda valor anterior
        el.press("Control+A")
        el.press("Delete")
        el.type(value, delay=20)  # tipeo “humano” suele disparar onChange
        el.press("Tab")

    # ---------- API pública ----------
    def set_rango_ultimos_dias(self, dias: int = 7) -> None:
        """Establece rango: desde = hoy - dias, hasta = hoy."""
        frame = self._get_frame()
        sel_desde = "#ctl00_maincontent_TxtFechaDesde"
        sel_hasta = "#ctl00_maincontent_TxtFechaHasta"

        pattern = self._detect_strftime_pattern(frame, sel_desde)
        hoy = date.today()
        desde = hoy - timedelta(days=dias)

        desde_s = self._fmt(desde, pattern)
        hasta_s = self._fmt(hoy, pattern)

        self._fill_and_blur(frame, sel_desde, desde_s)
        self._fill_and_blur(frame, sel_hasta, hasta_s)

    def consultar_y_capturar(self, screenshot_results: str = "screenshot_ws02_results.png") -> None:
        frame = self._get_frame()

        # Asegura que el botón esté habilitado
        frame.wait_for_selector("#ctl00_maincontent_BtnConsultar:not([disabled])", timeout=15_000)
        frame.locator("#ctl00_maincontent_BtnConsultar").click()

        # Espera resultados: o hay 'Detalle' o algún mensaje de “sin registros”
        # sube el timeout si el backend se demora
        timeout_ms = 30_000
        # 1) si aparece un detalle
        try:
            frame.locator("text=Detalle").first.wait_for(state="visible", timeout=timeout_ms)
            # contamos filas “Detalle”
            count = frame.locator("text=Detalle").count()
            assert count > 0, "Se esperaba al menos un resultado con 'Detalle'."
        except Exception:
            # 2) verifica si hay mensaje de sin datos
            no_data_locators = [
                "text=No existen registros", 
                "text=Sin resultados", 
                "text=No se encontraron registros"
            ]
            if any(frame.locator(sel).first.is_visible() for sel in no_data_locators):
                raise AssertionError("La consulta no devolvió resultados para el rango seleccionado.")
            # Si no hay ni detalle ni mensaje, reporta timeout específico
            raise AssertionError("No apareció 'Detalle' ni mensaje de 'sin registros' dentro del tiempo de espera.")

        # Evidencia
        self.page.wait_for_timeout(1000)
        evid = Path(__file__).resolve().parent.parent / "evidencias"
        evid.mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=str(evid / screenshot_results), full_page=True)
