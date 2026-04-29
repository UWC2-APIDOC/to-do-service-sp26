<!--
# markdownlint-disable
# vale off

layout: default
description: User Management
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
-->

# Assignment 5.3 : code examples from curl and postman

<!-- vale Google.Acronyms = off -->

**Author:** Khushbu Borole 

The endpoints in this document allows you to manage users via cURL and Postman.

## curl examples

cURL is a command-line tool used to interact with APIs from a terminal. In this section, you’ll fetch user details and create new users using the API.

Wherever you see {server_url}, it refers to your server’s base URL. For example, you might use localhost:3000.

### `GET` example (curl)

This request fetched details of user with id=1

#### `GET` example request (curl)

```bash
curl http://{server_url}/users/1
```

#### `GET` example response (curl)

```json
{
  "lastName": "Smith",
  "firstName": "Ferdinand",
  "email": "f.smith@example.com",
  "id": 1
}
```

### `POST` example (curl)

This request adds a new user names Jane Doe which has id=5

#### `POST` example request (curl)

```bash
curl -X POST http://{server_url}/users \
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
}
```

## Postman examples

Postman is a UI tool that allows you to interact with APIs. It is similar like cURL but with UI. In this section, you’ll fetch user details and create new users using the API.

Wherever you see {server_url}, it refers to your server’s base URL. For example, you might use localhost:3000.

### `GET` example (Postman)

This request fetched details of a task whose id = 1

#### `GET` example request (Postman)

```bash
http://{server_url}/tasks/1
```

#### `GET` example response (Postman)

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

### `POST` example (Postman)

This request adds a new task

#### `POST` example request (Postman)

```bash
http://{server_url}/tasks
```

##### `POST` request headers (Postman)

```text
Access-Control-Expose-Headers  Location
Location  http://localhost:3000/tasks/6
```

##### `POST` request data (Postman)

```json
{
    "userId": 6,
    "title": "Assignment",
    "description": "Complete UW API course assignment",
    "dueDate": "2026-06-30T17:00",
    "warning": "7"
}
```

#### `POST` example response (Postman)

```json
{
    "userId": 6,
    "title": "Assignment",
    "description": "Complete UW API course assignment",
    "dueDate": "2026-06-30T17:00",
    "warning": "7",
    "id": 5
}
```
