# todo-list
This is a CRUD to manage tasks.

## Running the application
This application uses docker compose. It is necessary to run the following commands to run the application:

`docker-compose build`

`docker-compose up`

The application will be running on port 5000 (it can be changed in `.env` file)

## Setting your local environment up
As this project uses [pipenv](https://github.com/pypa/pipenv), it is necessary to have it installed on your local machine.

After installing pipenv, run `pipenv shell` to access no your virtual environment.

Then, install the dev dependencies by running this command: `pipenv install --dev --ignore-pipfile`.

### Running the tests
On your local environment, simply run `nose2`.

## Routes
Basically there are six routes, they are:
- `/add`;
- `/get_all`;
- `/get_by_status/<status>`;
- `/get_by_name/<task_name>`;
- `/update/<task_name>`
- `/delete/<task_name>`

You also can see the details of all routes in the [wiki page](https://github.com/lgigek/todo_list_python/wiki/Route-details).

In addition, it is possible to import `insomnia.json` (located on `docs/`) to [Insomnia](https://insomnia.rest/).