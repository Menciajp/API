from flask_bcrypt import check_password_hash
from database.db import get_connection
from .entities.Persona import Persona

class LoginModel:
    @classmethod
    def login(self, usuario, contrasenia):
        """
    Autentica a un usuario verificando el nombre de usuario y la contraseña proporcionados.
    Primero, se busca el hash de la contraseña del usuario en la base de datos, si coundice con la contraseña
    ingresada, y le usuario existe, entonces se devuelve un diccionario con los detalles del usuario.

    Args:
        usuario (str): El nombre de usuario del usuario que intenta iniciar sesión.
        contrasena (str): La contraseña del usuario que intenta iniciar sesión.

    Returns:
        dict or None: Una representación en diccionario de los detalles del usuario si la autenticación es exitosa,
                      de lo contrario, None.

    Raises:
        Exception: Si hay un error durante la conexión a la base de datos o la ejecución de la consulta.
    """
        try:
            connection=get_connection()
            with connection.cursor() as cursor:
                cursor.execute('''SELECT  p.contrasena FROM personas p WHERE p.usuario = %s''', (usuario,))
                result = cursor.fetchone()
                persona = None
                if result == None:
                    return persona
                stored_password = result[0].tobytes()  
                # Verificar la contraseña
                if check_password_hash(stored_password, contrasenia):
                    cursor.execute('SELECT p.usuario, p.dniPer, p.apePer, p.nombrePer, p.mail, e.rol FROM personas p LEFT JOIN empleados e ON p.usuario = e.usuario WHERE p.usuario = %s''', (usuario,))
                    result = cursor.fetchone()
                    persona = Persona(usuario=result[0], dni=result[1], apellido=result[2], nombre=result[3], mail=result[4], rol=result[5])
            connection.close()
            return persona
        except Exception as ex:
            raise Exception(ex)   