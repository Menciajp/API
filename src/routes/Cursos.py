#para poder hacer "sistema de rutas"
from flask import Blueprint, jsonify, request
from psycopg2 import errors
from datetime import datetime
#modelos
from models.CursoModel import CursoModel
#seguridad
from utils.Security import Security

main = Blueprint('cursos', __name__)

@main.route('/registrar', methods=['POST'])
def registrar():
        required_fields = ['nombre','anio']
            
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
        nombre = data['nombre']
        anio = data['anio']
    # sirve pera registrar sudo, preceptor, admin, tutor
        acceso = Security.verify_token(request.headers,{"SUDO","ADMIN"})
        if acceso:
            try:
                resultado = CursoModel.crearCurso(nombre,anio)
                if resultado == 1:
                    return jsonify({'message': 'Curso registrado correctamente'}), 201
            except errors.UniqueViolation:
                return jsonify({'message': 'El curso ya existe'}), 400
            except Exception as e:
                error_message = str(e) 
                if "llave duplicada viola restricción de unicidad" in error_message:
                    return jsonify({'error': 'El curso ya existe'}), 400
                elif "no puede ser nulo" in error_message:
                    return jsonify({'error': 'Faltan datos obligatorios'}), 400
                else:
                    return jsonify({'error': f'Ocurrió un error inesperado: {error_message}'}), 500
        else:
            return jsonify({'error': 'No autorizado'}), 401

@main.route('/asignarPreceptor', methods=['POST'])
def asignarPreceptor():
    acceso = Security.verify_token(request.headers,{"SUDO","ADMIN"})
    if acceso:
        # Campos requeridos
        required_fields = ['nombreCurso','anioCurso','usuarioPreceptor']
            
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
            
        nombreCurso = data['nombreCurso']
        anio = data['anioCurso']
        usuarioPreceptor = data['usuarioPreceptor']
        
        # Lista de tutores que no pudieron ser asignados
        preceptoresNoAsignados = []

        for usuario in usuarioPreceptor:
            try:
                respuesta = CursoModel.asignarPreceptor(nombreCurso, anio ,usuario)
                if respuesta != 1:
                    preceptoresNoAsignados.append(usuario)
            except Exception as e:
                error_message = str(e)
                if "llave duplicada viola restricción de unicidad" in error_message:
                    preceptoresNoAsignados.append(usuario)
                elif "no puede ser nulo" in error_message:
                    return jsonify({'error': 'Faltan datos obligatorios'}), 400
                else:
                    return jsonify({'error': f'Ocurrió un error inesperado: {error_message}'}), 500

        # Verificar si hay tutores que no pudieron asignarse
        if len(preceptoresNoAsignados) == 0:
            return jsonify({'message': 'Todos los preceptores fueron asignados correctamente.'}), 201
        elif len(preceptoresNoAsignados) < len(usuarioPreceptor):
            return jsonify({
                'message': 'Algunos preceptores fueron asignados correctamente.',
                'preceptoresNoAsignados': preceptoresNoAsignados
            }), 207  # Estado 207: Multi-Status (algunas operaciones fallaron)
        else:
            return jsonify({
                'message': 'No se pudo asignar ninguno de los preceptores.',
                'tutoresNoAsignados': preceptoresNoAsignados
            }), 500
    else:
        return jsonify({'error': 'No autorizado'}), 401
    
@main.route('/preceptor', methods=['GET'])
def obtenerCursosPreceptor():
    acceso = Security.verify_token(request.headers,{"PRECEPTOR"})
    if acceso:
        try:
            # Se saca el usuario del preceptor del token
            cursos = CursoModel.obtenerCursosPreceptor(Security.get_user_from_token(request.headers))
            if cursos:
                return jsonify({'cursos': cursos}), 200
            else:
                return jsonify({'message': 'No se encontraron cursos para este usuario.'}), 404
        except Exception as e:
            return jsonify({'error': f'Ocurrió un error inesperado: {str(e)}'}), 500
    else:
        return jsonify({'error': 'No autorizado'}), 401

@main.route('/preceptor/<nombreCurso>/<anio>', methods=['GET'])
def obtenerPreceptoresDeCurso(nombreCurso,anio):
    acceso = Security.verify_token(request.headers,{"SUDO","ADMIN"})
    if acceso:
        try:
            # Se saca el usuario del preceptor del token
            preceptores = CursoModel.obtenerPreceptoresCurso(nombreCurso,anio)
            if preceptores:
                return jsonify({'preceptores': preceptores}), 200
            else:
                return jsonify({'message': 'No se encontraron preceptores para este curso.'}), 404
        except Exception as e:
            return jsonify({'error': f'Ocurrió un error inesperado: {str(e)}'}), 500
    else:
        return jsonify({'error': 'No autorizado'}), 401
    
@main.route('/', methods =['GET'])
def obtenerCursos():
    acceso = Security.verify_token(request.headers,{"SUDO","ADMIN"})
    if acceso:
        try:
            anio = str(datetime.now().year)
            cursos = CursoModel.obtenerCursos(anio)
            if cursos:
                return jsonify({'cursos': cursos}), 200
            else:
                return jsonify({'message': 'No se encontraron cursos.'}), 404
        except Exception as e:
            return jsonify({'error': f'Ocurrió un error inesperado: {str(e)}'}), 500
    else:
        return jsonify({'error': 'No autorizado'}), 401