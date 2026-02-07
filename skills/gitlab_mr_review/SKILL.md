---
name: gitlab_mr_review
description: GitLab Merge Request code review.
---

Input: {{DIFF_JSON}} (JSON string).

Rules:

* Parse the input as JSON. If parsing fails, return exactly one issue with risk="critical".
* Analyze only changes[].diff.
* If changes is missing, empty, or all diff values are empty, return exactly one issue with risk="medium".
* Create issues only for: security, performance, readability, architecture, best practices, error handling.
* Ignore database migrations and entity field deletion or renaming.
* Each issue must contain only:
  * risk: "critical" | "medium" | "low"
  * description: Russian text
  * recommendation: Russian text
* Merge duplicates and sort issues by risk: critical → medium → low.
* If no issues are found, return exactly {"issues":[]}.

Output (strict):

* Return only valid JSON.
* No markdown or extra text.
* Output must start with { and end with }.
* The root object must contain only the key "issues".
* Issue objects must contain only "risk","description","recommendation".
