"""
Page Object para el módulo **CM85 – Reporte de Tarjetas Emitidas**. Este
reporte lista las tarjetas emitidas en un periodo de tiempo y permite
exportar la información【547172095933312†L211-L213】.
"""

from playwright.sync_api import Page, expect


class CM85EmitidasPage:
    """Modela la pantalla CM85 – Reporte de Tarjetas Emitidas."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def open_from_menu(self, menu_page) -> None:
        menu_page.open_cm85()
        # esperar al iframe del módulo CM85
        self.page.wait_for_selector("iframe[name='iframe_CM85']", timeout=30_000)

    def _get_frame(self):
        iframe_el = self.page.wait_for_selector("iframe[name='iframe_CM85']", timeout=30_000)
        frame = iframe_el.content_frame()
        if frame is None:
            raise RuntimeError("No se pudo obtener el frame de CM85")
        return frame

    def set_bin(self, bin_label: str) -> None:
        frame = self._get_frame()
        frame.wait_for_selector("#ctl00_maincontent_CboBines", timeout=10_000)
        frame.locator("#ctl00_maincontent_CboBines").select_option(label=bin_label)

    def uncheck_modelo_oficina(self) -> None:
        frame = self._get_frame()
        try:
            chk_modelo = frame.locator("#ctl00_maincontent_ChkTodosModelo")
            if chk_modelo.count() > 0:
                chk_modelo.uncheck()
        except Exception:
            pass
        try:
            chk_ofi = frame.locator("#ctl00_maincontent_ChkTodasOfi")
            if chk_ofi.count() > 0:
                chk_ofi.uncheck()
        except Exception:
            pass

    def set_modelo(self, modelo_label: str) -> None:
        frame = self._get_frame()
        frame.wait_for_selector("#ctl00_maincontent_CboModelo", timeout=10_000)
        frame.wait_for_timeout(500)
        frame.locator("#ctl00_maincontent_CboModelo").select_option(label=modelo_label)

    def set_fecha_emision(self, fecha_str: str) -> None:
        frame = self._get_frame()
        frame.fill("#ctl00_maincontent_GMFechaEmision", fecha_str)

    def procesar_and_capture(self, screenshot_report: str = "screenshot_cm85_report.png") -> None:
        frame = self._get_frame()
        btn_procesar = frame.locator("#ctl00_maincontent_BtnProcesar")
        btn_procesar.wait_for(state="visible", timeout=15_000)
        with self.page.expect_popup() as popup_info:
            btn_procesar.click()
        report = popup_info.value
        report.wait_for_load_state("load")
        report.wait_for_timeout(1_000)
        try:
            report.screenshot(path=screenshot_report, full_page=True)
        except Exception:
            pass
        report.close()

    def buscar(self, fecha_inicio: str, fecha_fin: str) -> None:
        """Filtra las tarjetas emitidas entre las fechas indicadas."""
        # TODO: Actualizar selectors para datepicker
        self.page.fill("input[name='fechaInicio']", fecha_inicio)
        self.page.fill("input[name='fechaFin']", fecha_fin)
        self.page.click("button:has-text('Buscar')")
        expect(self.page.locator("table tr")).to_have_count(at_least=1)

    def exportar_excel(self) -> None:
        """Exporta el reporte generado a Excel."""
        self.page.click("button:has-text('Exportar')")
        # TODO: Validar existencia del archivo descargado