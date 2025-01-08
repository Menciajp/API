from database.db import get_connection
from .entities.Persona import Persona

class PersonaModel():
    # Este metodo es para traer a todas las personas de la bd con su rol, si rol es nulo son tutores. 
    @classmethod
    def login(self):
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
        