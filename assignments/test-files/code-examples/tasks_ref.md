---
# markdownlint-disable
# vale off

layout: default
description: Complete API reference for tasks resource endpoints
topic_type: reference
test:
  test_apps:
    - json-server@0.17.4
  server_url: localhost:3000
  local_database: /api/to-do-db-source.json
  testable:
    - GET all tasks / 200
    - GET task by ID / 200
    - POST new task / 201
    - PATCH task / 200
    - PUT task / 200
    - DELETE task / 200
# vale  on
# markdownlint-enable
---

# Tasks API

**Author:** `Test Suite`

Complete reference documentation for all tasks resource endpoints in the To-Do Service API.

## `GET` all tasks

Retrieve a list of all tasks in the system.

### `GET` all tasks request

```bash
curl http://{server_url}/tasks
```

### `GET` all tasks response

```json
[
  {
    "userId": 1,
    "title": "Grocery shopping",
    "description": "eggs, bacon, gummy bears",
    "dueDate": "2025-09-20T17:00",
    "warning": "10",
    "id": 1
  },
  {
    "userId": 1,
    "title": "Piano recital",
    "description": "Daughter's first concert appearance",
    "dueDate": "2025-10-02T15:00",
    "warning": "30",
    "id": 2
  },
  {
    "userId": 2,
    "title": "Oil change",
    "description": "5K auto service",
    "dueDate": "2025-11-10T09:00",
    "warning": "60",
    "id": 3
  },
  {
    "userId": 3,
    "title": "Get shots for dog",
    "description": "Annual vaccinations for poochy",
    "dueDate": "2025-12-11T14:00",
    "warning": "20",
    "id": 4
  }
]
```

## `GET` task by ID

Retrieve detailed information about a specific task by its ID.

### `GET` task by ID request

```bash
curl http://{server_url}/tasks/1
```

### `GET` task by ID response

```json
{
  "userId": 1,
  "title": "Grocery shopping",
  "description": "eggs, bacon, gummy bears",
  "dueDate": "2025-09-20T17:00",
  "warning": "10",
  "id": 1
}
```

## `POST` new task

Create a new task in the system.

### `POST` new task request

```bash
curl -X POST http://{server_url}/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "userId": 1,
    "title": "Buy birthday gift",
    "description": "Get something nice for mom",
    "dueDate": "2025-12-15T12:00",
    "warning": "7"
  }'
```

### `POST` new task response

```json
{
  "userId": 1,
  "title": "Buy birthday gift",
  "description": "Get something nice for mom",
  "dueDate": "2025-12-15T12:00",
  "warning": "7",
  "id": 5
}
```

## `PATCH` task

Update specific fields of an existing task without replacing the entire record.

### `PATCH` task request

```bash
curl -X PATCH http://{server_url}/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "description": "eggs, bacon, gummy bears, milk",
    "warning": "5"
  }'
```

### `PATCH` task response

```json
{
  "userId": 1,
  "title": "Grocery shopping",
  "description": "eggs, bacon, gummy bears, milk",
  "dueDate": "2025-09-20T17:00",
  "warning": "5",
  "id": 1
}
```

## `PUT` task

Replace an entire task record with new data.

### `PUT` task request

```bash
curl -X PUT http://{server_url}/tasks/2 \
  -H "Content-Type: application/json" \
  -d '{
    "userId": 1,
    "title": "Piano recital - updated",
    "description": "Daughter'\''s concert at the community center",
    "dueDate": "2025-10-02T18:00",
    "warning": "14"
  }'
```

### `PUT` task response

```json
{
  "userId": 1,
  "title": "Piano recital - updated",
  "description": "Daughter's concert at the community center",
  "dueDate": "2025-10-02T18:00",
  "warning": "14",
  "id": 2
}
```

## `DELETE` task

Remove a task from the system.

### `DELETE` task request

```bash
curl -X DELETE http://{server_url}/tasks/3
```

### `DELETE` task response

```json
{}
```
