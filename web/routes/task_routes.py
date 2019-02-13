from flask import request
from flask import jsonify
from flask import Blueprint
from services import task_service
from models.task import Task
import logging

task = Blueprint('task', __name__)


@task.route('/add', methods=['POST'])
def add_task():
    logging.info(f'HTTP Request to add a new task with data: {request}')
    request_json = request.get_json()
    logging.info(f'HTTP Request to add a new task with JSON: {request_json}')

    if not _is_request_json_a_task(request_json):
        logging.info('Incorrect parameters, task was not created')
        return jsonify({'Message': 'Incorrect parameters'}), 400

    new_task = Task(request_json['name'], request_json['description'], request_json['status'].lower())
    if task_service.is_registered(new_task):
        logging.info('There is a task with the same name, task was not created')
        return jsonify({'Message': 'Duplicated task'}), 400

    if new_task.status not in Task.expected_status:
        logging.info(f'Task with invalid status ({new_task.status}), task was not created')
        return jsonify({'Message': "Invalid value in 'status' field. Please use 'to_do', 'doing' or 'done'"})

    task_service.insert(new_task)
    logging.info('Task created successful')
    return jsonify({'name': new_task.name, 'description': new_task.description, 'status': new_task.status}), 201


def _is_request_json_a_task(request_json):
    if 'name' not in request_json or 'description' not in request_json or 'status' not in request_json:
        return False
    return True
