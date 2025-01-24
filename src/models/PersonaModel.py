from database.db import get_connection
from flask_bcrypt import generate_password_hash
from .entities.Persona import Persona
from .entities.Alumno import Alumno

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
        '''
        Registra una persona en la base de datos.
        Args:
            persona (Persona): Objeto de la clase Persona con los datos de la persona a registrar.
        '''
        try:
            connection=get_connection()
            hashed_password = generate_password_hash(persona.contrasenia,12)
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

    @classmethod
    def obtenerPersona(self, dni):
        '''
        Obtiene una persona por su DNI. Devuelve una lista de diccionarios con los datos de las personas con el
        mismo dni.
        Args:
            dni (str): DNI de la persona a buscar.
        '''
        try:
            connection=get_connection()
            personas = []
            with connection.cursor() as cursor:
                cursor.execute('SELECT p.usuario, p.dniPer, p.apePer, p.nombrePer, p.mail, e.rol FROM personas p LEFT JOIN empleados e ON p.usuario = e.usuario WHERE p.dniPer = %s', (dni,))
                result = cursor.fetchall()
                for persona in result:
                    persona = Persona(persona[1], persona[3], persona[2], persona[4], persona[0], persona[5])
                    personas.append(persona.to_JSON())
                print(personas)
            connection.close()
            return personas
        except Exception as ex:
            raise Exception(ex) 

    @classmethod
    def obtenerPreceptores(self):
        '''
        Obtiene todos los preceptores de la base de datos.
        '''
        try:
            connection=get_connection()
            preceptores = []
            with connection.cursor() as cursor:
                cursor.execute('SELECT p.usuario, p.dniPer, p.apePer, p.nombrePer, p.mail, e.rol FROM personas p JOIN empleados e ON p.usuario = e.usuario WHERE e.rol = %s', ('PRECEPTOR',))
                result = cursor.fetchall()
                for preceptor in result:
                    preceptor = Persona(dni=preceptor[1], nombre=preceptor[3], apellido=preceptor[2], mail=preceptor[4], usuario=preceptor[0], rol=preceptor[5])
                    preceptores.append(preceptor.to_JSON())
            connection.close()
            return preceptores
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def obtenerAlumnosAsociados(self, usuario):
        '''
        Obtiene los alumnos asociados a un usuario.
        Args:
            usuario(str): usuario del tutor que realiza la peticion
        '''
        connection = get_connection()
        alumnos = []
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT a.nombrealu,a.apealu,a.dnialu,a.idalu FROM alumnos a JOIN tutor_alu t ON a.idalu = t.idalu WHERE t.usuario = %s AND a.estado = %s',(usuario,'ACTIVO'))
                result = cursor.fetchall()
                for alumno in result:
                    alumnos.append({
                            'idAlu': alumno[3],
                            'nombre': alumno[0],
                            'apellido': alumno[1],
                            'dni': alumno[2],
                        })
                connection.close()
                return alumnos    
        except Exception as ex:
            raise Exception(ex)    