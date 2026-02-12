---
# markdownlint-disable
# vale off
# tags used by just-the-docs theme
layout: default
nav_order: 4
has_children: true
has_toc: false
# tags used by AI files
description: "Information about the `task` resource"
topic_type: reference
tags: 
    - api
categories: 
    - api-reference
ai_relevance: high
importance: 8
prerequisites: []
related_pages: 
    - /tutorials/add-a-new-task
examples: []
api_endpoints:
    - /tasks
version: "v1.0"
last_updated: "2026-03-01"
# vale  on
# markdownlint-enable
---

# `task` resource

<!-- vale write-good = NO -->
<!-- vale Google.Passive = NO -->
<!-- vale Google.Headings = NO -->
<!-- vale Google.Parens = NO -->
<!-- vale Google.Acronyms = NO -->

Base endpoint:

```shell
{server_url}/tasks
```

Contains information about tasks stored for the users of the service.

To have a task in the service, the user must be added to
the service first. Learn more about the [user resource](user.md).

## Resource properties

Sample `task` resource

```json

{
    "userId": 1,
    "title": "Grocery shopping",
    "description": "eggs, bacon, gummy bears",
    "dueDate": "2025-02-20T17:00",
    "warning": "10",
    "id": 1
}
```

<!-- markdownlint-disable MD013 -->

| Property name | Type | Description |
| ------------- | ----------- | ----------- |
| `userId` | number | The ID of the user resource to which this task is assigned |
| `title` | string | The title or short description of the task |
| `description` | string | The long description of the task |
| `dueDate` | string | The [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format of the date and time the task is due |
| `warning` | number | The number of minutes before the `dueDate` to alert the user of the task. This must be a positive integer. |
| `id` | number | The task's unique record ID |

<!-- markdownlint-enable MD013 -->

## READ

<!-- vale Vale.Terms = NO -->

* [Get all tasks _(coming soon)_](#resource-properties)
* [Get task by ID _(coming soon)_](#resource-properties)
* [Get task by user ID _(coming soon)_](#resource-properties)
