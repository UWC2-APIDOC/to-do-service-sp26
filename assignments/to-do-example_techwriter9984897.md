---
# markdownlint-disable
# vale off

layout: default
description: Gets information from http://localhost:3000/
topic_type: reference
# test:
#   test_apps:
#     - json-server@0.17.4
#   server_url: localhost:3000
#   local_database: /api/to-do-db-source.json
#   testable:
#     - GET example / 200
#     - POST example / 201
# vale  on
# markdownlint-enable
---

# {API 216}

<!-- vale Google.Acronyms = off -->

**Author:** `<Hillary Donaghy>`

Pulls information and updated information from the database.

## curl examples

This action retrieves data from the database about a user.

### `GET` example (curl)

Getting information about user number 4.

#### `GET` example request (curl)

```bash
curl http://localhost:3000/users/4
```

#### `GET` example response (curl)

```json
{
  "lastName": "Bailey",
  "firstName": "Bill",
  "email": "b.bailey@example.com",
  "id": 4
}%   }
```

### `POST` example (curl)

This action posts information to the server.

#### `POST` example request (curl)

```bash
curl -X POST http://localhost:3000/users \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Jane",
    "lastName": "Doe",
    "email": "jane.doe@example.com"
  }'
```

#### `POST` example response (curl)

```json
{
  "firstName": "Jane",
  "lastName": "Doe",
  "email": "jane.doe@example.com",
  "id": 5
}%  
```

## Postman examples

Getting and posting information from the database.

### `GET` example (Postman)

http://localhost:3000/tasks?user_id=1

#### `GET` example request (Postman)

```bash
Get hhttp://localhost:3000/tasks?user_id=1
```

#### `GET` example response (Postman)

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
    },
    {
        "id": 5
    },
    {
        "task_title": "Get new tires",
        "task_description": "Get new tires for Hoppity",
        "task_due_date": "2025-03-11T14:00",
        "task_warning": "-60",
        "id": 6
    }
```

### `POST` example (Postman)

Posting information about tasks.
#### `POST` example request (Postman)

```bash
Post http://localhost:3000/tasks
```

##### `POST` request headers (Postman)

```text
http://localhost:3000/tasks
```

##### `POST` request data (Postman)

```json
{
    "task_title": "Get new tires",
    "task_description": "Get new tires for Hoppity",
    "task_due_date": "2025-03-11T14:00",
    "task_warning": "-60"
}
```

#### `POST` example response (Postman)

```json
{
    "task_title": "Get new tires",
    "task_description": "Get new tires for Hoppity",
    "task_due_date": "2025-03-11T14:00",
    "task_warning": "-60",
    "id": 6
}
