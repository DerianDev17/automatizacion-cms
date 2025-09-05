"""
Fixtures de Pytest para inicializar el navegador, cargar la configuración
y gestionar el inicio de sesión en el CMS. Al centralizar estas tareas en
`conftest.py` evitamos duplicar código en cada prueba.
"""

import os
import glob
from datetime import datetime
from pathlib import Path
from typing import Generator

import pytest
from pytest_html import extras
import yaml
from dotenv import load_dotenv
from playwright.sync_api import BrowserContext, Page


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def config() -> dict:
    """
    Carga la configuración desde un archivo YAML en la carpeta `config/`.
    El entorno se define mediante la variable de entorno `CMS_ENV` (qa, prod).
    Por defecto se utiliza qa.
    """
    env = os.getenv("CMS_ENV", "qa").lower()
    config_path = Path(__file__).parent / "config" / f"{env}.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de configuración para el entorno '{env}'.")
    cfg = _load_yaml(config_path)
    return cfg


@pytest.fixture(scope="session")
def creds(config: dict) -> dict:
    """
    Carga credenciales de usuario desde variables de entorno o del archivo YAML.
    Prioriza variables de entorno definidas en el archivo `.env`.
    """
    load_dotenv()  # Carga variables desde .env si existe
    users = config.get("users", {})
    result = {}
    for user_key, info in users.items():
        username_env = os.getenv(f"{user_key.upper()}_USER")
        password_env = os.getenv(f"{user_key.upper()}_PASS")
        result[user_key] = {
            "username": username_env or info.get("username"),
            "password": password_env or info.get("password"),
        }
    return result


# --- ⬇️ Configuración de Playwright cuando se utiliza pytest-playwright ---

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    """
    Ajusta los argumentos de lanzamiento del navegador para que Playwright ignore
    errores de certificados durante toda la sesión. Esto permite evitar
    excepciones como `ERR_SSL_KEY_USAGE_INCOMPATIBLE` en entornos con
    certificados no válidos o mal configurados.

    La fixture `browser_type_launch_args` es proporcionada por pytest‑playwright y
    permite sobreescribir los parámetros de lanzamiento del navegador de
    manera centralizada.
    """
    # Añade el argumento de Chrome/Chromium para ignorar cualquier error de
    # certificado. Si ya existen otros argumentos, se combinan.
    args = browser_type_launch_args.get("args", [])
    return {**browser_type_launch_args, "args": args + ["--ignore-certificate-errors"]}


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    """
    Ajusta los parámetros del contexto del navegador para que Playwright ignore
    los errores HTTPS y grabe vídeo de cada prueba. Esta fixture es utilizada
    por pytest‑playwright al crear un nuevo contexto para cada test.
    """
    # Asegúrate de que exista la carpeta de vídeos
    videos_dir = Path("videos")
    videos_dir.mkdir(exist_ok=True)
    return {
        **browser_context_args,
        "ignore_https_errors": True,
        "record_video_dir": str(videos_dir),
        "record_video_size": {"width": 1280, "height": 720},
    }


# Eliminamos la fixture ``context`` personalizada para que PyTest utilice la
# proporcionada por pytest‑playwright. Las opciones de contexto se definen
# mediante la fixture ``browser_context_args`` de arriba.

# --- ⬇️ Configuración para adjuntar capturas y vídeos al reporte HTML ---

# Directorio donde se moverán los artefactos generados por cada test. Esto
# incluye capturas de pantalla (cuyos nombres comiencen por ``screenshot_``)
# y vídeos (cuyos nombres comiencen por ``video_``). Si el directorio no
# existe, se crea automáticamente.
ARTEFACTS_DIR = Path("artefacts")
ARTEFACTS_DIR.mkdir(exist_ok=True)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Después de la ejecución de cada test, este hook comprueba si se han
    generado nuevos archivos de captura o vídeo y los mueve al directorio
    ``artefacts``. A continuación, adjunta automáticamente estos archivos
    al reporte HTML a través de la API de pytest‑html. Se considera que un
    artefacto es nuevo si su fecha de modificación es inferior a 5 minutos
    respecto del momento de la prueba.
    """
    outcome = yield
    rep = outcome.get_result()
    # Solo al finalizar la fase de llamada del test
    if rep.when != "call":
        return

    # Inicializa la lista de extras si no existe
    rep.extra = getattr(rep, "extra", [])

    # Patrones a buscar: capturas de pantalla y vídeos generados
    patrones = [
        "screenshot_*.png",
        "screenshot_*.jpg",
        "video_*.webm",
        "video_*.mp4",
    ]

    # Marca de tiempo para filtrar archivos recientes (menos de 5 minutos)
    ahora = datetime.now().timestamp()

    for patron in patrones:
        for archivo in glob.glob(patron):
            # Comprueba si el archivo es reciente
            if ahora - os.path.getmtime(archivo) < 300:
                destino = ARTEFACTS_DIR / os.path.basename(archivo)
                # Solo copia si no existe ya una versión en artefacts
                if not destino.exists():
                    Path(archivo).rename(destino)
                # Determina si es imagen o vídeo para adjuntar correctamente
                if destino.suffix.lower() in {".png", ".jpg", ".jpeg"}:
                    rep.extra.append(extras.image(destino, name=destino.name))
                else:
                    rep.extra.append(extras.video(destino, name=destino.name))


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """
    Abre una nueva página a partir del contexto proporcionado por pytest‑playwright
    y toma una captura de pantalla al finalizar la prueba. La captura se
    guarda con prefijo ``screenshot_`` y la fecha/hora actual para ser
    recogida por el hook de reporte. Al utilizar el contexto creado por la
    fixture ``browser_context_args``, esta página hereda la configuración
    de ignorar errores HTTPS y grabar vídeo.
    """
    page = context.new_page()
    yield page
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        screenshot_name = f"screenshot_{timestamp}.png"
        page.screenshot(path=screenshot_name, full_page=True)
    except Exception:
        pass
    finally:
        page.close()


@pytest.fixture(scope="function")
def login(page: Page, config: dict, creds: dict):
    """
    Inicia sesión en el CMS usando las credenciales configuradas. Debe
    emplearse antes de ejecutar cualquier acción que requiera autenticación.
    Devuelve una función para permitir múltiples logins con distintos usuarios.
    """
    from cms_automation.pages.login_page import LoginPage
    from cms_automation.pages.menu_page import MenuPage

    def _do_login(user_key: str = "admin") -> MenuPage:
        base_url: str = config["base_url"]
        credentials = creds.get(user_key)
        if not credentials:
            raise KeyError(f"No hay credenciales para el usuario '{user_key}' en la configuración.")
        login_page = LoginPage(page, base_url)
        login_page.open()
        login_page.login(credentials["username"], credentials["password"])
        return MenuPage(page)

    return _do_login