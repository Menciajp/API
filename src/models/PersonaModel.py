from database.db import get_connection
from .entities.Persona import Persona
from utils.EncripContrasena import EncripContrasena

class PersonaModel():
    # Este metodo es para traer a todas las personas de la bd con su rol, si rol es nulo son tutores. 
    @classmethod
    def traerUsuario(self):
        try:
            connection=get_connection()
            personas = []
            with connection.cursor() as cursor:
                cursor.execute('SELECT p.usuario, p.dniPer, p.apePer, p.nombrePer, p.contrasena, p.mail, e.rol FROM personas p LEFT JOIN empleados e ON p.usuario = e.usuario')
                resultset = cursor.fetchall()
                for persona in resultset:
                    persona = Persona(persona[1], persona[3], persona[2], persona[4], persona[0], persona[5], persona[6])
                    personas.append(persona.to_JSON())
            connection.close()
            return personas 
        except Exception as ex:
            raise Exception(ex)      
  
    @classmethod
    def login(self, usuario, contrasena):
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
                cursor.execute('''SELECT  ENCODE(p.contrasena, 'hex') FROM personas p WHERE p.usuario = %s''', (usuario,))
                result = cursor.fetchone()
                persona = None
                if result == None:
                    return persona
                elif EncripContrasena.comparar_contrasena(contrasena, result[0]):
                    cursor.execute('SELECT p.usuario, p.dniPer, p.apePer, p.nombrePer, p.mail, e.rol FROM personas p LEFT JOIN empleados e ON p.usuario = e.usuario')
                    result = cursor.fetchone()
                    persona = Persona(result[1], result[3], result[2], result[4], result[0], result[5],None)
                    persona = persona.to_JSON()
            connection.close()
            return persona
        except Exception as ex:
            raise Exception(ex)    

    @classmethod
    def registrar(self, persona):
        try:
            connection=get_connection()
            with connection.cursor() as cursor:
                cursor.execute('''INSERT INTO personas (usuario, dniPer, apePer, nombrePer, contrasena, mail) VALUES (%s, %s, %s, %s, %s, %s)''', (persona.usuario, persona.dni, persona.apellido, persona.nombre, EncripContrasena.generar_hash(persona.contrasenia), persona.mail))
                filasAfectadas = cursor.rowcount
                connection.commit()   
            connection.close()
            return filasAfectadas
        except Exception as ex:
            raise Exception(ex)