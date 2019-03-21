# todo-list
This is a CRUD to manage tasks.

## Running the application
This application uses docker compose. It is necessary to run the following commands to run the application:

`docker-compose build`

`docker-compose up`

The application will be running on port 5000 (it can be changed in `.env` file)

## Running tests
To run tests, is necessary to execute "bash" the container and run the test there.

- `docker ps`: to get the container id of the python application;

- `docker exec -it <container_id> bash`: to execute "bash" on the python application container;

- `nose2`: to run the tests;

## Routes
Basically there are six routes, they are:
- `/add`;
- `/get_all`;
- `/get_by_status/<status>`;
- `/get_by_name/<task_name>`;
- `/update/<task_name>`
- `/delete/<task_name>`

You also can see the details of all routes in the [wiki page](https://github.com/lgigek/todo_list_python/wiki/Route-details).
