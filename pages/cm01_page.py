# pages/cm01_page.py
from playwright.sync_api import Page, FrameLocator, Locator

class CM01Page:
    MODAL_IFRAME_NAME = "iframe_CM01"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.frame: FrameLocator | None = None

    # ---------- Apertura del módulo ----------
    def open(self) -> None:
        self.page.fill("input[placeholder='Opción']", "CM01")
        self.page.click("button.searchB", force=True)
        self.frame = self.page.frame_locator(f"iframe[name='{self.MODAL_IFRAME_NAME}']")
        self.frame.locator("text=CM01 Solicitud de Tarjetas").first.wait_for(timeout=15_000)

    # ---------- Buscar por ----------
    @property
    def buscar_por_combo(self) -> Locator:
        return self.frame.locator("#ctl00_maincontent_CboBuscarPor")

    def select_buscar_por(self, label: str) -> None:
        self.buscar_por_combo.wait_for(state="visible", timeout=15_000)
        opciones = self.buscar_por_combo.inner_text()
        assert label in opciones, f"'Buscar por' no tiene la opción: {label}. Opciones: {opciones}"
        self.buscar_por_combo.select_option(label=label)

    # ---------- Consulta por nombre ----------
    @property
    def input_apellidos(self) -> Locator:
        return self.frame.locator("#ctl00_maincontent_TxtApellidos")

    @property
    def input_nombres(self) -> Locator:
        return self.frame.locator("#ctl00_maincontent_TxtNombres")

    def consultar_por_nombre(self, apellidos: str, nombres: str) -> None:
        self.input_apellidos.wait_for(state="visible", timeout=10_000)
        self.input_nombres.wait_for(state="visible", timeout=10_000)
        self.input_apellidos.fill(apellidos)
        self.input_nombres.fill(nombres)
        self.frame.locator("#ctl00_maincontent_BtnConsultar").click()
        filas = self.frame.locator("table tr")
        filas.first.wait_for(state="visible", timeout=15_000)
        assert filas.count() > 1, "La búsqueda por nombre no devolvió resultados."

    # ---------- Selección de cliente ----------
    def seleccionar_primer_resultado(self) -> None:
        primera_fila = self.frame.locator("table tr").nth(1)  # saltar header
        primera_fila.dblclick()
        self.frame.locator("text=Edit").first.wait_for(state="visible", timeout=10_000)

    # ---------- Editar redes, marcar y continuar ----------
    def editar_redes_y_continuar(self) -> None:
        self.frame.locator("text=Edit").first.click()

        # Estos selectores son genéricos; si tu grid cambia, afínalos
        self.frame.locator("input[type='checkbox']").first.check()
        self.frame.locator("text=Update").first.click()
        self.frame.locator("input[type='checkbox']").nth(1).check()

        self.frame.get_by_role("button", name="Continuar").click()

    # ---------- Verificación de siguiente paso ----------
    def should_show_tabs_generales_autorizaciones(self) -> None:
        self.frame.locator("text=Generales").first.wait_for(state="visible", timeout=15_000)
        self.frame.locator("text=Autorizaciones").first.wait_for(state="visible", timeout=15_000)
