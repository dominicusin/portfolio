# ALL-001 — digital library provenance, rights and structure (2026-11-25)

Scope: `neoallunity/allunity-diskussii`, `allunity-knigi`, `allunity-zhurnaly`.

| Repo | Size (API) | Files | Content | README | LICENSE | Author meta |
|---|---:|---:|---|---|---|---|
| allunity-diskussii | 172 670 KB | 5 | `index.html` + 4 `.mp3` | no | no | "Интегральное сообщество" |
| allunity-knigi | 45 553 KB | 32 | 11 `.pdf`, 11 `.html`, 8 extensionless dirs | no | no | same |
| allunity-zhurnaly | 46 884 KB | 44 | 15 `.html` in numbered issue dirs | no | no | same; footer "© Интегральная философия, 2025 №15" |

Provenance evidence: each `index.html` is titled "Интегральное Сообщество — Библиотека Документов", has `<meta name="author" content="Интегральное сообщество">`, and references `allunity.ru` assets, logo, Matomo and navigation. These are static captures of the AllUnity.ru document library, not original authored works by the repository owner.

Rights: **not established**. No LICENSE in any mirror, no README statement, no per-item rights field. The presence of a copyright notice on journal material and third-party author metadata means rights cannot be inferred from repository ownership. Do not assign MIT/MPL/CC, do not publish derived editions, and do not move bulk content into new public repositories until the owner decides.

Structure: flat static HTML plus per-issue directories and PDF/MP3 blobs committed to git history (~265 MB combined). Recommended non-destructive migration: keep the three source repositories unchanged and read-only; add a README with provenance/status; generate a manifest (path, title, source URL, author, rights=UNKNOWN) from the HTML; store bulk media outside git history (LFS/release/external storage) only after rights decision. No deletion or license assignment in this cycle.
