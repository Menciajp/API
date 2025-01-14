from database.db import get_connection

class AlumnoModel():
    @classmethod
    def crearAlumno(cls, alumno):
        '''
        Registra un alumno en la base de datos.
        args:
            alumno (Alumno): Objeto de la clase Alumno.
        '''
        try:
            connection=get_connection()
            with connection.cursor() as cursor:
                cursor.execute('''INSERT INTO alumnos ("nombrealu", "apealu", "dnialu", "fechingreso", "fechnac","estado") VALUES (%s, %s, %s, %s, %s,%s)''', (alumno.nombre, alumno.apellido, alumno.dni, alumno.fechIngreso, alumno.fechNac,"ACTIVO"))
                filasAfectadas = cursor.rowcount
                connection.commit()   
                print("Se registro un alumno correctamente")
            
            return filasAfectadas
        except Exception as ex:
            raise Exception(ex)
        finally:
            connection.close()