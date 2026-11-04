---
# markdownlint-disable
# vale off

layout: default
description: My Library
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

# {Assignment 5_4}

<!-- vale Google.Acronyms = off -->

**Author:** `Hillary Donaghy`

View attributes of books and magazines in database

## curl examples

GET and POST requests from database

### `GET` example (curl)

GET information on book 1

#### `GET` example request (curl)

```bash
curl http://{server_url}/books/1
```

#### `GET` example response (curl)

```json

```    {
      "Title": "East of Eden",
      "Author": "John Steinbeck",
      "Genre": "Fiction",
      "Year": 1952,
      "id": 1
    }

### `POST` example (curl)

Create a new entry for a book

#### `POST` example request (curl)

```bash
curl -X POST http://{server_url}/library \
  -H "Content-Type: application/json" \
  -d '{
      "Title": "My Name is Asher Lev",
      "Author": "Chaim Potok",
      "Genre": "Fiction",
      "Year": 1972,
  }'
```

#### `POST` example response (curl)

```json
  {
      "Title": "My Name is Asher Lev",
      "Author": "Chaim Potok",
      "Genre": "Fiction",
      "Year": 1972,
      "id": 2
  }'
```


