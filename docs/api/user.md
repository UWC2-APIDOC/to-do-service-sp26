---
# markdownlint-disable
# vale off
# tags used by just-the-docs theme
layout: default
nav_order: 5
has_children: true
has_toc: false
# tags used by AI files
description: "Information about the `user` resource"
topic_type: reference
tags: 
    - api
categories:
    - api-reference
ai_relevance: high
importance: 8
prerequisites: []
related_pages: 
    - /tutorials/enroll-a-new-user
examples: []
api_endpoints: 
    - /users
version: "v1.0"
last_updated: "2026-03-01"
# vale  on
# markdownlint-enable
---

# `user` resource

Base endpoint:

```shell

{server_url}/users
```

Contains information about the users of the service.

A user resource describes the owners of the tasks in the service.
Before you can create a `task` resource in the service,
you must create the 'user' resource to assign to the `task`.

Learn more about the [task resource](task.md).

## Resource properties

Example `user` resource

```json
{
    "lastName": "Smith",
    "firstName": "Ferdinand",
    "email": "f.smith@example.com",
    "id": 1
}
```

| Property name | Type | Description |
| ------------- | ----------- | ----------- |
| `lastName` | string | The user's last name |
| `firstName` | string | The user's first name |
| `email` | string | The user's email address |
| `id` | number | The user's unique record ID |

## Read operations

* [Get all users](users-get-all-users.md)
* [Get users by ID](users-get-user-by-id.md)
