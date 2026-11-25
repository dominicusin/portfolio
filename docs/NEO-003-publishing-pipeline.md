# NEO-003 — Publishing pipeline (canonical design)

Stages and mandated evidence:

1. `source` — acquire from an identified origin; store the source URL/citation, never only a copy.
2. `capture` — preserve a byte-identical snapshot with checksum and revision.
3. `metadata` — apply NEO-001 schema (`artifacts/NEO-001-material-metadata-schema.md`).
4. `editorial_review` — `editorial_status=draft → in_review`; reviewer identity recorded.
5. `translation` — a new material record linked by `related_to`, never an overwrite of the source.
6. `publication` — set `canonical_url` and `rights_scope`; rights_pending material is not published.
7. `indexing` — regenerate sitemap as a Wagtail task (AllUnitySitemap is a task, not a service).
8. `archive` — immutable revision retained; later edits create a new revision.

Prohibition: `Magazine/subprojects` and the eight `[MONOREPO] Read-only` repositories are historical snapshots; no new content enters them.
