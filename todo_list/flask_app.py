import logging
from flask import Flask

from todo_list.routes.task_routes import task


def create_app():
    """ Creates and returns a flask instance. Also sets some configurations """
    app = Flask(__name__)

    # Adds task blueprint
    app.register_blueprint(task, url_prefix='/task')

    # Disable alphabetically sort on flask.jsonify()
    app.config['JSON_SORT_KEYS'] = False

    # Enabling log in application
    setup_log()

    return app


def setup_log():
    """ Sets a pattern to 'logger' log """
    logger = logging.getLogger(__name__)

    my_formatter = logging.Formatter("%(asctime)s %(levelname)7s "
                                     "[%(filename)s:%(lineno)s - %(funcName)20s()] %(message)s")

    my_handler = logging.StreamHandler()
    my_handler.setFormatter(my_formatter)

    logger.addHandler(my_handler)
    logger.setLevel(logging.DEBUG)
