from dbs.mongo import tasks


def is_registered(task):
    if tasks.find({'name': task.name}).count() > 0:
        return True
    else:
        return False


def insert(task):
    tasks.insert_one(task.__dict__)
