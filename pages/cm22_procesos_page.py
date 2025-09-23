"""
Page Object para el módulo **CM22 – Reporte de Tarjetas por Procesos**. Este
reporte agrupa las tarjetas por el proceso que las generó (emisión,
renovación, reposición, etc.)【547172095933312†L221-L224】.
"""

from playwright.sync_api import Page, expect


class CM22ProcesosPage:
    """Modela la pantalla CM22 – Reporte de Tarjetas por Procesos."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.frame = None

    def open_from_menu(self, menu_page) -> None:
        menu_page.open_cm22()
        # Esperar al iframe de CM22 y guardar el frame
        expect(self.page.locator("iframe[name='iframe_CM22']")).to_be_visible()
        iframe_el = self.page.wait_for_selector("iframe[name='iframe_CM22']", timeout=30_000)
        self.frame = iframe_el.content_frame()
        if self.frame is None:
            raise RuntimeError("No se pudo obtener el frame de CM22")

    def seleccionar_proceso(self, proceso: str | None = None) -> None:
        """Selecciona el proceso dentro del iframe sobre el cual generar el reporte.

        Si `proceso` es `None` o una cadena vacía, no hace nada y deja el valor por defecto
        que muestra la pantalla (como en la captura adjunta).
        """
        if self.frame is None:
            raise RuntimeError("El frame de CM22 no está inicializado. Llame a open_from_menu primero.")

        if not proceso:
            # No se especificó proceso: usar el valor por defecto mostrado en la UI
            return

        # Intentamos usar select por label; si no existe, se puede adaptar el selector
        try:
            self.frame.select_option("select[name='proceso']", label=proceso)
        except Exception:
            # fallback: intentar seleccionar por texto en un elemento custom
            self.frame.fill("input[placeholder='Proceso']", proceso)
            self.frame.click("button.searchB", force=True)

    def seleccionar_detallado(self) -> None:
        """Marca la opción 'Detallado' dentro del iframe si existe."""
        if self.frame is None:
            raise RuntimeError("El frame de CM22 no está inicializado. Llame a open_from_menu primero.")
        try:
            # puede ser un radio con label 'Detallado'
            self.frame.get_by_label("Detallado").click()
        except Exception:
            # fallback: selector conocido por id si aplica
            try:
                self.frame.click("#ctl00_maincontent_OptOriD")
            except Exception:
                pass


    def imprimir_y_capturar_report(self, screenshot_report_path: str = "screenshot_cm22_report.png", screenshot_result_path: str = "screenshot_cm22_result.png") -> None:
        """Genera el reporte (Aceptar/Imprimir) y captura el popup PDF y la vista final con 'Fin del Reporte'."""
        if self.frame is None:
            raise RuntimeError("El frame de CM22 no está inicializado. Llame a open_from_menu primero.")

        # Relleno de botón Aceptar por rol/texto si existe
        try:
            btn_aceptar = self.frame.get_by_role("button", name="Aceptar")
            btn_aceptar.wait_for(state="visible", timeout=30_000)
            with self.page.expect_popup() as popup_info:
                btn_aceptar.click()
        except Exception:
            # fallback: intentar imprimir directamente con el control conocido
            btn = self.frame.locator("#ctl00_maincontent_BtnImprimir:not([disabled])")
            btn.wait_for(state="visible", timeout=30_000)
            with self.page.expect_popup() as popup_info:
                btn.click()
            popup_info = popup_info

        # Obtener el popup (si lo abrió la primera rama, popup_info ya existe)
        try:
            report = popup_info.value
            report.wait_for_load_state("load")
            report.wait_for_timeout(1_000)
            try:
                report.screenshot(path=screenshot_report_path, full_page=True)
            except Exception:
                pass
            report.close()
        except Exception:
            # Si no hay popup, continuar
            pass

        # volver al tab principal y asegurar el estado final
        self.page.bring_to_front()
        # a veces es necesario reclicar Aceptar para que aparezca "Fin del Reporte"
        try:
            # intentar reclicar el mismo botón aceptar
            if 'btn_aceptar' in locals():
                btn_aceptar.click()
        except Exception:
            pass

        # esperar el texto fin del reporte dentro del frame
        try:
            self.frame.wait_for_selector("text=Fin del Reporte", timeout=30_000)
        except Exception:
            pass

        # captura final
        self.page.wait_for_timeout(1_000)
        try:
            self.page.screenshot(path=screenshot_result_path, full_page=True)
        except Exception:
            pass


    def validar_resultados(self, min_rows: int = 1) -> None:
        """Valida que la tabla de resultados dentro del frame tenga al menos `min_rows` filas."""
        if self.frame is None:
            raise RuntimeError("El frame de CM22 no está inicializado. Llame a open_from_menu primero.")
        rows = self.frame.locator("table tr")
        self.frame.wait_for_timeout(500)
        count = rows.count()
        assert count >= min_rows, f"Se esperaban al menos {min_rows} filas, pero se encontraron {count}"