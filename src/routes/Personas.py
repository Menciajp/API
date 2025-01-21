#para poder hacer "sistema de rutas"
from flask import Blueprint, jsonify, request
from psycopg2 import errors
#modelos
from models.PersonaModel import PersonaModel
from models.entities.Persona import Persona
#seguridad
from utils.Security import Security

main = Blueprint('personas', __name__)

@main.route('/registrar', methods=['POST'])
def registrar():
    # sirve pera registrar sudo, preceptor, admin, tutor
    acceso = Security.verify_token(request.headers,{"SUDO","ADMIN"})
    if acceso:
        try:
            # Campos requeridos
            required_fields = ['dni', 'nombre', 'apellido', 'usuario', 'mail', 'rol','contrasenia']
            
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
            usuario = data['usuario']
            mail = data['mail']
            rol = data['rol'].upper()
            contrasenia = data['contrasenia']
            persona = Persona(dni=dni, nombre=nombre, apellido=apellido, usuario=usuario, mail=mail, rol=rol, contrasenia=contrasenia)
            respuesta = PersonaModel.registrar(persona)
            if respuesta == 1:
                return jsonify({'message': 'Usuario registrado correctamente'}), 201
            return jsonify({'message': 'Error al registrar el usuario'}), 500
        except errors.UniqueViolation:
            return jsonify({'message': 'El usuario ya existe'}), 400
        except Exception as e:
            error_message = str(e) 
            if "llave duplicada viola restricción de unicidad" in error_message:
                return jsonify({'error': 'El usuario ya existe'}), 400
            elif "no puede ser nulo" in error_message:
                return jsonify({'error': 'Faltan datos obligatorios'}), 400
            else:
                return jsonify({'error': f'Ocurrió un error inesperado: {error_message}'}), 500
    else:
        return jsonify({'error': 'No autorizado'}), 401
    
@main.route('/<DNI>', methods=['GET'])
def obtener(DNI):
    # Sirve para obtener una persona por su DNI
    acceso = Security.verify_token(request.headers,{"SUDO","ADMIN","PRECEPTOR"})
    if acceso:
        try:
            persona = PersonaModel.obtenerPersona(DNI)
            if persona != []:
                return (persona), 200
            return jsonify({'message': 'No se encontró la persona'}), 404
        except Exception as e:
            return jsonify({'message': 'Error al intentar utilizar la base de datos'}), 500
    else:
        return jsonify({'error': 'No autorizado'}), 401    
    
@main.route('/preceptores', methods=['GET'])
def obtenerPreceptores():
    # Sirve para obtener todos los preceptores
    acceso = Security.verify_token(request.headers,{"SUDO","ADMIN"})
    if acceso:
        try:
            preceptores = PersonaModel.obtenerPreceptores()
            if preceptores != []:
                return jsonify(preceptores), 200
            return jsonify({'message': 'No se encontraron preceptores'}), 404
        except Exception as e:
            return jsonify({'message': 'Error al intentar utilizar la base de datos'}), 500
    else:
        return jsonify({'error': 'No autorizado'}), 401    