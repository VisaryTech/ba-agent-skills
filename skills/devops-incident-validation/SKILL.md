---
name: devops-incident-validation
description: Determine from the JSON file INCIDENT_FILE whether DevOps intervention is required
---

## Input

### {{INCIDENT_FILE}}

The file {{INCIDENT_FILE}} must be parsed as JSON with the following structure:

```json
{
  "Title": "string",
  "Description": "string",
  "Labels": ["string"],
  "Comments": [
    {
      "author": "string",
      "text": "string"
    }
  ]
}
```

### Assumptions

* `Title`, `Description`, `Labels` are the primary sources of truth.
* `Comments` are used only for additional confirmation and clarification.
* Comments posted by you are published with `author: "sysuser"`.

## Algorithm

1. Open the `INCIDENT_FILE` file and extract the fields `Title`, `Description`, `Labels`, `Comments`.
2. Draw conclusions based on `Title` and `Description`. Comments may clarify context but must not override conclusions from the main fields.
3. Sequentially check the rules from the "Rejection reasons" section.
4. For each violated rule, add one unique reason to the `reasons` array.
5. If there are no violations, return `{"valid": true, "reasons": []}`.
6. If there is at least one violation, return `{"valid": false, "reasons": [...]}`.

## Rejection reasons

1. A routine or planned action is detected
   Example: Enable logging and metrics

2. The event is related to access or permission errors (403)
   Example: When calling the `/api/v1/orders` endpoint, users receive `403 Forbidden`.

3. The event is related to application-level errors (401, 404, 500) if logs do not indicate an infrastructure issue
   Example: The `orders` service returns `500` on `POST /api/v1/orders`.
   Application logs contain a stack trace with `NullPointerException` in the `OrderService.create()` method.
   No database connection errors, network timeouts, or Kubernetes issues were detected.

4. The required project label `project::*` is missing

5. The required environment label `namespace::*` is missing

6. A link to a resource or pipeline is missing
   Example: The site is not working

## Output

Strictly a JSON object of one of the following two types:

Valid incident:

```json
{
  "valid": true,
  "reasons": []
}
```

Invalid incident:

```json
{
  "valid": false,
  "reasons": [
    "The required project label project::* is missing",
    "A link to a resource or pipeline is missing"
  ]
}
```

### Constraints

* `valid` accepts only `true` or `false`.
* `reasons` is always an array of strings.
* Each reason corresponds to one violated rule.
* Reason texts are in Russian.
* Duplicate wording is prohibited.
* When `valid: true`, the `reasons` array must be empty.
