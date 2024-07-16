from flask import Flask
from backend.database.dao.TruliaHouseListingDAO import TruliaHouseListingDAO
from backend.database.services.TruliaHouseListingService import TruliaHouseListingService
from backend.database.services.TruliaScraperSchedulerService import TruliaScraperSchedulerService
from backend.exceptions import CursorError
from backend.database.common.DatabaseConnectionPool import DatabaseConnectionPool
import os
from backend.server.utils.Scheduler import scheduler
from dotenv import load_dotenv
from backend.server.controllers import UserController, TruliaScraperController, TruliaScraperSchedulerController
from flask_injector import FlaskInjector
from injector import singleton, Binder
from backend.database.dao.UserDAO import UserDAO
from backend.database.services.UserService import UserService
from backend.server.configurations import exception_handling_config
import logging
load_dotenv()
LOGGER = logging.getLogger(__name__)


def create_app() -> Flask:

    def configure_injections(binder: Binder):
        user_dao = UserDAO(app.db_pool['users'])
        user_service = UserService(user_dao)
        binder.bind(UserService, to=user_service, scope=singleton)
        trulia_house_listing_dao = TruliaHouseListingDAO(app.db_pool['home_data'])
        trulia_house_listing_service = TruliaHouseListingService(trulia_house_listing_dao)
        binder.bind(TruliaHouseListingService, to=trulia_house_listing_service, scope=singleton)
        binder.bind(TruliaScraperSchedulerService, to=TruliaScraperSchedulerService(), scope=singleton)

    
    app = Flask(__name__)
    app.db_pool = {
        'home_data': DatabaseConnectionPool(connectionString=os.getenv('CONNECTION_STRING_TEMPLATE').format('home_data')),
        'users': DatabaseConnectionPool(connectionString=os.getenv('CONNECTION_STRING_TEMPLATE').format('users'))
    }
    app.register_blueprint(UserController.userControllerBp, url_prefix='/api/user')
    app.register_blueprint(TruliaScraperController.truliaScraperBp, url_prefix='/api/trulia')
    app.register_blueprint(TruliaScraperSchedulerController.truliaScraperSchedulerBp, url_prefix='/api')
    app.register_blueprint(exception_handling_config.exceptionHandlerBp)

    FlaskInjector(app=app, modules=[configure_injections])

    if not hasattr(app, 'scheduler_started'):
        appScheduler = scheduler
        appScheduler.remove_all_jobs()
        appScheduler.start()
        app.scheduler = appScheduler
        app.scheduler_started = True 

    return app

app = create_app()


@app.route('/api/test-error')
def test_error():
    raise CursorError("Test error", cause="This is a test cause")

def main():
    try:
        app.run(debug=True, port=8000, use_reloader=False)
    finally:
        app.scheduler.shutdown()
if __name__ == "__main__":
    main()