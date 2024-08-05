from flask import jsonify, make_response

class ResponseBuilder():

    @staticmethod
    def buildSuccessResponse(data: dict | list, message: str):
        return jsonify({
            "data": data,
            "success": True,
            "message": message,
            "status": 200,
        })
    
    @staticmethod
    def buildSecureSuccessResponse(data: dict, message:str, token: str):
        responseData = jsonify({
            "data": data,
            "success": True,
            "message": message, 
            "status": 200
        })
        response = make_response(responseData)
        response.set_cookie('session_token', value=token, httponly=True, secure=True)
        return response
    

    @staticmethod
    def buildFailureResponse(message: str, statusCode: int = 400):
        return jsonify({
            "success": False,
            "message": message,
            "status": statusCode
        }), statusCode
    

