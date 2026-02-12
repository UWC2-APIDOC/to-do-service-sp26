---
# markdownlint-disable
# vale off
# tags used by just-the-docs theme
layout: default
nav_order: 3
parent: Tutorials
# tags used by AI files
description: Update a `task` resource in the service
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
    - PATCH /tasks/{id}
version: "v1.0"
last_updated: "2026-05-28"
# vale  on
# markdownlint-enable
---

# Tutorial: Update a task

In this tutorial, you learn the operations to call to update a task for a user
of the service.

Expect this tutorial to take about 10 minutes to complete.

## Before you start

Make sure you've completed the [Before you start a tutorial](../before-you-start-a-tutorial.md)
topic on the development system you'll use for the tutorial.

## Update a task

Updating a task in the service requires that you use the `PATCH` method to change the details of
the [`task`](../api/task.md) resource in the service.

To update a task:

1. Make sure your local service is running, or start it by using this command,
if it's not.

    ```shell
    cd <your-github-workspace>/to-do-service/api
    json-server -w to-do-db-source.json
    ```

1. Open the Postman app on your desktop.
1. In the Postman app, create a new request with these values:
    * **METHOD**: PATCH
    * **URL**: Specify the `{id}` of the task that you want to update.
        * `{{base_url}}/tasks/{id}`
    * **Headers**:
        * `Content-Type: application/json`
    * **Request body**:
        You can change the values of each property as you'd like, but don't
        change the property names.

        This example updates `dueDate` and `warning`.

        ```json
        {
            "dueDate": "2026-08-01T18:00",
            "warning": "50"
        }
        ```

1. In the Postman app, choose **Send** to make the request.
1. Watch for the response body, which should look something like this for the
task `id` of `1`.

    ```json
    {
        "userId": 1,
        "title": "Grocery shopping",
        "description": "eggs, bacon, gummy bears",
        "dueDate": "2026-08-01T18:00",
        "warning": "50",
        "id": 1
    }
    ```

After doing this tutorial in Postman, you might like to repeat it in
your favorite programming language. To do this, adapt the values from
the tutorial to the properties and arguments that the language uses to
make REST API calls.
