# tasktracker-ready-to-dev

Skill для проверки готовности задачи TaskTracker к разработке:

- получает данные задачи по URL через скилл `tasktracker-read-task`;
- проверяет качество постановки;
- при замечаниях публикует структурированный комментарий через скилл `tasktracker-comment-task`;
- при успешной проверке формирует план в `tasks/{TaskId}.md`.

## Важное правило workflow

Если `tasktracker-read-task` или `tasktracker-comment-task` недоступны, workflow должен быть остановлен с явной причиной.
