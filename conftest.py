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
    return _load_yaml(config_path)


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


# ----------------- Lanzamiento del browser -----------------

@pytest.fixture(scope="session")
def browser_type_launch_args(pytestconfig, browser_type_launch_args: dict) -> dict:
    """
    Lógica de headless robusta:
      - Si se usa --headed: ventana visible (sin headless).
      - Si NO se usa --headed:
          * HEADLESS_MODE=auto|new -> forzar 'new headless' (evita problemas TLS en Chromium).
          * HEADLESS_MODE=old      -> headless clásico (no recomendado).
          * HEADLESS_MODE=off      -> sin headless (equivalente a headed).
    Además: flags TLS relajados y canal opcional (chrome/chromium) por env.
    """
    args = list(browser_type_launch_args.get("args", []))

    headed = bool(pytestconfig.getoption("--headed"))
    headless_mode = os.getenv("HEADLESS_MODE", "auto").lower()  # auto|new|old|off

    use_new_headless = (not headed) and (headless_mode in {"auto", "new"})
    use_old_headless = (not headed) and (headless_mode == "old")

    # Flags TLS y otros
    extra_args = [
        "--ignore-certificate-errors",
        "--reduce-security-for-testing",
        "--allow-insecure-localhost",
        "--disable-features=CertificateTransparencyEnforcement",
    ]
    for a in extra_args:
        if a not in args:
            args.append(a)

    # Canal opcional (Chrome suele manejar mejor el trust store corporativo)
    channel = os.getenv("BROWSER_CHANNEL", "").strip().lower()  # "chrome" o "chromium"

    launch = dict(browser_type_launch_args)
    launch["args"] = args

    if use_new_headless:
        launch["headless"] = False
        if "--headless=new" not in launch["args"]:
            launch["args"].append("--headless=new")
    elif use_old_headless:
        launch["headless"] = True
    else:
        launch["headless"] = False  # ventana visible

    if channel:
        launch["channel"] = channel

    print(
        f"[PW LAUNCH] headed={headed} mode={headless_mode} "
        f"channel={launch.get('channel','<default>')} "
        f"headless={launch['headless']} args={' '.join(launch['args'])}"
    )
    return launch


# -------------- Contexto del browser y vídeo --------------

@pytest.fixture(scope="session")
def browser_context_args(config: dict, browser_context_args: dict) -> dict:
    videos_dir = Path("videos"); videos_dir.mkdir(exist_ok=True)
    return {
        **browser_context_args,
        "ignore_https_errors": bool(config.get("ignore_https_errors", True)),
        "record_video_dir": str(videos_dir),
        "record_video_size": {"width": 1280, "height": 720},
        "viewport": {"width": 1366, "height": 768},
    }


# -------------- Evidencias HTML (screenshots y vídeo) --------------

EVIDENCIAS_DIR = Path("evidencias")
EVIDENCIAS_DIR.mkdir(exist_ok=True)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Después de la ejecución de cada test, mueve evidencias recientes a `evidencias`
    y las adjunta al reporte HTML (pytest-html).
    """
    outcome = yield
    rep = outcome.get_result()
    if rep.when != "call":
        return

    rep.extra = getattr(rep, "extra", [])

    patrones = ["screenshot_*.png", "screenshot_*.jpg", "video_*.webm", "video_*.mp4"]
    ahora = datetime.now().timestamp()

    for patron in patrones:
        for archivo in glob.glob(patron):
            if ahora - os.path.getmtime(archivo) < 300:  # últimos 5 minutos
                destino = EVIDENCIAS_DIR / os.path.basename(archivo)
                if not destino.exists():
                    Path(archivo).rename(destino)
                    target = destino
                else:
                    # Si ya existe en evidencias, adjunta el archivo original
                    target = Path(archivo)

                if target.suffix.lower() in {".png", ".jpg", ".jpeg"}:
                    rep.extra.append(extras.image(target, name=target.name))
                else:
                    rep.extra.append(extras.video(target, name=target.name))


# ----------------- Fixture page única -----------------

@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """
    Abre una nueva página a partir del contexto (que ya ignora HTTPS).
    Toma screenshot al finalizar para el reporte.
    """
    page = context.new_page()

    # Smoke opcional (activar con SSL_SMOKE=1)
    if os.getenv("SSL_SMOKE", "0") == "1":
        page.goto("https://expired.badssl.com/", wait_until="domcontentloaded", timeout=10_000)

    yield page

    try:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        page.screenshot(path=f"screenshot_{ts}.png", full_page=True)
    except Exception:
        pass
    finally:
        page.close()


# ----------------- Login helper -----------------

@pytest.fixture(scope="function")
def login(page: Page, config: dict, creds: dict):
    """
    Inicia sesión en el CMS usando las credenciales configuradas.
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
        login_page.open()  # Recomendación: usar wait_until="domcontentloaded" en el POM
        login_page.login(credentials["username"], credentials["password"])
        return MenuPage(page)

    return _do_login
