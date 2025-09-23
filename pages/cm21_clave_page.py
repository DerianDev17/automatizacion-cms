"""
Page Object para el módulo **CM21 – Consulta de Clave**. Según la guía,
esta pantalla permite consultar la clave asociada a una tarjeta o
cliente【547172095933312†L214-L217】. El acceso a esta información suele
estar restringido, por lo que la automatización debe contemplar roles y
permisos adecuados.
"""

from playwright.sync_api import Page, expect


class CM21ClavePage:
    """Modela la pantalla CM21 – Consulta de Clave."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.frame = None

    def open_from_menu(self, menu_page) -> None:
        menu_page.open_cm21()
        # Esperar al iframe de CM21 y guardar el frame
        expect(self.page.locator("iframe[name='iframe_CM21']")).to_be_visible()
        iframe_el = self.page.wait_for_selector("iframe[name='iframe_CM21']", timeout=30_000)
        self.frame = iframe_el.content_frame()
        if self.frame is None:
            raise RuntimeError("No se pudo obtener el frame de CM21")

    def _get_frame(self):
        if self.frame is not None:
            return self.frame
        iframe_el = self.page.wait_for_selector("iframe[name='iframe_CM21']", timeout=30_000)
        frame = iframe_el.content_frame()
        if frame is None:
            raise RuntimeError("No se pudo obtener el frame de CM21")
        self.frame = frame
        return frame


    def set_fechas(self, fecha_inicio: str, fecha_fin: str) -> None:
        """Rellena las fechas de inicio y fin dentro del iframe del CM21."""
        frame = self._get_frame()
        frame.fill("#ctl00_maincontent_FecInicial", fecha_inicio)
        frame.fill("#ctl00_maincontent_FecFinal", fecha_fin)
        frame.wait_for_timeout(500)


    def consultar_clave(self, identificador: str) -> None:
        """Realiza la consulta de la clave por identificador de tarjeta/cliente dentro del iframe."""
        frame = self._get_frame()
        # Si el selector real es diferente, actualizar aquí
        frame.fill("#ctl00_maincontent_TxtTarjeta", identificador)
        # Disparar postback si la UI lo requiere
        try:
            frame.evaluate("__doPostBack('ctl00$maincontent$TxtTarjeta','');")
            frame.wait_for_timeout(2_000)
        except Exception:
            pass
        # En esta pantalla la UI enmascara el campo de tarjeta cuando la
        # búsqueda finaliza (por ejemplo aparece XXXX). Esperamos ese
        # enmascaramiento como señal de que la consulta terminó y el panel
        # está listo para continuar (por ejemplo pulsar Aceptar/Imprimir).
        frame.wait_for_selector("#ctl00_maincontent_TxtTarjeta[value*='XXXX']", timeout=10_000)


    def imprimir_y_capturar_report(self, screenshot_report_path: str = "screenshot_cm21_report.png") -> None:
        """Hace click en aceptar/imprimir dentro del iframe y captura el popup resultante."""
        frame = self._get_frame()
        # Algunos flujos muestran primero un botón "Aceptar" y luego permiten
        # la impresión. Intentamos pulsar el botón Aceptar si existe, y a
        # continuación pulsamos Imprimir para capturar el popup.
        try:
            aceptar = frame.locator("#ctl00_maincontent_BtnAceptar:not([disabled])")
            aceptar.wait_for(state="visible", timeout=5_000)
            aceptar.click()
        except Exception:
            # No hay botón Aceptar visible; seguir al flujo normal
            pass

        btn = frame.locator("#ctl00_maincontent_BtnImprimir:not([disabled])")
        btn.wait_for(state="visible", timeout=30_000)

        with self.page.expect_popup() as popup_info:
            btn.click()
        report = popup_info.value
        report.wait_for_load_state("load")
        report.wait_for_timeout(1_000)
        try:
            report.screenshot(path=screenshot_report_path, full_page=True)
        except Exception:
            pass
        report.close()
        self.page.bring_to_front()