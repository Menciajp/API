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

    @classmethod
    def asignarPreceptor(cls,nombreCurso, anio, usuarioPreceptor):
        '''
        Asigna un preceptor a un curso.
        args:
            nombreCurso (str): Nombre del curso.
            anio (int): Año del curso.
            usuarioPreceptor (str): Usuario del preceptor.
        '''
        try:
            connection=get_connection()
            with connection.cursor() as cursor:
                cursor.execute('''INSERT INTO precep_curso ("nombrecurso", "anio", "usuario") VALUES (%s, %s, %s)''', (nombreCurso, anio, usuarioPreceptor))
                filasAfectadas = cursor.rowcount
                connection.commit()
                print("Se asigno un preceptor al curso correctamente")
            return filasAfectadas
        except Exception as ex:
            raise Exception(ex)
        finally:
            connection.close()

    @classmethod
    def obtenerCursosPreceptor(cls,usuario):
        '''
        Obtiene todos los cursos registrados en la base de datos.
        '''
        try:
            connection=get_connection()
            cursos = []
            with connection.cursor() as cursor:
                cursor.execute('''SELECT * FROM cursos WHERE ("nombreCurso", "anio") IN (SELECT "nombrecurso","anio" FROM precep_curso WHERE usuario = %s)''', (usuario,))
                respuesta = cursor.fetchall()
                for curso in respuesta:
                    cursos.append(Curso(curso[0],curso[1]).to_JSON())
                print("Se obtuvieron los cursos correctamente")
            return cursos
        except Exception as ex:
            raise Exception(ex)
        finally:
            connection.close()