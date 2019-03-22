from todo_list.dbs.mongo import tasks

"""
This module manipulates the instance of a collection from MongoDb
"""


def is_registered(task_name):
    """ Verifies if there is a task with the informed name """
    if tasks.find({'name': task_name}).count() > 0:
        return True
    else:
        return False


def get_by_name(task_name):
    """ Returns the first task with the informed name """
    return tasks.find_one({'name': task_name})


def get_by_status(status):
    """ Returns all tasks with matching status """
    return list(tasks.find({'status': status}))


def get_all():
    """ Returns all the tasks """
    return list(tasks.find({}))


def update(task_name, task):
    """ Updates a task based on its name """
    tasks.update(
        {'name': task_name}, {"$set": {'name': task.name, 'description': task.description, 'status': task.status}})


def insert(task):
    """ Inserts a new task """
    tasks.insert_one(task.__dict__)


def delete(task_name):
    """ Deletes a task based on its name """
    tasks.delete_one({'name': task_name})
