from flask import jsonify
import logging

from todo_list.log.formatter import logger_name
from todo_list.repositories import task_repository
from todo_list.models.task import Task
from todo_list.routes.task_messages import TaskMessages

logger = logging.getLogger(logger_name)


def add(request):
    logger.info(f'HTTP Request to add a new task with data: {request}')
    request_json = request.get_json()
    logger.info(f'HTTP Request to add a new task with JSON: {request_json}')

    if not _is_a_task(request_json):
        logger.info('Incorrect parameters')
        return jsonify({'Message': TaskMessages.incorrect_parameters}), 400

    new_task = Task(request_json['name'], request_json['description'], request_json['status'].lower())
    if task_repository.is_registered(new_task.name):
        logger.info('Duplicated task name')
        return jsonify({'Message': TaskMessages.duplicated}), 400

    if not _is_status_valid(new_task.status):
        logger.info('Invalid status')
        return jsonify({'Message': TaskMessages.invalid_status}), 400

    task_repository.insert(new_task)
    logger.info('Task created')
    return jsonify({'Message': TaskMessages.created}), 201


def get_by_name(request, task_name):
    logger.info(f'HTTP Request to get a task by name with data: {request}')
    logger.info(f'Looking for a task with name "{task_name}"')

    task_found = task_repository.get_by_name(task_name)
    if task_found is None:
        logger.info('Task not found')
        return jsonify({'Message': TaskMessages.not_found}), 404

    logger.info('Returning task')
    return jsonify({'name': task_found['name'], 'description': task_found['description'],
                    'status': task_found['status']}), 200


def get_by_status(request, status):
    logger.info(f'HTTP Request to get tasks by status with data: {request}')
    logger.info(f'Looking for tasks with status equal to "{status}"')

    status = status.lower()

    if not _is_status_valid(status):
        logger.info('Invalid status')
        return jsonify({'Message': TaskMessages.invalid_status}), 400

    tasks_found = task_repository.get_by_status(status)

    logger.info('Returning tasks')
    return_list = []
    for t in tasks_found:
        if _is_a_task(t):
            return_list.append({'name': t['name'], 'description': t['description'],
                                'status': t['status']})

    return jsonify(return_list), 200


def get_all(request):
    logger.info(f'HTTP Request to get all tasks with data: {request}')
    logger.info('Returning all tasks')

    tasks_found = task_repository.get_all()

    return_list = []
    for t in tasks_found:
        if _is_a_task(t):
            return_list.append({'name': t['name'], 'description': t['description'],
                                'status': t['status']})

    return jsonify(return_list), 200


def update(request, task_name):
    logger.info(f'HTTP Request to update a task with data: {request}')
    request_json = request.get_json()
    logger.info(f'HTTP Request to update task with name {task_name} with JSON: {request_json}')

    if not task_repository.is_registered(task_name):
        logger.info('Task not found')
        return jsonify({'Message': TaskMessages.not_found}), 404

    if not _is_a_task(request_json):
        logger.info('Incorrect parameters')
        return jsonify({'Message': TaskMessages.incorrect_parameters}), 400

    task_with_new_values = Task(request_json['name'], request_json['description'], request_json['status'].lower())

    if task_repository.is_registered(task_with_new_values.name) and task_with_new_values.name != task_name:
        logger.info('Duplicated task name')
        return jsonify({'Message': TaskMessages.duplicated}), 400

    if not _is_status_valid(task_with_new_values.status):
        logger.info('Invalid status')
        return jsonify({'Message': TaskMessages.invalid_status}), 400

    task_repository.update(task_name, task_with_new_values)
    logger.info('Task updated')
    return jsonify({'Message': TaskMessages.updated}), 200


def delete(request, task_name):
    logger.info(f'HTTP Request to delete a task with data: {request}')
    logger.info(f'HTTP Request to delete task with name {task_name}')

    if not task_repository.is_registered(task_name):
        logger.info('Task not found')
        return jsonify({'Message': TaskMessages.not_found}), 404

    logger.info('Task deleted')
    task_repository.delete(task_name)
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
