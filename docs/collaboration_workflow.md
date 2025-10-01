# Guía de colaboración y versionado

Este documento describe el flujo de trabajo recomendado para colaborar en el proyecto `cms_automation`, desde la planificación del cambio hasta el despliegue y la posible reversión. Se asume el uso de Git y GitHub como repositorio remoto.

## 1. Resumen rápido (para copiar y pegar)

Si necesitas un recordatorio exprés de los comandos más usados, sigue esta tabla.
Cada fila contiene lo que debes hacer, el comando listo para copiar y una breve explicación.

| Acción | Comando para copiar | ¿Qué hace? |
| --- | --- | --- |
| Traer el proyecto por primera vez | `git clone git@github.com:tu-organizacion/automatizacion-cms.git`<br>`cd automatizacion-cms` | Descarga el repositorio y entra a la carpeta. |
| Asegurarte de tener la versión más reciente | `git checkout main`<br>`git pull origin main` | Cambia a la rama principal y descarga los cambios del servidor. |
| Crear tu rama de trabajo | `git checkout -b feature/cmXX-nombre-corto` | Crea una copia de trabajo con un nombre descriptivo. |
| Revisar qué archivos cambiaste | `git status` | Muestra archivos modificados o nuevos. |
| Guardar cambios en un commit | `git add <archivo>`<br>`git commit -m "mensaje"` | Prepara los archivos y guarda un punto de control con un mensaje. |
| Enviar tu rama al servidor | `git push -u origin feature/cmXX-nombre-corto` | Sube tu trabajo para que el equipo lo vea. |
| Traer cambios recientes de otros | `git fetch origin`<br>`git rebase origin/main` | Mezcla tus cambios con lo último del equipo. |
| Revertir un commit | `git revert <hash>` | Crea un commit que deshace los cambios del hash indicado. |

> Consejo: si no sabes qué significa un término (por ejemplo, "rama"), consulta el glosario al final del documento.

## 2. Preparación del entorno local

1. Clona el repositorio si aún no lo tienes. Copia y pega ambos comandos en tu terminal:
   ```bash
   git clone git@github.com:tu-organizacion/automatizacion-cms.git
   cd automatizacion-cms
   ```
   - `git clone` trae el código del repositorio remoto a tu computadora.
   - `cd automatizacion-cms` te mueve a la carpeta descargada para que los siguientes comandos funcionen.
2. Instala las dependencias del proyecto siguiendo la [guía de uso](usage.md). Esto asegura que puedas ejecutar pruebas y scripts sin errores.
3. Configura tu identidad de Git (sólo una vez por computadora):
   ```bash
   git config user.name "Tu Nombre"
   git config user.email "tu.email@empresa.com"
   ```
   - Estos datos aparecen en los commits y ayudan a identificar quién hizo cada cambio.

## 3. Planificación del cambio

1. Revisa los issues o historias de usuario asignados.
2. Define el alcance del cambio y los impactos en pruebas o documentación.
3. Asegúrate de tener claridad sobre el criterio de aceptación y la evidencia requerida.

## 4. Crear una rama de trabajo

1. Actualiza la rama principal (main). Ejecuta los dos comandos en orden:
   ```bash
   git checkout main
   git pull origin main
   ```
   - `git checkout main` cambia a la rama principal.
   - `git pull origin main` descarga los últimos cambios del servidor.
2. Crea una rama descriptiva basada en el formato `feature/`, `bugfix/` o `docs/` según corresponda:
   ```bash
   git checkout -b feature/cmXX-nombre-corto
   ```
   - Piensa en la rama como un "carril" separado para tu tarea. El nombre debe reflejar el objetivo (por ejemplo, `feature/cm45-formulario-contacto`).

## 5. Desarrollo y commits

1. Realiza los cambios de código o documentación necesarios.
2. Ejecuta las pruebas locales relevantes (`pytest`, linters, etc.) para verificar que nada se rompa.
3. Revisa el estado del repositorio:
   ```bash
   git status
   ```
   - Git te dirá qué archivos cambiaste y si están listos para ser guardados.
4. Agrupa los cambios por contexto y crea commits atómicos con mensajes claros en español o inglés:
   ```bash
   git add docs/collaboration_workflow.md
   git commit -m "docs: documentar flujo de colaboración"
   ```
   - `git add` marca los archivos que quieres guardar en el próximo commit. Puedes usar `.` para agregar todos, pero es mejor listar sólo los necesarios.
   - `git commit -m` guarda un punto de control. El mensaje debe explicar qué cambiaste (ejemplo: `feat: agregar validación de email`).
5. Si necesitas reescribir la historia antes de publicar, utiliza `git commit --amend` o `git rebase -i HEAD~n`. Hazlo sólo antes de compartir tu rama para no afectar al equipo.
6. ¿Te equivocaste en un archivo? Puedes volver al último guardado usando `git checkout -- <archivo>`. Esto descarta los cambios sin confirmar.

## 6. Sincronización con el remoto

1. Asegúrate de que tu rama local esté actualizada con la rama principal:
   ```bash
   git fetch origin
   git rebase origin/main
   ```
   - `git fetch origin` trae información nueva del servidor sin mezclarla todavía.
   - `git rebase origin/main` inserta tus commits encima de la versión más reciente de `main`.
   - Si hay conflictos, Git te lo dirá. Abre los archivos marcados, quédate con la versión correcta y ejecuta `git add <archivo>` seguido de `git rebase --continue`.
2. Publica la rama en el remoto:
   ```bash
   git push -u origin feature/cmXX-nombre-corto
   ```
   - Con `-u` Git recordará la rama remota y más adelante bastará con `git push`.
3. Si quieres actualizar tu PR después de hacer más cambios, repite los pasos 1 y 2 y Git actualizará la rama remota con los nuevos commits.

## 7. Solicitud de Pull Request

1. Abre un Pull Request (PR) en GitHub apuntando a `main`.
2. Completa la plantilla del PR con:
   - Resumen del cambio.
   - Pasos de prueba ejecutados y evidencia.
   - Riesgos o dependencias.
3. Pide revisión a otro miembro del equipo y atiende los comentarios realizando commits adicionales en la misma rama.

## 8. Aprobación y merge

1. Una vez aprobado el PR y con los checks en verde, realiza el merge preferentemente con `Squash and merge` o `Rebase and merge` según la política del equipo.
2. Asegúrate de eliminar la rama remota tras el merge para mantener el repositorio limpio (`Delete branch`).
3. Sincroniza la rama principal localmente:
   ```bash
   git checkout main
   git pull origin main
   ```

## 9. Versionado

1. Identifica si el cambio amerita una nueva versión (por ejemplo, `v1.2.0`). Si es un ajuste menor, quizá sólo debas actualizar la documentación.
2. Actualiza el historial de versiones o `CHANGELOG.md` si existe para dejar constancia de lo incluido.
3. Crea y publica una etiqueta anotada (tag):
   ```bash
   git tag -a v1.2.0 -m "Release v1.2.0"
   git push origin v1.2.0
   ```
   - El tag sirve como un "marcador" de la versión actual. Usa nombres semánticos (`vMayor.Menor.Parche`).
4. Si se utiliza GitHub Releases, genera la nota de versión enlazando los PR incluidos y la evidencia relevante.

## 10. Rollback (reversión)

### 10.1 Revertir un commit o PR específico

1. Identifica el hash del commit a revertir (`git log --oneline`). El hash es un código corto como `a1b2c3d`.
2. Crea un nuevo commit de reversión:
   ```bash
   git revert <hash>
   ```
   - Este comando crea automáticamente un commit que deshace los cambios del hash indicado.
3. Resuelve posibles conflictos, guarda y cierra el editor.
4. Ejecuta las pruebas necesarias para asegurar que la reversión no introduce regresiones.
5. Publica el commit y abre un PR con la reversión explicando el motivo y el impacto.

### 10.2 Rollback de una versión etiquetada

1. Si ya se publicó una etiqueta y se necesita volver a la versión anterior:
   ```bash
   git checkout main
   git revert --no-commit <hash_del_ultimo_merge>
   git commit -m "revert: volver a estado previo a v1.2.0"
   git push origin main
   ```
   - `--no-commit` te permite revisar los cambios antes de guardarlos. Si todo luce bien, crea el commit con el mensaje sugerido.
2. Crea una nueva etiqueta que represente el rollback (por ejemplo, `v1.1.1`) y publícala para dejar rastro de la corrección.

### 10.3 Rollback emergente en producción

1. Comunica al equipo el problema detectado y el alcance del rollback. Usa los canales de alerta acordados (chat, llamada, etc.).
2. Identifica el último estado estable (tag o commit). Normalmente será la versión anterior o el último despliegue exitoso.
3. Implementa el revert en una rama temporal (por ejemplo, `hotfix/rollback-2023-10-05`) y solicita aprobación rápida.
4. Despliega el commit revertido y documenta la causa raíz y las acciones preventivas.
5. Actualiza los tableros o issues relacionados para dejar registro del incidente.

## 11. Buenas prácticas de colaboración

- Mantén conversaciones relevantes en los issues o PRs para preservar el contexto.
- Documenta decisiones arquitectónicas importantes en `docs/`.
- Automatiza pruebas y validaciones en CI para garantizar la calidad antes del merge.
- Revisa periódicamente las ramas abiertas y cierra las que estén obsoletas.

## 12. Ejemplo completo de principio a fin

1. Recibes la tarea "Agregar validación de formulario".
2. Actualizas `main` (`git checkout main` + `git pull origin main`).
3. Creas tu rama (`git checkout -b feature/cm52-validacion-formulario`).
4. Realizas cambios en `pages/form.py` y `tests/test_form.py`.
5. Ejecutas `pytest` para asegurarte de que todo pasa.
6. Guardas tus cambios (`git add pages/form.py tests/test_form.py` + `git commit -m "feat: validar campos obligatorios"`).
7. Traes los últimos cambios (`git fetch origin` + `git rebase origin/main`).
8. Subes tu rama (`git push -u origin feature/cm52-validacion-formulario`).
9. Abres el PR en GitHub, adjuntas evidencia (capturas, resultados de pruebas) y solicitas revisión.
10. Tras la aprobación, haces merge desde GitHub y borras la rama remota.
11. Finalmente, actualizas tu `main` local y continúas con la siguiente tarea.

## 13. Glosario de términos comunes

- **Commit**: Guardado de tus cambios con un mensaje descriptivo.
- **Rama (branch)**: Línea paralela de trabajo para una tarea específica.
- **Merge**: Unir los cambios de una rama con otra.
- **Rebase**: Reordenar tus commits para que se apoyen en la versión más reciente.
- **Tag**: Etiqueta que marca un punto importante en la historia del repositorio (generalmente una versión).
- **Rollback/Revert**: Acción de deshacer uno o varios cambios ya publicados.


## 14. Recursos adicionales

- [Guía oficial de Git](https://git-scm.com/doc)
- [Flujo de GitHub](https://docs.github.com/es/get-started/quickstart/github-flow)
- [Convenciones de commits](https://www.conventionalcommits.org/es/v1.0.0/)

Mantener este flujo asegura trazabilidad, facilita la colaboración y permite reaccionar rápidamente ante incidentes en los entornos gestionados por el equipo.
