from flask import Flask

from config import config
#Rutas
from routes import Login

app = Flask(__name__)

#para gestion de error
def page_not_found(error):
    return 'This page does not exist', 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    #blueprints
    #url prefix es para que todas las rutas de login tengan un prefijo
    app.register_blueprint(Login.main, url_prefix='/login')

    #manejo de errores
    app.register_error_handler(404, page_not_found)
    app.run()