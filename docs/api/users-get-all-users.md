---
# markdownlint-disable
# vale off
# tags used by just-the-docs theme
layout: default
parent: user resource
nav_order: 1
# tags used by AI files
description: GET all `user` resources from the service
topic_type: reference
tags:
    - api
categories:
    - api-reference
ai_relevance: high
importance: 7
prerequisites:
    - /api/user
related_pages: []
examples:
    - GET /users
test:
    test_apps:
        - json-server@0.17.4
    server_url: localhost:3000
    local_database: /api/to-do-db-source-test.json
    testable:
        - GET example
api_endpoints: 
    - /users
version: "v1.0"
last_updated: "2026-03-01"
# vale  on
# markdownlint-enable
---

# Get all users

Returns an array of [`user`](user.md) objects that contains all users that have registered with the service.

[Jump to examples](#examples)

## Endpoint

```shell
{server_url}/users
```

## Parameters

None

## Request headers

| Header | Value | Required |
| ------ | ----- | -------- |
| `Accept` | `application/json` | No |

## Request body

None

## Response body

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
    }
]
```

## Examples

### `GET` example request

```bash
curl -G -H "Accept: application/json" \
    --url "http://localhost:3000/users"
```

#### `GET` example response

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
    }
]
```

## Response status

| HTTP status value | Description |
| ------------- | ----------- |
| 200 | **Success:** Requested data returned successfully |
| ECONNREFUSED | Service is offline. Start, or restart the service and try again. |
