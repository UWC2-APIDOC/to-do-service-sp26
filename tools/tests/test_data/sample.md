---
layout: default
parent: user resource
nav_order: 2
description: GET the user resource with the specified ID from the service
topic_type: reference
tags: ["api"]
categories: ["api-reference"]
test:
  test_apps:
    - json-server@0.17.4
  server_url: localhost:3000
  local_database: /api/to-do-db-source.json
  testable:
    - GET example / 200
    - POST example / 201
---

# Sample Test Document

This is a sample markdown file for testing documentation utilities.

## GET example request

```bash
curl http://localhost:3000/users/1
```

## GET example response

```json
{
  "id": 1,
  "name": "Test User",
  "email": "test@example.com"
}
```

## POST example request

```bash
curl -X POST http://localhost:3000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "New User", "email": "new@example.com"}'
```

## POST example response

```json
{
  "id": 2,
  "name": "New User",
  "email": "new@example.com"
}
```
