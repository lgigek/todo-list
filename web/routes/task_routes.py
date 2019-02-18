from flask import request
from flask import jsonify
from flask import Blueprint
from services import task_service
from models.task import Task
import logging

task = Blueprint('task', __name__)


@task.route('/add', methods=['POST'])
def add():
    logging.info(f'HTTP Request to add a new task with data: {request}')
    request_json = request.get_json()
    logging.info(f'HTTP Request to add a new task with JSON: {request_json}')

    if not _is_request_json_a_task(request_json):
        logging.info('Incorrect parameters, task was not created')
        return jsonify({'Message': 'Incorrect parameters'}), 400

    new_task = Task(request_json['name'], request_json['description'], request_json['status'].lower())
    if task_service.is_registered(new_task.name):
        logging.info('There is a task with the same name, task was not created')
        return jsonify({'Message': 'Duplicated task'}), 400

    if not _is_status_valid(new_task.status):
        logging.info(f'Task with invalid status ({new_task.status}), task was not created')
        return jsonify({'Message': "Invalid value in 'status' field. Please use 'to_do', 'doing' or 'done'"})

    task_service.insert(new_task)
    logging.info('Task created successful')
    return jsonify({'name': new_task.name, 'description': new_task.description, 'status': new_task.status}), 201


@task.route('/get_by_name/<string:task_name>', methods=['GET'])
def get_by_name(task_name):
    logging.info(f'HTTP Request to get a task by name with data: {request}')
    logging.info(f'Looking for a task with name equal to "{task_name}"')

    task_found = task_service.get_by_name(task_name)
    if task_found is None:
        logging.info('Task not found')
        return jsonify({'Message': 'Task not found'}), 404

    logging.info('Task found, returning its data')
    return jsonify({'name': task_found['name'], 'description': task_found['description'],
                    'status': task_found['status']}), 200


@task.route('/get_by_status/<string:status>', methods=['GET'])
def get_by_status(status):
    logging.info(f'HTTP Request to get tasks by status with data: {request}')
    logging.info(f'Looking for tasks with status equal to "{status}"')

    status = status.lower()

    if not _is_status_valid(status):
        logging.info(f'Invalid status value ({status})')
        return jsonify({'Message': "Invalid status. Please use 'to_do', 'doing' or 'done'"}), 400

    tasks_found = task_service.get_by_status(status)

    logging.info('Returning tasks')
    return_list = []
    for t in tasks_found:
        return_list.append({'name': t['name'], 'description': t['description'],
                            'status': t['status']})

    return jsonify(return_list), 200


@task.route('/get_all', methods=['GET'])
def get_all():
    logging.info(f'HTTP Request to get all tasks with data: {request}')
    logging.info('Returning all tasks')

    tasks_found = task_service.get_all()

    return_list = []
    for t in tasks_found:
        return_list.append({'name': t['name'], 'description': t['description'],
                            'status': t['status']})

    return jsonify(return_list), 200


@task.route('/update/<string:task_name>', methods=['PUT'])
def update(task_name):
    logging.info(f'HTTP Request to update a task with data: {request}')
    request_json = request.get_json()
    logging.info(f'HTTP Request to update task with name {task_name} with JSON: {request_json}')

    if not task_service.is_registered(task_name):
        logging.info('Task not found')
        return jsonify({'Message': 'Task not found'}), 404

    if not _is_request_json_a_task(request_json):
        logging.info('Incorrect parameters')
        return jsonify({'Message': 'Incorrect parameters'}), 400

    task_with_new_values = Task(request_json['name'], request_json['description'], request_json['status'].lower())

    if task_service.is_registered(task_with_new_values.name) and task_with_new_values.name != task_name:
        logging.info('Task not updated, the name would be duplicated')
        return jsonify({'Message': 'Task not updated, the name would be duplicated'}), 400

    if not _is_status_valid(task_with_new_values.status):
        logging.info('Invalid status')
        return jsonify({'Message': "Invalid status. Please use 'to_do', 'doing' or 'done'"}), 400

    task_service.update(task_name, task_with_new_values)
    logging.info('Task updated')
    return jsonify({'name': task_with_new_values.name, 'description': task_with_new_values.description,
                    'status': task_with_new_values.status}), 200


@task.route('/delete/<string:task_name>', methods=['DELETE'])
def delete(task_name):
    logging.info(f'HTTP Request to delete a task with data: {request}')
    logging.info(f'HTTP Request to delete task with name {task_name}')

    if not task_service.is_registered(task_name):
        logging.info('Task not found')
        return jsonify({'Message': 'Task not found'}), 404

    logging.info('Task deleted')
    task_service.delete(task_name)
    return jsonify({'Message': 'Task deleted'}), 200


def _is_request_json_a_task(request_json):
    if 'name' not in request_json or 'description' not in request_json or 'status' not in request_json or \
            request_json['name'] == '' or request_json['description'] == '' or request_json['status'] == '':
        return False
    return True


def _is_status_valid(status):
    if status.lower() in Task.expected_status:
        return True
    return False
