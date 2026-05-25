---
# markdownlint-disable
# vale off

layout: default
description: fruits and vegetables endpoints
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

# Fruits and vegetables API endpoints

<!-- vale Google.Acronyms = off -->

**Author:** `Khushbu Borole`

This article exposed GET and POST method endpoints for fruits and vegetables.

## Client URL examples - curl

This section explores GET and POST methods for fruits and vegetables endpoints.
In the future content, if you see {server_url}, know that it's the base URL for
your API endpoint.

### `GET` example - curl

This get request fetched all the fruits in the database.

#### `GET` example request - curl

```bash
curl http://{server_url}/fruits
```

#### `GET` example response - curl

```json
[
  {
    "name": "Apple",
    "color": "Red",
    "taste": "Sweet",
    "id": 1
  },
  {
    "name": "Orange",
    "color": "Orange",
    "taste": "Sour",
    "id": 2
  },
  {
    "name": "Mango",
    "color": "Yellow",
    "taste": "Sweet",
    "id": 3
  }
]
```

### `POST` example - curl

This request adds a new vegetable and assigns it an ID of 4.

#### `POST` example request - curl

```bash
curl -X POST http://{server_url}/vegetables \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Okra",
    "color": "Green",           
    "comment": "Kids love okra"
  }'
```

#### `POST` example response - curl

```json
{
  "name": "Okra",
  "color": "Green",
  "comment": "Kids love okra",
  "id": 4
}
```
