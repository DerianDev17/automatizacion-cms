# CMS Automation Project

Este proyecto provee una estructura base para automatizar los módulos del **Card Management System (CMS)** de la Red Transaccional Cooperativa. Se utilizan **Python**, **pytest** y **Playwright** para ejecutar pruebas end‑to‑end reutilizables.

El objetivo es centralizar las automatizaciones en un único repositorio, reutilizar código entre los diferentes módulos y proporcionar una guía clara de uso. La guía operativa de CMS describe muchos módulos (CM01, CM03, CM06, CM14, CM16, CM18, CM19, CM21, CM22, CM44, CM45, CM46, CM60, CM85, etc.), cada uno de los cuales corresponde a una página o reporte dentro del sistema【547172095933312†L194-L241】. A partir de dicha guía se incluyen ejemplos de automatización de los módulos de consultas y reportes y se generan archivos de prueba esqueleto para los módulos no cubiertos.

## Estructura de carpetas

```
cms_automation/
├── README.md                # Esta descripción general del proyecto
├── requirements.txt         # Paquetes Python necesarios
├── conftest.py              # Fixtures globales para pytest
├── config/
│   ├── qa.yaml              # Configuración para entorno QA (URLs, credenciales, timeouts)
├── pages/
│   ├── login_page.py        # Page Object para la página de login
│   ├── menu_page.py         # Page Object para la navegación por el menú
│   ├── cm14_trazabilidad_page.py
│   ├── cm44_reimpresion_page.py
│   ├── cm45_consulta_page.py
│   ├── cm16_cuenta_page.py
│   ├── cm18_opcion_page.py
│   ├── cm19_historial_page.py
│   ├── cm21_clave_page.py
│   ├── cm22_procesos_page.py
│   ├── cm46_lotes_pendientes_page.py
│   ├── cm60_canceladas_page.py
│   ├── cm85_emitidas_page.py
│   └── placeholders.py      # Clases placeholder para otros CM descritos en la guía
├── tests/
│   ├── e2e/
│   │   ├── __init__.py
│   │   ├── test_cm14_trazabilidad.py
│   │   ├── test_cm44_reimpresion.py
│   │   ├── test_cm45_consulta.py
│   │   ├── test_cm16_cuenta.py
│   │   ├── test_cm18_opcion.py
│   │   ├── test_cm19_historial.py
│   │   ├── test_cm21_clave.py
│   │   ├── test_cm22_procesos.py
│   │   ├── test_cm46_lotes_pendientes.py
│   │   ├── test_cm60_canceladas.py
│   │   ├── test_cm85_emitidas.py
│   │   └── test_placeholders.py     # Pruebas esqueleto para otros CM
│   └── api/
│       ├── __init__.py
│       ├── test_ws01_movimientos_switch.py
│       └── test_ws02_consulta_transacciones.py
├── utils/
│   ├── __init__.py
│   ├── selectors.py         # Selectores centralizados (data-testids, labels)
│   ├── waits.py             # Funciones de espera robustas
│   ├── files.py             # Gestión de descargas y archivos exportados
│   └── auth.py              # Ayudas para login y refresco de sesión
├── docs/
│   ├── usage.md             # Instrucciones para ejecutar las pruebas
│   └── project_doc.md       # Documentación detallada del proyecto y de los módulos
└── fixtures/
    └── __init__.py         # Lugar para generadores de datos reutilizables

```

## Conceptos clave

### Page Object Model (POM)

Las automatizaciones se basan en el patrón **Page Object Model**. Cada archivo en `pages/` encapsula las interacciones de una pantalla o módulo CMS. Esto permite reutilizar código y abstraer la lógica de UI:

```python
from playwright.sync_api import Page, expect

class CM14TrazabilidadPage:
    """Modela la pantalla CM14 – Trazabilidad de Tarjetas."""

    def __init__(self, page: Page):
        self.page = page

    def open_from_menu(self, menu_page):
        """Navega al módulo a través del menú principal."""
        menu_page.open_cm14()

    def buscar_tarjeta(self, numero: str):
        # Implementación de búsqueda: rellenar campo, pulsar buscar, esperar tabla
        pass

    def validar_resultados(self, min_rows: int = 1):
        # Validar que la tabla de resultados tenga al menos `min_rows` filas
        pass
```

### Fixtures globales

El archivo `conftest.py` define fixtures para inicializar el navegador, cargar configuración y gestionar el inicio de sesión. Estas fixtures están disponibles en todas las pruebas sin necesidad de importarlas explícitamente.

### Archivos de configuración

Se proveen ejemplos de archivos YAML en `config/` para separar las URLs, credenciales y timeouts según el entorno (QA, producción, etc.). Para datos sensibles se utiliza un archivo `.env` (no incluido en el repositorio) que se carga mediante [`dotenv`](https://github.com/theskumar/python-dotenv).

### Selección de suites

Las pruebas se etiquetan con marcas `pytest` como `@pytest.mark.cm14`, `@pytest.mark.regression` o `@pytest.mark.sanity`. De esta forma puedes ejecutar subconjuntos de pruebas:

```bash
pytest -m "cm14 and regression"
```

### Módulos cubiertos

En esta versión se han incluido automatizaciones base para los siguientes módulos de consultas y reportes descritos en la guía operativa【547172095933312†L194-L241】:

| Módulo | Descripción (según guía) | Archivo de prueba |
|-------|---------------------------|-------------------|
| **CM14** | Trazabilidad de Tarjetas | `tests/e2e/test_cm14_trazabilidad.py` |
| **CM44** | Reimpresión de Solicitudes | `tests/e2e/test_cm44_reimpresion.py` |
| **CM45** | Consulta de Tarjetas | `tests/e2e/test_cm45_consulta.py` |
| **CM18** | Tarjetas Por Opción | `tests/e2e/test_cm18_opcion.py` |
| **CM87** | Historia de Tarjetas por Oficina | Prueba esqueleto en `test_placeholders.py` |
| **CM19** | Historial de Tarjetas | `tests/e2e/test_cm19_historial.py` |
| **CMA4** | Tarjetas Emitidas por Producto | Prueba esqueleto |
| **CM85** | Reporte de Tarjetas Emitidas | `tests/e2e/test_cm85_emitidas.py` |
| **CM16** | Tarjeta por Cuenta | `tests/e2e/test_cm16_cuenta.py` |
| **CM21** | Consulta de Clave | `tests/e2e/test_cm21_clave.py` |
| **CM88** | Reporte de tarjetas Anuladas, Suspendidas, Bloqueadas | Prueba esqueleto |
| **CM60** | Tarjetas Canceladas | `tests/e2e/test_cm60_canceladas.py` |
| **CM17** | Reporte de Costos | Prueba esqueleto |
| **CM22** | Reporte de Tarjetas por Procesos | `tests/e2e/test_cm22_procesos.py` |
| **CM89** | Reporte de Tarjetas por Vencer | Prueba esqueleto |
| **CM97** | Reporte de Tarjetas por BIN | Prueba esqueleto |
| **CM46** | Reporte de Lotes Pendientes | `tests/e2e/test_cm46_lotes_pendientes.py` |
| **MD16** | Reporte de autorización de transacciones | Prueba esqueleto |

Para los módulos sin prueba implementada se provee una clase placeholder en `pages/placeholders.py` y un test esqueleto en `tests/e2e/test_placeholders.py` con instrucciones de cómo completarlo.

## Próximos pasos y mejoras

* **Completar los Page Objects**: Para cada módulo placeholder se deben implementar métodos concretos según los campos y acciones de la interfaz.
* **Agregar validaciones específicas**: Las pruebas esqueleto solo contienen la estructura básica; es necesario añadir verificaciones de resultados, exportación de archivos y aserciones según los requisitos de cada reporte.
* **Configurar CI/CD**: Integrar este proyecto en un pipeline (GitLab CI, Jenkins, GitHub Actions, etc.) para ejecutar las pruebas automáticamente en cada commit o de manera programada.
* **Datos de prueba**: Crear fixtures con datos sintéticos para cubrir distintos escenarios (tarjetas existentes, inexistentes, fechas fuera de rango, etc.).

Para más detalles sobre la ejecución y configuración consulta el archivo [`docs/usage.md`](docs/usage.md).