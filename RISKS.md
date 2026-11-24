# Риски

| Риск | Статус | Митигация |
|---|---|---|
| 870 Dependabot и 133 Code Scanning алерта | OPEN | триаж по активности репозитория |
| Surypus tenant isolation stubs | OPEN | SUR-001 + негативные тесты |
| UAW JSON-state без транзакционности | OPEN | UAW-001 + crash-тест |
| Правовой статус медиа-зеркал (~265 МБ) | BLOCKED | решение владельца; до него read-only |
| GHC 9.10.3 локально vs 9.6.x в CI | OPEN | flake/Nix pin |
| Приватные ядра вне публичного аудита | MITIGATED | аудит через gh api с affiliation=owner |
