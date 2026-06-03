---
# markdownlint-disable
# vale off
# tags used by just-the-docs theme
layout: default
parent: task resource
nav_order: 1
# tags used by AI files
description: POST a `task` resource to the service
topic_type: reference
tags:
    - api
categories:
    - api-reference
ai_relevance: high
importance: 7
prerequisites:
    - /api/task
related_pages: []
examples:
    - POST /tasks
test:
    test_apps:
        - json-server@0.17.4
    server_url: localhost:3000
    local_database: /api/to-do-db-source-test.json
    testable:
        - POST example / 201
api_endpoints: 
    - /tasks
version: "v1.0"
last_updated: "2026-06-02"
# vale  on
# markdownlint-enable
---

# Create a task

Sends a [`task`](task.md) object to store the details of the new task resource
in the service. The new task is for a registered user of the service.

[Jump to examples](#examples)

## Endpoint

```shell
{server_url}/tasks
```

## Parameters

None

## Request headers

| Header | Value | Required |
| ------ | ----- | -------- |
| `content-type` | `application/json` | Yes |

## Request body

```json
{
    "userId": 1,
    "title": "Grocery shopping",
    "description": "eggs, bacon, gummy bears",
    "dueDate": "2026-02-20T17:00",
    "warning": "10"
}
```

## Response body

Returns a [`task` resource](./task.md#resource-properties)

## Examples

### `POST` example request

```bash
curl -H 'content-type: application/json' \
    --url http://localhost:3000/tasks \
    -d '{
            "userId": 1,
            "title": "Grocery shopping",
            "description": "eggs, bacon, gummy bears",
            "dueDate": "2025-09-20T17:00",
            "warning": "10"
        }'
```

#### `POST` example response

```json
{
    "userId": 1,
    "title": "Grocery shopping",
    "description": "eggs, bacon, gummy bears",
    "dueDate": "2025-09-20T17:00",
    "warning": "10",
    "id": 3
}
```

## Response status

| HTTP status value | Description |
| ------------- | ----------- |
| 201 | **Success:** Task resource created successfully |
| 400 | **Error:** Malformed request not processed. Verify syntax and try again. |
| 500 | **Error:** Server rejected the data. Verify data and try again. |
