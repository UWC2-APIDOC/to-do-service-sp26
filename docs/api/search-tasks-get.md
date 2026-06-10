---
# markdownlint-disable
# vale off
# tags used by just-the-docs theme
layout: default
nav_order: 1
parent: task resource
# tags used by AI files
description: search task resource
topic_type: tutorial
tags:
    - api
categories: 
    - reference
ai_relevance: high
importance: 6
prerequisites:
    - /before-you-start-a-tutorial
    - /api/task
related_pages: []
examples: []
api_endpoints:
    - GET /tasks?q=
version: "v1.0"
last_updated: "2026-02-05"
# vale  on
# markdownlint-enable
---

# Search task resource

<!--vale Google.Acronyms = NO -->

Search a task in the database using curl and Postman.
The query returns all the matching instances of the text
provided against the parameter.

## Endpoint

```bash
    {base-URL}/tasks?q=
```

**NOTE** - {base-URL}/tasks?q= returns all resource instances
because no filtering text is present.

## Parameters

* q : provide the text you want to search in database.

## Request headers

Not required

## Search task resource via curl

### Request body - curl

```bash
    curl "{base_url}/tasks?q={text-to-search}"
```

### Example request body - curl

```bash
    curl "{base_url}/tasks/?q=dog"
```

### Response body - curl

```bash
[
  {
    "userId": 3,
    "title": "Get shots for dog",
    "description": "Annual vaccinations for poochy",
    "dueDate": "2025-12-11T14:00",
    "warning": "20",
    "id": 4
  }
]
```

## Search task resource via Postman

### Request body - `Postman`

* **METHOD**: GET
* **URL**: `{base_url}/tasks?q={text-to-search}`

### Example request body - `Postman`

* **METHOD**: GET
* **URL**: `{base_url}/tasks?q=dog`

### Response body - `Postman`

```bash
[
  {
    "userId": 3,
    "title": "Get shots for dog",
    "description": "Annual vaccinations for poochy",
    "dueDate": "2025-12-11T14:00",
    "warning": "20",
    "id": 4
  }
]
```

### Response code - `Postman`

* 200 OK : Request successful
