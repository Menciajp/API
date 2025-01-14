from database.db import get_connection
from .entities.Curso import Curso

class CursoModel():
    @classmethod
    def crearCurso(cls,curso, anio):
        '''
        Registra un curso en la base de datos.
        args:
            curso (str): Nombre del curso.
            anio (int): Año del curso
        '''
        try:
            connection=get_connection()
            print(curso)
            print(anio)
            with connection.cursor() as cursor:
                cursor.execute('''INSERT INTO cursos ("nombreCurso", "anio") VALUES (%s, %s)''', (curso,anio))
                filasAfectadas = cursor.rowcount
                connection.commit()   
                print("Se registro un curso correctamente")
            
            return filasAfectadas
        except Exception as ex:
            raise Exception(ex)
        finally:
            connection.close()
