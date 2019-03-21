class Task:

    expected_status = ['to_do', 'doing', 'done']

    def __init__(self, name, description, status):
        self.name = name
        self.description = description
        self.status = status
