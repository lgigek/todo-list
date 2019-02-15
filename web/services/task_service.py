from dbs.mongo import tasks


def is_registered(task):
    if tasks.find({'name': task.name}).count() > 0:
        return True
    else:
        return False


def get_by_name(task_name):
    return tasks.find_one({'name': task_name})


def get_by_status(status):
    return list(tasks.find({'status': status}))


def get_all():
    return list(tasks.find({}))


def insert(task):
    tasks.insert_one(task.__dict__)
