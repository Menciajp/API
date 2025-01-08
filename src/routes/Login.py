#para poder hacer "sistema de rutas"
from flask import Blueprint, jsonify
#modelos
from models.PersonaModel import PersonaModel

main = Blueprint('main', __name__)

@main.route('/')
def login():
    try:
        personas = PersonaModel.login()
        return jsonify(personas)
    except Exception as e:
        return jsonify({'message': e}), 500