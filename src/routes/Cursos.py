#para poder hacer "sistema de rutas"
from flask import Blueprint, jsonify, request
from psycopg2 import errors
#modelos
from models.CursoModel import CursoModel
#seguridad
from utils.Security import Security

main = Blueprint('cursos', __name__)

@main.route('/registrar/<nombreCurso>/<anio>', methods=['POST'])
def registrar(nombreCurso,anio):
    # sirve pera registrar sudo, preceptor, admin, tutor
    acceso = Security.verify_token(request.headers,{"SUDO","ADMIN"})
    if acceso:
        try:
            resultado = CursoModel.crearCurso(nombreCurso,anio)
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