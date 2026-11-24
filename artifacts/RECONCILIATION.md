# Сверка черновиков 24.11 с полным аудитом 25.11

Два присланных плана (`58 репозиториев` и `57 репозиториев`) и `MASTER-IMPLEMENTATION-PLAN.md` описывают одну экосистему с разной полнотой данных. Ниже — построчное подтверждение/опровержение и список принятых дополнений. Источник истины — `repository-audit.json`, `source-inspection.json`, `inventory.csv` и повторные `gh api`-запросы от 2026-11-25.

## 1. Почему 57 / 58 / 78

| Подсчёт | Как получен | Вердикт |
|---|---|---|
| 57 | 38 `dominicusin` + 3 `surypus` + 16 `neoallunity` — **только публичные** | Неполный: исключены 21 приватный репозиторий |
| 58 | 41 + 3 + 14 — публичные плюс часть приватных, с расхождением в счёте | Неточный |
| **78** | `user/repos?affiliation=owner` → 38 public + 13 private; `orgs/surypus` → 3+3; `orgs/neoallunity` → 16+5 | **[ПРОВЕРЕНО]** канон |

Итог: 57 публичных + 21 приватный = 78. Часть ключевых репозиториев приватная (`Linux-Serv-Ansible`, `guix-config`, `.github-private` в обеих организациях) — любые инвентаризации только по публичным страницам заведомо неполны.

## 2. Черновик «58 репозиториев» — проверка утверждений

| Утверждение | Вердикт | Доказательство / действие |
|---|---|---|
| 27 зелёных CI-workflow в `surypus` | `[ЧАСТИЧНО]` | 82 workflow-файла; на `main` 29 success / 1 failure за последние 30 запусков. «Зелёный» не является gating вне 6 защищённых репозиториев |
| ~110 файлов в корне `surypus` | `[ПРОВЕРЕНО]` | 100 файлов в корне (без каталогов), плюс 10+ агентных директорий |
| `polyresolver`: README ссылается на `nousresearch/polyresolver`, LICENSE 8 байт | `[ПРОВЕРЕНО]` | README содержит `nousresearch`; `LICENSE` = 10 байт, содержимое `MPL-2.0\n` — не текст лицензии. Добавить полный MPL-2.0 и исправить URL clone |
| `MessageGateway`: нет README и LICENSE | `[ПРОВЕРЕНО]` | Оба файла отсутствуют |
| `Linux-Serv-Ansible` и `guix-config` приватные | `[ПРОВЕРЕНО]` | `private: true`; accounted в 78 |
| Медиа-зеркала ~264 МБ | `[ПРОВЕРЕНО]` | 172 670 + 45 553 + 46 884 КБ ≈ 265 МБ |
| 11 открытых issues в `AllUnitySitemap` | `[ОПРОВЕРЖЕНО]` | 0 открытых issue, 11 открытых PR (почти все Dependabot/Snyk) |
| 9 форков «без уникальных коммитов» | `[НЕ ПРОВЕРЕНО]` | Требует пофоркового сравнения с upstream; в план включено как задача, не как факт |
| `zfs-win` не архивирован, мёртв | `[ПРОВЕРЕНО]` | В реестре active/fork, последнее обновление 2026-08-27 (метаданные), код наследие Google Code |
| Notion/Linear — SoT задач, DOM-6/DOM-7 | `[ПРОПОЗИЦИЯ]` | Внешние системы не проверяются GitHub API. Принято как организующая зависимость с разграничением: Linear = SoT задач, `portfolio` = SoT технического состояния, Notion = управленческий граф |
| Vercel не работает, Pages — prod, Netlify preview | `[НЕ ПРОВЕРЕНО]` | Pages workflow в репозитории есть; состояние Vercel/Netlify требует доступа к аккаунтам. Принято как операторский контекст (DOM-6) |
| Лицензионная матрица: код MPL-2.0, тексты CC-BY-4.0, конфиги Unlicense | `[ПРОПОЗИЦИЯ]` принята с оговоркой | Фактически: `surypus` MPL-2.0, `polyresolver` декларирует MPL-2.0 (текст отсутствует), `Magazine` LGPL-2.1, `Linux-Serv-Ansible` CC-BY-SA-4.0, `guix-config` Unlicense, `allunity-wagtail` без лицензии. Нужна ADR с grandfathering, а не слепая замена |

## 3. Черновик «57 репозиториев» — проверка утверждений

| Утверждение | Вердикт | Доказательство / действие |
|---|---|---|
| `ai-orchestration-platform` — 925+ тестов | `[ПРОВЕРЕНО с поправкой]` | 62 файла `test_*.py`, **977** определений `def test_` (976 в `tests/`). README-бейдж «13 тестов» устарел. Фактический pass-счёт неизвестен: CI падает 7/7 на отсутствующем `requirements.txt` |
| Есть ветка `Surypus2` | `[ОПРОВЕРЖЕНО]` | Ветки репозитория: `main`, `gh-pages`. `Surypus2` — путь генерации в `.gitignore`, `run.sh`, `docker-compose*.yml`, `orchestration/*` |
| Хардкод пути генерации | `[ПРОВЕРЕНО]` | `--output-path default="/home/domini/src/petr/test2/Surypus2"` в `orchestration.py:1512` и `pipeline.py:878` — переносимый default required |
| `Magazine` LGPL-2.1, `allunity-wagtail` без лицензии | `[ПРОВЕРЕНО]` | Метаданные GitHub и дерево файлов |
| `trackerslist` каноничен в `transgregorial` | `[ПРОВЕРЕНО]` | Описание репозитория: `DUPLICATED → moved to transgregorial org` |
| «Безымянный Haskell-форк (2★)» | `[ИДЕНТИФИЦИРОВАН]` | `dominicusin/carma-public`, Haskell, fork |
| «~3 неучтённых репозиториев neoallunity» | `[ЗАКРЫТО]` | В реестре все 21 (16 public + 5 private); пропусков нет |
| 9 архивных STUB-ов | `[ПРОВЕРЕНО]` | 21 archived всего, конкретный список — в `inventory.csv` |
| 129 issues в `surypus` «вероятно автогенерация» | `[ПРОВЕРЕНО]` | 129 = 19 точных дублей + 12 робо-отчётов + ~98 реальных задач. Не все автогенерация |
| Правовой статус медиа-зеркал неизвестен | `[ПРОПОЗИЦИЯ]` принята | Риск требует решения владельца; до решения mirrors keep-private/read-only, не публиковать новые копии |

## 4. Принятые дополнения к MASTER-IMPLEMENTATION-PLAN

1. **Разделение мета-репозиториев (снимает конфликт двух черновиков):**
   - `dominicusin/portfolio` — SoT по системам, статусам, метрикам, аудитам (управление).
   - `dominicusin/.github` — GitHub-native reusable workflows (`haskell-ci`, `python-ci`, `js-site-ci`, `docs-ci`, `mirror-gitlab`), шаблоны issue/PR, CODEOWNERS. Сейчас README этого репозитория заполнен чужим текстом про AlphaEvolve — заменить.
2. **Граница учёта:** Linear — SoT задач; `portfolio` — SoT технического состояния и evidence; Notion — управленческий граф. Зеркалирование только outbound, чтобы не было тройного ввода.
3. **Лицензионная ADR (ADR-0008):** код — MPL-2.0 (если уже MPL) / MIT (для новых Python/CLI), тексты и медиа — CC-BY-4.0, личные конфиги — Unlicense; существующие LGPL-2.1/CC-BY-SA-4.0 — grandfathering до отдельного решения. `polyresolver LICENSE` и `MessageGateway LICENSE/README` — P0.
4. **Портативность AI-конвейера:** убрать абсолютный путь `/home/domini/src/petr/test2/Surypus2`, сделать `--output-path` обязательным или относительным от корня; обновить README-метрику тестов (977 вместо 13); документировать контракт приёма сгенерированного Haskell обратно в `surypus` через PR.
5. **Медиа-зеркала:** до подтверждения правового статуса — read-only, без новых публикаций; вынос тяжёлых данных из git (LFS/релизы/отдельное хранилище), цель <20 МБ истории.
6. **Операторские зависимости (внешние):** DOM-6 (Vercel→Pages), DOM-7 (PR #451), Notion TЗ для `MessageGateway`, Linear DOM-ключи — отражать в карточках portfolio как `external_dependencies`, не выдавать за проверенный GitHub-факт.
7. **Topics/описания:** единая схема `system:<id>` + `kind:site|tool|config|paper|mirror` + `status:active|experiment|archived` для всех live-репозиториев; 10 шаблонных описаний «utility repository…» переписать.
8. **`js-site-ci` и `docs-ci`** добавляются к уже описанным tier1/tier2; превью — GitHub Pages/Netlify, решение по Vercel фиксируется ADR.

## 5. Что осталось непроверенным и не должно выдаваться за факт

- Наличие уникальных коммитов в 11 форках относительно upstream (нужен `git fetch upstream` + `git log --left-right`).
- Фактический pass-счёт 977 тестов `ai-orchestration-platform` (CI красный, локальный прогон не производился).
- Состояние DOM-6/DOM-7 в Linear, содержимое Notion, доступы Netlify/Vercel.
- Правовой статус контента медиа-зеркал.

Эти пункты перенесены в задачи portfolio с пометкой `evidence_required`; до получения доказательств статус — `BLOCKED`, а не `DONE`.
