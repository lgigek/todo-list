import logging
import os
from flask import jsonify
from flask import request

from todo_list.repositories import task_repository
from todo_list.models.task import Task
from todo_list.services.task_messages import TaskMessages

logger = logging.getLogger(os.environ.get('LOGGER_NAME'))


def add(req: request):
    """
    Adds a new task.

    It may return 400 if payload does not contain the necessary fields (name, description and status).
    It may return 400 if payload contains the name of a task that is already registered.
    It may return 400 if payload contains status with invalid value.
    If everything goes well, it returns 201.
    """
    logger.info(f'HTTP Request to add a new task with data: {req}')
    request_payload = req.get_json()
    logger.info(f'HTTP Request to add a new task with payload: {request_payload}')

    # Verifies if payload is valid
    if not _is_a_task(request_payload):
        logger.info('Incorrect parameters')
        return jsonify({'Message': TaskMessages.incorrect_parameters}), 400

    new_task: Task = Task(request_payload['name'], request_payload['description'],
                          request_payload['status'].lower())

    # Verifies if there is a task with same name
    if task_repository.is_registered(new_task.name):
        logger.info('Duplicated task name')
        return jsonify({'Message': TaskMessages.duplicated}), 400

    # Verifies if payload "status" is valid
    if not _is_status_valid(new_task.status):
        logger.info('Invalid status')
        return jsonify({'Message': TaskMessages.invalid_status}), 400

    # Creates the task!
    task_repository.insert(new_task)
    logger.info('Task created')
    return jsonify({'Message': TaskMessages.created}), 201


def get_by_name(req: request, task_name: str):
    """
    Returns a task based on its name.

    It may return 404 if task was not found.
    If the task was found, returns 200.
    """
    logger.info(f'HTTP Request to get a task by name with data: {req}')
    logger.info(f'Looking for a task with name "{task_name}"')

    # Gets a task by its name
    task_found: Task = task_repository.get_by_name(task_name)

    # Verifies if task exists
    if task_found is None:
        logger.info('Task not found')
        return jsonify({'Message': TaskMessages.not_found}), 404

    # Returns the task!
    logger.info('Returning task')
    return jsonify({'name': task_found['name'], 'description': task_found['description'],
                    'status': task_found['status']}), 200


def get_by_status(req: request, status: str):
    """
    Returns a list of tasks based on its status.

    It may return 400 if the status is invalid
    If the status is valid, returns 200.
    """
    logger.info(f'HTTP Request to get tasks by status with data: {req}')
    logger.info(f'Looking for tasks with status equal to "{status}"')

    status = status.lower()

    # Verifies if status is valid
    if not _is_status_valid(status):
        logger.info('Invalid status')
        return jsonify({'Message': TaskMessages.invalid_status}), 400

    # Gets tasks by status
    tasks_found: list = task_repository.get_by_status(status)

    # Creates list to return tasks
    logger.info('Returning tasks')
    return_list = []
    for t in tasks_found:
        if _is_a_task(t):
            return_list.append({'name': t['name'], 'description': t['description'],
                                'status': t['status']})

    # Returns tasks!
    return jsonify(return_list), 200


def get_all(req: request):
    """
    Returns a list with all the tasks.

    It always returns 200.
    """
    logger.info(f'HTTP Request to get all tasks with data: {req}')
    logger.info('Returning all tasks')

    # Gets all tasks
    tasks_found: list = task_repository.get_all()

    # Creates list to return tasks
    return_list = []
    for t in tasks_found:
        if _is_a_task(t):
            return_list.append({'name': t['name'], 'description': t['description'],
                                'status': t['status']})

    # Returns all tasks!
    return jsonify(return_list), 200


def update(req: request, task_name: str):
    """
    Updates an existing task.

    It may return 404 if task was not found.
    It may return 400 if payload does not contain the necessary fields (name, description and status).
    It may return 400 if payload contains the name of a task that is already registered.
    It may return 400 if payload contains status with invalid value.
    If everything goes well, it returns 200.
    """
    logger.info(f'HTTP Request to update a task with data: {req}')
    request_payload = req.get_json()
    logger.info(f'HTTP Request to update task with name {task_name} with payload: {request_payload}')

    # Verifies if task exists
    if not task_repository.is_registered(task_name):
        logger.info('Task not found')
        return jsonify({'Message': TaskMessages.not_found}), 404

    # Verifies if payload is valid
    if not _is_a_task(request_payload):
        logger.info('Incorrect parameters')
        return jsonify({'Message': TaskMessages.incorrect_parameters}), 400

    task_with_new_values: Task = Task(request_payload['name'], request_payload['description'],
                                      request_payload['status'].lower())

    # Verifies if there is a task with same name
    if task_repository.is_registered(task_with_new_values.name) and task_with_new_values.name != task_name:
        logger.info('Duplicated task name')
        return jsonify({'Message': TaskMessages.duplicated}), 400

    # Verifies if payload "status" is valid
    if not _is_status_valid(task_with_new_values.status):
        logger.info('Invalid status')
        return jsonify({'Message': TaskMessages.invalid_status}), 400

    # Updates the task!
    task_repository.update(task_name, task_with_new_values)
    logger.info('Task updated')
    return jsonify({'Message': TaskMessages.updated}), 200


def delete(req: request, task_name: str):
    """
    Deletes a task.

    It may return 404 if task was not found.
    It returns 200 if task was delete.
    """
    logger.info(f'HTTP Request to delete a task with data: {req}')
    logger.info(f'HTTP Request to delete task with name {task_name}')

    if not task_repository.is_registered(task_name):
        logger.info('Task not found')
        return jsonify({'Message': TaskMessages.not_found}), 404

    logger.info('Task deleted')
    task_repository.delete(task_name)
    return jsonify({'Message': TaskMessages.deleted}), 200


def _is_a_task(obj):
    """
    Verifies if the parameter "obj" contains the necessary fields do be a task.

    The necessary fields are "name", "description" and "status"

    If returns True if "obj" contains all fields and returns "False" if does not.
    """

    if 'name' not in obj or 'description' not in obj or 'status' not in obj or \
            obj['name'] == '' or obj['description'] == '' or obj['status'] == '':
        return False
    return True


def _is_status_valid(status: str):
    """
    Verifies if the parameter "status" is valid.

    The status is valid if it is in "Task.expected_status".

    It returns True if "status" is valid and return False if does not.
    """

    if status.lower() in Task.expected_status:
        return True
    return False
