
# =========================
#  Módulo de Autenticación de Usuarios
# =========================

# Diccionario de usuarios y contraseñas (en un entorno real, usar base de datos y hash de contraseñas)
USERS = {
    "admin": "password",      # Usuario administrador
    "user": "passuser",      # Usuario estándar
    "guest": "guestpass"     # Usuario invitado
}

def check_login(username: str, password: str) -> bool:
    """
    Verifica si el usuario y la contraseña proporcionados son válidos.
    
    Args:
        username (str): Nombre de usuario ingresado.
        password (str): Contraseña ingresada.
    
    Returns:
        bool: True si las credenciales son correctas, False en caso contrario.
    
    Nota:
        En producción, nunca almacenes contraseñas en texto plano. Utiliza hashing seguro y almacenamiento en base de datos.
    """
    # Busca el usuario en el diccionario y compara la contraseña
    return USERS.get(username) == password