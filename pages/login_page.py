"""
Page Object para la pantalla de inicio de sesión del CMS. Encapsula
la navegación y el formulario de autenticación. Todas las pruebas deben
usar este objeto para ingresar al sistema en lugar de replicar el código
de login en cada test.
"""

from playwright.sync_api import Page, expect


class LoginPage:
    """Modela la pantalla de login del CMS."""

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")

    def open(self) -> None:
        """Navega a la ruta de login del CMS."""
        self.page.goto(f"{self.base_url}/#/Login")
        # Esperar a que el campo de usuario sea visible
        expect(self.page.locator("input[placeholder='Usuario']")).to_be_visible()

    def login(self, username: str, password: str) -> None:
        """Realiza el proceso de autenticación y espera a que cargue el menú principal."""
        self.page.fill("input[placeholder='Usuario']", username)
        self.page.fill("input[placeholder='Clave']", password)
        self.page.get_by_role("button", name="Iniciar sesión").click()
        self.page.wait_for_load_state("networkidle", timeout=15_000)
        self.page.wait_for_selector("input[placeholder='Opción']", timeout=15_000)
