# tasktracker-ready-to-dev

Skill для проверки готовности задачи TaskTracker к разработке:

- получает данные задачи по URL через ERP API;
- проверяет качество постановки;
- при замечаниях публикует структурированный комментарий;
- при успешной проверке формирует план в `tasks/{TaskId}.md`.

## Переменные окружения

Для работы `scripts/get_task_data.py` добавьте в `.env`:

```env
erp_client_id=your_client_id
erp_client_secret=your_client_secret
```

`.env` читается автоматически из текущей рабочей директории.