---
name: gitlab_mr_review
description: GitLab Merge Request code review based on DIFF_JSON.
---

Input: {{DIFF_JSON}} (JSON string).

Algorithm:

1. Try to parse {{DIFF_JSON}} as JSON.

   * If parsing fails, return an object:
     * error: Invalid JSON input

2. Check for file and changes.

   * If the file is not found, return an object:
     * error: File not found
   * If the changes key is missing, is not an array, the array is empty, or all changes elements have a missing or empty diff field, return an object:
     * error: No changes to analyze

3. Analyze only changes[].diff.

   * Ignore any other fields, including file names and metadata.
   * Ignore compatibility-related changes only if the identified issue affects compatibility exclusively and does not impact:
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

   * Create issues by categories:
     * security
     * performance
     * readability
     * architecture
     * best practices
     * error handling

4. Risk level definition:

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

5. Issue structure:

   * Each issue contains only:
     * risk: "critical" | "medium" | "low"
     * description: English text
     * recommendation: English text
   * Each issue must be directly tied to the changes in the diff.

6. Deduplication and sorting:

   * Merge semantically duplicate issues.
   * Sort issues by risk level: critical first, then medium, then low.

7. If no issues are found, return exactly:
   * {"issues":[]}

Output (strict):

* Return only valid JSON without any extra text.
* If there is an error, the root object contains only the error key with English text.
* If there is no error, the root object contains only the issues key.
* The output must start with { and end with }.
