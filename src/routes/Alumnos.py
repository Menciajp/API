#para poder hacer "sistema de rutas"
from flask import Blueprint, jsonify, request
#modelos
from models.AlumnoModel import AlumnoModel
from models.entities.Alumno import Alumno
#utils
from psycopg2 import errors
from datetime import datetime
from utils.Security import Security
main = Blueprint('alumnos', __name__)

@main.route('/registrar', methods=['POST'])
def registrar():
    acceso = Security.verify_token(request.headers,{"SUDO","ADMIN"})
    if acceso:
        try:
            # Campos requeridos
            required_fields = ['dni', 'nombre', 'apellido', 'fechNac']
            
            # Obtener datos de la solicitud
            data = request.json
            
            # Validar que existan y no estén vacíos
            empty_fields = [field for field in required_fields if not data.get(field) or data.get(field).strip() == ""]
            if empty_fields:
                return jsonify({'error': f"Los siguientes campos están vacíos: {', '.join(empty_fields)}"}), 400
            
            # Extraer datos
            dni = data['dni']
            nombre = data['nombre']
            apellido = data['apellido']
            fechNac = data['fechNac']
            fechIngreso = datetime.now().date().strftime('%Y-%m-%d')
            alumno = Alumno(dni=dni, nombre=nombre, apellido=apellido, fechNac=fechNac, fechIngreso=fechIngreso)
            respuesta = AlumnoModel.crearAlumno(alumno)
            if respuesta == 1:
                return jsonify({'message': 'Alumno registrado correctamente'}), 201
            else:
                return jsonify({'message': 'No se pudo registrar el alumno'}), 500
        except errors.UniqueViolation:
            return jsonify({'message': 'El alumno ya existe'}), 400
        except Exception as e:
            error_message = str(e) 
            if "llave duplicada viola restricción de unicidad" in error_message:
                return jsonify({'error': 'El alumno ya existe'}), 400
            elif "no puede ser nulo" in error_message:
                return jsonify({'error': 'Faltan datos obligatorios'}), 400
            else:
                return jsonify({'error': f'Ocurrió un error inesperado: {error_message}'}), 500
    else:
        return jsonify({'error': 'No autorizado'}), 401

@main.route('/curso', methods=['POST'])
def asignarCurso():
    acceso = Security.verify_token(request.headers,{"SUDO","ADMIN"})
    if acceso:
        try:
            # Campos requeridos
            required_fields = ['id','curso','anio']
            
            # Obtener datos de la solicitud
            data = request.json
            
            # Validar que existan y no estén vacíos
            empty_fields = [field for field in required_fields if not data.get(field) or data.get(field).strip() == ""]
            if empty_fields:
                return jsonify({'error': f"Los siguientes campos están vacíos: {', '.join(empty_fields)}"}), 400
            
            # Extraer datos
            id = data['id']
            curso = data['curso']
            año = data['anio']
            respuesta = AlumnoModel.asignarCurso(id,curso,año)
            if respuesta == 1:
                return jsonify({'message': 'Alumno asignado al curso correctamente'}), 201
            else:
                return jsonify({'message': 'No se pudo asignar el alumno al curso'}), 500
        except errors.UniqueViolation:
            return jsonify({'message': 'El alumno ya está asignado al curso'}), 400
        except Exception as e:
            error_message = str(e) 
            if "llave duplicada viola restricción de unicidad" in error_message:
                return jsonify({'error': 'El alumno ya está asignado al curso'}), 400
            elif "no puede ser nulo" in error_message:
                return jsonify({'error': 'Faltan datos obligatorios'}), 400
            else:
                return jsonify({'error': f'Ocurrió un error inesperado: {error_message}'}), 500
    else:
        return jsonify({'error': 'No autorizado'}), 401    
    
@main.route('/tutor', methods=['POST'])
def asignarTutor():
    acceso = Security.verify_token(request.headers,{"SUDO","ADMIN"})
    if acceso:
        
        # Campos requeridos
        required_fields = ['idAlu','usuarioTutor']
            
        # Obtener datos de la solicitud
        data = request.json
            
        # Validar que existan y no estén vacíos
        empty_fields = [
            field for field in required_fields
            if not data.get(field) or
            (isinstance(data.get(field), str) and data.get(field).strip() == "") or
            (isinstance(data.get(field), list) and len(data.get(field)) == 0)
        ]
        if empty_fields:
            return jsonify({'error': f"Los siguientes campos están vacíos: {', '.join(empty_fields)}"}), 400
            
        idAlu = data['idAlu']
        tutor = data['usuarioTutor']
        
        # Lista de tutores que no pudieron ser asignados
        tutoresNoAsignados = []

        for usuario in tutor:
            try:
                respuesta = AlumnoModel.asignarTutor(idAlu, usuario)
                if respuesta != 1:
                    tutoresNoAsignados.append(usuario)
            except Exception as e:
                error_message = str(e)
                if "llave duplicada viola restricción de unicidad" in error_message:
                    tutoresNoAsignados.append(usuario)
                elif "no puede ser nulo" in error_message:
                    return jsonify({'error': 'Faltan datos obligatorios'}), 400
                else:
                    return jsonify({'error': f'Ocurrió un error inesperado: {error_message}'}), 500

        # Verificar si hay tutores que no pudieron asignarse
        if len(tutoresNoAsignados) == 0:
            return jsonify({'message': 'Todos los tutores fueron asignados correctamente.'}), 201
        elif len(tutoresNoAsignados) < len(tutor):
            return jsonify({
                'message': 'Algunos tutores fueron asignados correctamente.',
                'tutoresNoAsignados': tutoresNoAsignados
            }), 207  # Estado 207: Multi-Status (algunas operaciones fallaron)
        else:
            return jsonify({
                'message': 'No se pudo asignar ninguno de los tutores.',
                'tutoresNoAsignados': tutoresNoAsignados
            }), 500
    else:
        return jsonify({'error': 'No autorizado'}), 401
    
@main.route('/<nombreCurso>/<anio>', methods=['GET'])
def recuperarAlumnos(nombreCurso,anio):
    '''
    Recupera todos los alumnos de un curso
    '''
    acceso = Security.verify_token(request.headers,{"SUDO","ADMIN","PRECEPTOR"})
    if acceso:
        try:
            alumnos = AlumnoModel.recuperarAlumnos(nombreCurso,anio)
            return jsonify(alumnos), 200
        except Exception as e:
            return jsonify({'error': f'Ocurrió un error inesperado: {str(e)}'}), 500
    else:
        return jsonify({'error': 'No autorizado'}), 401

@main.route('/asistencia', methods=['POST'])
def cargarAsistencia():
    '''
    Registra la asistencia de un alumno en la base de datos.
    '''
    acceso = Security.verify_token(request.headers,{"SUDO","ADMIN","PRECEPTOR"})
    if acceso:
        
            # Campos requeridos
            required_fields = ['alumnos','fecha',]
            
            # Obtener datos de la solicitud
            data = request.json
            
        # Validar que existan y no estén vacíos
            empty_fields = [
                field for field in required_fields
                if not data.get(field) or
                (isinstance(data.get(field), str) and data.get(field).strip() == "") or
                (isinstance(data.get(field), list) and len(data.get(field)) == 0)
            ]
            if empty_fields:
                return jsonify({'error': f"Los siguientes campos están vacíos: {', '.join(empty_fields)}"}), 400
            
            # Extraer datos
            alumnos = data['alumnos']
            fecha = data['fecha']
            asistenciasNoCargadas = [];
            for alumno in alumnos:
                try:
                    respuesta = AlumnoModel.cargarAsistencia(alumno,fecha)
                    if respuesta != 1:
                        asistenciasNoCargadas.append(alumno)
                except Exception as e:
                    error_message = str(e)
                    if "llave duplicada viola restricción de unicidad" in error_message:
                        asistenciasNoCargadas.append(alumno)
                    elif "no puede ser nulo" in error_message:
                        return jsonify({'error': 'Faltan datos obligatorios'}), 400
                    else:
                        asistenciasNoCargadas.append(alumno)
            if len(asistenciasNoCargadas) == 0:
                return jsonify({'message': 'Todas las asistencias fueron cargadas correctamente.'}), 201
            elif len(asistenciasNoCargadas) < len(alumnos):
                return jsonify({
                'message': 'Algunas asistencias fueron cargadas correctamente.',
                'alumnos no cargados': asistenciasNoCargadas
                }), 207  # Estado 207: Multi-Status (algunas operaciones fallaron)
            else:
                return jsonify({
                'message': 'No se pudo guardar ninguna de las asistencias.',
                'tutoresNoAsignados': asistenciasNoCargadas
                }), 500
    else:
        return jsonify({'error': 'No autorizado'}), 401
    
@main.route('/asistencia/<id>', methods=['GET'])
def recuperarAsistencias(id):
    '''
    Recupera todas las asistencias de un alumno
    '''
    acceso = Security.verify_token(request.headers,{"SUDO","ADMIN","PRECEPTOR","TUTOR"})
    if acceso:
        try:
            asistencias = AlumnoModel.situacionAlumno(id)
            return jsonify(asistencias), 200
        except Exception as e:
            return jsonify({'error': f'Ocurrió un error inesperado: {str(e)}'}), 500
    else:
        return jsonify({'error': 'No autorizado'}), 401