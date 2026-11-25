# MASTER IMPLEMENTATION PLAN — экосистема dominicusin / surypus / neoallunity

**Дата:** 2026-11-25. **Статус:** полный аудит выполнен, план исполнения.

**Источники и артефакты:**
- `repository-audit.json` — полный аудит 78 репозиториев: метаданные, ветки, protection, releases, security-алерты, коммиты за 90 дней, манифесты зависимостей, workflow-файлы.
- `source-inspection.json` — выгрузка структуры и исходного кода 9 ключевых репозиториев (surypus, uaw, MessageGateway, polyresolver, Linux-Serv-Ansible, ai-orchestration-platform, package-maximizer, allunity-wagtail, integral-philosophy).
- `PLAN.md` + `inventory.csv` — предыдущая группировка и реестр 78 репозиториев с решениями.
- Присланный стратегический черновик — использован как источник доменов, бэклога и целевых архитектур; все его оценки помечены здесь как `[ПРОВЕРЕНО]`, `[ЧАСТИЧНО]` или `[ПРОПОЗИЦИЯ]`.

**Правило достоверности:** ни одна задача не считается выполненной без артефакта-доказательства (зелёный required CI, тест, release tag, зафиксированный `gh api`-ответ). Заявленное в README состояние доказательством не является.

---

## 0. Резюме: что изменилось после полного аудита

1. **[ПРОВЕРЕНО] Репозиториев 78, а не 75** (51 личный, 6 `surypus`, 21 `neoallunity`). Фаза 0 из присланного плана завершена: `repository-audit.json` уже содержит требуемый audit dump.
2. **[ПРОВЕРЕНО] Активность за 90 дней:** 834 коммита (с ограничением 100 на репозиторий); 18 репозиториев — ноль коммитов. Ядра: `surypus`, `dominicusin`, `dominicusin.github.io`, `Linux-Serv-Ansible`, `package-maximizer`, `alpine-wdmch-builder` (по 100+), `allunity-wagtail` (76).
3. **[ПРОВЕРЕНО] Security-долг:** 870 открытых Dependabot-алертов и 133 открытых Code Scanning-алерта (счётчики ограничены 100 на репозиторий, реально больше). Максимум — в форках и legacy-сайтах, но 33 алерта в `surypus/surypus` и 100 в `dominicusin.github.io` — в активных ядрах.
4. **[ПРОВЕРЕНО] Защита веток:** только 6 репозиториев из 78 (`surypus`, `dominicusin.github.io`, `package-maximizer`, `ai-orchestration-platform`, `integral-philosophy`, `Magazine`). Relese-процесс есть лишь у 5.
5. **[ПРОВЕРЕНО] Surypus уже имеет код JWT, RBAC и tenant-context** — вопреки осторожной формулировке черновика. Но есть конкретные дыры: `src/MultiTenancy/Isolation.hs:37` — `getTenantFromRequest = pure Nothing`, `:41` — `checkTenantAccess = pure True`; `src/Surypus/API/AuthMiddleware.hs:43` — `authenticateRequest` использует третий аргумент (method) как Authorization header и нигде не вызывается; `src/Surypus/JWT/Token.hs:95` — при генерации токена `role` всегда пустой список. Это «ложное состояние выполнено» в чистом виде: функции существуют, но не верифицируют.
6. **[ПРОВЕРЕНО] UAW действительно хранит состояние в JSON-файлах** (`core/state_manager.py:77,93`, `core/uaw_core.py:186,210`), при этом в репозитории есть `orchestrator/workflow_engine.py` и 10 тестов, но нет транзакционного хранилища, idempotency keys и policy-engine как отдельного компонента.
7. **[ПРОВЕРЕНО] Главный блокер — не архитектура, а работоспособность:** 5 из 8 ядер имеют систематически красный CI (детали в §1.4). Приоритет P0 смещён: сначала зелёный CI и устранение дыр в авторизации, затем новые модули.

---

## 1. Результаты полного аудита

### 1.1 Портфель

| Показатель | Значение |
|---|---|
| Репозиториев | 78 = 51 + 6 + 21 |
| Архивировано / форков | 21 / 11 |
| Без README / без лицензии | 5 / 16 |
| С Actions | 26 |
| С защитой ветки | 6 |
| С release | 5 |
| Коммиты за 90 дней (cap 100/репо) | 834; 18 репозиториев без коммитов |
| Открытые Dependabot-алерты | 870 (cap 100/репо) |
| Открытые Code Scanning-алерты | 133 (cap 100/репо) |
| Открытые issue в `surypus` | 129 = 19 точных дублей + 12 робо-отчётов + ~98 уникальных |

### 1.2.Security-алерты (топ)

| Репозиторий | Dependabot | Code scanning |
|---|---:|---:|
| `dominicusin/carma-public` | 100+ | — |
| `dominicusin/deepsite-locally` | 100+ | — |
| `dominicusin/rails_sample_app` | 100+ | — |
| `dominicusin/webring` | 100+ | — |
| `neoallunity/neoallunity` | 100+ | — |
| `dominicusin/website-optimization` | 80 | — |
| `dominicusin/neoallunity` | 66 | — |
| `dominicusin/onionshare` | 62 | — |
| `dominicusin/AllUnitySitemap` | 56 | — |
| `dominicusin/dominicusin.github.io` | 18 | 100 (cap) |
| `surypus/surypus` | — | 33 |

Вывод: 870 алертов — это не «technically debt», а маскировка реальных уязвимостей. Триаж по правилу: активный репозиторий → чинить или документировать accepts-risk; архив/форк → закрыть как `wontfix` с причиной и перевести в archived.

### 1.3 Ветки и релизы

- Защищены только 6 репозиториев (список выше). Остальные 72 — без required checks, значит «CI зелёный» не блокирует merge нигде, кроме этих шести.
- Релизы: `alpine-wdmch-builder v3.21.8-15` (2026-09-30), `package-maximizer v0.21.0` (2026-09-08), `surypus v1.1.1`, `dominicusin.github.io v0` (2025-10-20), `pmo-solovyov-article build-3`. У остальных 73 — ни одного release, хотя часть — активные продукты.

### 1.4 Фактический CI на защищённых/основных ветках

| Репозиторий | Результат | Причина (из логов) |
|---|---|---|
| `Linux-Serv-Ansible` | 20 failures / 30 | ansible-lint: 10 ошибок в 353 файлах; `ModuleNotFoundError: jinja2` (тесты не в venv) |
| `ai-orchestration-platform` | 7 / 7 failures | `Could not open requirements file: 'requirements.txt'` |
| `Magazine` | 24 / 30 failures | LaTeX/Biber; старые логи недоступны (HTTP 410) |
| `allunity-wagtail` | 13 / 30 failures | `Could not parse the remainder: '%'` в шаблоне; deploy падает отдельно |
| `integral-philosophy` | `Monorepo CI` последний успех 27.08 | Further только dynamic Dependabot, `pip in /. - Update` еженедельно красный |
| `dominicusin.github.io` | 3 / 30 failures | SBOM: `Failed to persist attestation: Resource not accessible by integration` |
| `surypus` | 1 / 30 failure | `Security Scan`: `missing gitleaks license` |
| `package-maximizer` | 3 / 30 failures | `Package Maximizer CI/CD` |
| `neoallunity/neoallunity` | 17 / 25 failures | Dependabot `node-forge` в legacy Django |

### 1.5 Верификация исходного кода ключевых проектов

**Surypus** (384 `.hs` в `src/`, 81 spec-файл в `test/`):
- JWT: `src/Surypus/JWT/Token.hs` — HS256, `verifyClaims` с audience `"surypus-api"`, exp/iat; secret из `SURYPUS_JWT_SECRET`; есть `defaultSecretKey` «DO NOT USE IN PRODUCTION».
- RBAC: `src/Surypus/API/Authorization.hs` (Permission/Resource, path→permission), `src/Surypus/RBAC.hs`, middleware `withAuthzResolverAdvanced` проверяет `checkPerm userId permission` И role-based fallback; тесты `test/RBACCanonSpec.hs`, `test/JWTSpec.hs`.
- Tenant: `src/DAL/Database.hs` — `IORef`-контекст и `set_config('app.tenant_id', …)`, `src/MultiTenancy/Middleware.hs` — контекст из verified JWT claim `tenant_id`. Но `src/MultiTenancy/Isolation.hs` содержит два stub-значения (`pure Nothing`, `pure True`), которые более нигде не вызываются — удалить или реализовать и покрыть негативными тестами.
- Бухгалтерия: `src/Core/Accounting/ReadModel.hs`, `src/Finance/AccTurn2.hs`, `test/QuickCheckInvariantsSpec.hs`, `test/Domain/InvariantsSpec.hs` — property-тесты существуют, но debit=credit инвариант требует отдельного integration-теста на реальной БД.
- Остальный мусор: в `src/` лежат `.planning/` и `.claude/` — 4896 `.md` файлов в репозитории, что объясняет 244 МБ рабочего дерева и шум в grep. Вынести planning-архив из `src/` в отдельный каталог/репозиторий.
- Локальная сборка не запускалась: GHC 9.10.3 против resolver lts-22.21 / CI GHC 9.6.5 — несовместимость версий; требуется pin через flake/Nix (см. §8).

**UAW** (80 `.py`, 10 тестов):
- `core/state_manager.py` и `core/uaw_core.py` читают/пишут состояние через `json.dump` — нет транзакционности и locking.
- `orchestrator/workflow_engine.py`, `core/audit.py`, `config/automation_config.py` (idempotency упоминается), `adapters/registry.py` — каркас есть, но capability discovery и реальные доступы не верифицированы.
- Вывод: план черновика верен — P0 UAW = persistent state + idempotency + approvals + verification, а не новые интеграции.

**NeoAllUnity:** `integral-philosophy` — 1271 файл, но 498 `.dot` и 216 `.html` — это сгенерированные артефакты, а не исходники; `Magazine` дублирует `subprojects/*` после слияния; `allunity-wagtail` — 27 страниц, миграции воспроизводимы, но живой инстанс отсутствует.

---

## 2. Сверка с присланным черновиком

| Утверждение черновика | Вердикт | Что делать |
|---|---|---|
| «75 репозиториев» | `[ПРОВЕРЕНО]` — 78 | Обновить все упоминания в документации |
| «Полный аудит ещё не сделан» | `[ПРОВЕРЕНО]` — сделан | Использовать `repository-audit.json` как Фазу 0 |
| «Surypus JWT/RBAC/tenant isolation требуют реализации с нуля» | `[ЧАСТИЧНО]` — код есть, но есть stubs и fail-open paths | Не переписывать, а верифицировать и закрыть конкретные дыры (§5.1) |
| «UAW — JSON-state, нужен execution framework» | `[ПРОВЕРЕНО]` | Реализовать transactional state, planner/engine split, idempotency, approvals |
| «FTN/Usenet — отдельная система» | `[ПРОПОЗИЦИЯ]` принята | Выделить в S5, не смешивать с UAW/Surypus |
| «Systems lab Guix/Nix/BSD/Plan9» | `[ЧАСТИЧНО]` — Guix/Nix-репозитории есть, BSD/Plan9-репозиториев в аккаунтах нет | Создать каталог как новую инициативу, не выдавать за существующую |
| «Portfolio repository как источник истины» | `[ПРОПОЗИЦИЯ]` принята | Объединить с предложенным `ecosystem/meta` в один `dominicusin/portfolio` |
| «Приоритет P0 — безопасность/финансовые инварианты» | `[ПРОПОЗИЦИЯ]` принята с поправкой | P0 = зелёный required CI + безопасность/инварианты; новые фичи — после |
| «Не считать dependency analytics задачами разработки» | `[ПРОВЕРЕНО]` — 12 робо-issue в `surypus` | Перенести отчёты в дашборд, отключить создание issue |

---

## 3. Целевая карта систем

| ID | Система | Канонические репозитории | Роль | Приоритет | Решение по остальным |
|---|---|---|---|---|---|
| S1 | **Surypus ERP/CRM** | `surypus/surypus`, `surypus.github.io` | Бизнес-ядро: учёт, RBAC, event sourcing | P0 | `Ergonomicguiforerpcrm` → UI-спайк внутри S1; `demo-repository` → archive |
| S2 | **UAW agentic workspace** | `dominicusin/uaw` | Execution framework, workflow DAG, audit | P0 | `ai-orchestration-platform` → отдельный R&D, не часть UAW до стабилизации CI |
| S3 | **NeoAllUnity publishing** | `neoallunity/integral-philosophy`, `allunity-wagtail`, `Magazine` (archive snapshot), `AllUnitySitemap` (в pipeline) | Knowledge platform + CMS | P1 | 8 archived module-репозиториев — read-only; `neoallunity/neoallunity` — legacy freeze; медиа-зеркала — data |
| S4 | **Systems & infrastructure** | `Linux-Serv-Ansible`, `alpine-wdmch-builder`, `gsi-x6812b`, `guix-config`, `Quasar`, `my-nixos-config` | Воспроизводимая системная лаборатория | P0/P1 | `nixos-config` — archive (legacy 2018); BSD/Plan9 — новые каталоги в portfolio |
| S5 | **FTN / messaging** | `MessageGateway`, `fidogate`, `polyresolver` (R&D), Husky/HPT как external | Маршрутизация FTN/NNTP/email | P1 | `zapret`, `onionshare`, `shadowbroker` — форки с политикой upstream, не часть S5 |
| S6 | **Site & knowledge** | `dominicusin.github.io`, `docs`, `.github`, `resume`/`Awesome-CV` (один канон) | Публичный интерфейс портфеля | P1 | `astro-experiment` — experiment с явным статусом; 3 CV → 1 |
| S7 | **R&D / libraries** | `package-maximizer`, `ai-orchestration-platform`, `polyresolver`, `uaw` adapters | Библиотеки и эксперименты | P1/P2 | Каждый получает статус `product | library | spec-only (archived)` |
| S8 | **Archive / forks / mirrors** | 21 archived + 11 forks + 10 «utility» stubs | История и внешние snapshot | P3 | Политика: archived + причина; fork + upstream policy; 0 шаблонных описаний |

Отображение всех 78 репозиториев по системам — в `inventory.csv`, граф зависимостей и метрики — в `repository-audit.json`.

---

## 4. Portfolio Control Plane

Создаётся **один** репозиторий `dominicusin/portfolio` (вместо двух предложений `ecosystem` и `portfolio` в черновике/предыдущем плане). Он заменяет `PLAN.md` как операционный источник истины; текущие `inventory.csv` и `repository-audit.json` переносятся в него.

```text
dominicusin/portfolio/
├── README.md, PORTFOLIO.md, ROADMAP.md, STATUS.md, PRIORITIES.md
├── DECISIONS.md, RISKS.md, DEPENDENCIES.md
├── repository-audit.json          # уже готов
├── inventory.csv                  # уже готов
├── source-inspection.json         # уже готов
├── domains/{business,agentic,systems,networking,publishing,web}/
├── projects/{surypus,uaw,neoallunity,infrastructure,ftn,website,...}.yaml
├── schemas/{project,task,milestone}.schema.json
├── automation/{github,audit,release,reporting}/
├── workflows/{tier1-build,tier2-quality,scheduled}.yml
├── templates/{issue,pr,security,contributing,codeowners}
└── .github/workflows/portfolio-weekly.yml
```

**Карточка проекта (обязательные поля):**

```yaml
project:
  id: surypus
  name: Surypus ERP/CRM
  domain: business-systems
  system: S1
  status: ACTIVE            # DISCOVERY|SPEC|READY|ACTIVE|BLOCKED|VERIFY|RELEASE|MAINTENANCE|ARCHIVED
  priority: P0
  repository: [surypus/surypus, surypus/surypus.github.io]
  owner: dominicusin
  objective: Verified accounting and ERP core
  milestones: [{id: core-stability, status: ACTIVE}]
  dependencies: [PostgreSQL, CI, Authentication, Authorization]
  risks: [RBAC correctness, tenant isolation, financial invariants]
  completion: {build: required, unit_tests: required, integration_tests: required,
               security_review: required, release_verification: required}
  evidence:                  # обязательно для статуса VERIFY/RELEASE
    ci: https://github.com/.../actions/runs/...
    release: v1.1.1
    test_report: ...
```

**Единые метки:** `priority/P0..P3`, `type/{bug,feature,refactor,research,documentation,security,infrastructure}`, `status/{discovery,ready,active,blocked,verify}`, `domain/{surypus,agentic,infrastructure,ftn,publishing,philosophy,web}`, `verified/*` (подтверждено артефактом).

**Автоматизация (ежедневно/еженедельно):** `automation/audit/` переиспользует скрипты, уже применённые в этом аудите: список репозиториев, CI conclusion на защищённых ветках, security-алерты, дубли issue, расхождение roadmap и кода, 180-дневная неактивность. Выход — `PORTFOLIO WEEKLY REPORT` в issue `portfolio`, а не в basic-трекерах проектов.

---

## 5. Детальные планы по системам

### 5.1 S1 Surypus — P0, главный продукт

**Верифицированная отправная точка:** сборка и тесты в CI в основном зелёные (29/30), 384 модуля, 81 spec, release `v1.1.1`, защита ветки включена. Следовательно задача — **не «собрать заново», аProve: устранить конкретные дыры и доказать инварианты**.

| ID | Задача (точный файл/issue) | Критерий готовности |
|---|---|---|
| SUR-001 | Удалить/реализовать stubs в `MultiTenancy/Isolation.hs`: `getTenantFromRequest = pure Nothing`, `checkTenantAccess = pure True` | Негативные тесты: запрос без валидного tenant → 403; попытка чтения чужого `tenant_id` → 403; 0 stubs в `.hs` |
| SUR-002 | Убрать `authenticateRequest _secret _path method` (method как Authorization header) и `defaultSecretKey` из production-пути | Dead code удалён; secret только из `SURYPUS_JWT_SECRET`; тест на отсутствие env → явный fail старта |
| SUR-003 | JWT: `role`claim всегда `[]` при генерации (`JWT/Token.hs:95`); добавить проверку `iss`, refresh replay detection (`RefreshTokenRepo`), expiry/audience тесты | `JWTSpec` проверяет подпись, exp, aud, iss, rotation, replay; 0 обходов |
| SUR-004 | RBAC:все endpoints path→permission; deny-by-default; тесты `#243` и `RBACCanonSpec` | 100% unprotected endpoints перечислены в publicPaths и обоснованы; негативные тесты проходят |
| SUR-005 | Tenant isolation: контекст из verified JWT, `set_config('app.tenant_id')`, RLS-политики в БД, тест кросс-tenant доступа | Два tenant в тестовой БД; ни один запрос не видит чужие строки; `#210`-аналог для tenant |
| SUR-006 | Реальные DAL вместо заглушек: `#57/#162/#163/#184`; DB connection обязателен | 0 handlers с `pure []`/empty response; API без БД не стартует; `#198` CI gates |
| SUR-007 | Бухгалтерский инвариант debit = credit на уровне транзакции; VAT precision | Property + integration test на PostgreSQL; `#208` currency_id/exchange_rate |
| SUR-008 | CQRS/event store: `#65/#185` → `#71/#220` → `#237/#236` | EventStore integration spec зелёный; replay идемпотентен |
| SUR-009 | Build pin: GHC 9.6.5/Stack 3 через flake; `#66/#204` hashtables GCC16 | `nix develop` → `stack build --test` воспроизводимо; локальный GHC 9.10.3 больше не ломает сборку |
| SUR-010 | Вынести `src/.planning/`, `.claude/`, `.agents/` из `src/` в `docs/planning/` или portfolio | `src/` содержит только Haskell; размер репозитория уменьшен |
| SUR-011 | Трекер: закрыть 19 дублей, 12 робо-отчётов → дашборд, 82 workflow → tiering | 129 → ~98 уникальных issue; 0 новых бот-issue |
| SUR-012 | Security Scan: `GITLEAKS_LICENSE` через GitHub Secrets/vault; 33 code-scanning алерта → триаж | `Security Scan` зелёный без отключения; 0 критических алертов без плана |

**Critical path:** SUR-009 (build pin) → SUR-001/002/003 (auth holes) → SUR-004/005 (RBAC/tenant) → SUR-006/007 (DB/invariants) → SUR-008 (events) → integration → release candidate.

**Критерий готовности S1:** `task surypus:demo` поднимает API+БД и проходит сценарий login → account → journal entry → balance → report; required CI зелёный 10 запусков подряд; 0 дублей issue; evidence в карточке проекта.

### 5.2 S2 UAW — P0/P1, execution framework

**[ПРОВЕРЕНО]** JSON-state в `core/state_manager.py`, `core/uaw_core.py`; есть `orchestrator/workflow_engine.py`, `core/audit.py`, 10 тестов. Нет транзакционного хранилища, idempotency, planner/engine split, policy engine как отдельного модуля.

| ID | Задача | Критерий готовности |
|---|---|---|
| UAW-001 | Заменить JSON-файл на транзакционное хранилище (PostgreSQL/SQLite с WAL), атомарная запись + lock + recovery | Crash-тест: прервать workflow на каждом шаге, перезапуск продолжает с последнего commit'а |
| UAW-002 | Workflow engine: DAG, dependencies, retry с backoff, timeout, cancellation, dead-letter | 4 сценария из черновика воспроизводимы как integration tests |
| UAW-003 | Idempotency keys для всех write-операций + resource mappings с conflict resolution | Повторная синхронизация 2 раза → тот же результат; тест конфликта mapping |
| UAW-004 | Planner отделён от executor; capability discovery и реальная проверка доступов коннекторов | Registry возвращает фактические capabilities; недоступный коннектор → понятный отказ |
| UAW-005 | Policy engine L0–L4, approvals для deletion/send/publish/financial, dry-run всего workflow | Опасная операция без approval не выполняется; dry-run не имеет side effects |
| UAW-006 | Verification результата (не только успешного вызова), audit immutable, secrets вне логов | Тест «external вызов успешен, результат неверен» → помечен failed |
| UAW-007 | Наблюдаемость: metrics/tracing/logs/alerts + UAW adapter для S5 FTN | Дашборд и алерт по failed workflow |

**Критерий готовности S2:** UAW выполняет сценарий «Issue → план → branch → tests → PR → preview → verification → notify» от начала до конца с approval на опасных шагах.

### 5.3 S3 NeoAllUnity — P1

- **NEO-001** Информационная архитектура: единый ID материала, схема метаданных (ID, автор, языки, даты, тип, категории, источники, лицензия, revision, canonical URL, статус редактуры), разделение первоисточников/авторских текстов/переводов/комментариев.
- **NEO-002** Канонизация: `integral-philosophy/modules/*` — единственный код; `Magazine/subprojects` и 8 archived-репозиториев — historical snapshot; обновить `neoallunity/README`, `.github`, `Magazine/README` (сейчас указывают `dominicusin/integral-philosophy`).
- **NEO-003** Publishing pipeline: source → capture → metadata → editorial review → translation → publication → indexing → archive; `AllUnitySitemap` становится задачей генерации sitemap в Wagtail, а не отдельным сервисом.
- **NEO-004** Живой Wagtail-инстанс: починить шаблон `%` и smoke-тесты, разделить CI и deploy, опубликовать (сейчас живой только статический PythonAnywhere mirror — другой код).
- **NEO-005** Восстановить `Monorepo CI` как required (последний успех 27.08), убрать сломанные pip-Dependabot; починить Biber-сборку `Magazine` или archive с причиной.
- **NEO-006** Semantic knowledge layer (RDF/OWL/SKOS/Wikibase, граф связей) — P2, только после NEO-001/002.
- **Критерий:** один канонический publishing pipeline, живой CMS, 0 устаревших ссылок на модули.

### 5.4 S4 Systems & infrastructure — P0/P1

- **INF-001** Hardware inventory: каталог хост → OS → storage → boot; включить wdmch (RTD1295), Quasar (i9-9820X/GTX 1050 Ti/188 GB), сервер 192.168.1.2.
- **INF-002** Unified system configuration: `guix-config` (канон для Quasar), `Quasar` (flake-слой), `my-nixos-config` (legacy), `nixos-config` (archive);Polyglot CM Fabric — один ресурс-owned-one-manager (P2).
- **INF-003** `Linux-Serv-Ansible`: ansible-lint 0 ошибок, тесты в venv `~/.cache/ansvenv/bin/python`, `--check` прогон на wdmch и documented idempotency proof.
- **INF-004** `alpine-wdmch-builder`: сохранить зелёный build/release/validate, control-суммы образов, verified procedure проверки флешки; release tag как evidence.
- **INF-005** Backup/restore-тесты и мониторинг (в т.ч. для FTN и БД), отде secrets от репозиториев.
- **INF-006** Новые каталоги BSD/Solaris/Plan9 — только как proposals в portfolio, не как существующие репозитории.
- **Критерий:** `task infra:verify` → lint 0, idempotent check 0, документированный restore-тест.

### 5.5 S5 FTN / messaging — P1

- **FTN-001** Gateway stability: единая схема адресации, inbound/outbound, разделение очередей mailer, locking и защита от повторной обработки, backup message bases + restore-тест. (Учитывать известную специфику wdmch: JAM `DW = unixtime − 10368000`, sqpack/hpucode cron — не менять без крайней нужды.)
- **FTN-002** Unified routing model, конфиг маршрутов из Git, FTN/NNTP/email, retry + dead-letter, мониторинг доставки.
- **FTN-003** Usenet: INN2, peering, иерархия групп, retention, disk quota, feed monitoring.
- **FTN-004** PolyResolver: только после стабилизации gateway — абстракция адреса, backend, cache/TTL/fallback/health checks, CLI/API.
- **FTN-005** UAW adapter для автоматизации и мониторинга (после UAW-007).
- **Критерий:** сообщение проходит FTN → gateway → NNTP/email с подтверждением доставки и восстановлением из backup.

### 5.6 S6 Site & knowledge — P1

- **WEB-001** Hugo как канон; `astro-experiment` — STATUS: EXPERIMENT или archive; один CV из 3; `.github` README про AlphaEvolve заменить на индекс экосистемы.
- **WEB-002** SBOM: `attestations: write` или отключить шаг; Security Scanning зелёный; 100 code-scanning алертов → триаж.
- **WEB-003** Сабмодули awesome-списков: зафиксировать коммиты и `git submodule status` в CI или заменить снимками контента.
- **WEB-004** Сайт как портал: Projects/Engineering/Research/Writing/Infrastructure/Open source/Knowledge graph/Changelog по черновику; SEO/JSON-LD, RSS, поиск, Lighthouse, a11y, preview builds.
- **Критерий:** деплой зелёный, 0 красных required-проверок, 1 каноническое CV.

### 5.7 S7 R&D / libraries — P1/P2

- **PKG-001** `package-maximizer`: 3 падения CI → 10 зелёных запусков; PyPI/ReadTheDocs как канон; benchmark воспроизводим; разделение discovery/resolution/optimization; интеграция с Guix/Nix — только после подтверждения назначения.
- **PKG-002** `ai-orchestration-platform`: починить requirements.txt → `pyproject.toml` (CI 7/7 красный); README-бейдж «13 тестов» устарел — в коде 62 файла `test_*.py` и 977 определений `def test_`, но фактический pass-счёт неизвестен, пока CI красный; убрать абсолютный путь `/home/domini/src/petr/test2/Surypus2` (`orchestration.py:1512`, `pipeline.py:878`); решить product vs archive.
- **PKG-003** `MessageGateway` (3 `.hs`) и `polyresolver` (91 `.hs`, spec-only): либо объединить в `haskell-lab` с общим cabal.project, либо archive с сохранённым SRS. `polyresolver` — 45 stub-маркеров, статус Phase 0 правдив.
- **Критерий:** у каждого репозитория ровно один статус и работающий (или честно отключённый) CI.

### 5.8 S8 Archive / forks — P3

21 archived + 11 forks + 10 «utility» репозиториев: пометить причину (`moved to …`, `snapshot`, `fork of …`), 0 шаблонных описаний, для `fidogate`/`zapret`/`onionshare` — upstream policy, `shadowbroker`/`rails_sample_app`/`deepsite-locally` — security/dis provenance review или archive.

---

## 6. Единый бэклог (ID из черновика → конкретные задачи)

| ID | Задача | Приоритет | Система | Зависимости | Evidence завершения |
|---|---|---|---|---|---|
| PORT-001 | Полный repository audit | P0 | Portfolio | — | `repository-audit.json` ✅ |
| PORT-002 | Portfolio dashboard + карточки проектов | P0 | Portfolio | PORT-001 | `portfolio/PORTFOLIO.md` + weekly report |
| PORT-003 |_labels/templates/CODEOWNERS | P0 | Portfolio | PORT-002 | 7 активных репозиториев по шаблону |
| SEC-001 | Security baseline (-tier1) | P0 | Все | PORT-003 | required checks на 7 ядрах |
| SEC-002 | Secrets audit + триаж 870/133 алертов | P0 | Все | SEC-001 | 0 critical без плана; GITLEAKS_LICENSE |
| SUR-001…012 | См. §5.1 | P0 | S1 | SEC-001 | demo-сценарий + evidence |
| UAW-001…007 | См. §5.2 | P0/P1 | S2 | PORT-002 | 4 сценария integration tests |
| INF-001…006 | См. §5.4 | P0/P1 | S4 | SEC-001 | `task infra:verify` = 0 |
| FTN-001…005 | См. §5.5 | P1 | S5 | INF-005, UAW-007 | доставка + restore |
| NEO-001…006 | См. §5.3 | P1/P2 | S3 | PORT-003 | живой CMS + 0 устаревших ссылок |
| WEB-001…004 | См. §5.6 | P1 | S6 | SEC-001 | зелёный Pages + SBOM |
| POLY-001 | Polyglot CM Fabric prototype | P2 | S4 | INF-002 | один ресурс = один manager, тест конфликта |
| PKG-001…003 | См. §5.7 | P1/P2 | S7 | SEC-001 | 10 зелёных запусков / archive |
| WDM-001 | Reproducible WDMCH build | P1 | S4 | INF-001 | release + checksums ✅ частично |

---

## 7. Дорожная карта (скорректированная последовательность)

| Фаза | Срок | Содержание | Exit criteria |
|---|---|---|---|
| **0 — Аудит и достоверность** | ✅ завершена | 78 репозиториев, CI, issue, алерты, исходники ядер | `repository-audit.json`, `source-inspection.json`, этот план |
| **1 — GitHub/портфель** | неделя 1 | `dominicusin/portfolio`, Labels, templates, CODEOWNERS, protection на 7 ядрах | required checks включены, карточки заполнены |
| **2 — Security/Reliability baseline** | недели 2–4 | tier1/tier2, SBOM, secret scan, триаж алертов, restore-тесты | 0 критических алертов без плана; SBOM зелёный |
| **3 — P0 продукты** | недели 3–10 | SUR-001…012 (сначала!), UAW-001…005, INF-001/003 | Surypus demo-сценарий; UAW state+idempotency; infra check |
| **4 — Общие компоненты** | недели 6–14 | CI templates, release tooling, metadata schema, event model, identity | ≥5 репозиториев используют reusable workflow |
| **5 — Интеграция систем** | недели 10–20 | UAW↔GitHub/Surypus/FTN, NeoAllUnity↔сайт/архив, CM fabric | сквозные сценарии с verification |
| **6 — Автономная разработка** | месяцы 4–6 | 19-шаговый жизненный цикл задачи под policy, а не под prompt-only | audit логов automation, approval на опасных шагах |

**Почему Surypus перед UAW:** у Surypus есть конкретные устойчивые дыры (tenant stub, role claim) и активный бэклог из 98 уникальных задач; UAW —framework без рабочего state, его интеграции до P0-стабилизации только распылят усилия.

---

## 8. Единая воспроизводимая инфраструктура

**Версии (одна точка — `portfolio/toolchain/.tool-versions` + flake):**
GHC 9.6.5 / Stack 3.x (surypus), Python 3.11+ (Wagtail 3.12), Node 24, Hugo Extended 0.164.0, ansible-core 2.14 + venv `~/.cache/ansvenv`, Docker/compose pinned.

**Тиры проверок:**
- `tier1` (required): build, unit tests, lint/format, secret scan, license check → блокирует merge.
- `tier2` (informational): coverage, benchmarks, SBOM, docs, link check.
- `scheduled`: deps, stale, analytics → **не создаёт issue в basic-трекере**, пишет в portfolio dashboard.

**Секреты:** `GITLEAKS_LICENSE`, JWT secret, deploy-токены — GitHub Secrets/OIDC или vault; никогда в issue/README/чате. Локальные тесты Ansible — только venv-интерпретатором.

**Запрет «ложного done»:** если roadmap/issue говорит «done», но нет зелёного tier1 + артефакта, статус принудительно `BLOCKED` и создаётся задача верификации. Отключённый тест приравнивается к проваленному.

---

## 9. Definition of Done (обновлённый)

Задача/проект завершена только при наличии всех пунктов:
1. Требования сформулированы и привязаны к issue.
2. Архитектура/решение зафиксированы в ADR.
3. Код существует и собран чистой сборкой с зафиксированными версиями.
4. Unit + integration tests проходят в CI на защищённой ветке.
5. Security checks проходят (секреты нет, license проверен, critical-алерты обработаны).
6. Негативные тесты (RBAC/tenant/approval/recovery) проходят.
7. Документация и roadmap обновлены под фактическое состояние.
8. Deployment проверен, backup/restore проверен, rollback описан.
9. Release tag/artifact создан, где требуется.
10. В карточке проекта заполнено поле `evidence` со ссылкой на CI/release.

---

## 10. Метрики, риски, решения

| KPI | Сейчас | Цель |
|---|---:|---:|
| Ядра с зелёным required CI | 2/7 | 7/7 |
| Защищено веток | 6/78 | 7/7 ядер + все активные |
| Репозиториев без лицензии | 16 | 0 активных |
| Дублирующих активных репозиториев | 8 модулей + 3 CV + 4 конфига + 2 demo | 0 |
| Открытые issue Surypus | 129 (19 дублей) | 98 уникальных, 0 дублей |
| Workflow в Surypus | 82 | ≤15 с владельцами и tier |
| Critical security-алерты без плана | неизвестно (870/133 всего) | 0 |
| Воспроизводимость сборки | частично | `nix develop` + `task bootstrap` для 7 ядер |

**Риски:** несовместимость GHC 9.10.3/lts-22.21 (решение — flake); сломанные ссылки при архивации (оставить redirect-README); публикация Wagtail может затронуть live allunity.ru (parallel run + rollback); права на `attestations`/секреты (если нет — явно блокировать, не отключать checks); распыление усилий (единый portfolio + policy-gated automation).

**ADR к принятию:** ADR-0001 канонические репозитории; ADR-0002 CI tiering; ADR-0003 Wagtail как канон NeoAllUnity; ADR-0004 Surypus issue/tracker policy; ADR-0005 upstream-политика форков; ADR-0006 запрет «ложного done»; ADR-0007 Polyglot CM (один ресурс — один manager).

---

## 11. Ближайшие действия (следующий проход)

1. Создать `dominicusin/portfolio` и перенести туда 4 артефакта аудита + этот план.
2. Включить required checks на 7 ядрах (сначала исправить красные, затем включать).
3. SUR-001/002 — убрать stubs и dead-code auth-ловушки в Surypus; добавить негативные тесты.
4. SUR-009 — GHC/Stack pin через flake; попробовать `stack build --test` вpins-окружении.
5. `GITLEAKS_LICENSE` в vault → починить Security Scan в Surypus и SBOM в блоге.
6. UAW-001 — выбрать транзакционное хранилище и написать crash-тест.
7. Закрыть 19 дублей issue и отключить 12 робо-отчётов.
8. Обновить README NeoAllUnity/.github/Magazine под канон монOREPO.
9. Починить `%` в шаблоне Wagtail и разделить CI/deploy.
10. Запустить `portfolio` weekly report как cron и сверять метрики §10 еженедельно.

---

## 12. Сверка с черновиками 24.11 и принятые дополнения

Подробная построчная сверка — в `RECONCILIATION.md`. Кратко:

- **57 и 58 репозиториев** — это неполные счёты только по публичным репозиториям (57 = 38+3+16). Полный аудит: **78 = 57 публичных + 21 приватный**. Часть ядер (`Linux-Serv-Ansible`, `guix-config`, `.github-private`) приватная.
- Опровергнуто: 11 issues в `AllUnitySitemap` — это **11 PR, 0 issue**; ветки `Surypus2` не существует (это путь генерации); `Magazine` уже LGPL-2.1, `allunity-wagtail` действительно без лицензии; «безымянный Haskell-форк» — `carma-public`.
- Подтверждено: `polyresolver` содержит `nousresearch`-URL и 10-байтовый pseudo-LICENSE `MPL-2.0`; `MessageGateway` без README/LICENSE; 100 файлов в корне `surypus`; ~265 МБ медиа-зеркал; хардкод `/home/domini/src/petr/test2/Surypus2`.
- Уточнено: в `ai-orchestration-platform` 977 тестовых функций (README говорит 13), но CI 7/7 красный — pass-счёт не доказан.
- Принято: `dominicusin/portfolio` = SoT технического состояния; `dominicusin/.github` = reusable workflows и шаблоны; Linear = SoT задач; Notion = управленческий граф; политика по лицензиям (ADR-0008); медиа-зеркала read-only до решения о правах; external_dependencies для DOM-6/DOM-7 и Notion TЗ.
- Не доказано и переведено в `BLOCKED/evidence_required`: уникальные коммиты в 11 форках, реальный pass-счёт 977 тестов, состояние Linear/Notion/Netlify/Vercel, правовой статус медиа.

---

Приложение: `repository-audit.json` (78 записей), `source-inspection.json` (9 репозиториев), `inventory.csv` (78 решений), `RECONCILIATION.md` (сверка черновиков), `PLAN.md` (предыдущая группировка). Все файлы — в `/home/dominicusin/ecosystem-plan/`.

## 13. Фактическое исполнение 25.11 (после цикла)

| Пункт плана | Статус | Доказательство |
|---|---|---|
| PORT-001/002 — аудит и control plane | DONE | `dominicusin/portfolio`, `artifacts/repository-audit.json` (78 репо) |
| PORT-003 — еженедельная метрика | DONE | `automation/weekly_report.py` обновлён; cron `3dcb53f3f8a5` (пн 09:00 EET, `no_agent`); локальный прогон создал `reports/2026-11-25.md` и запушил его |
| SEC-001 — required checks | ЧАСТИЧНО | Включены и проверены: `uaw:state-durability`, `allunity-wagtail:test`, `ai-orchestration-platform:test`, `surypus:{coverage,Scan for committed secrets,license-check}`. `Linux-Serv-Ansible` — 403 (нужен Pro/публичный репо), issue #10 |
| SEC-001 — Gitleaks | BLOCKED | Ключ был в чате → требуется ротация; vault заблокирован на passphrase; `automation/set-gitleaks-secret.py` готов, GitHub Secret не выставлялся. Issue #2 |
| SUR-001/002 — stubs + негативные тесты | DONE (PR #258 merged; PR #261 in review) | #258 удалил no-op stubs; #261: реальные HS256-фикстуры, 7 негативных кейсов tenant isolation; исправлен разбор registered `sub` (`claimSub` + prism `string`) в `Surypus/JWT.hs` и `JWT/Token.hs`. Локально `stack test`: **1202 examples, 0 failures, 3 pending** |
| SUR-009 — GHC/Stack pin | DONE (проверка) | `stack.yaml` = lts-22.21, `flake.nix` + `flake.lock` присутствуют; PR #259 починил toolchain в CI |
| UAW-001 — транзакционное хранилище | DONE | SQLite/WAL, `synchronous=FULL`, `RLock`, legacy-миграция; `tests/test_state_durability.py` 4/4; PR #3 merged, job `state-durability` pass; required check включён |
| NEO README/.github/Magazine | DONE | PRы `neoallunity/README#2`, `.github#1`, `Magazine#1` merged — канонический monorepo, исправлены fence-ы и лицензионная формулировка |
| Wagtail шаблоны | ДУБЛИКАТ ОШИБКИ АУДИТА | Заявленные 22 TemplateSyntaxError не воспроизводятся: `scripts/validate_templates.py` (Django 4.2 + Wagtail 5.2.8) → `TOTAL_ERRORS 0`. Проверка добавлена в CI, PR #2 merged, Required check `test` включён |
| Еженедельный отчёт | DONE | portfolio cron job + реальный push |

Оставшиеся блокеры не требуют нового кода: ротация/разблокировка vault, расширение прав токена для archived/fork и приватного Ansible-репо, полное восстановление legacy-тестов UAW (`TaskQueue`/`DependencyGraph` отсутствуют в дереве).
