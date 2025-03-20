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
                'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(hours=2),  # Expiración
                'iat': datetime.datetime.now(tz=cls.tz),  # Creación
                'usuario': usuarioAutenticado.usuario,  # Usuario
                'rol': usuarioAutenticado.rol  # Rol
            }
            
            # Generar el token JWT
            return jwt.encode(payload, cls.secret, algorithm='HS256')
        except Exception as e:
            print(f"Error al generar el token: {e}")
            raise Exception(f"Error al generar el token: {e}")

    @classmethod
    def verify_token(cls, headers,rolEsperado):
        """
        Verifica si un token JWT es válido y si el rol del usuario autenticado es el esperado.
        Args:
            headers (dict): Encabezados de la petición HTTP.
            rolEsperado (list): Lista de roles esperados.
        """
        if 'Authorization' in headers.keys():
            autorizacion = headers['Authorization']
            # Aca se agarra el token en si.
            token = autorizacion.split(' ')[1]
            try:
                payload = jwt.decode(token, cls.secret, algorithms=['HS256'])
                if payload['rol'] in rolEsperado:
                    return True
                return False
            except (jwt.ExpiredSignatureError,jwt.InvalidTokenError):
                return False
        return False    
    
    @classmethod
    def get_user_from_token(cls, headers):
        """
        Decodifica un token JWT y extrae el usuario.
        
        Args:
            headers (dict): Encabezados de la petición HTTP.
        
        Returns:
            str: El usuario extraído del token si es válido, o None si no lo es.
        """
        if 'Authorization' in headers:
            autorizacion = headers['Authorization']
            token = autorizacion.split(' ')[1]  # Extrae el token del encabezado
            
            try:
                payload = jwt.decode(token, cls.secret, algorithms=['HS256'])
                return payload.get('usuario')  # Devuelve el usuario
            except jwt.ExpiredSignatureError:
                print("El token ha expirado.")
                return None
            except jwt.InvalidTokenError:
                print("El token es inválido.")
                return None
        
        print("El encabezado 'Authorization' no está presente.")
        return None