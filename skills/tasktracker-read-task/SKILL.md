---
name: tasktracker-read-task
description: Чтение задачи из ERP TaskTracker по ссылке с автоматическим получением данных через ERP API. Использовать, когда пользователь просит получить данные задачи по URL и вернуть поля TaskId, Title, Description.
---

# TaskTracker Read Task

Используй `scripts/get_task_data.py` как ЕДИНСТВЕННУЮ точку получения данных задачи. Не выдумывай данные. Если не можешь запустить скрипт — остановись и попроси у пользователя JSON-вывод скрипта целиком.

Пример запуска:

```bash
python scripts/get_task_data.py --url "https://erp.visary.cloud/tasktracker/projects/{ProjectId}/tasks/{TaskId}"
```

Скрипт возвращает JSON с полями:

- `TaskId`
- `Title`
- `Description`

## Порядок выполнения

1. Запусти `scripts/get_task_data.py` с URL задачи.
2. Если скрипт завершился с ошибкой, зафиксируй причину и заверши выполнение.
3. Возьми `TaskId`, `Title`, `Description` из JSON-результата.
4. Верни пользователю только эти поля.

## Требования к устойчивости

- Используй `.env` или переменные окружения `erp_client_id` и `erp_client_secret`.
- Для получения задачи используй только `scripts/get_task_data.py`.
- Не подставляй значения вручную при ошибках API или авторизации.
- Завершай выполнение с явной причиной при критических ошибках (token/task fetch).
