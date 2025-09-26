"""
Page Object para el módulo **WS01 – Reporte de Movimientos Switch**.
Permite generar reportes de movimientos del switch con opción de visualizar
el detalle completo de las transacciones.
"""

from playwright.sync_api import Page, expect
from pathlib import Path
from datetime import datetime, timedelta


class WS01MovimientosPage:
    """Modela la pantalla WS01 – Reporte de Movimientos Switch."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def open_from_menu(self, menu_page) -> None:
        """Utiliza el MenuPage para abrir este módulo."""
        menu_page.open_ws01()
        # Esperar al iframe del módulo en lugar del texto que puede estar oculto
        self.page.wait_for_selector("iframe[name='iframe_WS01']", timeout=30_000)

    def _get_frame(self):
        """Retorna el frame interno del módulo WS01 (o lanza si no existe)."""
        iframe_el = self.page.wait_for_selector("iframe[name='iframe_WS01']", timeout=30_000)
        frame = iframe_el.content_frame()
        if frame is None:
            raise RuntimeError("No se pudo obtener el frame de WS01")
        return frame

    def set_fechas(self, fecha_fin: datetime = None) -> None:
        """Configura el rango de fechas para el reporte.
        
        Args:
            fecha_fin: Fecha fin del reporte (por defecto hoy).
                     La fecha inicio se calcula automáticamente como 15 días antes.
        """
        if fecha_fin is None:
            fecha_fin = datetime.now()
        fecha_inicio = fecha_fin - timedelta(days=15)
        
        frame = self._get_frame()
        
        # Formatear fechas en el formato esperado por el datepicker (dd/MM/yyyy)
        fecha_inicio_str = fecha_inicio.strftime("%Y/%m/%d")
        fecha_fin_str = fecha_fin.strftime("%Y/%m/%d")
        
        # Llenar los campos de fecha
        frame.fill("#ctl00_maincontent_TxtFechaDesde", fecha_inicio_str)
        frame.fill("#ctl00_maincontent_TxtFechaHasta", fecha_fin_str)

    def seleccionar_detalle(self) -> None:
        """Selecciona la opción 'Detalles' en el frame y valida que quedó marcada."""
        frame = self._get_frame()
        # Hacer click en radio button 'Detalles'
        frame.locator("xpath=//*[@id='ctl00_maincontent_RBOK0_1']").click()
        # Validar que quedó seleccionado
        assert frame.locator("xpath=//*[@id='ctl00_maincontent_RBOK0_1']").is_checked(), \
            "No quedó seleccionado 'Detalles'"

    def generar_y_capturar_reporte(self, screenshot_report: str = "screenshot_ws01_report.png") -> None:
        """Genera el reporte haciendo click en el botón y captura el popup PDF.
        
        La captura se guarda en el directorio 'evidencias/' con el nombre dado
        por screenshot_report (por defecto 'screenshot_ws01_report.png').
        """
        frame = self._get_frame()
        boton_generar = frame.locator("xpath=//*[@id='ctl00_maincontent_BtnGenerar']")
        boton_generar.wait_for(state="visible", timeout=15_000)

        # Preparar directorio de evidencias
        evid = Path(__file__).resolve().parent.parent / "evidencias"
        evid.mkdir(parents=True, exist_ok=True)
        screenshot_path = evid / screenshot_report

        try:
            # Capturar el popup al hacer click en Generar
            with self.page.expect_popup(timeout=15_000) as popup_info:
                boton_generar.click()
            report_page = popup_info.value

            # Esperar a que cargue y hacer screenshot
            report_page.wait_for_load_state("load")
            report_page.wait_for_timeout(1_000)
            report_page.screenshot(path=str(screenshot_path), full_page=True)
            report_page.close()
        except Exception:
            # Fallback: buscar PDF embebido o capturar la página principal
            pdf_el = self.page.query_selector("iframe[src*='.pdf'], embed[type='application/pdf']")
            if pdf_el:
                try:
                    pdf_el.screenshot(path=str(screenshot_path))
                except Exception:
                    self.page.screenshot(path=str(screenshot_path), full_page=True)
            else:
                self.page.screenshot(path=str(screenshot_path), full_page=True)

        # Volver al tab principal y verificar que podemos seguir operando
        self.page.bring_to_front()
        self.page.wait_for_selector("input[placeholder='Opción']")