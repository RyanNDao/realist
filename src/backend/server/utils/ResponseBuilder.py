from flask import jsonify

class ResponseBuilder():

    @staticmethod
    def buildSuccessResponse(data: dict, message: str):
        return jsonify({
            "data": data,
            "success": True,
            "message": message,
            "status": 200,
        })
    
    @staticmethod
    def buildFailureResponse(message: str, statusCode: int = 400):
        return jsonify({
            "success": False,
            "message": message,
            "status": statusCode
        })
    

