from flask import request
from flask import Blueprint

from todo_list.services import task_service
from todo_list.routes import urls

task = Blueprint('task', __name__)


@task.route(urls.add_task, methods=['POST'])
def add():
    """ Method for the route that adds a new task """
    return task_service.add(request)


@task.route(urls.get_task_by_name + '/<string:task_name>')
def get_by_name(task_name):
    """ Method for the route that returns a task based on its name """
    return task_service.get_by_name(request, task_name)


@task.route(urls.get_task_by_status + '/<string:status>')
def get_by_status(status):
    """ Method for the route that returns tasks based on its status """
    return task_service.get_by_status(request, status)


@task.route(urls.get_all_tasks)
def get_all():
    """ Method for the route that returns all tasks """
    return task_service.get_all(request)


@task.route(urls.update_task + '/<string:task_name>', methods=['PUT'])
def update(task_name):
    """ Method for the route that updates a task based on its name """
    return task_service.update(request, task_name)


@task.route(urls.delete_task + '/<string:task_name>', methods=['DELETE'])
def delete(task_name):
    """ Method for the route that deletes a task based on its name """
    return task_service.delete(request, task_name)
