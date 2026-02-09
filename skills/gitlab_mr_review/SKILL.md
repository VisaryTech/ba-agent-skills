---
name: gitlab_mr_review
description: GitLab Merge Request code review based on DIFF_JSON.
---

## Input

The environment variable DIFF_FILE contains a path to a file.
This file must be opened and its entire contents must be parsed as JSON
with the following structure:


```json
[
  {
    "changes": [
      {
        "diff": "string"
      }
    ],
    "notes": [
      {
        "body": "string",
        "author.username": "string"
      }
    ]
  }
]
```

## Algorithm

1. Open {{DIFF_FILE}} and parse the JSON.

2. Analyze only `changes[].diff`.

   * Ignore all other fields, including file names and metadata.
   * Ignore compatibility-only changes if they do not affect:

     * security
     * system logic
     * error handling
     * performance
     * architecture or maintainability
   * Compatibility-related changes include:

     * database schema changes
     * API changes
     * database migrations
     * removal or renaming of entity fields
   * Create issues in the following categories:

     * security
     * performance
     * readability
     * architecture
     * best practices
     * error handling

3. Risk level definition:

   * critical:

     * security vulnerabilities
     * unhandled exceptions causing application crashes
     * logical errors that change system behavior
     * memory leaks
   * medium:

     * potential bugs and edge cases
     * performance issues under increased load
     * architectural decisions that complicate maintenance or scaling
   * low:

     * readability and style issues
     * best practice violations without direct stability impact
     * redundant or hard-to-maintain code

4. Issue structure:

   * Each issue contains only:

     * risk: "critical" | "medium" | "low"
     * description: Russian text
     * recommendation: Russian text
   * Each issue must be directly tied to the changes in the diff.

5. Deduplication and sorting:

   * Merge semantically duplicate issues.
   * Sort issues by risk level: critical first, then medium, then low.

6. If no issues are found, return exactly:

   * `{"issues":[]}`

## Output

Strictly a JSON object of one of the following two types.

1. If no issues are found:

```json
{
  "issues": []
}
```

2. If issues are found:

```json
{
  "issues": [
    {
      "risk": "critical" | "medium" | "low",
      "description": "Russian text",
      "recommendation": "Russian text"
    }
  ]
}
```

* Return only valid JSON without any extra text.
* The root object must contain only the `issues` key.
* The output must start with `{` and end with `}`.
* Failure to comply with the output format invalidates the response.
