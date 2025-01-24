#para poder hacer "sistema de rutas"
from flask import Blueprint, jsonify, request
from psycopg2 import errors
#modelos
from models.PersonaModel import PersonaModel
#seguridad
from utils.Security import Security

main = Blueprint('tutores', __name__)

@main.route('/', methods=['GET'])
def recuperarAlumnosAsociados():
    try:    
        alumnos = PersonaModel.obtenerAlumnosAsociados(Security.get_user_from_token(request.headers))
        if alumnos:
            return (alumnos), 200
        else:
            return jsonify({'message': 'No se encontraron alumnos para este usuario.'}), 404
    except Exception as e:
            return jsonify({'error': f'Ocurrió un error inesperado: {str(e)}'}), 500