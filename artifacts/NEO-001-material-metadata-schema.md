# NEO-001 — Canonical material metadata schema

One material = one stable ID, independent of repository or file path.

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | string (slug) | yes | stable, never reused |
| `title` | string | yes | original language title |
| `authors` | list of {name, orcid?} | yes | ORCID optional |
| `languages` | list of BCP-47 codes | yes | source language first |
| `dates` | {created?, published?, updated} | yes | ISO-8601 |
| `type` | enum | yes | `primary_source`, `author_text`, `translation`, `commentary`, `media` |
| `categories` | list of strings | no | controlled vocabulary (SKOS later) |
| `sources` | list of URLs/citations | no | provenance, not copies |
| `license` | SPDX id or `rights_pending` | yes | mirrors are `rights_pending` |
| `revision` | integer or git SHA | yes | immutable content version |
| `canonical_url` | URL | yes | one public address |
| `editorial_status` | enum | yes | `draft`, `in_review`, `published`, `archived` |
| `rights_scope` | enum | yes | `public_domain`, `licensed`, `rights_pending` |
| `related_to` | list of material IDs | no | links source ↔ translation ↔ commentary |

Separation rule: primary sources, author texts, translations and commentary are distinct records linked by `related_to` (not file copies). Media mirrors remain read-only until `rights_scope` is resolved.
