---
# markdownlint-disable
# vale off

layout: default
description: Local database that contains flowers and their characteristics
topic_type: reference
# test:
#   test_apps:
#     - json-server@0.17.4
#   server_url: localhost:3000
#   local_database: /api/flowers-db.json
#   testable:
#     - GET example / 200
#     - POST example / 201
# vale  on
# markdownlint-enable
---

# Flowers service examples

<!-- vale Google.Acronyms = off -->

**Author:** `Maya Nakamura`

Local database that contains flowers and their characteristics

## `cURL` examples

GET and POST requests where {server_url} is localhost:3000

### `GET` example

Request data of flower with id 1.

#### `GET` example request

```bash
curl http://{server_url}/flowers/1
```

#### `GET` example response

```json
{
  "commonName": "Fuji",
  "scientificName": "Wisteria floribunda",
  "nativeRange": "Japan",
  "id": 1
}
```

### `POST` example

Submit data to create a flower with a new id.

#### `POST` example request

```bash
curl -X POST http://{server_url}/flowers \
  -H "Content-Type: application/json" \
  -d '{
    "commonName": "Tsubaki",
    "scientificName": "Camellia japonica",
    "nativeRange": "China and Japan"
  }'
```

#### `POST` example response

```json
{
  "commonName": "Tsubaki",
  "scientificName": "Camellia japonica",
  "nativeRange": "China and Japan",
  "id": 2
}
```
