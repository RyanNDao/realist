from backend.exceptions import CursorError
from backend.server.utils.CommonLogger import CommonLogger
from backend.server.utils.ResponseBuilder import ResponseBuilder
import traceback
from flask import Blueprint
import logging

exceptionHandlerBp = Blueprint('exceptionHandler', __name__)


@exceptionHandlerBp.app_errorhandler(CursorError)
def handle_db_error(error):
    return ResponseBuilder.buildFailureResponse(f'An error occurred while making a request to the database: {error.cause}', 400)

@exceptionHandlerBp.app_errorhandler(Exception)
def handle_unhandled_error(error):
    CommonLogger.LOGGER.error(traceback.format_exc())
    return ResponseBuilder.buildFailureResponse(f'An unhandled error has occurred: {error}', 400)