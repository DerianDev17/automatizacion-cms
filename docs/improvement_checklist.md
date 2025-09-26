# Lista de verificación de mejoras sugeridas

Esta lista agrupa iniciativas que pueden planificarse para aumentar la robustez y el alcance de la automatización. Marca cada elemento al completarlo y añade comentarios cuando sea necesario.

## Infraestructura y mantenimiento

- [ ] Configurar un pipeline de integración continua (por ejemplo, GitHub Actions o Jenkins) que ejecute `pytest` en cada push.
- [ ] Publicar los reportes HTML generados en `reports/` como artefactos del pipeline.
- [ ] Automatizar la limpieza periódica de `artefacts/`, `videos/` y `reports/` para evitar que crezcan sin control.
- [ ] Documentar un procedimiento de restauración de dependencias cuando se actualicen versiones de Playwright o Python.

## Cobertura funcional

- [ ] Priorizar con el equipo funcional los módulos de Consultas y Reportes que aún no tienen automatización.
- [ ] Elaborar casos de prueba para WS01 y WS02 una vez que los endpoints estén disponibles.
- [ ] Incorporar pruebas negativas (errores esperados, validaciones de permisos) en los módulos existentes.
- [ ] Añadir validaciones de contenido descargado (por ejemplo, comparar CSVs o PDFs generados).

## Calidad de código y reutilización

- [ ] Unificar los selectores en `utils/selectors.py` y reemplazar localizaciones frágiles por atributos `data-testid` cuando estén disponibles.
- [ ] Implementar validaciones de esquema de datos (con `pydantic` o `jsonschema`) para los servicios web.
- [ ] Crear utilidades para manejar datos de prueba parametrizados en `fixtures/`.
- [ ] Definir convenciones de nombrado para evidencias (capturas y vídeos) y documentarlas en `docs/`.

## Observabilidad y reporte

- [ ] Habilitar Allure en el pipeline y publicar el reporte en cada ejecución nocturna.
- [ ] Registrar métricas de duración de pruebas y fallas repetidas para priorizar refactorizaciones.
- [ ] Evaluar la integración con herramientas de gestión de pruebas (TestRail, Zephyr) para vincular casos automáticos con casos manuales.

## Onboarding y documentación

- [ ] Revisar la documentación cada sprint y actualizarla cuando cambien los flujos del CMS.
- [ ] Añadir capturas de pantalla de los módulos clave para facilitar el entendimiento de nuevos integrantes.
- [ ] Documentar requisitos de red o VPN necesarios para acceder al CMS desde fuera de la intranet.
- [ ] Crear un glosario de términos y siglas utilizados en el proyecto dentro de `docs/`.

Personaliza esta lista según las prioridades del equipo e incorpora nuevas tareas conforme se identifiquen oportunidades adicionales.
