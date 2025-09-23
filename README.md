# Automatización del Card Management System (CMS)

Este repositorio recopila la automatización end-to-end de los módulos de **Consultas y Reportes** del *Card Management System* (CMS) utilizado por la Red Transaccional Cooperativa. Las pruebas se implementan con **Python**, **pytest** y **Playwright**, siguen el patrón **Page Object Model (POM)** y comparten fixtures reutilizables para iniciar sesión, navegar por el menú y manipular evidencias.

La intención principal es ofrecer una base mantenible sobre la cual extender la cobertura funcional del CMS, reutilizar código entre módulos y documentar el flujo completo de ejecución.

## Características principales

- Page Objects que encapsulan la lógica de cada módulo del CMS (login, menú, CM14, CM16, CM18, CM19, CM21, CM22, CM44, CM45, CM46, CM60, CM85 y placeholders para el resto).
- Fixtures centralizadas en `conftest.py` para cargar configuración YAML, preparar credenciales, lanzar Playwright, manejar grabación de vídeo y recoger evidencias.
- Configuración por entorno (`config/qa.yaml`) y soporte para sobrescribir credenciales mediante variables de entorno o archivos `.env`.
- Estructura lista para generar reportes HTML (`pytest-html`), almacenar capturas/vídeos en `artefacts/` y consumir Allure si se desea.
- Pruebas esqueleto para servicios web (WS01 y WS02) y módulos aún no automatizados, lo que facilita planificar la cobertura futura.

## Requisitos previos

- Python 3.11 o superior.
- `pip` actualizado.
- Node.js únicamente si aún no cuentas con los navegadores de Playwright instalados (`playwright install --with-deps`).
- Acceso a las URL del CMS (por ejemplo, entorno QA) y credenciales válidas.

> ℹ️ El paquete se importa en el código como `cms_automation`. Si clonas el repositorio con otro nombre, renombra la carpeta o ajusta tu `PYTHONPATH` para que Python pueda resolver ese módulo.

## Instalación rápida

1. **Clona el proyecto** (se recomienda utilizar el nombre `cms_automation` para evitar ajustes adicionales):

   ```bash
   git clone <url-del-repositorio> cms_automation
   cd cms_automation
   ```

   En PowerShell:

   ```powershell
   git clone <url-del-repositorio> cms_automation
   Set-Location cms_automation
   ```

2. **Crea y activa un entorno virtual**.

   Bash / Linux / macOS:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   PowerShell (Windows):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Instala dependencias y navegadores de Playwright**:

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   playwright install --with-deps
   ```

   `--with-deps` instala dependencias del sistema necesarias para Chromium/Firefox/WebKit. En Windows puedes omitirlo si ya cuentas con los navegadores.

## Configuración del proyecto

### Selección de entorno y archivo YAML

- La fixture `config` lee `config/<entorno>.yaml`. Por defecto se usa `config/qa.yaml`, pero puedes definir la variable `CMS_ENV` para apuntar a otro archivo (por ejemplo `CMS_ENV=prod`).
- Cada YAML incluye la URL base, timeouts y credenciales por usuario. Crea archivos adicionales (`prod.yaml`, `staging.yaml`, etc.) siguiendo la misma estructura.
- `ignore_https_errors: true` permite ejecutar en entornos con certificados no válidos; modifícalo si tu infraestructura requiere validar TLS.

### Credenciales y variables de entorno

- Las credenciales se obtienen de `config/<entorno>.yaml` pero pueden sobrescribirse mediante variables de entorno como `ADMIN_USER` y `ADMIN_PASS`. Esta lógica está en la fixture `creds`.
- Puedes crear un archivo `.env` en la raíz para cargar automáticamente las variables:

  ```env
  ADMIN_USER=usuario_admin
  ADMIN_PASS=super-segura
  ```

  Recuerda **no versionar** archivos con credenciales reales.

### Datos de prueba

- Algunos Page Objects (por ejemplo, `CM14TrazabilidadPage`) esperan archivos de datos. El método `load_cards_from_csv` busca `tests/data/cards.csv` con una columna `card_number`.
- Crea el directorio y un CSV antes de ejecutar las pruebas:

  ```csv
  card_number
  1234567890123456
  6543210987654321
  ```

- Ajusta los valores a tarjetas válidas en tu entorno.

## Ejecución de pruebas

Ejecuta los siguientes comandos desde la raíz del proyecto con el entorno virtual activo.

- **Todas las pruebas end-to-end**:

  ```bash
  pytest tests/e2e
  ```

- **Filtrar por marcador** (marcadores definidos en `pytest.ini`):

  ```bash
  pytest -m cm14
  pytest -m "cm14 or cm45"
  ```

- **Ejecutar un archivo o prueba concreta**:

  ```bash
  pytest tests/e2e/test_cm14_trazabilidad_tarjetas.py
  pytest tests/e2e/test_cm14_trazabilidad_tarjetas.py::test_cm14_trazabilidad_tarjetas
  ```

- **Modo con interfaz y cámara lenta** (útil para depuración):

  ```bash
  pytest --headed --slowmo 300 -m cm45
  ```

- **Ejecución en paralelo** (requiere `pytest-xdist`):

  ```bash
  pytest -n auto -m "cm14 or cm60"
  ```

- **Pruebas de servicios web**: actualmente `tests/api/` contiene esqueletos que realizan `pytest.skip`. Mantén estos archivos para completar cuando los endpoints estén disponibles.

## Reportes y evidencias

- `pytest.ini` añade por defecto `--html=reports/report.html --self-contained-html`, por lo que cada corrida genera un reporte HTML independiente.
- El hook `pytest_runtest_makereport` mueve las capturas y vídeos recientes a `artefacts/` y los adjunta en el reporte. Los vídeos se guardan en `videos/` gracias a `browser_context_args`.
- Para generar reportes **Allure**:

  ```bash
  pytest --alluredir=reports/allure
  allure serve reports/allure
  ```

  Asegúrate de tener Allure instalado localmente.

## Estructura del repositorio

```
cms_automation/
├── config/                  # Archivos YAML por entorno (qa, prod, etc.)
├── docs/                    # Documentación ampliada (guías de uso y arquitectura)
├── pages/                   # Page Objects del CMS (login, menú y módulos CM)
├── tests/
│   ├── e2e/                 # Pruebas end-to-end por módulo
│   └── api/                 # Pruebas de servicios web (esqueletos)
├── utils/                   # Selectores, waits, utilidades de archivos y autenticación
├── conftest.py              # Fixtures globales y hooks de pytest
├── pytest.ini               # Marcadores y configuración de pytest
├── requirements.txt         # Dependencias Python
└── README.md                # Este documento
```

## Extender la automatización

1. **Crear/actualizar el Page Object** del módulo en `pages/`, encapsulando acciones de negocio (búsquedas, exportaciones, validaciones).
2. **Agregar la prueba** correspondiente en `tests/e2e/`, reutilizando la fixture `login` para autenticarse y `MenuPage` para navegar.
3. **Etiquetar con `@pytest.mark.cmXX`** para poder filtrar por módulo.
4. **Centralizar selectores** en `utils/selectors.py` cuando se reutilicen en varias pantallas.
5. **Actualizar la documentación** (`README.md` y `docs/`) para reflejar el nuevo alcance.

## Documentación adicional

- [`docs/usage.md`](docs/usage.md): guía paso a paso para configurar el entorno, ejecutar pruebas y revisar reportes.
- [`docs/project_doc.md`](docs/project_doc.md): descripción arquitectónica, cobertura de módulos y convenciones de desarrollo.

## Buenas prácticas

- Prioriza el uso de atributos `data-testid` al definir selectores para mejorar la resiliencia ante cambios de UI.
- Mantén los Page Objects pequeños y con responsabilidades claras; evita mezclar lógica de negocio con asserts complejos en los tests.
- Crea datos de prueba controlados (CSV, fixtures parametrizadas) y evita depender de información sensible.
- Limpia periódicamente los directorios `artefacts/`, `videos/` y `downloads/` para evitar acumular archivos pesados.

Con estas guías podrás ejecutar y extender la automatización del CMS de manera ordenada y reproducible. ¡Felices pruebas!
