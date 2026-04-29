---
# markdownlint-disable
# vale off
layout: default
description: User Management
topic_type: reference
# vale  on
# markdownlint-enable
---

# Assignment 5.3 : code examples from curl and Postman

<!-- vale Google.Acronyms = off -->
<!-- vale Google.Headings = off -->

<!-- vale off -->

**Author:** Khushbu Borole

<!-- vale on -->

<!-- vale Vale.Terms = NO -->
<!-- The terminology consistency is very strict-->

The endpoints in this document allows you to manage users via curl and postman.

## Client URL examples - curl

curl is a command-line tool used to interact with API from a terminal. In this section,
you’ll fetch user details and create new users using the API.

Wherever you see {server_url}, it refers to your server’s base URL. For example,
you might use localhost:3000.

### `GET` curl example

This request fetched details of user with id=1

#### `GET` curl example request

```bash
curl http://{server_url}/users/1
```

#### `GET` curl example response

```json
{
  "lastName": "Smith",
  "firstName": "Ferdinand",
  "email": "f.smith@example.com",
  "id": 1
}
```

### `POST` curl example

This request adds a new user names Jane Doe which has id=5

#### `POST` curl example request

```bash
curl -X POST http://{server_url}/users \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Jane",
    "lastName": "Doe",
    "email": "jane.doe@example.com"
  }'
```

#### `POST` curl example response

```json
{
  "firstName": "Jane",
  "lastName": "Doe",
  "email": "jane.doe@example.com",
  "id": 5
}
```

## Postman examples

Postman is a UI tool that allows you to interact with API. It's like
curl but with UI. In this section, you’ll fetch user details and create
new users using the API.

Wherever you see {server_url}, it refers to your server’s base URL.
For example, you might use localhost:3000.

### `GET` postman example

This request fetched details of a task whose id = 1

#### `GET` postman example request

```bash
http://{server_url}/tasks/1
```

#### `GET` postman example response

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

### `POST` postman example

This request adds a new task

#### `POST` postman example request

```bash
http://{server_url}/tasks
```

##### `POST` postman request headers

```text
Access-Control-Expose-Headers  Location
Location  http://localhost:3000/tasks/6
```

##### `POST` postman request data

```json
{
    "userId": 6,
    "title": "Assignment",
    "description": "Complete UW API course assignment",
    "dueDate": "2026-06-30T17:00",
    "warning": "7"
}
```

#### `POST` postman example response

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
