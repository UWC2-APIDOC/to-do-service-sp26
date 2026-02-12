---
layout: api
title: Incomplete Config
test:
  testable:
    - GET example
  test_apps:
    - json-server@0.17.4
  server_url: localhost:3000
  # Missing local_database
---

# Incomplete Config

This file has a test section but is missing the local_database field.
