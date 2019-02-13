# todo_list_python
This is a CRUD to manage tasks.

## Running the application
This application uses docker compose. It is necessary to run the following commands to run the application:

`docker-compose build`

`docker-compose up`

The application will be running on port 5000 (it can be changed in `.env` file)

## Routes
All routes have the prefix `/task`. Example, to add a task, is necessary to make a request do `/task/add`.   

`/add`: HTTP route to create a new task

### /add
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

- HTTP 400 if "status" field id different from `to_do`, `doing` or `done`:

```
{
  "Message": "Invalid value in 'status' field. Please use 'to_do', 'doing' or 'done'"
}
``` 