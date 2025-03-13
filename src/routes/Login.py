#para poder hacer "sistema de rutas"
from flask import Blueprint, jsonify, request
#modelos
from models.LoginModel import LoginModel
#utils
from utils.Security import Security
main = Blueprint('login', __name__)

#GET
@main.route('/', methods=['POST'])
def login():
    try:
        required_fields = ['usuario','contrasenia']
            
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
        usuario = data['usuario']
        contrasenia = data['contrasenia']
        persona = LoginModel.login(usuario,contrasenia)
        if persona != None:
            encoded_token = Security.generate_token(persona)
            # Ahora tambien devuelve nombres 6/3 
            return jsonify({'success':True, 'token': encoded_token, 'rol' : persona.rol, 'usuario': persona.usuario, 'nombre':persona.nombre}, ), 200
        else:
            return jsonify({'message': 'Usuario o contraseña incorrectos'}), 404
    except Exception as e:
        return jsonify({'message': 'Error al intentar utilizar la base de datos',}), 500