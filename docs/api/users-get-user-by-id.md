---
# markdownlint-disable
# vale off
# tags used by just-the-docs theme
layout: default
parent: user resource
nav_order: 2
# tags used by AI files
description: GET the `user` resource with the specified ID from the service
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
    - GET /users/{id}
test:
    test_apps:
        - json-server@0.17.4
    server_url: localhost:3000
    local_database: /api/to-do-db-source-test.json
    testable:
        - GET example / 200
api_endpoints: 
    - GET /users
version: "v1.0"
last_updated: "2026-03-01"
# vale  on
# markdownlint-enable
---

# Get a user by ID

Returns an array of  [`user`](user.md) objects that contains only
the user specified by the `id` parameter, if it exists.

[Jump to examples](#examples)

## Endpoint

```shell
{server_url}/users/{id}
```

## Parameters

| Name | Type | Value | Description |
| ----- | ------ | ------ | ------------ |
| `id` | URL | number | The record ID of the `user` resource to return |

## Request headers

| Header | Value | Required |
| ------ | ----- | -------- |
| `Accept` | `application/json` | No |

## Request body

None

## Response body

Returns a [`user` resource](./user.md#resource-properties)

## Examples

### `GET` example request

```bash
curl -G -H "Accept: application/json" \
    --url "http://localhost:3000/users/2"
```

#### `GET` example response

```json
    {
        "lastName": "Jones",
        "firstName": "Jill",
        "email": "j.jones@example.com",
        "id": 2
    }
```

## Response status

| HTTP status value | Description |
| ------------- | ----------- |
| 200 | **Success**: Requested data returned successfully |
| 404 | **Error**: Specified user record not found |
| ECONNREFUSED | Service is offline. Start, or restart the service and try again. |
