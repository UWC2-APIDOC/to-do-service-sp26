---
# markdownlint-disable
# vale off

layout: default
description: Local database that contains users and tasks
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

# To-Do Service examples

<!-- vale Google.Acronyms = off -->

**Author:** `Maya Nakamura`

Local database that contains users and tasks

## `cURL` examples

GET and POST requests where {server_url} is localhost:3000

### `GET` example using `cURL`

Request data of user with id 1.

#### `GET` example request using `cURL`

```bash
curl http://{server_url}/users/1
```

#### `GET` example response using `cURL`

```json
{
  "lastName": "Smith",
  "firstName": "Ferdinand",
  "email": "f.smith@example.com",
  "id": 1
}
```

### `POST` example using `cURL`

Submit data to create a user with a new id.

#### `POST` example request using `cURL`

```bash
curl -X POST http://{server_url}/users \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Jane",
    "lastName": "Doe",
    "email": "jane.doe@example.com"
  }'
```

#### `POST` example response using `cURL`

```json
{
  "firstName": "Jane",
  "lastName": "Doe",
  "email": "jane.doe@example.com",
  "id": 5
}
```

## `Postman` examples

GET and POST requests where {server_url} is localhost:3000

### `GET` example using `Postman`

Request data of user with id 1.

#### `GET` example request using `Postman`

```bash
{server_url}/users/1
```

#### `GET` example response using `Postman`

```json
{
    "lastName": "Smith",
    "firstName": "Ferdinand",
    "email": "f.smith@example.com",
    "id": 1
}
```

### `POST` example using `Postman`

Submit data to create a user with a new id.

#### `POST` example request using `Postman`

```bash
{server_url}/users
```

##### `POST` request headers using `Postman`

No headers needed.

##### `POST` request data using `Postman`

```json
{
    "lastName": "Hancock",
    "firstName": "John",
    "email": "j.hancock@example.com"
}
```

#### `POST` example response using `Postman`

```json
{
    "lastName": "Hancock",
    "firstName": "John",
    "email": "j.hancock@example.com",
    "id": 6
}
```
