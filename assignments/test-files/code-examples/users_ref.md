---
# markdownlint-disable
# vale off

layout: default
description: Complete API reference for users resource endpoints
topic_type: reference
test:
  test_apps:
    - json-server@0.17.4
  server_url: localhost:3000
  local_database: /api/to-do-db-source.json
  testable:
    - GET all users / 200
    - GET user by ID / 200
    - POST new user / 201
    - PATCH user / 200
    - PUT user / 200
    - DELETE user / 200
# vale  on
# markdownlint-enable
---

# Users API

**Author:** `Test Suite`

Complete reference documentation for all users resource endpoints in the To-Do Service API.

## `GET` all users

Retrieve a list of all users in the system.

### `GET` all users request

```bash
curl http://{server_url}/users
```

### `GET` all users response

```json
[
  {
    "lastName": "Smith",
    "firstName": "Ferdinand",
    "email": "f.smith@example.com",
    "id": 1
  },
  {
    "lastName": "Jones",
    "firstName": "Jill",
    "email": "j.jones@example.com",
    "id": 2
  },
  {
    "lastName": "Martinez",
    "firstName": "Marty",
    "email": "m.martinez@example.com",
    "id": 3
  },
  {
    "lastName": "Bailey",
    "firstName": "Bill",
    "email": "b.bailey@example.com",
    "id": 4
  }
]
```

## `GET` user by ID

Retrieve detailed information about a specific user by their ID.

### `GET` user by ID request

```bash
curl http://{server_url}/users/1
```

### `GET` user by ID response

```json
{
  "lastName": "Smith",
  "firstName": "Ferdinand",
  "email": "f.smith@example.com",
  "id": 1
}
```

## `POST` new user

Create a new user in the system.

### `POST` new user request

```bash
curl -X POST http://{server_url}/users \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Jane",
    "lastName": "Doe",
    "email": "jane.doe@example.com"
  }'
```

### `POST` new user response

```json
{
  "firstName": "Jane",
  "lastName": "Doe",
  "email": "jane.doe@example.com",
  "id": 5
}
```

## `PATCH` user

Update specific fields of an existing user without replacing the entire record.

### `PATCH` user request

```bash
curl -X PATCH http://{server_url}/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "email": "ferdinand.smith.updated@example.com"
  }'
```

### `PATCH` user response

```json
{
  "lastName": "Smith",
  "firstName": "Ferdinand",
  "email": "ferdinand.smith.updated@example.com",
  "id": 1
}
```

## `PUT` user

Replace an entire user record with new data.

### `PUT` user request

```bash
curl -X PUT http://{server_url}/users/2 \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Jillian",
    "lastName": "Jones-Anderson",
    "email": "jillian.jones@example.com"
  }'
```

### `PUT` user response

```json
{
  "firstName": "Jillian",
  "lastName": "Jones-Anderson",
  "email": "jillian.jones@example.com",
  "id": 2
}
```

## `DELETE` user

Remove a user from the system.

### `DELETE` user request

```bash
curl -X DELETE http://{server_url}/users/3
```

### `DELETE` user response

```json
{}
```
