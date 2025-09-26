# Guía de uso y operación — `cms_automation`

Esta guía describe paso a paso cómo preparar el entorno, ejecutar las pruebas y revisar la evidencia generada por el proyecto de automatización del CMS.

## 1. Preparar el entorno

### 1.1 Clonar el repositorio (por terminal)

Se recomienda clonar el repositorio usando el nombre `cms_automation` para que los imports (`from cms_automation.pages...`) funcionen sin configuraciones adicionales. Elige la terminal que utilices:

**PowerShell (Windows)**

```powershell
git clone <url-del-repositorio> cms_automation
Set-Location cms_automation
```

**Símbolo del sistema o Git Bash (Windows)**

```bash
git clone <url-del-repositorio> cms_automation
cd cms_automation
```

**Bash (Linux, macOS o WSL)**

```bash
git clone <url-del-repositorio> cms_automation
cd cms_automation
```

> Si prefieres mantener otro nombre de carpeta, asegúrate de que Python pueda resolver el paquete `cms_automation`. Puedes crear un enlace simbólico o ajustar `PYTHONPATH` y los imports según convenga.

### 1.2 Crear y activar el entorno virtual

El siguiente bloque resume los comandos para cada terminal. En todos los casos el entorno virtual se creará en `.venv` dentro del proyecto.

**PowerShell (Windows)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

> Si PowerShell bloquea la ejecución del script de activación, ejecuta `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` e inténtalo nuevamente.

**Símbolo del sistema o Git Bash (Windows)**

```bash
python -m venv .venv
source .venv/Scripts/activate
```

**Bash (Linux, macOS o WSL)**

```bash
python -m venv .venv
source .venv/bin/activate
```

Para salir del entorno virtual en cualquier terminal, ejecuta `deactivate`.

### 1.3 Instalar dependencias

Con el entorno virtual activo, instala las librerías Python y los navegadores de Playwright. Ejecuta los comandos en la terminal correspondiente (el prefijo `python` utiliza el intérprete del entorno virtual):

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
playwright install --with-deps
```

En Windows, `--with-deps` es opcional. Ejecuta `playwright install` al menos una vez para que se descarguen los binarios necesarios. Si el comando solicita privilegios de administrador en Linux, antepon `sudo` únicamente a `playwright install --with-deps`.

### 1.4 Configurar variables de entorno

- La fixture `config` lee el archivo `config/<entorno>.yaml` según la variable `CMS_ENV`. Por defecto usa `config/qa.yaml`.
- Crea archivos adicionales (`config/staging.yaml`, `config/prod.yaml`, etc.) replicando la estructura si necesitas otros entornos.
- Las credenciales declaradas dentro de `users` pueden sobrescribirse con variables de entorno (`ADMIN_USER`, `ADMIN_PASS`, etc.) o a través de un archivo `.env`.

Ejemplo de `.env` (no lo subas al repositorio):

```env
ADMIN_USER=usuario_admin
ADMIN_PASS=clave-super-segura
```

Carga automática: el proyecto utiliza `python-dotenv`, por lo que las variables definidas en `.env` estarán disponibles al ejecutar pytest.

### 1.5 Datos de prueba

Algunos flujos requieren archivos de datos. `CM14TrazabilidadPage`, por ejemplo, busca `tests/data/cards.csv` con la columna `card_number`:

```csv
card_number
1234567890123456
6543210987654321
```

Crea la carpeta `tests/data/` y ajusta los números de tarjeta a los que existan en tu entorno QA.

## 2. Ejecutar pruebas

### 2.1 Comandos básicos

Desde la raíz del proyecto:

- **Todas las pruebas E2E**:

  ```bash
  pytest tests/e2e
  ```

- **Solo un archivo**:

  ```bash
  pytest tests/e2e/test_cm46_reporte_lotes_pendientes.py
  ```

- **Una prueba puntual**:

  ```bash
  pytest tests/e2e/test_cm14_trazabilidad_tarjetas.py::test_cm14_trazabilidad_tarjetas
  ```

### 2.2 Filtros por marcador

Los marcadores se definen en `pytest.ini`. Algunos ejemplos:

```bash
pytest -m cm14              # Ejecuta únicamente CM14
pytest -m "cm14 or cm45"    # Ejecuta CM14 y CM45
pytest -m "not ws01"        # Excluye los tests de servicios web
```

### 2.3 Modos de ejecución

- **Modo headed y cámara lenta** (útil para depurar pasos visualmente):

  ```bash
  pytest --headed --slowmo 300 -m cm45
  ```

- **Ejecución en paralelo** (`pytest-xdist`):

  ```bash
  pytest -n auto -m "cm14 or cm60"
  ```

- **Reintentos automáticos** (si instalas `pytest-rerunfailures`):

  ```bash
  pytest --reruns 2 -m cm46
  ```

### 2.4 Pruebas de servicios web

`tests/api/` contiene esqueletos para WS01 y WS02. Actualmente utilizan `pytest.skip` porque los endpoints no están disponibles. Cuando se publiquen:

1. Implementa la llamada HTTP (por ejemplo, con `requests` o la API `api_request_context` de Playwright).
2. Valida el código de estado y el esquema JSON.
3. Retira el `pytest.skip` y añade asserts reales.

### 2.5 Mantener el paquete importable

Si ves el error `ModuleNotFoundError: No module named 'cms_automation'`, significa que Python no encuentra el paquete. Soluciones habituales:

- Renombrar la carpeta del proyecto a `cms_automation`.
- Crear un enlace simbólico:
  - Linux/macOS: `ln -s $(pwd) ../cms_automation`
  - PowerShell (modo administrador): `New-Item -ItemType SymbolicLink -Path ..\cms_automation -Target (Get-Location)`
- Ajustar los imports a rutas relativas (último recurso si no puedes modificar el nombre de la carpeta).

## 3. Reportes y evidencias

- **Reporte HTML**: `pytest.ini` ya incluye `--html=reports/report.html --self-contained-html`, por lo que cada ejecución genera un reporte autónomo en `reports/`.
- **Capturas y vídeos**: el hook `pytest_runtest_makereport` mueve archivos recientes (prefijos `screenshot_` o `video_`) a la carpeta `artefacts/` y los adjunta automáticamente en el reporte HTML. Los vídeos provienen de la configuración `record_video_dir` en `browser_context_args`.
- **Descargas**: utiliza `utils/files.py::save_download` para guardar archivos descargados durante las pruebas en la carpeta `downloads/` (se crea bajo demanda).
- **Reportes Allure** (opcional):

  ```bash
  pytest --alluredir=reports/allure
  allure serve reports/allure
  ```

  Necesitas tener Allure instalado de forma global o mediante `npm/yarn`.

## 4. Buenas prácticas operativas

- Ejecuta `pytest -q` localmente antes de subir cambios para detectar fallas rápidas.
- Mantén los Page Objects enfocados en acciones de alto nivel; delega validaciones complejas a los tests o helpers.
- Prioriza selectores basados en `data-testid`; si no existen, documenta los selectores alternativos y centralízalos en `utils/selectors.py`.
- Versiona únicamente credenciales ficticias. Para información real utiliza `.env` o variables de entorno del sistema.
- Limpia periódicamente `artefacts/`, `videos/` y `reports/` para evitar ocupar espacio innecesario.

## 5. Resolución de problemas comunes

| Problema | Causa probable | Solución sugerida |
|----------|----------------|-------------------|
| `ModuleNotFoundError: cms_automation` | El intérprete no encuentra el paquete | Renombra la carpeta, crea un enlace simbólico o ajusta `PYTHONPATH` según la sección 2.5. |
| `Timeout 30000ms exceeded` al abrir módulos | Selectores desactualizados o entorno lento | Revisa los selectores en el Page Object correspondiente y considera aumentar los `timeout` en `config/<entorno>.yaml` o en los métodos `wait_for_*`. |
| Capturas vacías en `artefacts/` | Playwright cerró la página antes de capturar | Asegura que el test no finalice abruptamente; puedes añadir `page.wait_for_timeout(1000)` antes de cerrar o revisar que la fixture `page` no se interrumpa por excepciones. |
| Errores SSL en QA | Certificados no válidos | `browser_type_launch_args` y `browser_context_args` ya establecen `--ignore-certificate-errors` e `ignore_https_errors=True`. Verifica que se esté utilizando la configuración por defecto. |
| Sin datos en reportes CM | CSV vacío o tarjetas inexistentes | Verifica el contenido de `tests/data/cards.csv` y que las tarjetas existan en el entorno de prueba. |

## 6. Recursos adicionales

- [Documentación del proyecto (`docs/project_doc.md`)](project_doc.md): descripción detallada de la arquitectura, módulos cubiertos y convenciones de desarrollo.
- [Sitio oficial de Playwright](https://playwright.dev/python/): referencia para ampliar comandos y patrones de automatización.
- [Pytest](https://docs.pytest.org/): documentación oficial para marcadores, fixtures y plugins.

Con estos pasos podrás instalar, ejecutar y mantener las automatizaciones del CMS de forma consistente. Ante cualquier actualización del sistema, revisa también la documentación del proyecto para mantener alineados los Page Objects y las pruebas.
