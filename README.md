# Automatización del Card Management System (CMS)

Este repositorio contiene la automatización end-to-end de los módulos de **Consultas y Reportes** del *Card Management System* (CMS) de la Red Transaccional Cooperativa. Las pruebas están implementadas con **Python**, **pytest** y **Playwright** utilizando el patrón **Page Object Model (POM)** para facilitar el mantenimiento y la reutilización.

El objetivo es ofrecer una base probada, bien documentada y lista para extender la cobertura funcional del CMS sin fricción para nuevos integrantes del equipo.

## Características principales

- Page Objects especializados para cada módulo automatizado (CM14, CM16, CM18, CM19, CM21, CM22, CM44, CM45, CM46, CM60, CM85), además de la autenticación y navegación principal.
- Fixtures centralizadas en `conftest.py` para cargar configuración YAML, preparar credenciales, lanzar Playwright con manejo de vídeo y mover evidencias a una ubicación controlada.
- Configuración por entorno en `config/` con soporte para variables de entorno y archivos `.env`.
- Integración nativa con `pytest-html`, posibilidad de ejecutar en paralelo (`pytest-xdist`) y hooks que generan artefactos listos para auditoría.
- Documentación ampliada en `docs/` para profundizar en la arquitectura y el flujo operativo.

## Requisitos previos

- Python 3.11 o superior.
- `pip` actualizado a la última versión disponible.
- Navegadores de Playwright instalados (se descargan con `playwright install`).
- Acceso a la URL del CMS del entorno que se desea automatizar y credenciales válidas.

> ℹ️ El paquete se importa como `cms_automation`. Se recomienda clonar el repositorio usando ese nombre para evitar configurar rutas adicionales.

## Instalación rápida (paso a paso por terminal)

Selecciona la terminal que uses habitualmente y sigue los comandos indicados. En todos los casos se asume que cuentas con Python 3.11+ en el `PATH`.

### PowerShell (Windows)

```powershell
# 1. Clonar el repositorio
git clone <url-del-repositorio> cms_automation
Set-Location cms_automation

# 2. Crear el entorno virtual
python -m venv .venv

# 3. Activar el entorno virtual
.\.venv\Scripts\Activate.ps1

# 4. Actualizar pip e instalar dependencias
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 5. Descargar navegadores de Playwright
playwright install
```

> Si PowerShell bloquea la ejecución del script de activación, ejecuta una sola vez `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.

### Símbolo del sistema o Git Bash en Windows

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio> cms_automation
cd cms_automation

# 2. Crear el entorno virtual
python -m venv .venv

# 3. Activar el entorno virtual
source .venv/Scripts/activate

# 4. Actualizar pip e instalar dependencias
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 5. Descargar navegadores de Playwright
playwright install
```

### Bash (Linux / macOS / WSL)

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio> cms_automation
cd cms_automation

# 2. Crear el entorno virtual
python -m venv .venv

# 3. Activar el entorno virtual
source .venv/bin/activate

# 4. Actualizar pip e instalar dependencias
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 5. Descargar navegadores de Playwright (con dependencias del sistema)
playwright install --with-deps
```

> En distribuciones Linux puede solicitar privilegios de superusuario para instalar dependencias del sistema. Ejecuta el comando con `sudo` solo si es necesario.

## Configuración del proyecto

### Descripción de la carpeta `config/`

Los archivos YAML de `config/` definen parámetros por entorno. El archivo `config/qa.yaml` incluye por defecto:

```yaml
base_url: "https://..."
timeout: 30000           # Tiempo de espera en milisegundos para acciones Playwright
ignore_https_errors: true
users:
  admin:
    username: "usuario"
    password: "contraseña"
```

- **Selección de entorno**: la variable de entorno `CMS_ENV` determina qué archivo usar (por ejemplo, `CMS_ENV=staging` utilizaría `config/staging.yaml`). Si no se define, se carga `qa`.
- **Usuarios**: declara los roles que utilizarán las pruebas (`admin`, `analyst`, etc.). Cada entrada debe contener `username` y `password`.
- **Parámetros adicionales**: agrega claves personalizadas (por ejemplo `downloads_path`, `api_base_url`) según las necesidades del entorno. Mantén los comentarios y ejemplos actualizados para nuevos miembros del equipo.

### Credenciales y variables de entorno

- Las credenciales del YAML pueden sobrescribirse mediante variables de entorno (`ADMIN_USER`, `ADMIN_PASS`, etc.) o un archivo `.env` en la raíz.
- Ejemplo de `.env` (no debe versionarse):

  ```env
  ADMIN_USER=usuario_admin
  ADMIN_PASS=clave-super-segura
  CMS_ENV=qa
  ```

- El proyecto utiliza `python-dotenv`, por lo que las variables definidas se cargan automáticamente al ejecutar `pytest`.

### Datos de prueba

- Algunos flujos consumen archivos CSV ubicados en `tests/data/`. Crea la carpeta y el archivo `cards.csv` con una columna `card_number` si vas a ejecutar los escenarios de trazabilidad.
- Ajusta los valores a tarjetas válidas en tu entorno para evitar falsos negativos.

## Uso habitual

Con el entorno virtual activo, estos son los comandos principales:

- **Ejecutar toda la suite end-to-end**:

  ```bash
  pytest tests/e2e
  ```

- **Filtrar por marcador** (marcadores declarados en `pytest.ini`):

  ```bash
  pytest -m cm14
  pytest -m "cm14 or cm45"
  pytest -m "not ws"
  ```

- **Ejecutar un archivo o una prueba específica**:

  ```bash
  pytest tests/e2e/test_cm14_trazabilidad_tarjetas.py
  pytest tests/e2e/test_cm14_trazabilidad_tarjetas.py::test_cm14_trazabilidad_tarjetas
  ```

- **Depurar con interfaz visible y cámara lenta**:

  ```bash
  pytest --headed --slowmo 300 -m cm45
  ```

- **Ejecución en paralelo** (requiere instalar `pytest-xdist`):

  ```bash
  pytest -n auto -m "cm14 or cm60"
  ```

> Los archivos en `tests/api/` sirven como plantillas para futuras pruebas de servicios web. Actualmente se marcan con `pytest.skip` hasta que los endpoints estén disponibles.

## Ciclos de tarjetas en preparación

Dos nuevos frentes de automatización —**Tarjetas nominadas** y **Tarjetas innominadas**— ya cuentan con andamiaje listo para
integrar pruebas end-to-end sin afectar la suite existente. Toda la información del ciclo de vida se centraliza en
`utils/workflows.py`, lo que evita duplicar descripciones y códigos de módulo.

### Tarjetas nominadas

- CM01. Solicitud de tarjeta – Ciclo vida Tarjeta nominada
- CM10. Emisión de tarjetas – Ciclo vida Tarjeta nominada
- CM07. Recepción de tarjetas – Ciclo vida Tarjeta nominada
- CM03. Entrega de tarjetas – Ciclo vida Tarjeta nominada
- CM02. Solicitud de tarjeta adicional – Ciclo vida Tarjeta nominada

### Tarjetas innominadas

- CM83. Cupos por oficina – Ciclo vida Tarjeta innominada
- CM70. Solicitud de tarjetas innominadas – Ciclo vida Tarjeta innominada
- CM10. Emisión de tarjetas – Ciclo vida Tarjeta innominada
- CM07. Recepción de tarjetas – Ciclo vida Tarjeta innominada
- CM06. Mantenimiento de tarjetas – Ciclo vida Tarjeta innominada

Las pruebas esqueleto residen en `tests/e2e/ciclos/` y están marcadas con `@pytest.mark.skip(reason="pendiente implementación")`
para no romper la ejecución actual. Cuando los flujos estén listos, elimina el `skip` y ejecuta de forma segmentada con:

```bash
pytest -m ciclo_nominada
pytest -m ciclo_innominada
```

Los Page Objects asociados (estructura vacía) se encuentran en `pages/ciclos/ciclo_tarjeta.py` y cada función levanta
`NotImplementedError` hasta que se agregue la lógica real.

## Reportes y evidencias

- `pytest.ini` añade por defecto `--html=reports/report.html --self-contained-html`, generando un reporte HTML independiente por ejecución.
- El hook `pytest_runtest_makereport` centraliza capturas de pantalla y vídeos en `artefacts/` y adjunta los archivos relevantes al reporte.
- Para generar reportes **Allure** (opcional):

  ```bash
  pytest --alluredir=reports/allure
  allure serve reports/allure
  ```

  Asegúrate de tener Allure instalado localmente (`npm install -g allure-commandline` o instaladores oficiales).

## Estructura del repositorio

```
cms_automation/
├── config/                  # Configuración por entorno (YAML, seleccionados con CMS_ENV)
├── docs/                    # Guías detalladas y documentación de arquitectura
├── pages/                   # Page Objects y helpers de navegación
│   └── ciclos/              # Stubs de los flujos Tarjetas_nominadas e innominadas
├── tests/
│   ├── e2e/                 # Pruebas end-to-end por módulo del CMS
│   │   └── ciclos/          # Nuevos escenarios de ciclo de tarjetas (skip por ahora)
│   └── api/                 # Plantillas para pruebas de servicios web
├── utils/                   # Selectores, workflows y utilidades varias
│   └── workflows.py         # Definición centralizada de los ciclos de tarjetas
├── fixtures/                # Datos compartidos para pruebas específicas
├── conftest.py              # Fixtures globales y hooks de pytest
├── pytest.ini               # Marcadores y configuración general de pytest
├── requirements.txt         # Dependencias Python del proyecto
└── README.md                # Este documento
```

## Extender la automatización

1. **Crear/actualizar el Page Object** del módulo en `pages/`, encapsulando acciones de negocio y selectores.
2. **Agregar la prueba** correspondiente en `tests/e2e/`, reutilizando la fixture `login` para autenticarse y `MenuPage` para navegar.
3. **Definir o reutilizar un marcador `cmXX`** en `pytest.ini` para facilitar ejecuciones filtradas.
4. **Centralizar selectores** en `utils/selectors.py` cuando se reutilicen en varias pantallas.
5. **Actualizar la documentación** (`README.md`, `docs/`) cada vez que se incorpore un nuevo flujo.

## Documentación adicional

- [`docs/usage.md`](docs/usage.md): guía operativa paso a paso para configurar el entorno, ejecutar pruebas y revisar reportes.
- [`docs/project_doc.md`](docs/project_doc.md): descripción arquitectónica, estado de los módulos y convenciones de desarrollo.
- [`docs/improvement_checklist.md`](docs/improvement_checklist.md): lista de verificación con oportunidades de mejora priorizadas.

## Buenas prácticas

- Prioriza selectores estables (`data-testid`, atributos semánticos) para reducir roturas por cambios de UI.
- Mantén los Page Objects con responsabilidades acotadas; las aserciones complejas deben vivir en los tests o helpers.
- Versiona únicamente datos ficticios. Las credenciales reales deben cargarse vía `.env` o variables de entorno.
- Limpia periódicamente `artefacts/`, `videos/`, `reports/` y `downloads/` para evitar que crezcan en exceso.
- Ejecuta `pytest` localmente antes de subir cambios o abrir un Pull Request.

Con esta guía tendrás una referencia completa para preparar el entorno, ejecutar las pruebas y extender la automatización del CMS con confianza.
