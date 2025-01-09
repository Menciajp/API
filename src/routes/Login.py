#para poder hacer "sistema de rutas"
from flask import Blueprint, jsonify
#modelos
from models.PersonaModel import PersonaModel

main = Blueprint('login', __name__)

#GET
@main.route('/<usuario>/<contrasena>', methods=['GET'])
def login(usuario, contrasena):
    try:
        persona = PersonaModel.login(usuario,contrasena)
        if persona != None:
            return persona
        else:
            return jsonify({'message': 'Usuario o contraseña incorrectos'}), 404
    except Exception as e:
        return jsonify({'message': 'Error al intentar utilizar la base de datos'}), 500