# Guía de uso de la automatización CMS

Esta guía explica cómo configurar y ejecutar las pruebas end‑to‑end del
proyecto **cms_automation**. Las pruebas se basan en **pytest** y
**Playwright**, y modelan distintos módulos del Card Management System
(CMS) descritos en la guía operativa【547172095933312†L194-L241】.

## Requisitos previos

1. **Python 3.8 o superior** instalado en el sistema.
2. **Node.js y Playwright**: las dependencias se instalan automáticamente
   mediante `pip`, pero es necesario ejecutar `playwright install` una vez
   para descargar los navegadores.
3. Acceso a los entornos de CMS (QA o producción) y a credenciales de
   usuario válidas.

## Instalación

1. Clona el repositorio y entra en la carpeta `cms_automation`:
   ```bash
   git clone <repo_url>
   cd cms_automation
   ```
2. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   # Instala los navegadores de Playwright
   playwright install --with-deps
   ```
4. Configura un archivo `.env` en la raíz del proyecto para guardar
   credenciales y variables sensibles. Por ejemplo:
   ```dotenv
   ADMIN_USER=usuario_de_pruebas
   ADMIN_PASS=contraseña_secreta
   ```
5. Selecciona el entorno mediante la variable `CMS_ENV`. Por defecto
   apunta a `qa` y leerá `config/qa.yaml`. Puedes exportar la variable
   antes de ejecutar pytest:
   ```bash
   export CMS_ENV=qa
   ```

## Ejecución de pruebas

Para ejecutar **todas** las pruebas end‑to‑end:

```bash
pytest -m "not ws01 and not ws02"
```

Para ejecutar sólo las pruebas de un módulo específico, usa las marcas
definidas en cada test. Por ejemplo, para el módulo CM14:

```bash
pytest -m cm14
```

Para ejecutar las pruebas en paralelo (aprovechando varios núcleos):

```bash
pytest -n auto -m "cm14 or cm45"
```

Para generar reportes de Allure:

```bash
pytest --alluredir=reports/allure
```
Luego genera el reporte HTML con:
```bash
allure serve reports/allure
```

## Variables de entorno importantes

| Variable | Descripción | Ejemplo |
|---------|-------------|---------|
| `CMS_ENV` | Selecciona el archivo de configuración (`qa` o `prod`). | `CMS_ENV=qa` |
| `ADMIN_USER` | Usuario de acceso. Sobrescribe el valor de `config/qa.yaml`. | `ADMIN_USER=admin` |
| `ADMIN_PASS` | Contraseña de acceso. Sobrescribe el valor de `config/qa.yaml`. | `ADMIN_PASS=secret` |

Las variables se pueden definir en un archivo `.env` o exportarse
temporalmente en la terminal.

## Ejecución de pruebas de API

Las pruebas bajo `tests/api/` (`ws01` y `ws02`) son actualmente
esqueletos y están marcadas como `skip` porque los endpoints todavía no
están disponibles. Cuando existan, reemplaza el `skip` por la lógica de
llamada al servicio usando `requests` o `playwright.api_request` y
valida la respuesta.

## Consejos

* Ajusta los **selectores** en los Page Objects tan pronto como se
  identifiquen atributos `data-testid` en la interfaz. Esto hará que
  las pruebas sean más estables.
* Marca con `@pytest.mark.skip` los tests que dependan de módulos o
  funcionalidades no disponibles en tu entorno.
* Utiliza `pytest-rerunfailures` para reintentar pruebas flakey si es
  necesario; sin embargo, lo ideal es mejorar los tiempos de espera y la
  robustez de los selectores.

Con esta guía deberías poder instalar y ejecutar las pruebas de
automatización de forma local o en un servidor de integración continua.