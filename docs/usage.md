# Guía de uso rápido — cms_automation

Guía práctica para configurar y ejecutar las pruebas E2E en entornos
locales (incluye comandos para PowerShell/Windows).

Requisitos

- Python 3.8+
- Node.js (para Playwright) — sólo si no está ya instalado por dependencias
- Acceso a entorno QA y credenciales válidas

Instalación (Windows / PowerShell)

1. Clona el repo y entra en la carpeta del proyecto:

```powershell
git clone <repo_url>
cd cms_automation
```

2. Crear y activar entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instalar dependencias y navegadores Playwright:

```powershell
python -m pip install -r requirements.txt
playwright install --with-deps
```

4. Añadir credenciales en `.env` (opcional, recomendado):

```powershell
# Crear archivo .env con variables:
@\