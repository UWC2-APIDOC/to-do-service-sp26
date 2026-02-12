---
layout: api
title: Get Tasks - Config B
test:
  testable:
    - GET tasks
  test_apps:
    - json-server@0.17.4
  server_url: localhost:4000
  local_database: /api/tasks.json
---

# Get Tasks

Test file with configuration B (different server and database).
