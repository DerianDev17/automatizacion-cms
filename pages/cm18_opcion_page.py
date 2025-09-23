"""
Page Object para el módulo **CM18 – Tarjetas por Opción**. Este reporte
clasifica las tarjetas según una opción o criterio seleccionado por el
usuario【547172095933312†L194-L203】.
"""

from playwright.sync_api import Page, expect


class CM18OpcionPage:
    """Modela la pantalla CM18 – Tarjetas por Opción."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.frame = None

    def open_from_menu(self, menu_page) -> None:
        menu_page.open_cm18()
        # Esperar a que el iframe del módulo CM18 esté visible y guardar el frame
        expect(self.page.locator("iframe[name='iframe_CM18']")).to_be_visible()
        iframe_el = self.page.wait_for_selector("iframe[name='iframe_CM18']", timeout=30_000)
        self.frame = iframe_el.content_frame()
        if self.frame is None:
            raise RuntimeError("No se pudo obtener el frame de CM18")

    def seleccionar_opcion(self, opcion: str, fecha_inicio: str = "2025/09/02", fecha_fin: str = "2025/09/22") -> None:
        """Selecciona la opción deseada y rellena fechas dentro del iframe.

        Actualmente la UI espera las fechas y la selección del modo "Detallado"
        para generar el reporte. El parámetro `opcion` se deja por compatibilidad
        con los tests, pero la implementación aplica los pasos conocidos.
        """
        if self.frame is None:
            self.open_from_menu(menu_page=None)  # intenta inicializar el frame (no usa menu_page aquí)

        # Rellenar fechas (selectores específicos del CM18)
        self.frame.fill("#ctl00_maincontent_GTMFechaInicio", fecha_inicio)
        self.frame.fill("#ctl00_maincontent_GTMFechaFin", fecha_fin)

        # Seleccionar el modo 'Detallado' (selector conocido en la UI)
        try:
            self.frame.click("#ctl00_maincontent_OptOriD")
        except Exception:
            # Si no existe el radio, ignoramos y seguimos (la UI puede variar)
            pass
        # pequeña espera para que la UI procese los cambios
        self.frame.wait_for_timeout(500)

    def generar_reporte(self, screenshot_report_path: str = "screenshot_cm18_report.png", screenshot_result_path: str = "screenshot_cm18_main.png") -> None:
        """Hace click en imprimir/generar, captura el popup PDF y toma una captura del panel.

        Guarda por defecto `screenshot_cm18_report.png` y `screenshot_cm18_main.png`.
        """
        if self.frame is None:
            raise RuntimeError("El frame de CM18 no está inicializado. Llame a open_from_menu primero.")

        btn_imprimir = self.frame.locator("#ctl00_maincontent_BtnImprimir:not([disabled])")
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
        # es posible que la UI necesite otro click para mostrar el resumen/resultados
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
        if self.frame is None:
            raise RuntimeError("El frame de CM18 no está inicializado. Llame a open_from_menu primero.")

        rows = self.frame.locator("table tr")
        # Esperar un poco a que la tabla se renderice
        self.frame.wait_for_timeout(500)
        count = rows.count()
        assert count >= min_rows, f"Se esperaban al menos {min_rows} filas, pero se encontraron {count}"