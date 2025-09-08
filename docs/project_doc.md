# Documentación del proyecto cms_automation

Este documento resume el estado del proyecto y las guías rápidas para
extender y mantener las automatizaciones centradas en Consultas y
Reportes del CMS.

Estado de módulos (resumen)

Implementados

- CM14 — Trazabilidad (`pages/cm14_trazabilidad_page.py`, `tests/e2e/test_cm14_trazabilidad.py`)
- CM16 — Tarjeta por Cuenta
- CM18 — Tarjetas por Opción

Pendientes / Placeholders

- CM17, CM87, CM88, CM89, CM97, CMA4, MD16 — hay clases placeholder en `pages/placeholders.py` y tests esqueleto en `tests/e2e/test_placeholders.py`.

Diseño y buenas prácticas

- Page Object Model (POM): cada archivo en `pages/` debe exponer acciones de alto nivel (abrir, buscar, exportar, validar).
- Fixtures: `conftest.py` expone `config`, `browser/context/page` y `login`.
- Selectores: centralizar selectores reutilizables en `utils/selectors.py`.

Contrato mínimo de un Page Object

- Inputs: `page` (Playwright) y parámetros de negocio (número de tarjeta, rango de fechas).
- Outputs: resultados visibles (tabla) y/o archivos generados.
- Errores: lanzar excepción clara cuando la página no carga o faltan elementos.

Cómo extender el proyecto (pasos rápidos)

1. Crear o completar un Page Object en `pages/`. Mantén métodos pequeños y descriptivos.
2. Añadir un test en `tests/e2e/` que use la fixture `login` para autenticarse y navegar.
3. Marcar el test con `@pytest.mark.cmXX` y validar localmente.
4. Agregar selectores compartidos a `utils/selectors.py` si aplican.

Notas

- Prioriza el uso de `data-testid` en la aplicación para selectores estables.
- Mantén la documentación actualizada al completar módulos.
- Para cambios mayores (por ejemplo, reorganizar `pages/`), actualiza este archivo y `README.md`.
# Documentación del proyecto de automatización CMS

## Introducción

El proyecto **cms_automation** surgió con el objetivo de consolidar y
reutilizar las automatizaciones de los distintos módulos del *Card Management
System* (CMS) de la Red Transaccional Cooperativa. El manual operativo
describe numerosos módulos con funciones de parametrización, ciclo de
tarjeta, mantenimiento, tarjetas innominadas y reportes【547172095933312†L194-L241】.
En particular, esta automatización se centra en los módulos de **Consultas
y Reportes** (sección 9 del manual).

## Lista de módulos de consultas y reportes

La siguiente tabla resume los módulos listados en la sección 9 del manual
operativo【547172095933312†L194-L241】, indica si ya existe una automatización
en este proyecto y enlaza la clase correspondiente en `pages/`:

| Módulo | Descripción breve | Estado de automatización | Clase / Prueba |
|-------|--------------------|---------------------------|---------------|
| **CM14** | Trazabilidad de Tarjetas | Implementado | `CM14TrazabilidadPage` / `test_cm14_trazabilidad.py` |
| **CM44** | Reimpresión de Solicitudes | Implementado | `CM44ReimpresionPage` / `test_cm44_reimpresion.py` |
| **CM45** | Consulta de Tarjetas | Implementado | `CM45ConsultaPage` / `test_cm45_consulta.py` |
| **CM18** | Tarjetas por Opción | Implementado | `CM18OpcionPage` / `test_cm18_opcion.py` |
| **CM87** | Historia de Tarjetas por Oficina | Pendiente | Clase placeholder `CM87HistoriaOficinaPage` |
| **CM19** | Historial de Tarjetas | Implementado | `CM19HistorialPage` / `test_cm19_historial.py` |
| **CMA4** | Tarjetas Emitidas por Producto | Pendiente | Clase placeholder `CMA4EmitidasProductoPage` |
| **CM85** | Reporte de Tarjetas Emitidas | Implementado | `CM85EmitidasPage` / `test_cm85_emitidas.py` |
| **CM16** | Tarjeta por Cuenta | Implementado | `CM16CuentaPage` / `test_cm16_cuenta.py` |
| **CM21** | Consulta de Clave | Implementado | `CM21ClavePage` / `test_cm21_clave.py` |
| **CM88** | Reporte de tarjetas Anuladas, Suspendidas, Bloqueadas | Pendiente | Clase placeholder `CM88AnuladasSuspendidasPage` |
| **CM60** | Tarjetas Canceladas | Implementado | `CM60CanceladasPage` / `test_cm60_canceladas.py` |
| **CM17** | Reporte de Costos | Pendiente | Clase placeholder `CM17CostosPage` |
| **CM22** | Reporte de Tarjetas por Procesos | Implementado | `CM22ProcesosPage` / `test_cm22_procesos.py` |
| **CM89** | Reporte de Tarjetas por Vencer | Pendiente | Clase placeholder `CM89VencerPage` |
| **CM97** | Reporte de Tarjetas por BIN | Pendiente | Clase placeholder `CM97BinPage` |
| **CM46** | Reporte de Lotes Pendientes | Implementado | `CM46LotesPendientesPage` / `test_cm46_lotes_pendientes.py` |
| **MD16** | Reporte de autorización de transacciones | Pendiente | Clase placeholder `MD16AutorizacionesPage` |

Los módulos marcados como *pendiente* están representados por clases
placeholder que heredan de `BasePlaceholderPage`. Estos placeholders
permiten navegar al módulo correspondiente pero lanzan un
`NotImplementedError` en su método `not_implemented()`, recordando que
falta la automatización.

## Diseño y reutilización de código

### Patrón Page Object

Cada pantalla del CMS se modela como una clase en la carpeta `pages/`. Los
métodos de estas clases encapsulan acciones de alto nivel (abrir la página,
realizar búsquedas, seleccionar opciones, generar reportes, etc.), de forma
que las pruebas (`tests/e2e/`) solo llaman a estos métodos y realizan
aserciones. Este patrón tiene varias ventajas:

* **Reutilización**: Los mismos métodos se pueden utilizar en distintas
  pruebas o flujos, evitando duplicación.
* **Mantenibilidad**: Si cambia la interfaz (nombres de campos o botones),
  únicamente se actualiza la clase Page Object.
* **Legibilidad**: Los tests se leen como pasos de negocio en lugar de
  secuencias de clicks y waits.

### Fixtures compartidas

El archivo `conftest.py` define fixtures de alto nivel:

* `config`: lee parámetros desde `config/<entorno>.yaml` dependiendo de la
  variable `CMS_ENV`.
* `creds`: combina las credenciales definidas en YAML con las variables de
  entorno cargadas a partir de `.env`.
* `browser`/`context`/`page`: inicializan Playwright de forma aislada para
  cada prueba.
* `login`: realiza el proceso de autenticación y devuelve un `MenuPage`.

Estas fixtures evitan repetir la misma lógica en cada test y facilitan el
cambio de configuración (por ejemplo, poder ejecutar las pruebas tanto en
QA como en producción sin modificar el código).

### Selectores centralizados

El módulo `utils/selectors.py` es el lugar para definir selectores CSS,
XPath o `data-testid`. Actualmente contiene ejemplos, pero se recomienda
convenir con el equipo de desarrollo del CMS la inclusión de atributos
`data-testid` en los elementos clave de la interfaz. De esta forma, los
selectores serán más robustos y no dependerán de textos visibles que
pueden cambiar.

### Utilidades genéricas

Además de selectores, el paquete `utils/` contiene funciones que pueden
reutilizarse en distintos contextos:

* `waits.py`: funciones de espera personalizadas como `wait_for_spinner` o
  `wait_for_download` para sincronizar la interacción con la UI.
* `files.py`: gestiona la descarga y almacenamiento de archivos
  generados por los reportes (Excel, PDF).
* `auth.py`: incluye marcadores para futuras extensiones como refresco de
  sesión vía API.

### Esqueletos de API

Las pruebas bajo `tests/api/` están pensadas para validar los servicios
web (WS) que interactúan con el CMS. Actualmente las pruebas WS01 y
WS02 están marcadas como pendientes (`pytest.skip`) porque los
endpoints todavía no están disponibles. Cuando se publiquen, se podrán
implementar utilizando bibliotecas como `requests` o la API de
Playwright `api_request`.

## Cómo extender el proyecto

1. **Crear un nuevo Page Object** en `pages/` para el módulo que quieras
   automatizar. Usa como plantilla una de las clases existentes y
   define métodos descriptivos según las acciones de la pantalla.
2. **Crear una prueba** en `tests/e2e/` importando la clase del paso 1.
   Usa la fixture `login` para autenticación y el menú para navegar.
   Añade marcas `pytest.mark.cmXX` para filtrar la ejecución.
3. **Actualizar la documentación** en este archivo y en `README.md` para
   reflejar el nuevo módulo.
4. **Ajustar selectores y timeouts**: cuando la aplicación esté disponible,
   reemplaza los selectores genéricos por `data-testid`. Ajusta los
   timeouts en `waits.py` según la velocidad de respuesta de la
   aplicación.

## Créditos y referencias

La estructura y cobertura de este proyecto se basan en la **Guía
Operativa CMS** (julio de 2021), documento que describe las funciones de
cada módulo【547172095933312†L194-L241】. La idea es ofrecer una base sobre la cual
ampliar la automatización de forma sostenible, facilitando la adopción de
buenas prácticas como el uso de Page Objects, configuración externa y
documentación clara.