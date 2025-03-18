from database.db import get_connection
from utils.DateFormat import DateFormat
import datetime

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
    
    @classmethod
    def asignarCurso(cls,id, curso, anio):
        try:
            connection=get_connection()
            with connection.cursor() as cursor:
                cursor.execute('''INSERT INTO alu_curso ("idalu", "nombrecurso", "anio") VALUES (%s, %s, %s)''', (id,curso,anio))
                filasAfectadas = cursor.rowcount
                connection.commit()   
                print("Se asigno un alumno a un curso correctamente.")
            
            return filasAfectadas
        except Exception as ex:
            raise Exception(ex)
        finally:
            connection.close()

    @classmethod
    def asignarTutor(cls, idAlumno, usuarioTutor):
        '''
        Asigna un tutor a un alumno.
        args:
            idAlumno (int): ID del alumno.
            usuarioTutor (str): Usuario del tutor.
        '''
        try:
            connection=get_connection()
            with connection.cursor() as cursor:
                cursor.execute('''INSERT INTO tutor_alu ("usuario", "idalu") VALUES (%s, %s)''', (usuarioTutor,idAlumno))
                filasAfectadas = cursor.rowcount
                connection.commit()   
                print("Se asigno un tutor a un alumno correctamente.")
            
            return filasAfectadas
        except Exception as ex:
            raise Exception(ex)
        finally:
            connection.close()

    @classmethod
    def recuperarAlumnos(cls,nombreCurso,anio):
        '''
        Recupera todos los alumnos registrados en la base de datos registrados en un curso determinado.
        args:
        nombreCurso (str): Nombre del curso.
        anio (int): Año del curso.
        '''
        try:
            connection=get_connection()
            alumnos = []
            with connection.cursor() as cursor:
                cursor.execute('''SELECT * FROM alumnos WHERE idalu IN (SELECT idalu FROM alu_curso WHERE nombrecurso=%s AND anio=%s)''',(nombreCurso,anio))
                respuesta = cursor.fetchall()
                for alumno in respuesta:
                    alumnos.append({
                        'idAlu': alumno[0],
                        'nombre': alumno[3],
                        'apellido': alumno[2],
                        'dni': alumno[1],
                        'fechIngreso': DateFormat.convert_date_to_string(alumno[4]),
                        'fechNac': DateFormat.convert_date_to_string(alumno[5]),
                        'estado': alumno[6]
                    })
                return alumnos
        except Exception as ex:
            raise Exception(ex)
        finally:
            connection.close()
    
    @classmethod
    def cargarAsistencia(cls, alumno, fecha):
        '''
        Registra la asistencia de un alumno en la base de datos en una fecha determinada.
        args:
            alumno(obj): Objeto de la clase Alumno. {'id':int, 'estado':str}
            fecha (str): Fecha de la asistencia.
        '''
        try:
            connection=get_connection()
            with connection.cursor() as cursor:
                cursor.execute('''INSERT INTO asistencias ("idalu", "fecha","tipo") VALUES (%s, %s,%s)''', (alumno['id'], fecha,alumno['estado'].upper()))
                filasAfectadas = cursor.rowcount
                connection.commit()   
                print("Se registro la asistencia de un alumno correctamente.")
            
            return filasAfectadas
        except Exception as ex:
            raise Exception(ex)
        finally:
            connection.close()

    @classmethod
    def situacionAlumno(cls,id):
        try:
            connection=get_connection()
            with connection.cursor() as cursor:
                # Primer query para el resumen
                cursor.execute('''
                    SELECT tipo, COUNT(*) AS cantidad
                    FROM asistencias
                    WHERE idAlu = %s AND tipo IN ('TARDANZA', 'FALTA') AND
                    EXTRACT(YEAR FROM fecha) = EXTRACT(YEAR FROM CURRENT_DATE)
                    GROUP BY tipo;
                ''', (id,))
                respuesta = cursor.fetchall()
                respuesta = {item[0]: item[1] for item in respuesta}
                if 'TARDANZA' not in respuesta:
                    respuesta['TARDANZA'] = 0
                if 'FALTA' not in respuesta:
                    respuesta['FALTA'] = 0
                # Segundo query para el detalle
                cursor.execute('''
                    SELECT fecha, tipo
                    FROM asistencias
                    WHERE idAlu = %s AND tipo IN ('TARDANZA', 'FALTA') AND
                    EXTRACT(YEAR FROM fecha) = EXTRACT(YEAR FROM CURRENT_DATE)
                    ORDER BY fecha;
                ''', (id,))
                detalle = cursor.fetchall()
                # Agregar detalle a respuesta
                respuesta['detalle'] = [{'fecha': DateFormat.convert_date_to_string(fecha), 'tipo': tipo} for fecha, tipo in detalle]
                return respuesta
        except Exception as ex:
            raise Exception(ex)
        finally:
            connection.close()

    @classmethod
    def obtenerIdAlumno(cls,dni,nombre,apellido):
        try:
            connection=get_connection()
            with connection.cursor() as cursor:
                cursor.execute('''SELECT idalu FROM alumnos WHERE dnialu=%s AND nombrealu=%s AND apealu=%s''',(dni,nombre,apellido))
                respuesta = cursor.fetchone()
                return respuesta[0]
        except Exception as ex:
            raise Exception(ex)
        finally:
            connection.close()        