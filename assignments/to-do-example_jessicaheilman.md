---
# markdownlint-disable
# vale off

layout: default
description: Examples of GET and Post requests to the `/users` endpoint using curl and Postman
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

# Requests to the To-Do Service

<!-- vale Google.Acronyms = off -->

**Author:** `Jessica Heilman`

Manages users of the To-Do Service using the `/users` endpoint.

## curl examples

The examples in the following show GET and POST requests to the `/users` endpoint using curl.

### `GET` example (curl)

Retrieves a user

#### `GET` example request (curl)

```bash
curl http://localhost:3000/users/1
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

Posts a user

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
}
```

## Postman examples

The examples in the following show GET and POST requests to the `/users` endpoint using Postman.

### `GET` example (Postman)

Returns a user

#### `GET` example request (Postman)

```bash
http://localhost:3000/users/1
```

#### `GET` example response (Postman)

```json
{
    "lastName": "Smith",
    "firstName": "Ferdinand",
    "email": "f.smith@example.com",
    "id": 1
}
```

### `POST` example (Postman)

Creates a new user.

#### `POST` example request (Postman)

```bash
http://localhost:3000/users
```

##### `POST` request headers (Postman)

```text
Content-Type: application/json
```

##### `POST` request data (Postman)

```json
{
  "firstName": "Jane",
  "lastName": "Doe",
  "email": "jane.doe@example.com"
}
```

#### `POST` example response (Postman)

```json
{
    "firstName": "Jane",
    "lastName": "Doe",
    "email": "jane.doe@example.com",
    "id": 6
}
```
