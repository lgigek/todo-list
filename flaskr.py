from flask import Flask
from todo_list.routes.task_routes import task
from todo_list.log import log_formatter

app = Flask(__name__)

app.register_blueprint(task, url_prefix='/task')

# Disable flask jsonify from sorting alphabetically
app.config['JSON_SORT_KEYS'] = False
