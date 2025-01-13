from database.db import get_connection
from flask_bcrypt import generate_password_hash
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
    def registrar(self, persona):
        try:
            connection=get_connection()
            hashed_password = generate_password_hash(persona.contrasenia,12)
            print(f"Hash generado: {hashed_password}")
            with connection.cursor() as cursor:
                cursor.execute('''INSERT INTO personas (usuario, dniPer, apePer, nombrePer, contrasena, mail) VALUES (%s, %s, %s, %s, %s, %s)''', (persona.usuario, persona.dni, persona.apellido, persona.nombre, hashed_password, persona.mail))
                filasAfectadas = cursor.rowcount
                connection.commit()   
                if persona.rol != "tutor":
                    cursor.execute('''INSERT INTO empleados (usuario, rol) VALUES (%s, %s)''', (persona.usuario, persona.rol))
                    filasAfectadas = cursor.rowcount
                    connection.commit() 
                    print("Se registro un empleado correctamente")
            
            return filasAfectadas
        except Exception as ex:
            raise Exception(ex)
        finally:
            connection.close()