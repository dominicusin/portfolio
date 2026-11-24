# План консолидации GitHub-экосистемы dominicusin / surypus / neoallunity

**Дата аудита:** 2026-11-25. **Метод:** полный перебор репозиториев через GitHub API (`user/repos` + `orgs/*/repos`), деревья файлов всех default-веток, статус workflow-запусков, открытые issue, содержимое README/STRATEGY/`.gitmodules`. **Охват:** 78 репозиториев — 51 личный, 6 `surypus`, 21 `neoallunity`. Машиночитаемый реестр: `inventory.csv` (по строке на репозиторий с системой, языком, размером, датой, лицензией и решением).

---

## 1. Вердикт

Экосистема — не 78 независимых проектов, а **6 продуктовых систем разной зрелости**. Реально активны 7 ядер: `surypus/surypus`, `neoallunity/integral-philosophy`, `neoallunity/allunity-wagtail`, `dominicusin/dominicusin.github.io`, `dominicusin/Linux-Serv-Ansible`, `dominicusin/alpine-wdmch-builder`, `dominicusin/package-maximizer`. Остальное — supporting-репозитории, форки, конспекты, архив и нашипки.

Ключевые цифры:

| Показатель | Значение |
|---|---|
| Репозиториев всего | 78 (51 / 6 / 21) |
| Архивировано | 21 (из них 8 — уже слитые модули монOREPO) |
| Форков | 11 |
| Без лицензии в метаданных | 16 |
| Без README | 5 |
| С CONTRIBUTING / CODE_OF_CONDUCT / SECURITY | 9 / 10 / 10 |
| Workflow-файлов только в `surypus/surypus` | 82 |
| Открытых issue в `surypus/surypus` | 129, из них **19 точных дублей** и **12 робо-отчётов** |
| Репозиториев с Actions | 26 |

**Главные проблемы, мешающие «рабочему состоянию»:**

1. **CI красный ровно там, где проекты должны быть опорными.** 5 из 8 ключевых репозиториев имеют систематические падения на `main`, а не случайные разовые ошибки.
2. **Дублирование уже частично устранено на уровне кода, но не на уровне метаданных и документации:** 8 модулей слиты в `integral-philosophy`, однако org-README, `.github` и README `Magazine` продолжают ссылаться на старые репозитории как на актуальные.
3. **Нет единого контракта инфраструктуры:** версии инструментов, required-проверки, секреты, шаблоны issue/PR, лицензии и политики архивации заданы хаотично.
4. **Issue-трекер `surypus` замусорен** дублированными импортом и еженедельными робо-отчётами — приоритеты реальной работы в нём не читаются.

---

## 2._product systems: что есть и чем должно стать

| Система | Репо | Роль | Состояние | Целевое состояние |
|---|---|---|---|---|
| **S1 Surypus ERP/CRM** | 6 | Основной продукт: Haskell, формальная верификация, event sourcing | Прототип, 382 модуля, 792 теста, CI в основном зелёный, 129 issue | Один рабочий вертикальный срез: вход → JWT/RBAC → ДБ → проводка → отчёт; issue-трекер очищен |
| **S2 NeoAllUnity publishing** | 23 | Издательская платформа: монOREPO, Wagtail-сайт, зеркала, sitemap | МонOREPO собран, но CI не запускался с 27.08; Wagtail нигде не опубликован; 8 модулей-дублей в архиве | Один канонический монOREPO + один объяснённый сайт + зеркала как данные |
| **S3 Infra & ops** | 16 | Серверная автоматизация, rescue-образ, сетевые утилиты, конфиги хостов | Ansible CI падает 29/30; rescue-образ CI в норме; конфиги размазаны по 4 репо | Воспроизводимая инфраструктура с проверенными прогонами и одной точкой истины по хосту |
| **S4 Site & knowledge** | 16 | Личный сайт, блог, CV, заметки | Hugo-сайт деплоится; SBOM-задача падает 13/13; 3 CV-репозитория; 10+ сабмодулей | Hugo как канон, единое CV, рабочие проверки безопасности, архив экспериментов |
| **S5 R&D / Haskell** | 6 | Эксперименты: DNS, шлюз сообщений, AI-конвейер, солверы | Pre-spec / CI 7/7 красный / зрелый пакет в одном репо | Каждый проект либо становится продуктом с работающим CI, либо переводится в архив с формулировкой причины |
| **S6 Archive / forks / stubs** | 11 | Старые песочницы, форки, демо, стоп-репозитории | Часть помечена `[STUB — inactive]`, часть — просто форки без политики | Явная политика: archived + причина в README, либо апстрим-политика для форков |

---

## 3. Найденные проблемы (с фактами)

### 3.1 Состояние CI на `main`

| Репозиторий | Последние проверки на `main` | Корень проблемы (из логов) |
|---|---|---|
| `dominicusin/Linux-Serv-Ansible` | 20 failures / 30, 9 cancelled | `ansible-lint`: 10 ошибок в 353 файлах (trailing spaces, `yaml[commas]` в `roles/mgmt_guard/tasks/main.yml`); отдельно `ModuleNotFoundError: No module named 'jinja2'` — тесты запускаются не в venv |
| `dominicusin/ai-orchestration-platform` | 7 failures / 7 | `ERROR: Could not open requirements file: 'requirements.txt'` — workflow ссылается на несуществующий файл, хотя есть `pyproject.toml` |
| `neoallunity/Magazine` | 24 failures / 30 | Build LaTeX Journal with Biber; логи старых запусков уже недоступны (HTTP 410), что само по себе блокирует диагностику |
| `neoallunity/allunity-wagtail` | 13 failures / 30 | Тест smoke-home: `Could not parse the remainder: '%'` (синтаксис шаблона Django); `Deploy to CodeRed Cloud` падает отдельно; активность с 02.09 |
| `neoallunity/integral-philosophy` | `Monorepo CI` последний успех 27.08; дальше только dynamic Dependabot, `pip in /. - Update` падает каждую неделю | CI по сути не работает как gating; Dependabot несовместим с текущими зависимостями |
| `dominicusin/dominicusin.github.io` | 3 failures / 30 | SBOM: `Failed to persist attestation: Resource not accessible by integration` (не хватает прав/настройки); Security Scanning тоже красный |
| `surypus/surypus` | 1 failure / 30 | `Security Scan`: `missing gitleaks license` — нужен секрет `GITLEAKS_LICENSE` |
| `dominicusin/package-maximizer` | 3 failures / 30 | `Package Maximizer CI/CD`, редкие падения на релизных запусках |
| `neoallunity/neoallunity` | 17 failures / 25 (все recent — Dependabot) | `npm_and_yarn in /boiler for node-forge` — уязвимый транзитив в legacy-сайте |

Вывод: «CI зелёный» в README `surypus` и `allunity-wagtail` — это утверждение про момент времени, а не про текущее состояние. Нужна проверка required-задач в каждой точке входа.

### 3.2 Дублирование и конкуренция за роль

1. **8 репозиториев `neoallunity/integral-philosophy-*` уже слиты** в `neoallunity/integral-philosophy/modules/*` и архивированы. Это корректно, но:
   - `neoallunity/README` и `neoallunity/.github/README.md` до сих пор перечисляют их как активные модули;
   - `neoallunity/Magazine` хранит `subprojects/integral-philosophy-*` (8 каталогов) и `.gitmodules` с пометкой DEPRECATED — каноническая копия одна, но физически код лежит в двух местах;
   - README `Magazine` предлагает `git clone github.com/dominicusin/integral-philosophy.git`, тогда как канон — `neoallunity/integral-philosophy`.
2. **Профиль-конфиги:** `dominicusin/neoallunity` (CSS) и `neoallunity/neoallunity` (Python, 22 МБ, includes `boiler/` и вендор Bootstrap) — два разных сайта/профиля с одним именем; плюс `allunity-wagtail` — третья реализация AllUnity. Требуется явная иерархия: **live-сайт → Wagtail-реализация → legacy Django → архив**.
3. **Конфиги рабочей станции:** `guix-config`, `my-nixos-config`, `nixos-config` (legacy 2018), `Quasar` (flake), плюс `dominicusin/.github` с чужим по смыслу README про AlphaEvolve. Нужно выбрать один канон (Suggested: `guix-config` для quasar + `Quasar` как flake-слой; `nixos-config` — архив с пометкой legacy).
4. **CV:** `Awesome-CV`, `Modern-Simple-CV`, `resume`, `pmo-solovyov-article` — 3 резюме + статья. Один канон, остальные redirects/archived.
5. **Демо-репозитории:** `surypus/demo-repository`, `neoallunity/demo-repository` — удалить/архивировать.
6. **«Utility repository in the dominicusin ecosystem»** — шаблонное описание у 10 репозиториев в трёх аккаунтах, включая `Quasar` с полноценным README. Это признак массового авто-создания репозиториев без классификации: описания нужно переписать или репозитории слитить.
7. **`surypus` issue-трекер:** 19 пар точных дублей (например, `#244/#73`, `#222/#72`, `#220/#71`, `#219/#70`, `#216/#140`, `#184/#64`, `#163/#162/#57`), 12 еженедельных робо-отчётов (`📈 Weekly Build Analytics`, `📦 Weekly Outdated Dependencies Report`). Из 129 реальных уникальных задач ~98.
8. **`dominicusin/trackerslist` уже помечен как дубль** с каноном `transgregorial/trackerslist` — корректный прецедент, который стоит применить остальным.

### 3.3 Гигиена

- 16 репозиториев без лицензии в метаданных — нельзя автоматически проверить соответствие при повторном использовании.
- 5 без README: `dominicusin/MessageGateway`, `dominicusin/spring-fleet-sapphire-monarch`, `neoallunity/allunity-{diskussii,knigi,zhurnaly}` (зеркала медиа).
- 11 форков без единой политики upstream: часть живые (`fidogate`, `zapret`, `onionshare`), часть — музейные (`shadowbroker`, `DokanCloudFS`, `rails_sample_app`).
- `surypus/surypus`: 82 workflow-файла при 0 открытых PR — инфраструктура процесса опережает сам продукт. Требуются tiering и устранение дублей (`stale.yml` + `stale-management.yml`, `security-scan` + `security-hardening` + `security-supply-chain`, `release-automation` + `semantic-release` + `release-drafter`).

### 3.4 Канонические адреса и документация

- `surypus.github.io`: `site_url` должен быть `https://surypus.github.io/surypus/`, иначе относительные ссылки вида `/ARCHITECTURE/` дают 404 (уже известная проблема).
- `neoallunity/README`, `neoallunity/.github`, `Magazine/README` — обновить ссылки на канонический монOREPO и текущий сайт; убрать устаревшие `dominicusin/integral-philosophy`.
- `dominicusin/dominicusin.github.io`: `.gitmodules` содержит сабмодули awesome-листов; нужно либо зафиксировать коммиты и добавить `--recurse-submodules` в CI, либо заменить на снимки контента — сейчас сборка зависит от внешних репозиториев без pinning-стратегии.

---

## 4. Целевая архитектура (правила, а не точечные правки)

1. **Один канон на артефакт.** Для каждого проекта ровно один репозиторий объявляется каноническим; остальные — архив с Readme «Moved to …» или mirror read-only. Это же правило применяется к issue-трекеру (дубли закрываются как `duplicate of #…` с сохранением ссылки).
2. **Категории репозитория фиксируются в метаданных:** `topic: product | library | infrastructure | site | archive | fork | mirror`, лицензия, `HOMEPAGE`, `CONTRIBUTING.md`, `SECURITY.md` — обязательны для активных.
3. **Три уровня CI:** `required` (build/test/lint/secret-scan), `informational` (coverage, benchmarks, analytics), `scheduled` (dependabot, stale, reports). Только `required` блокирует merge. Робо-отчёты не создают открытые issue в basic-трекере — они пишут в отдельный репозиторий/дашборд.
4. **Инструментальные цепочки фиксируются centrally:** GHC 9.6.5 + Stack 3.x (`surypus`), Python 3.11/3.12, Node 24, Hugo Extended 0.164.0, Ansible-core 2.14, Docker/compose версии для Wagtail. Версии хранятся в одном `.tool-versions`/flake и переиспользуются workflow.
5. **Секреты не в issue и не в чате:** `GITLEAKS_LICENSE`, токены деплоя, ключи подписи — через GitHub Secrets/OIDC или Hermes vault для локальных сценариев. Локальные тесты роли запускаются venv-интерпретатором (`~/.cache/ansvenv/bin/python`), системный `python3` без jinja2 использовать запрещено.
6. **Форки:** либо поддерживают `upstream` remote и политику rebase, либо переводятся в архив с пометкой «snapshot, no updates».

---

## 5. Приоритеты и дорожная карта

**P0 — 1–2 недели: вернуть работоспособность опорных проектов и убрать мусор в трекерах.**
**P1 — 3–6 недель: единая инфраструктура и канонизация.**
**P2 — 7–12 недель: доведение продуктов до демонстрационно рабочего состояния.**
**P3 — после 12 недель: долгосрочная автоматизация и публикации.**

### P0 — блокер №1: красный CI (приоритет по убыванию влияния)

| # | Задача | Репозиторий | Критерий готовности |
|---|---|---|---|
| 0.1 | Починить ansible-lint (10 замечаний) и перевести тесты на venv с jinja2 | `Linux-Serv-Ansible` | `CI` зелёный на `main` 3 запуска подряд; `ansible-lint` 0 ошибок, `pytest` в venv |
| 0.2 | Заменить `pip install -r requirements.txt` на `pip install -e .` / `uv sync` | `ai-orchestration-platform` | `AI Pipeline CI` зелёный; 13 тестов проходят; README соответствует реальной структуре |
| 0.3 | Починить шаблон `%` и smoke-тесты; разделить CI и deploy | `allunity-wagtail` | `CI` зелёный, 26+ тестов; `Deploy` либо зелёный, либо явно отключён с причиной |
| 0.4 | Восстановить `Monorepo CI` как required, убрать/починить `pip` Dependabot | `integral-philosophy` | обязательный workflow запускается на каждом push/PR; `pytest tests/` зелёный |
| 0.5 | Починить Biber/LaTeX-сборку и включить сохранение логов ≥30 дней | `Magazine` | `Build LaTeX Journal with Biber` зелёный или репозиторий переводится в archive с причиной |
| 0.6 | Выдать `attestations: write`/permissions либо убрать шаг attestations | `dominicusin.github.io` | `Supply Chain` зелёный; SBOM артефакт загружается |
| 0.7 | Добавить секрет `GITLEAKS_LICENSE` в vault и workflow | `surypus/surypus` | `Security Scan` зелёный без отключения проверки |
| 0.8 | Разобрать 3 падения `Package Maximizer CI/CD` | `package-maximizer` | 10 зелёных запусков подряд |

### P0 — блокер №2: дедупликация

| # | Задача | Критерий готовности |
|---|---|---|
| 0.9 | Закрыть 19 дублей issue в `surypus/surypus` как `duplicate`, оставить канонические номера | 129 → ~110 открытых; у каждой пары ссылка `duplicate of #…` |
| 0.10 | Перенести 12 робо-отчётов из issue в отдельный дашборд/репозиторий, отключить создание issue | 0 новых бот-issue в неделю |
| 0.11 | Обновить `neoallunity/README`, `.github/README`, `Magazine/README`: канон — `neoallunity/integral-philosophy` | Все ссылки на `dominicusin/integral-philosophy` и на 8 archived-модулей убраны из разделов «активные» |
| 0.12 | Зафиксировать `site_url` для `surypus.github.io` | Ссылки `/ARCHITECTURE/` открываются, 404 нет |
| 0.13 | Удалить/заархивировать 2 `demo-repository` и переписать 10 шаблонных описаний | 0 репозиториев с «utility repository in the dominicusin ecosystem» в описании |

### P1 — единая инфраструктура

| # | Задача | Критерий готовности |
|---|---|---|
| 1.1 | Создать репозиторий `ecosystem` (или `meta`) с `Taskfile`/`mise`, devcontainer и Nix flake | `task bootstrap` поднимает любое ядро за одну команду на Linux/macOS |
| 1.2 | Зафиксировать версии тулчейнов в `.tool-versions` и flake | GHC 9.6.5 / Stack 3 / Python 3.11+ / Node 24 / Hugo 0.164 / ansible-core 2.14 — JSON-вывод версий совпадает в CI и локально |
| 1.3 | Вынести повторяемые workflow в organization-level reusable workflows (`surypus/.github`, `neoallunity/.github`, `dominicusin/.github`) | Один `"ci-tier1"` workflow используется минимум 5 репозиториями |
| 1.4 | Внедрить обязательные проверки и защиту веток (`required checks`, 1 approver, no force push) на 7 ядрах | `gh api repos/{repo}/branches/{branch}/protection` возвращает конфиг для всех 7 |
| 1.5 | Единые шаблоны issue/PR, labels, CODEOWNERS, SECURITY.md, CONTRIBUTING.md | Активные репозитории (не архив, не форк) имеют все 5 артефактов |
| 1.6 | Политика лицензий: добавить лицензию или пометку «no license / private use» в 16 репозиториях | 0 активных репозиториев без лицензии |
| 1.7 | Сократить workflow-шум в `surypus`: 82 → ~15 required/informational/scheduled | Каждый workflow имеет владельца и назначенный tier; дубли объединены |
| 1.8 | Единая политика Dependabot/Renovate: group updates, авто-merge только patch у dev-зависимостей, обязательный manual review для runtime | Еженедельные `pip in /. - Update` перестают падать/засорять main |
| 1.9 | Секреты и OIDC: реестр секретов, ротация, запрет на `GITLEAKS_LICENSE` в коде | Секреты доступны через GitHub Secrets/vault; 0 секретов в diff за 30 дней |
| 1.10 | Реестр канонических репозиториев (`REGISTRY.yaml`) как single source of truth для скриптов и документации | `inventory.csv` и `REGISTRY.yaml` согласованы; CI проверяет расхождения |

### P2 — продукты до рабочего состояния

**S1 Surypus (главный продукт, самый высокий приоритет среди продуктов):**

- P2.1 Стабилизация сборки: `stack build` с GHC 9.6.5, починить `hashtables` на GCC 16 (issue `#66/#204`), подтвердить 792 теста.
- P2.2 Реальные данные вместо заглушек: `#57/#162/#163/#184` — заменить `pure (SomeResponse [])` на DAL-запросы; `#210` — настоящая валидация JWT; `#63/#180` — RBAC.
- P2.3 CQRS/event store: `#65/#185` → `#71/#220` → `#237` (Accounts Event Store) → read-model replay `#236`.
- P2.4 Вертикальный срез: логин → создание счёта → проводка → баланс → отчёт, покрытый property-тестами (`#197`, `#203`) и integration-тестами (`#233`).
- P2.5,QML/Web UI подключить к реальному API (`#73/#244`, `#202`); Prometheus — реальные метрики (`#72/#222`).
- P2.6 Документация: `docs/`, API reference и README привести к текущему состоянию (`#245`), исправить `site_url` (0.12).
- **Критерий готовности S1:** один скрипт `task demo` поднимает API+БД и проходит сценарий от registration до отчёта; required CI зелёный; 0 дублей issue.

**S2 NeoAllUnity:**

- P2.7 Канонизация монOREPO: `modules/*` — единственный источник; `Magazine/subprojects` и 8 archived-репозиториев — historical snapshot с README-указателями; `integral-philosophy` переименовать описание и структуру в README под реальное (`modules/`, а не `subprojects/` — сейчас не совпадает).
- P2.8 Опубликовать Wagtail-инстанс (сейчас задеплоен только статический mirror на PythonAnywhere, это другой код): выбрать хост, ограничить docker-compose, проверить `Deploy to CodeRed Cloud`.
- P2.9 Объединить сайтовую цепочку: `AllUnitySitemap` (Replit) → импорт в `allunity-wagtail` как задача генерации `/sitemap.xml`, а не отдельный сервис; `neoallunity/neoallunity` (legacy Django) пометить archived/live-freeze.
- P2.10 Медиа-зеркала `allunity-knigi/zhurnaly/diskussii` — перевести в data-репозитории с манифестом и README (сейчас 3 из 5 repo без README), исключить из CI-сборки контента, хранить как big files с checksums.
- P2.11 CI монOREPO в required-режим + `pytest tests/` + сборка web; убрать сломанные pip-Dependabot.
- **Критерий готовности S2:** один канон publishes-пайплайн, живой Wagtail-сайт, 8 archived-модулей больше не упоминаются как активные.

**S3 Infra & ops:**

- P2.12 `Linux-Serv-Ansible`: зелёный lint + idempotent-прогон на wdmch (192.168.1.2) с `--check`, затем реальный прогон; тесты роли — только venv-интерпретатором.
- P2.13 `alpine-wdmch-builder`: зафиксировать релизный процесс (уже есть build/release/validate), проверить control-суммы образов, версия ядра 6.18.x, documented procedure проверки флешки до прошивки.
- P2.14 Конфиги: выбрать канон（`guix-config` для рабочей станции + `Quasar` как flake; `my-nixos-config` — legacy; `nixos-config` —archive）。
- P2.15 Форки: для `fidogate`, `zapret`, `onionshare` — политика upstream; `shadowbroker`, `rails_sample_app`, `deepsite-locally`, `academicpages.github.io`, `DokanCloudFS`, `zfs-win` — архив/snapshot с пометкой.
- **Критерий готовности S3:** `task infra-check` запускает lint + idempotency check и возвращает 0; каждый активный репо имеет владельца и понятный статус upstream.

**S4 Site & knowledge:**

- P2.16 Hugo — канон; `astro-experiment` — либо experiment с явным STEADY/ARCHIVED статусом, либо удалён. `#site_url`, SBOM, security-scan — зелёные.
- P2.17 Собрать одно CV из `Awesome-CV` / `Modern-Simple-CV` / `resume`; остальные — archive с указанием канона.
- P2.18 `.github` личного аккаунта: заменить чужой README про AlphaEvolve на профиль/индекс экосистемы.
- P2.19 Сабмодули: зафиксировать коммиты, добавить проверку `git submodule status` в CI или убрать внешние awesome-сабмодули.
- **Критерий готовности S4:** сайт деплоится, 0 красных required-проверок, 1 каноническое CV.

**S5 R&D:**

- P2.20 `package-maximizer`: починить CI, зафиксировать PyPI/ReadTheDocs как каноническую публикацию.
- P2.21 `polyresolver` и `MessageGateway`: сейчас Phase 0/spec + пустой README; либо объединить в `haskell-lab` с общим cabal.project, либо архивировать с SRS на месте.
- P2.22 `ai-orchestration-platform`: после 0.2 Decide — полезный инструмент или archived experiment; 99+ провайдеров и 925+ тестов в описании конфликтуют с 13 тестами в README. Привести цифры в соответствие с реальностью.
- P2.23 `uaw`, `spring-fleet-sapphire-monarch`: categorize или archive.
- **Критерий готовности S5:** у каждого репозитория есть один из статусов `product | library | spec-only (archived)` и соответствующий CI.

---

## 6. Воспроизводимая инфраструктура разработки (детальная спецификация)

### 6.1 Структура мета-репозитория

```text
ecosystem/
├── REGISTRY.yaml          # канон каждого артефакта: repo, owner, system, tier, status, license
├── toolchain/
│   ├── .tool-versions     # ghc, stack, node, python, hugo, ansible-core
│   ├── flake.nix          # nix develop — полная среда
│   └── Dockerfile.dev     # devcontainer
├── workflows/
│   ├── tier1-build.yml    # reusable: build + unit tests + lint + secret scan
│   ├── tier2-quality.yml  # reusable: coverage, docs, SBOM (informational)
│   └── scheduled.yml      # reusable: stale, dependency graph, reports → не в issues
├── templates/
│   ├── issue.yml, pr.yml, security.yml, contributing.md, codeowners
├── scripts/
│   ├── inventory.py       # проверка REGISTRY.yaml ↔ GitHub API (в т.ч. inventory.csv)
│   ├── dedup-issues.py    # находит дубли и робо-отчёты в issue-трекерах
│   └── ci-health.py       # сводка conclusion по защищённым веткам
└── docs/
    ├── ADR-0001-canonical-repos.md
    ├── ADR-0002-ci-tiers.md
    └── RUNBOOK.md
```

### 6.2 Контракт проверок

| Tier | Проверки | Блокирует merge |
|---|---|---|
| `tier1` | build, unit tests, formatter/linter, secret scan, license check | Да |
| `tier2` | coverage, benchmarks, SBOM, docs build, link check, cross-compile | Нет (отчёт в PR) |
| `scheduled` | deps, stale, analytics | Не создаёт issue |

### 6.3 Версии (единая точка)

| Инструмент | Версия | Где используется |
|---|---|---|
| GHC / Stack | 9.6.5 / 3.x | `surypus`, Haskell R&D |
| Python | 3.11+ (3.12 для Wagtail) | `surypus` scripts, `allunity-wagtail`, `package-maximizer`, `integral-philosophy` |
| Node | 24 | `dominicusin.github.io`, `surypus` JS-часть, workflow Actions |
| Hugo Extended | 0.164.0 | `dominicusin.github.io` |
| ansible-core | 2.14 | `Linux-Serv-Ansible` (тесты — из venv `~/.cache/ansvenv`) |
| Docker/compose | pin в compose file | `allunity-wagtail`, `package-maximizer` |

### 6.4 Секреты

- `GITLEAKS_LICENSE` — для `surypus/surypus` Security Scan.
- OIDC для деплоя Pages/Cloud — без статических токенов.
- Локальные секреты — только `hermes-vault`/GitHub Secrets; никогда в issue, README или чате.
- Проверка утечек — `gitleaks`/`secret-guard` в tier1, плюс еженедельный аудит.

### 6.5 Приёмка инфраструктуры

`task ci-health --org dominicusin --org surypus --org neoallunity` печатает таблицу: репозиторий → system → tier → последний conclusion на защищённой ветке → нарушает ли контракт. Цель: 0 нарушений среди ядер.

---

## 7. Порядок выполнения и зависимости

```
0.1–0.8 (CI)  ─┬─→ 1.1–1.4 (meta-repo, toolchain, reusable workflows, branch protection)
0.9–0.13 (cleanup) ─┘        │
                             ├─→ 2.x (продукты: S1 → S2 → S3 → S4 → S5)
                             └─→ 1.5–1.10 (шаблоны, лицензии, тиры, секреты, REGISTRY)
```

Почему именно так: без зелёного tier1 в ядрах любая «унификация» просто растиражирует красные проверки в 7 репозиториях. Без очистки issue-трекера приоритеты P2 невозможно отследить. S1 идёт первым среди продуктов, потому что у него есть уже определённый вертикальный срез и активный issue-бэклог; S2 — второй, потому что требует организационного решения о каноническом сайте.

---

## 8. Метрики успеха

| Метрика | Сейчас | Цель |
|---|---|---|
| Ядра с зелёным required CI | 2 / 7 | 7 / 7 |
| Дублирующие репозитории (активные) | 8 модулей + 3 CV + 4 конфига + 2 demo | 0 |
| Открытые issue `surypus` | 129 (19 дублей + 12 ботов) | ≤ 98 уникальных, 0 дублей |
| Активные репозитории без лицензии / README / CONTRIBUTING | 16 / 5 / 9 | 0 / 0 / 100% активных |
| Workflow на репозиторий (surypus) | 82 | ≤ 15 с владельцами и tier |
| Время от push до verdict tier1 | измеряется вручную | ≤ 10 мин, один reusable workflow |
| Воспроизводимость сборки | частично (alpine-wdmch, wagtail) | `task bootstrap` + `nix develop` для всех ядер |

---

## 9. Риски

| Риск | Митигация |
|---|---|
| Архивация модулей сломает старые ссылки/_tag | Оставить archived repo с README «Moved to …», не удалять; сохранить теги |
| Переход Wagtail в прод прервет live allunity.ru | Сначала parallel run + smoke-тесты, затем DNS/редирект; откат — freeze legacy |
| Исправление CI потребует прав на секреты/attestations | Проверить видимость секретов через gh api; если прав нет — явно зафиксировать блокер, не отключать проверку молча |
| GCC 16 / GHC 9.6.5 несовместимость (`hashtables`) | Pin toolchain через flake до обновления пакета; завести отдельный ADR |
| Массовое переименование/архивация вызовет путаницу | REGISTRY.yaml + обновлённые org-README + ADR до начала изменений |

---

## 10. Решения, которые нужно зафиксировать в ADR

1. **ADR-0001:** канонические репозитории для каждой из 6 систем и статус всех остальных (archive / fork / mirror / experiment).
2. **ADR-0002:** CI tiering и rule «required checks только из tier1».
3. **ADR-0003:** Wagtail — канонический сайт NeoAllUnity; legacy Django — freeze; `AllUnitySitemap` — задача внутри Wagtail.
4. **ADR-0004:** `surypus` — продуктовый репозиторий, robots-отчёты не создают issue; бэклог хранится в issue, дубли закрываются.
5. **ADR-0005:** политика форков и порядок upstream-синхронизации.

---

Приложение A — полный реестр всех 78 репозиториев с решениями: `inventory.csv`.
Приложение B — развёрнутый список репозиториев по системам: ниже.

---

## Приложение B — реестр по системам


### S1 Surypus ERP/CRM (6)

| Репозиторий | Язык | Обновлён | Статус | Решение |
|---|---|---|---|---|
| `surypus/.github` | — | 2026-09-04 | active | KEEP — supporting |
| `surypus/.github-private` | — | 2026-09-04 | active | KEEP — supporting |
| `surypus/Ergonomicguiforerpcrm` | TypeScript | 2026-09-04 | active | FIX metadata or MERGE |
| `surypus/demo-repository` | HTML | 2026-09-03 | active | ARCHIVE — demo junk |
| `surypus/surypus` | JavaScript | 2026-10-30 | active | KEEP — primary |
| `surypus/surypus.github.io` | HTML | 2026-10-11 | active | KEEP — supporting |

### S2 NeoAllUnity publishing (23)

| Репозиторий | Язык | Обновлён | Статус | Решение |
|---|---|---|---|---|
| `dominicusin/AllUnitySitemap` | TypeScript | 2026-08-27 | active | CONSOLIDATE / DECIDE |
| `dominicusin/neoallunity` | CSS | 2026-08-27 | active | CONSOLIDATE / DECIDE |
| `neoallunity/.github` | — | 2026-08-25 | fork | FORK — set upstream policy |
| `neoallunity/.github-private` | — | 2026-08-27 | active | FIX metadata or MERGE |
| `neoallunity/Magazine` | Python | 2026-08-27 | active | CONSOLIDATE / DECIDE |
| `neoallunity/README` | — | 2026-08-27 | active | KEEP — supporting |
| `neoallunity/allunity-diskussii` | HTML | 2026-08-27 | active | KEEP — supporting |
| `neoallunity/allunity-divio` | Python | 2026-08-31 | active | CONSOLIDATE / DECIDE |
| `neoallunity/allunity-knigi` | HTML | 2026-08-27 | active | KEEP — supporting |
| `neoallunity/allunity-wagtail` | Python | 2026-09-02 | active | KEEP — primary |
| `neoallunity/allunity-zhurnaly` | HTML | 2026-08-27 | active | KEEP — supporting |
| `neoallunity/demo-repository` | HTML | 2026-08-27 | archived | ARCHIVE — demo junk |
| `neoallunity/integral-philosophy` | HTML | 2026-08-27 | active | KEEP — primary |
| `neoallunity/integral-philosophy-cli` | — | 2026-08-25 | archived | KEEP archived (merged) |
| `neoallunity/integral-philosophy-config` | — | 2026-08-25 | archived | KEEP archived (merged) |
| `neoallunity/integral-philosophy-content` | — | 2026-08-25 | archived | KEEP archived (merged) |
| `neoallunity/integral-philosophy-core` | Python | 2026-08-25 | archived | KEEP archived (merged) |
| `neoallunity/integral-philosophy-deploy` | — | 2026-08-25 | archived | KEEP archived (merged) |
| `neoallunity/integral-philosophy-docs` | — | 2026-08-25 | archived | KEEP archived (merged) |
| `neoallunity/integral-philosophy-tests` | — | 2026-08-25 | archived | KEEP archived (merged) |
| `neoallunity/integral-philosophy-web` | Python | 2026-08-25 | archived | KEEP archived (merged) |
| `neoallunity/neoallunity` | Python | 2026-08-27 | active | CONSOLIDATE / DECIDE |
| `neoallunity/web-capture-pal` | TypeScript | 2026-08-27 | active | FIX metadata or MERGE |

### S3 Infra & ops (16)

| Репозиторий | Язык | Обновлён | Статус | Решение |
|---|---|---|---|---|
| `dominicusin/DokanCloudFS` | C# | 2026-08-27 | fork | FORK — set upstream policy |
| `dominicusin/How-To-Secure-A-Linux-Server-With-Ansible` | Jinja | 2026-08-27 | fork | FORK — set upstream policy |
| `dominicusin/Linux-Serv-Ansible` | Haskell | 2026-11-08 | active | KEEP — primary |
| `dominicusin/Quasar` | Nix | 2026-08-27 | active | FIX metadata or MERGE |
| `dominicusin/alpine-wdmch-builder` | Shell | 2026-10-06 | active | KEEP — primary |
| `dominicusin/chocolatey-packages` | — | 2026-08-27 | active | KEEP — supporting |
| `dominicusin/fidogate` | C | 2026-08-27 | fork | FORK — set upstream policy |
| `dominicusin/gsi-x6812b` | Shell | 2026-10-09 | active | KEEP — supporting |
| `dominicusin/guix-config` | Scheme | 2026-08-27 | active | CONSOLIDATE / DECIDE |
| `dominicusin/my-nixos-config` | Nix | 2026-08-27 | active | CONSOLIDATE / DECIDE |
| `dominicusin/nixos-config` | Nix | 2026-08-27 | active | CONSOLIDATE / DECIDE |
| `dominicusin/onionshare` | Python | 2026-08-27 | fork | FORK — set upstream policy |
| `dominicusin/package-maximizer` | Python | 2026-10-22 | active | KEEP — primary |
| `dominicusin/shadowbroker` | Python | 2026-08-27 | fork | FORK — set upstream policy |
| `dominicusin/zapret` | C | 2026-08-27 | fork | FORK — set upstream policy |
| `dominicusin/zfs-win` | C++ | 2026-08-27 | active | KEEP — supporting |

### S4 Site & knowledge (16)

| Репозиторий | Язык | Обновлён | Статус | Решение |
|---|---|---|---|---|
| `dominicusin/.github` | Jupyter Notebook | 2026-08-27 | active | KEEP — supporting |
| `dominicusin/Awesome-CV` | TeX | 2026-08-27 | active | CONSOLIDATE / DECIDE |
| `dominicusin/Layerstructureforfigma` | TypeScript | 2026-08-27 | active | FIX metadata or MERGE |
| `dominicusin/Modern-Simple-CV` | TeX | 2026-08-27 | active | FIX metadata or MERGE |
| `dominicusin/academicpages.github.io` | — | 2026-08-25 | archived | REVIEW archive (keep historical) |
| `dominicusin/astro-experiment` | Astro | 2026-09-08 | active | KEEP — supporting |
| `dominicusin/docs` | MDX | 2026-08-25 | archived | REVIEW archive (keep historical) |
| `dominicusin/dominicusin` | — | 2026-11-12 | active | KEEP — supporting |
| `dominicusin/dominicusin.dev-portfolio` | TypeScript | 2026-08-27 | active | FIX metadata or MERGE |
| `dominicusin/dominicusin.github.io` | JavaScript | 2026-10-23 | active | KEEP — primary |
| `dominicusin/miniature-succotash` | TeX | 2026-08-25 | archived | REVIEW archive (keep historical) |
| `dominicusin/pmo-solovyov-article` | TeX | 2026-08-27 | active | KEEP — supporting |
| `dominicusin/resume` | TeX | 2026-08-27 | active | CONSOLIDATE / DECIDE |
| `dominicusin/vite-react` | CSS | 2026-08-27 | active | FIX metadata or MERGE |
| `dominicusin/webring` | Nunjucks | 2026-08-27 | active | KEEP — supporting |
| `dominicusin/website-optimization` | TypeScript | 2026-08-27 | active | FIX metadata or MERGE |

### S5 R&D / Haskell (6)

| Репозиторий | Язык | Обновлён | Статус | Решение |
|---|---|---|---|---|
| `dominicusin/MessageGateway` | Haskell | 2026-10-18 | active | CONSOLIDATE / DECIDE |
| `dominicusin/ai-orchestration-platform` | Python | 2026-08-27 | active | CONSOLIDATE / DECIDE |
| `dominicusin/carma-public` | Haskell | 2026-08-27 | fork | FORK — set upstream policy |
| `dominicusin/polyresolver` | Haskell | 2026-10-19 | active | CONSOLIDATE / DECIDE |
| `dominicusin/spring-fleet-sapphire-monarch` | JavaScript | 2026-10-19 | active | KEEP — supporting |
| `dominicusin/uaw` | Python | 2026-10-20 | active | KEEP — supporting |

### S6 Other (11)

| Репозиторий | Язык | Обновлён | Статус | Решение |
|---|---|---|---|---|
| `dominicusin/AppCenter` | — | 2026-08-25 | archived | REVIEW archive (keep historical) |
| `dominicusin/ConsoleApp1` | F# | 2026-08-27 | archived | REVIEW archive (keep historical) |
| `dominicusin/cautious-carnival` | — | 2026-08-25 | archived | REVIEW archive (keep historical) |
| `dominicusin/deepsite-locally` | TypeScript | 2026-08-27 | fork | FORK — set upstream policy |
| `dominicusin/desktop-tutorial` | — | 2026-08-27 | archived | REVIEW archive (keep historical) |
| `dominicusin/fudforum` | — | 2026-08-25 | archived | REVIEW archive (keep historical) |
| `dominicusin/hugo-quickstart` | HTML | 2026-08-25 | archived | REVIEW archive (keep historical) |
| `dominicusin/mydocs` | Python | 2026-08-25 | archived | REVIEW archive (keep historical) |
| `dominicusin/preview` | TypeScript | 2026-08-25 | archived | REVIEW archive (keep historical) |
| `dominicusin/rails_sample_app` | Ruby | 2026-08-27 | fork | FORK — set upstream policy |
| `dominicusin/trackerslist` | — | 2026-09-08 | archived | REVIEW archive (keep historical) |
