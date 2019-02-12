# todo_list_python
This is a CRUD to manage tasks.

## Running the application
This application uses docker compose. It is necessary to run the following commands to run the application:

`docker-compose build`

`docker-compose up`

The application will be running on port 5000 (it can be changed in `.env` file)

## Routes
`/add_task`: HTTP route to create a new task

### /add_task
This route expects an POST with a Json that contains the task data.

Json example:

```
{
    "name": "task_name",
    "description": "task_description",
    "status": "task_status"
} 
```

Returns:
- HTTP 201 if task was created:

```
{
    "description": "task_description",
    "name": "task_name",
    "status": "task_status"
}
```

- HTTP 400 if there is a task created with the same name:

```
{
    "Message": "Task task_name was not created because it is already registered"
}
```
 
- HTTP 400 if Json does not contains necessary fields:

```
{
    "Message": "Incorrect parameters"
}
``` 