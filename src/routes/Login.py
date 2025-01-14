#para poder hacer "sistema de rutas"
from flask import Blueprint, jsonify
#modelos
from models.LoginModel import LoginModel
#utils
from utils.Security import Security
main = Blueprint('login', __name__)

#GET
@main.route('/<usuario>/<contrasena>', methods=['GET'])
def login(usuario, contrasena):
    try:
        persona = LoginModel.login(usuario,contrasena)
        if persona != None:
            encoded_token = Security.generate_token(persona)
            return jsonify({'success':True, 'token': encoded_token}), 200
        else:
            return jsonify({'message': 'Usuario o contraseña incorrectos'}), 404
    except Exception as e:
        return jsonify({'message': 'Error al intentar utilizar la base de datos',}), 500