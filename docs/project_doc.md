# Documentación del proyecto `cms_automation`

Este documento ofrece una visión detallada de la arquitectura, los módulos cubiertos y las convenciones de desarrollo del repositorio de automatización del Card Management System (CMS).

## 1. Resumen general

- **Tecnologías principales**: Python 3.11+, pytest, Playwright, pytest-html, pytest-xdist.
- **Patrón**: Page Object Model (POM) para encapsular la lógica de cada módulo del CMS y facilitar la reutilización de código.
- **Alcance actual**: automatización de los módulos de la sección de Consultas y Reportes del CMS y esqueletos para los servicios web WS01 y WS02.
- **Objetivo**: centralizar la automatización en un único repositorio, simplificar la ejecución de pruebas y proporcionar documentación operativa clara.

## 2. Arquitectura de la solución

### 2.1 Capas principales

| Capa | Elementos clave | Descripción |
|------|-----------------|-------------|
| Configuración | `config/<entorno>.yaml`, variables de entorno, `.env` | Define URLs, timeouts y usuarios por entorno. `CMS_ENV` selecciona el archivo YAML. |
| Fixtures | `conftest.py` | Gestiona la carga de configuración, credenciales, inicialización de Playwright, videos y evidencia. |
| Page Objects | `pages/*.py` | Modelan pantallas del CMS y encapsulan acciones de negocio (búsquedas, exportes, validaciones). |
| Tests | `tests/e2e`, `tests/api` | Casos end-to-end por módulo y esqueletos para servicios web. |
| Utilidades | `utils/` | Selectores, waits personalizados, helpers de archivos y marcadores para autenticación avanzada. |
| Documentación | `README.md`, `docs/` | Manual de uso y guías de arquitectura para mantener la información del proyecto. |

### 2.2 Flujo típico de una prueba E2E

1. `pytest` inicia y carga las fixtures definidas en `conftest.py`.
2. `config()` lee `config/<entorno>.yaml` y devuelve un diccionario con parámetros de entorno.
3. `creds()` combina las credenciales del YAML con las variables de entorno (prioridad para estas últimas) y expone un mapa por rol.
4. `browser_type_launch_args` y `browser_context_args` ajustan Playwright para ignorar errores HTTPS, grabar vídeo y almacenar evidencias.
5. La fixture `page` abre una nueva pestaña, la proporciona al test y captura automáticamente un screenshot al finalizar.
6. La fixture `login` utiliza `LoginPage` y `MenuPage` para autenticarse y devolver un objeto de menú listo para navegar.
7. El test usa el Page Object correspondiente para ejecutar acciones concretas del módulo y validar resultados.
8. Tras cada prueba, `pytest_runtest_makereport` mueve capturas/vídeos recientes al directorio `artefacts/` y los adjunta en el reporte HTML.

## 3. Cobertura de módulos

La siguiente tabla resume el estado de automatización de los módulos de Consultas y Reportes, indicando la clase principal y el archivo de prueba asociado.

| Módulo | Descripción | Estado | Page Object | Prueba |
|--------|-------------|--------|-------------|--------|
| CM14 | Trazabilidad de Tarjetas | Implementado | `CM14TrazabilidadPage` (`pages/cm14_trazabilidad_page.py`) | `tests/e2e/test_cm14_trazabilidad_tarjetas.py` |
| CM16 | Tarjeta por Cuenta | Implementado | `CM16CuentaPage` (`pages/cm16_cuenta_page.py`) | `tests/e2e/test_cm16_tarjetas_por_cuentas.py` |
| CM18 | Tarjetas por Opción | Implementado | `CM18OpcionPage` (`pages/cm18_opcion_page.py`) | `tests/e2e/test_cm18_reporte_tarjetas_por_opcion.py` |
| CM19 | Historial de Tarjetas | Implementado | `CM19HistorialPage` (`pages/cm19_historial_page.py`) | `tests/e2e/test_cm19_historial_tarjetas_debito.py` |
| CM21 | Consulta de Clave | Implementado | `CM21ClavePage` (`pages/cm21_clave_page.py`) | `tests/e2e/test_cm21_reporte_consultas_clave.py` |
| CM22 | Reporte de Tarjetas por Procesos | Implementado | `CM22ProcesosPage` (`pages/cm22_procesos_page.py`) | `tests/e2e/test_cm22_reporte_tarjetas_por_procesos.py` |
| CM44 | Reimpresión de Solicitudes | Implementado | `CM44ReimpresionPage` (`pages/cm44_reimpresion_page.py`) | `tests/e2e/test_cm44_reimpresion_documentos.py` |
| CM45 | Consulta de Tarjetas | Implementado | `CM45ConsultaPage` (`pages/cm45_consulta_page.py`) | `tests/e2e/test_cm45_personal.py` |
| CM46 | Reporte de Lotes Pendientes | Implementado | `CM46LotesPendientesPage` (`pages/cm46_lotes_pendientes_page.py`) | `tests/e2e/test_cm46_reporte_lotes_pendientes.py` |
| CM60 | Tarjetas Canceladas | Implementado | `CM60CanceladasPage` (`pages/cm60_canceladas_page.py`) | `tests/e2e/test_cm60_reporte_tarjetas_canceladas.py` |
| CM85 | Reporte de Tarjetas Emitidas | Implementado | `CM85EmitidasPage` (`pages/cm85_emitidas_page.py`) | `tests/e2e/test_cm85_reporte_tarjetas_emitidas.py` |
| Placeholders | CM17, CM87, CMA4, CM88, CM89, CM97, MD16 | Pendiente | Clases en `pages/placeholders.py` | `tests/e2e/test_placeholders.py` |
| WS01 / WS02 | Servicios web del switch | Pendiente | No aplica | `tests/api/test_ws01_movimientos_switch.py`, `tests/api/test_ws02_consulta_transacciones.py`, `tests/api/test_ws02_consulta_transacciones_switch.py` |

> Los módulos marcados como *pendiente* disponen de clases placeholder que abren el módulo desde el menú y lanzan `NotImplementedError` para recordar que falta la automatización.

## 4. Componentes clave

### 4.1 Page Objects y navegación

- `LoginPage`: encapsula la navegación a la pantalla de login y la autenticación.
- `MenuPage`: provee métodos `open_cmXX` para abrir cada módulo desde el buscador del menú principal. Internamente usa `_open_menu_item` y espera el `iframe` correspondiente.
- Cada Page Object implementa métodos de interacción específicos (por ejemplo, `CM14TrazabilidadPage.run_all_from_csv` procesa tarjetas desde un CSV y captura reportes).
- Los placeholders (`pages/placeholders.py`) comparten la lógica base `BasePlaceholderPage` que abre el módulo y lanza `NotImplementedError`.

### 4.2 Fixtures y hooks relevantes

- `config` (scope `session`): carga YAML según `CMS_ENV`.
- `creds` (scope `session`): combina credenciales del YAML con variables de entorno, utilizando `python-dotenv`.
- `browser_type_launch_args`: añade `--ignore-certificate-errors` a Chromium/Chrome.
- `browser_context_args`: habilita `ignore_https_errors`, crea el directorio `videos/` y graba cada prueba.
- `page`: abre una nueva pestaña, la entrega al test y toma un screenshot automático.
- `login`: retorna una función que realiza el login y entrega un `MenuPage` listo para navegar.
- `pytest_runtest_makereport`: mueve capturas/vídeos recientes a `artefacts/` y los adjunta en el reporte HTML utilizando `pytest-html`.

### 4.3 Utilidades (`utils/`)

- `selectors.py`: centraliza selectores CSS/XPath. Contiene ejemplos listos para ser sustituidos por `data-testid` en cuanto estén disponibles.
- `waits.py`: helpers para esperar spinners (`wait_for_spinner`) o descargas (`wait_for_download`).
- `files.py`: función `save_download` para almacenar archivos descargados con Playwright.
- `auth.py`: marcador para futuras extensiones de autenticación (renovación de sesión vía API).

### 4.4 Estructura de datos y evidencias

- `tests/data/`: carpeta sugerida para almacenar CSV u otros archivos de datos. No existe por defecto; créala según tus necesidades.
- `artefacts/`: destino final de capturas y vídeos relevantes por prueba.
- `videos/`: carpeta temporal donde Playwright guarda los vídeos antes de ser movidos a `artefacts/`.
- `reports/`: salida de `pytest-html` (por defecto `report.html`). También puede albergar reportes Allure (`reports/allure`).

## 5. Extensión y mantenimiento

### 5.1 Añadir un nuevo módulo del CMS

1. Crea el Page Object en `pages/` siguiendo el patrón de los módulos existentes.
2. Implementa la navegación desde `MenuPage` si aún no existe un método `open_cmXX` para el nuevo módulo.
3. Añade la prueba correspondiente en `tests/e2e/`, utilizando la fixture `login` y el nuevo Page Object.
4. Define un marcador en `pytest.ini` (`cmXX`) para facilitar la ejecución selectiva.
5. Documenta el nuevo módulo en este archivo y en el README.

### 5.2 Implementar un placeholder pendiente

1. Actualiza la clase en `pages/placeholders.py` reemplazando la herencia de `BasePlaceholderPage` por un Page Object real.
2. Completa la prueba específica en `tests/e2e/` y elimina la entrada correspondiente del `parametrize` en `test_placeholders.py`.
3. Asegúrate de retirar la expectativa `NotImplementedError` y de añadir asserts reales.

### 5.3 Pruebas de servicios web

- Reutiliza `pytest` puro para WS01/WS02. Cuando los endpoints estén disponibles, utiliza `requests` o `playwright.sync_api.APIRequestContext`.
- Define fixtures para tokens, cabeceras o payloads reutilizables.
- Considera validar contratos con bibliotecas como `pydantic` o `jsonschema`.

### 5.4 Buenas prácticas de mantenimiento

- Mantén los selectores en un único lugar (`selectors.py`) y anota en comentarios cuándo fue la última validación en producción/QA.
- Documenta cualquier workaround temporal directamente en el Page Object con TODOs claros.
- Revisa y limpia periódicamente los directorios `artefacts/`, `videos/` y `downloads/` para evitar que crezcan sin control.
- Ejecuta `pytest` en local antes de subir cambios y, si es posible, integra la suite en un pipeline de CI (GitHub Actions, Jenkins, etc.).

## 6. Referencias cruzadas

- [`README.md`](../README.md): resumen general y pasos rápidos de instalación.
- [`docs/usage.md`](usage.md): instrucciones operativas detalladas para ejecutar la suite.
- Código fuente de Page Objects y pruebas (`pages/`, `tests/`) para ejemplos concretos de implementación.

Mantener esta documentación actualizada cada vez que se incorpora un nuevo módulo o se modifica un flujo es clave para conservar la trazabilidad del proyecto y facilitar la incorporación de nuevos miembros al equipo.
