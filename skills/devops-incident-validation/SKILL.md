---
name: devops-incident-validation
description: Determine from the JSON file INCIDENT_FILE whether DevOps intervention is required
---

## Input

The environment variable INCIDENT_FILE contains a path to a file.
This file must be opened and its entire contents must be parsed as JSON
with the following structure:

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

* Title, Description, and Labels are the primary sources of truth.
* Comments are used only for additional confirmation and clarification.
* Comments previously created by you are published with author: `sysuser`.

## Algorithm

1. Open the INCIDENT_FILE and extract Title, Description, Labels, and Comments.
2. Draw conclusions based on Title and Description. Comments may clarify context but must not override conclusions from the main fields.
3. Sequentially evaluate all rules from the "Rejection reasons" section.
4. For each violated rule, add exactly one unique reason to the reasons array.
5. If no rules are violated, return {"valid": true, "reasons": []}.
6. If one or more rules are violated, return {"valid": false, "reasons": [...]}.

## Rejection reasons

1. A routine or planned action is detected  
   Example: Enable logging and metrics

2. The event is related to access or permission errors (403)  
   Example: When calling the /api/v1/orders endpoint, users receive 403 Forbidden

3. The event is related to application-level errors (401, 404, 500) and logs do not indicate an infrastructure issue  
   Example:  
   The orders service returns 500 on POST /api/v1/orders.  
   Application logs contain a stack trace with NullPointerException in OrderService.create().  
   No database connection errors, network timeouts, or Kubernetes issues were detected.

4. The required project label `project::*` is missing

5. The required environment label `namespace::*` is missing

6. A link to a resource or pipeline is missing  
   Example: The site is not working

## Output requirements

* The response must consist of exactly one JSON object.
* Any text outside the JSON object is forbidden.
* Explanations, comments, logs, or service messages are forbidden.
* Markdown, code blocks, or quoting the JSON are forbidden.
* No whitespace or line breaks are allowed before or after the JSON.
* When valid is true, the reasons array must be empty.
* All reason texts must be written in Russian.
* Duplicate reason wording is forbidden.

## Output

Return strictly ONE JSON object and nothing else.

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
    "string"
  ]
}
```

Failure to comply with the output format invalidates the response.