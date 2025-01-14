from flask import Flask
from flask_bcrypt import Bcrypt

from config import config
#Rutas
from routes import Login
from routes import Personas
from routes import Cursos
from routes import Alumnos
app = Flask(__name__)
bcrypt = Bcrypt(app)

#para gestion de error
def page_not_found(error):
    return 'This page does not exist', 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    #blueprints
    #url prefix es para que todas las rutas de login tengan un prefijo
    app.register_blueprint(Login.main, url_prefix='/login')
    app.register_blueprint(Personas.main, url_prefix='/personas')
    app.register_blueprint(Cursos.main, url_prefix='/cursos')
    app.register_blueprint(Alumnos.main, url_prefix='/alumnos')

    #manejo de errores
    app.register_error_handler(404, page_not_found)
    app.run()