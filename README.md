# Portfolio Control Plane

Источник истины по экосистеме **dominicusin / surypus / neoallunity**.

- 78 репозиториев (57 публичных + 21 приватный), 8 продуктовых систем.
- Полный аудит: `artifacts/repository-audit.json`.
- Мастер-план: `artifacts/MASTER-IMPLEMENTATION-PLAN.md`.
- Сверка черновиков: `artifacts/RECONCILIATION.md`.

Быстрый старт:

```sh
python automation/audit.py        # пересобрать аудит через gh CLI
python automation/ci_health.py    # статус CI на защищённых ветках
python automation/dedup_issues.py surypus/surypus
python automation/weekly_report.py
```

Принципы: один канон на артефакт; требуется evidence со ссылкой на CI/release; непроверенное состояние — `BLOCKED`, а не `DONE`.
