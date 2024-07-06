import datetime
from flask import Blueprint, request
from backend.helpers.database_helpers import generate_token
from backend.server.utils.ResponseBuilder import ResponseBuilder
import bcrypt
from backend.database.services.UserService import UserService
from injector import inject
import jwt
import os


userControllerBp = Blueprint('userController', import_name=__name__,  url_prefix='/user')


class UserController():
    
    
    @userControllerBp.route('/create', methods=['POST', 'PUT'])
    @inject
    def createUser(user_service: UserService):
        req = request.json
        username = req.get('username')
        passwordHash = bcrypt.hashpw(req.get('password').encode('UTF-8'), bcrypt.gensalt())
        user_service.createUser(username, passwordHash.decode('UTF-8'))
        return ResponseBuilder.buildSuccessResponse({"username": username}, f'User {username} was created successfully!')
    
    @userControllerBp.route('/authenticate', methods=['POST'])
    @inject
    def authenticateProfile(user_service: UserService):
        req = request.json
        username = req.get('username')
        password = req.get('password', '').encode('UTF-8')
        user = user_service.authenticate(username, password)
        if user:
            userUsername = user.get('username')
            userId = user.get('id')
            isAdmin = user.get('is_admin')
            token = generate_token(userUsername, userId, os.getenv('JWT_SECRET_KEY'))
            return ResponseBuilder.buildSecureSuccessResponse({
                'username': userUsername,
                'id': userId,
                'isAdmin': isAdmin,
                }, f'User {username} was authenticated!',
                token=token
            )
        else:
            return ResponseBuilder.buildFailureResponse(f'User {username} was not authenticated!', 401)
        

