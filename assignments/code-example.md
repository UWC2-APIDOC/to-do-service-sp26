---
# markdownlint-disable
# vale off

layout: default
description: <REPLACE WITH description of this API endpoint>
topic_type: reference
test:
  test_apps:
    - json-server@0.17.4
  server_url: localhost:3000
  local_database: /api/to-do-db-source.json
  testable:
    - GET example / 200
    - POST example / 201
# vale  on
# markdownlint-enable
---

# {REPLACE WITH endpoint name}

**Author:** `<REPLACE WITH your name>`

Brief description of what this endpoint does.

## `GET` example

Description of the `GET` request and what it returns.

### `GET` example request

```bash
curl http://{server_url}/users/1
```

### `GET` example response

```json
{
  "id": 1,
  "firstName": "Ferdinand",
  "lastName": "Smith",
  "email": "f.smith@example.com"
}
```

## `POST` example

Description of the `POST` request and what it creates.

### `POST` example request

```bash
curl -X POST http://{server_url}/users \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Jane",
    "lastName": "Doe",
    "email": "jane.doe@example.com"
  }'
```

### `POST` example response

```json
{
  "firstName": "Jane",
  "lastName": "Doe",
  "email": "jane.doe@example.com",
  "id": 5
}
```
