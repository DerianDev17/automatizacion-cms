"""
Page Object para el módulo **CM60 – Tarjetas Canceladas**. Permite
consultar las tarjetas canceladas dentro de un rango de fechas o por
criterio【547172095933312†L219-L220】.
"""

from playwright.sync_api import Page, expect
from datetime import date, timedelta


class CM60CanceladasPage:
    """Modela la pantalla CM60 – Tarjetas Canceladas."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def open_from_menu(self, menu_page) -> None:
        menu_page.open_cm60()
        # Esperar al iframe del módulo CM60 en lugar del texto que puede estar oculto
        self.page.wait_for_selector("iframe[name='iframe_CM60']", timeout=30_000)

    def _get_frame(self):
        iframe_el = self.page.wait_for_selector("iframe[name='iframe_CM60']", timeout=30_000)
        frame = iframe_el.content_frame()
        if frame is None:
            raise RuntimeError("No se pudo obtener el frame de CM60")
        return frame

    def buscar(self, fecha_inicio: str, fecha_fin: str) -> None:
        """Busca tarjetas canceladas dentro de un rango de fechas (YYYY-MM-DD)."""
        # Usar el iframe del módulo para rellenar fechas y buscar
        frame = self._get_frame()
        frame.fill("#ctl00_maincontent_FecInicial", fecha_inicio)
        frame.fill("#ctl00_maincontent_FecFinal", fecha_fin)
        frame.click("button:has-text('Buscar')")
        expect(frame.locator("table tr")).to_have_count(at_least=1)

    def set_date_range_days(self, days: int = 15) -> None:
        """Establece el rango de fechas en el formulario: hoy y hoy - `days` (formato YYYY/MM/DD)."""
        frame = self._get_frame()
        hoy = date.today()
        inicio = hoy - timedelta(days=days)
        fmt = lambda d: d.strftime("%Y/%m/%d")
        frame.fill("#ctl00_maincontent_FecInicial", fmt(inicio))
        frame.fill("#ctl00_maincontent_FecFinal", fmt(hoy))

    def set_filters(self, por: str = "Oficina Origen", oficina: str = "Todas", motivo: str = "Todos") -> None:
        """Configura los selects 'Por', 'Oficina' y 'Motivo' dentro del iframe.

        El método intenta localizar los <select> con varios selectores y seleccionar
        la opción por su texto (label). Esto centraliza los fallbacks usados antes en tests.
        """
        frame = self._get_frame()

        def _try_select(selectors, label_text):
            for sel in selectors:
                try:
                    sel_loc = frame.locator(sel)
                    if sel_loc.count() == 0:
                        alt = sel.replace('#', '')
                        sel_loc = frame.locator(alt)
                        if sel_loc.count() == 0:
                            continue

                    # intentar seleccionar por option text
                    option_loc = sel_loc.locator("option", has_text=label_text)
                    if option_loc.count() > 0:
                        val = option_loc.first.get_attribute('value')
                        if val is not None:
                            frame.select_option(sel_loc, value=val)
                            return True

                    # fallback: select by label
                    try:
                        frame.select_option(sel_loc, label=label_text)
                        return True
                    except Exception:
                        continue
                except Exception:
                    continue
            return False

        por_selectors = ["#ctl00_maincontent_CboPor", "select[name='ctl00$maincontent$CboPor']"]
        oficina_selectors = ["#ctl00_maincontent_CboOficina", "select[name='ctl00$maincontent$CboOficina']", "xpath=//*[@id=\"ctl00_maincontent_CboOficina\"]"]
        motivo_selectors = ["#ctl00_maincontent_CboMotivos", "select[name='ctl00$maincontent$CboMotivos']", "xpath=//*[@id=\"ctl00_maincontent_CboMotivos\"]"]

        _try_select(por_selectors, por)
        _try_select(oficina_selectors, oficina)
        _try_select(motivo_selectors, motivo)

    def generate_and_capture(self, screenshot_report: str = "screenshot_cm60_report.png", screenshot_result: str = "screenshot_cm60_result.png") -> None:
        """Genera el reporte (Imprimir) y captura el PDF popup y la vista final con 'Fin del Reporte'."""
        frame = self._get_frame()

        btn_aceptar = frame.locator("#ctl00_maincontent_BtnImprimir")
        btn_aceptar.wait_for(state="visible", timeout=15_000)
        # Intentar capturar el popup PDF; si no aparece, usar fallback
        try:
            with self.page.expect_popup(timeout=15_000) as popup_info:
                btn_aceptar.click()
            report = popup_info.value

            report.wait_for_load_state("load")
            report.wait_for_timeout(1_000)
            try:
                from pathlib import Path
                evid = Path(__file__).resolve().parent.parent / "evidencias"
                evid.mkdir(parents=True, exist_ok=True)
                rpt_path = evid / screenshot_report
                report.screenshot(path=str(rpt_path), full_page=True)
            except Exception:
                pass
            finally:
                try:
                    report.close()
                except Exception:
                    pass
        except Exception:
            # Fallback: quizá el PDF se incrusta en la página o no abre popup
            try:
                from pathlib import Path
                evid = Path(__file__).resolve().parent.parent / "evidencias"
                evid.mkdir(parents=True, exist_ok=True)
                # buscar elementos que contengan PDF embebido
                pdf_el = self.page.query_selector("iframe[src*='.pdf'], embed[type='application/pdf'], object[type='application/pdf']")
                if pdf_el:
                    rpt_path = evid / screenshot_report
                    try:
                        pdf_el.screenshot(path=str(rpt_path))
                    except Exception:
                        # si el elemento no admite screenshot, capturar la página completa
                        self.page.screenshot(path=str(rpt_path), full_page=True)
                else:
                    # Capturar la página principal como último recurso
                    rpt_path = evid / screenshot_report
                    self.page.screenshot(path=str(rpt_path), full_page=True)
            except Exception:
                pass

        # volver al tab principal y asegurar el estado final
        self.page.bring_to_front()
        try:
            frame.click("#ctl00_maincontent_BtnImprimir")
        except Exception:
            pass
        try:
            frame.wait_for_selector("text=Fin del Reporte", timeout=30_000)
        except Exception:
            pass

        self.page.wait_for_timeout(1_000)
        try:
            from pathlib import Path
            evid = Path(__file__).resolve().parent.parent / "evidencias"
            evid.mkdir(parents=True, exist_ok=True)
            res_path = evid / screenshot_result
            self.page.screenshot(path=str(res_path), full_page=True)
        except Exception:
            pass

    def validar_resultados(self, min_rows: int = 1) -> None:
        expect(self.page.locator("table tr")).to_have_count(at_least=min_rows)