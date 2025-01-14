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
    