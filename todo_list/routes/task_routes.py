from flask import request
from flask import Blueprint

from todo_list.services import task_service

task = Blueprint('task', __name__)


@task.route('/add', methods=['POST'])
def add():
    return task_service.add(request)


@task.route('/get_by_name/<string:task_name>', methods=['GET'])
def get_by_name(task_name):
    return task_service.get_by_name(request, task_name)


@task.route('/get_by_status/<string:status>', methods=['GET'])
def get_by_status(status):
    return task_service.get_by_status(request, status)


@task.route('/get_all', methods=['GET'])
def get_all():
    return task_service.get_all(request)


@task.route('/update/<string:task_name>', methods=['PUT'])
def update(task_name):
    return task_service.update(request, task_name)


@task.route('/delete/<string:task_name>', methods=['DELETE'])
def delete(task_name):
    return task_service.delete(request, task_name)
