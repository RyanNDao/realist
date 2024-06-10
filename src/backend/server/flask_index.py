from flask import Flask
from backend.exceptions import CursorError
from backend.server.utils.ResponseBuilder import ResponseBuilder
from flask_login import LoginManager
from backend.database.common.DatabaseConnectionPool import DatabaseConnectionPool
import os
from dotenv import load_dotenv
from backend.server.controllers import UserController
from flask_injector import FlaskInjector
from injector import singleton, Binder
from backend.database.dao.UserDAO import UserDAO
from backend.database.services.UserService import UserService
from backend.server.configurations import exception_handling_config
load_dotenv()

def create_app() -> Flask:

    def configure_injections(binder: Binder):
        user_dao = UserDAO(app.db_pool['users'])
        user_service = UserService(user_dao)
        binder.bind(UserService, to=user_service, scope=singleton)
    
    app = Flask(__name__)
    app.db_pool = {
        'home_data': DatabaseConnectionPool(connectionString=os.getenv('CONNECTION_STRING_TEMPLATE').format('home_data')),
        'users': DatabaseConnectionPool(connectionString=os.getenv('CONNECTION_STRING_TEMPLATE').format('users'))
    }
    app.register_blueprint(UserController.userControllerBp, url_prefix='/api/user')
    app.register_blueprint(exception_handling_config.exceptionHandlerBp)

    FlaskInjector(app=app, modules=[configure_injections])

    return app

app = create_app()






login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/api")
def hello_world():
    return ResponseBuilder.buildSuccessResponse({"world" :"hello"}, 'Hello world successful!')

@app.route('/api/create-user')
def create_user():
    pass

@app.route('/api/test-error')
def test_error():
    raise CursorError("Test error", cause="This is a test cause")

def main():
    app.run(debug=True, port=5000)

if __name__ == "__main__":
    main()