---
# markdownlint-disable
# vale off

layout: default
description: /Knives endpoint
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

# Requests to the Knives API

<!-- vale Google.Acronyms = off -->

**Author:** `Jessica Heilman`

Manage knives using the `/knives` endpoint

## curl examples

The examples in the following show GET and POST requests to the `/knives` endpoint.
Replace `{server_url}` with the address of your API server.

### `GET` example (curl)

Retrieves a knife by id.

#### `GET` example request (curl)

```bash
curl http://{server_url}/knives/1
```

#### `GET` example response (curl)

```json
{
  "Type": "Paring",
  "Brand": "Shun",
  "Size": "Small",
  "Handle type": "Japanese",
  "id": 1
}
```

### `POST` example (curl)

Creates a new knife. Required fields: `Type`, `Brand`, `Size`, and `Handle type`.
The server assigns and returns a unique `id`.

#### `POST` example request (curl)

```bash
curl -X POST http://{server_url}/knives \
  -H "Content-Type: application/json" \
  -d '{
    "Type": "Chef",
    "Brand": "Wüsthof",
    "Size": "Large",
    "Handle type": "Western"
  }
```

#### `POST` example response (curl)

```json
{
  "Type": "Chef",
  "Brand": "Wüsthof",
  "Size": "Large",
  "Handle type": "Western",
  "id": 2
}
```
