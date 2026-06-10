---
layout: default
parent: To-Do Service API
nav_order: 2
description: "API landing page"
topic_type: overview
---

# To-Do Service API `(KhushbuB)`

<!-- vale write-good = NO -->
<!-- vale Google.Passive = NO -->
<!-- vale Google.Headings = NO -->
<!-- vale Google.Parens = NO -->
<!-- vale Google.Acronyms = NO -->
<!-- vale Google.We = NO -->

## Plan it - Track it - Get it done

Welcome to the To-Do Service API.  

Use this API to manage tasks and onboard users with simple, easy-to-use endpoints.

## What you can do

* Enroll new users
* Create new tasks
* Update or delete tasks
* Search tasks using keywords

## Getting Started

1. Start the server  
2. Send requests to `http://localhost:3000`  
3. Use curl, Postman, or any API client to see how easy the To-Do Service is to use

## API Endpoints

### Tasks

* Get all tasks - `GET /tasks`
* Get a task by ID - `GET /tasks/{id}`
* Replace a task - `PUT /tasks/{id}`
* Delete a task - `DELETE /tasks/{id}`
* Search tasks - `GET /tasks?q=`
* Add a new task - `POST /tasks`

### Users

* Get all users - `GET /users`
* Get a user by ID - `GET /users/{id}`
* Enroll a new user - `POST /users`

## Learn more

* [Before you start a tutorial](../before-you-start-a-tutorial.md)
* [task resource](../api/task.md)
    * [Add a new task](../tutorials/add-a-new-task.md)
* [user resource](../api/user.md)
    * [Enroll a new user](../tutorials/enroll-a-new-user.md)
    * [Get all users](../api/users-get-all-users.md)
    * [Get a user by ID](../api/users-get-user-by-id.md)

## References

* [Writer’s guide](../contributors-guide/writers-guide.md)
* [Documentation requirements](../contributors-guide/documentation-requirements.md)
* [Fixing validation errors](../contributors-guide/validation-errors-table.md)
* [Pull request validation](../contributors-guide/pr-validation.md)

## Contact Us

Have questions, feedback, or found an issue?

* Mail: [support@todoapi.dev](mailto:support@todoapi.dev)  
* Slack: #todo-api-support  
* GitHub: [To-Do Service Repository](https://github.com/UWC2-APIDOC/to-do-service-sp26)
