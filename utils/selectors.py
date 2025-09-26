"""
Centralización de selectores CSS, XPath y data‑testids.

Al definir todos los selectores de la aplicación en un único lugar, es
posible modificar los identificadores de la interfaz sin necesidad de
recorrer todos los Page Objects. Cuando el equipo de desarrollo añada
atributos `data-testid` en el frontend, actualiza este módulo con
nombres descriptivos.

Ejemplo:

```python
LOGIN_USER_INPUT = "input[placeholder='Usuario']"
LOGIN_PASS_INPUT = "input[placeholder='Contraseña']"
LOGIN_BUTTON = "button:has-text('Ingresar')"
```
"""

# Por ahora este archivo contiene solo ejemplos. Agrega aquí tus selectores.
LOGIN_USER_INPUT = "input[placeholder='Usuario']"
LOGIN_PASS_INPUT = "input[placeholder='Contraseña']"
LOGIN_BUTTON = "button:has-text('Ingresar')"
