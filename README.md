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
# CMS Automation (cms_automation)

Repositorio con las automatizaciones end-to-end para los módulos de Consultas y Reportes del Card Management System (CMS).

Resumen rápido
- Lenguajes y herramientas: Python, pytest, Playwright.
- Objetivo: pruebas E2E mantenibles usando Page Objects y fixtures reutilizables.

Estructura relevante

- `config/` — archivos YAML por entorno (`qa.yaml` por defecto).
- `pages/` — Page Objects que encapsulan interacciones UI.
- `tests/e2e/` — pruebas end-to-end por módulo.
- `tests/api/` — pruebas de servicios web (esqueletos actualmente).
- `utils/` — utilidades (selectores, waits, archivos, auth).
- `docs/` — documentación del proyecto (esta carpeta).

Principales puntos

- Pattern: Page Object Model (POM) — cada `pages/*` expone acciones de alto nivel.
- Fixtures globales en `conftest.py` para inicializar Playwright, cargar configuración y manejar login.
- Selectores centralizados en `utils/selectors.py` para facilitar mantenimiento.

Instalación (Windows / PowerShell)

1. Crear y activar un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependencias:

```powershell
python -m pip install -r requirements.txt
# Instalar navegadores de Playwright (si no está instalado como dependencia directa):
playwright install --with-deps
```

3. Configurar credenciales y entorno: crear un archivo `.env` en la raíz con variables como `ADMIN_USER`, `ADMIN_PASS` y opcionalmente exportar `CMS_ENV=qa`.

Ejecución de pruebas (PowerShell)

- Ejecutar todas las pruebas E2E:

```powershell
pytest -m "not ws01 and not ws02"
```

- Ejecutar pruebas marcadas (ej. CM14):

```powershell
pytest -m cm14
```

- Ejecutar en paralelo (pytest-xdist):

```powershell
pytest -n auto -m "cm14 or cm45"
```

Reportes Allure (si está configurado)

```powershell
pytest --alluredir=reports/allure
# Luego, en Windows puedes servir el reporte si tienes Allure instalado:
allure serve reports/allure
```

Buenas prácticas y notas

- Prioriza `data-testid` para selectores cuando sea posible.
- Mantén Page Objects pequeños y con responsabilidades claras.
- Usa fixtures para datos de prueba y limpieza de entorno.

Documentación adicional
- `docs/usage.md` — guía de instalación y ejecución.
- `docs/project_doc.md` — detalles sobre módulos y diseño.

Si quieres, puedo también:
- añadir un ejemplo de test minimal ejecutable (fixture + una prueba que abre la página de login).
- preparar un pipeline básico de GitHub Actions para ejecutar las pruebas.