---
# markdownlint-disable
# vale off
# tags used by just-the-docs theme
layout: default
nav_order: 3
parent: Tutorials
# tags used by AI files
description: Update an existing `task` instance
topic_type: tutorial
tags:
    - api
categories: 
    - tutorial
ai_relevance: high
importance: 6
prerequisites:
    - /before-you-start-a-tutorial
    - /api/task
related_pages: []
examples: []
api_endpoints:
    - PUT /tasks
version: "v1.0"
last_updated: "2026-02-05"
# vale  on
# markdownlint-enable
---

# Tutorial: Update an existing task

<!--vale Google.Acronyms = NO -->

In this tutorial, you learn to update an existing task resource instance
using the PUT method. In REST API, the PUT method replaces an existing instance
with new information.
In this case, you must know the exact ID of the task resource.

Expect this tutorial to take about 10 minutes to complete.

## You learn

In this tutorial you learn to:

* Update an existing task using Postman
* Update an existing task using curl command

## Prerequisites

1. Review and complete [Before you start a tutorial](../before-you-start-a-tutorial.md)
topic on your development system.
1. Task resource id of the task you want to update.

## Update an existing task using Postman

To update an existing task using Postman:

1. Start the local server, ignore if server is already started.

    ```bash
    cd <your-github-workspace>/to-do-service-sp26/api
    json-server -w to-do-db-source.json
    ```

1. Open Postman desktop app.
1. In the Postman app, create a new request with following values:
    * **METHOD**: PUT
    * **URL**: `{base_url}/tasks/{task-id}`
    * **Request body**: Change the values of each property as you'd like.

        ```json
        {
            "userId": 11,
            "title": "Buy Flowers",
            "description": "Get beautiful Sunflowers and Lillies",
            "dueDate": "2026-05-10T17:00",
            "warning": "8"
        }
        ```

1. Click **Send** to make the request.
1. Check the task changes in response body.

    ```json
    {
        "userId": 11,
        "title": "Buy Flowers",
        "description": "Get beautiful Sunflowers and Lillies",
        "dueDate": "2026-05-10T17:00",
        "warning": "8",
        "id": 1
    }
    ```

> **Note:** Verify that the information matches to what you provided.

### Validation

To test the changes:

1. In the Postman app, create a new request with following values:
    * **METHOD**: GET
    * **URL**: `{base_url}/tasks/{task-id}`

    Mention the task ID that you used in the procedure.
    You should get the updated user details in the response body.

## Update an existing task using curl

To update an existing task using curl:

1. Start the local server, ignore if server is already started.

    ```bash
    cd <your-github-workspace>/to-do-service-sp26/api
    json-server -w to-do-db-source.json
    ```

1. Open a new terminal window.
1. Navigate to your GitHub project directory.
1. Type following in your terminal.
Change the values of each property as you'd like.

    ```bash
        curl -X PUT http://{base_url}/tasks/{task-id} \
        -H "Content-Type: application/json" \
        -d '{
                "userId": 11,
                "title": "Walk Dog",
                "description": "NA",
                "dueDate": "2026-05-10T17:00",
                "warning": "9",
                "id": {task-id}
            }
    ```

1. Press enter.
1. Terminal should return the exact information on successful update.

### Testing

To test the changes:

1. In the terminal, type following:

    ```bash
        curl http://{base_url}/tasks/{task-id}
    ```

    Mention the task ID that you used in the procedure.
    You should get the updated user details in the response body.

### Example

```bash

        $ curl -X PUT http://localhost:3000/tasks/4 \
        -H "Content-Type: application/json" \
        -d '{
                "userId": 4,
                "title": "Walk Dog",
                "description": "NA",
                "dueDate": "2026-05-10T17:00",
                "warning": "9",
                "id": 4
            }'

        {
            "userId": 4,
            "title": "Walk Dog",
            "description": "NA",
            "dueDate": "2026-05-10T17:00",
            "warning": "9",
            "id": 4
        }

        $ curl http://localhost:3000/tasks/4
        {
                "userId": 4,
                "title": "Walk Dog",
                "description": "NA",
                "dueDate": "2026-05-10T17:00",
                "warning": "9",
                "id": 4
        }    
```

## References

* Add a new task
* Delete a task
