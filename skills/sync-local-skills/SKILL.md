---
name: sync-local-skills
description: Устанавливать или обновлять все локальные скиллы из папки skills в директорию Codex skills. Использовать, когда нужно массово синхронизировать навыки проекта в $CODEX_HOME/skills или ~/.codex/skills.
---

# Sync Local Skills

Синхронизировать локальные скиллы через скрипт `scripts/sync_local_skills.py`.

## Команды

- Предпросмотр изменений:
  `python skills/sync-local-skills/scripts/sync_local_skills.py --source skills --dry-run`
- Установить/обновить все скиллы в дефолтную директорию Codex:
  `python skills/sync-local-skills/scripts/sync_local_skills.py --source skills`
- Явно указать целевую директорию:
  `python skills/sync-local-skills/scripts/sync_local_skills.py --source skills --dest <path-to-codex-skills>`

## Правила выполнения

- Запускать `--dry-run`, если пользователь просит сначала показать план.
- Считать директорией скилла только папку, где есть `SKILL.md`.
- При обновлении удалять существующую папку целевого скилла и копировать заново.
- Если запуск в sandbox блокирует запись в домашнюю директорию, запрашивать escalation.

## Результат

- После синхронизации сообщать количество `installed` и `updated`.
- Рекомендовать перезапустить Codex, чтобы новые/обновленные скиллы подхватились.
