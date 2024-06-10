from flask import Blueprint, request
from backend.server.utils.ResponseBuilder import ResponseBuilder
import bcrypt
from backend.database.services.UserService import UserService
from injector import inject
userControllerBp = Blueprint('userController', import_name=__name__,  url_prefix='/user')


class UserController():
    
    
    @userControllerBp.route('/create', methods=['POST', 'PUT'])
    @inject
    def createUser(user_service: UserService):
        print(user_service)
        req = request.json
        username = req.get('username')
        passwordHash = bcrypt.hashpw(req.get('password').encode('UTF-8'), bcrypt.gensalt())
        user_service.createUser(username, passwordHash)
        return ResponseBuilder.buildSuccessResponse({"username": username}, f'User {username} was created successfully!')
    