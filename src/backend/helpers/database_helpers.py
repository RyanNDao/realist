from functools import wraps
from flask import request
import logging 
import datetime
import jwt
from backend.server.utils.ResponseBuilder import ResponseBuilder
import os

LOGGER = logging.getLogger(__name__)


def build_dynamic_update_query_template(dataColumns: dict, keyName: str):
    setAttributesList = []
    for columnName, options in dataColumns.items():
        if columnName != keyName:
            setAttributesList.append( \
                f'{columnName} = %({columnName})s' if options.get('setToNullOnNonUpdate') \
                else f'{columnName} = COALESCE(%({columnName})s, {columnName})'
            )
    setAttributeValues = '\t' + ',\n\t'.join(setAttributesList)
    return f"""
    UPDATE {{tableName}}
    SET
    {setAttributeValues}
    WHERE {{keyName}} = %({{keyName}})s
    RETURNING *
    """

def generate_token(userUsername, userId, secret_key, tokenLifeInSeconds=60*60*1):
    expirationTime = datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=tokenLifeInSeconds)

    payload = {
        'username': userUsername,
        'id': userId,
        'exp': expirationTime
    }

    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        bearerToken = request.authorization.token if request.authorization else None
        sessionToken = request.cookies.get('session_token') if request.cookies else None
            
        if not (sessionToken or bearerToken):
            return ResponseBuilder.buildFailureResponse('Token is missing', 403)
        try:
            token = sessionToken if sessionToken else bearerToken
            jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
        except jwt.exceptions.ExpiredSignatureError:
            return ResponseBuilder.buildFailureResponse('Token has expired', 403)
        except:
            return ResponseBuilder.buildFailureResponse('Token is invalid', 403)
        return f(*args, **kwargs)
    return decorated