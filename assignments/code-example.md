---
# markdownlint-disable
# vale off

layout: default
description: <REPLACE with description of this API endpoint>
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

# {INSERT page title}

<!-- vale Google.Acronyms = off -->

**Author:** `<REPLACE WITH your name>`

{REPLACE WITH a brief description of what this endpoint does.}

## curl examples

{REPLACE WITH an overview of this section. Be sure to explain what {server_url} means if you use it.}

### `GET` example (curl)

{REPLACE WITH a description of the `GET` request and what it returns.}

#### `GET` example request (curl)

```bash
curl http://{server_url}/users/1
```

#### `GET` example response (curl)

```json
{REPLACE WITH a response buffer from the `GET` request.}
```

### `POST` example (curl)

{REPLACE WITH a description of the `POST` request and what it creates.}

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
{REPLACE WITH a response buffer from the `POST` request.}
```

## Postman examples

{REPLACE WITH an overview of this section. Be sure to explain what {server_url} means if you use it.}

### `GET` example (Postman)

{REPLACE WITH a description of the `GET` request and what it returns.}

#### `GET` example request (Postman)

```bash
{Replace with URL used in your Postman request}
```

#### `GET` example response (Postman)

```json
{REPLACE WITH a response buffer from the `GET` request.}
```

### `POST` example (Postman)

{REPLACE WITH a description of the `POST` request and what it creates.}

#### `POST` example request (Postman)

```bash
{Replace with URL used in your Postman request}
```

##### `POST` request headers (Postman)

```text
{REPLACE WITH the request headers used by the `POST` request.}
```

##### `POST` request data (Postman)

```json
{REPLACE WITH a data buffer for the `POST` request.}
```

#### `POST` example response (Postman)

```json
{REPLACE WITH a data buffer from the `POST` request.}
```
