import datetime
import pytz
import jwt
from decouple import config

class Security:
    # Atributos de clase
    secret = config('JWT_KEY')  # Clave secreta desde el archivo .env
    tz = pytz.timezone('America/Argentina/Buenos_Aires')  # Zona horaria

    @classmethod
    def generate_token(cls, usuarioAutenticado):
        """
        Genera un token JWT para un usuario autenticado.

        Args:
            usuarioAutenticado (obj): Objeto con los atributos `usuario` y `rol`.

        Returns:
            str: Token JWT generado.
        """
        try:
            # Validar que el objeto tenga los atributos necesarios
            if not hasattr(usuarioAutenticado, 'usuario') or not hasattr(usuarioAutenticado, 'rol'):
                raise ValueError("El objeto usuarioAutenticado debe tener los atributos 'usuario' y 'rol'.")

            # Crear el payload del token
            payload = {
                'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(minutes=10),  # Expiración
                'iat': datetime.datetime.now(tz=cls.tz),  # Creación
                'usuario': usuarioAutenticado.usuario,  # Usuario
                'rol': usuarioAutenticado.rol  # Rol
            }

            # Generar el token JWT
            return jwt.encode(payload, cls.secret, algorithm='HS256')
        except Exception as e:
            raise Exception(f"Error al generar el token: {e}")
