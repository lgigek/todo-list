from flask import request
from flask import jsonify
from flask import Blueprint
from services import task_service
from models.task import Task
from routes.task_messages import TaskMessages
import logging

task = Blueprint('task', __name__)


@task.route('/add', methods=['POST'])
def add():
    logging.info(f'HTTP Request to add a new task with data: {request}')
    request_json = request.get_json()
    logging.info(f'HTTP Request to add a new task with JSON: {request_json}')

    if not _is_a_task(request_json):
        logging.info('Incorrect parameters')
        return jsonify({'Message': TaskMessages.incorrect_parameters}), 400

    new_task = Task(request_json['name'], request_json['description'], request_json['status'].lower())
    if task_service.is_registered(new_task.name):
        logging.info('Duplicated task name')
        return jsonify({'Message': TaskMessages.duplicated}), 400

    if not _is_status_valid(new_task.status):
        logging.info('Invalid status')
        return jsonify({'Message': TaskMessages.invalid_status})

    task_service.insert(new_task)
    logging.info('Task created')
    return jsonify({'Message': TaskMessages.created}), 201


@task.route('/get_by_name/<string:task_name>', methods=['GET'])
def get_by_name(task_name):
    logging.info(f'HTTP Request to get a task by name with data: {request}')
    logging.info(f'Looking for a task with name "{task_name}"')

    task_found = task_service.get_by_name(task_name)
    if task_found is None:
        logging.info('Task not found')
        return jsonify({'Message': TaskMessages.not_found}), 404

    logging.info('Returning task')
    return jsonify({'name': task_found['name'], 'description': task_found['description'],
                    'status': task_found['status']}), 200


@task.route('/get_by_status/<string:status>', methods=['GET'])
def get_by_status(status):
    logging.info(f'HTTP Request to get tasks by status with data: {request}')
    logging.info(f'Looking for tasks with status equal to "{status}"')

    status = status.lower()

    if not _is_status_valid(status):
        logging.info('Invalid status')
        return jsonify({'Message': TaskMessages.invalid_status}), 400

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
        if _is_a_task(t):
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
        return jsonify({'Message': TaskMessages.not_found}), 404

    if not _is_a_task(request_json):
        logging.info('Incorrect parameters')
        return jsonify({'Message': TaskMessages.incorrect_parameters}), 400

    task_with_new_values = Task(request_json['name'], request_json['description'], request_json['status'].lower())

    if task_service.is_registered(task_with_new_values.name) and task_with_new_values.name != task_name:
        logging.info('Duplicated task name')
        return jsonify({'Message': TaskMessages.duplicated}), 400

    if not _is_status_valid(task_with_new_values.status):
        logging.info('Invalid status')
        return jsonify({'Message': TaskMessages.invalid_status}), 400

    task_service.update(task_name, task_with_new_values)
    logging.info('Task updated')
    return jsonify({'Message': TaskMessages.updated}), 200


@task.route('/delete/<string:task_name>', methods=['DELETE'])
def delete(task_name):
    logging.info(f'HTTP Request to delete a task with data: {request}')
    logging.info(f'HTTP Request to delete task with name {task_name}')

    if not task_service.is_registered(task_name):
        logging.info('Task not found')
        return jsonify({'Message': TaskMessages.not_found}), 404

    logging.info('Task deleted')
    task_service.delete(task_name)
    return jsonify({'Message': TaskMessages.deleted}), 200


def _is_a_task(obj):
    if 'name' not in obj or 'description' not in obj or 'status' not in obj or \
            obj['name'] == '' or obj['description'] == '' or obj['status'] == '':
        return False
    return True


def _is_status_valid(status):
    if status.lower() in Task.expected_status:
        return True
    return False
