from flask import Flask
from flask import request
from flask import jsonify
from services import task_service
from models.task import Task

app = Flask(__name__)


@app.route('/add_task', methods=['POST'])
def add_task():
    request_json = request.get_json()

    if not _is_request_json_a_task(request_json):
        return jsonify({'Message': 'Incorrect parameters'}), 400

    task = Task(request_json['name'], request_json['description'], request_json['status'])
    if task_service.is_registered(task):
        return jsonify({'Message': 'Duplicated task'}), 400
    else:
        task_service.insert(task)
        return jsonify({'name': task.name, 'description': task.description, 'status': task.status}), 201


def _is_request_json_a_task(request_json):
    if 'name' not in request_json or 'description' not in request_json or 'status' not in request_json:
        return False
    return True
