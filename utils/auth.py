"""
Funciones auxiliares relacionadas con autenticación. Aunque la mayor
parte del flujo de login se maneja a través del `LoginPage` y la fixture
`login` en `conftest.py`, este módulo puede contener helpers para
refrescar la sesión, validar expiración de tokens o llamar a APIs de
autenticación si fuera necesario.

Actualmente este archivo solo define un marcador para futuras
extensiones.
"""


def refresh_session():
    """
    Marcador para una función que renueve la sesión sin necesidad de
    volver a autenticarse mediante la interfaz gráfica. Implementa una
    llamada a la API de backend cuando esté disponible.
    """
    raise NotImplementedError("La función refresh_session aún no está implementada.")