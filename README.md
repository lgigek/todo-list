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
`/get_by_name/<task_name>`: HTTP route to get a task by its name
`/get_by_status/<status>`: HTTP route to get tasks by its status
`/get_all`: HTTP route to get all tasks 
`/update/<task_name>`: HTTP route to update a task by its name

### /add
This route expects a POST with a Json that contains the task data.

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
  "name": "task_name",
  "description": "task_description",
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

### /get_by_name/<task_name>
This route expects a GET with the task name in path variable

Returns: 
- HTTP 200 if task was found:

```
{
  "name": "task_name",
  "description": "task_description",
  "status": "task_status"
}
```

- HTTP 404 if task was not found:

```
{
  "Message": "Task not found"
}
```

### /get_by_status/<status>
This route expects a GET with the status in path variable

Returns: 
- HTTP 200 if tasks were found:

```
[
  {
    "name": "task_name",
    "description": "task_description",
    "status": "task_status"
  }
  ...
]
```

- HTTP 400 if status is invalid:

```
{
  "Message": "Invalid status. Please use 'to_do', 'doing' or 'done'"
}
```

- HTTP 404 is there are no tasks with a valid status:

```
{
  "Message": "Task not found"
}
```

### /get_all
This route expects a GET

Returns: 
- HTTP 200 if tasks were found:

```
[
  {
    "name": "task_name",
    "description": "task_description",
    "status": "task_status"
  }
  ...
]
```

- HTTP 404 is there are no tasks with a valid status:

```
{
  "Message": "Task not found"
}
```

### /update/<task_name>
This route expects a PUT with a Json that contains the new data 