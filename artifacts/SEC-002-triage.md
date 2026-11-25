# SEC-002 — Alert triage (generated from repository-audit.json)

Counts are GitHub API values with a 100-per-repository cap for Dependabot. Status is evidence-based; no alert was dismissed without the required token scope.

## Priority 1 — active repositories (commits in last 90 days)

| Repository | Dependabot | Code scanning | Commits/90d |
|---|---:|---:|---:|
| `dominicusin/dominicusin.github.io` | 18 | 100 | 100 |
| `dominicusin/webring` | 100 | 0 | 1 |
| `neoallunity/neoallunity` | 100 | 0 | 2 |
| `dominicusin/website-optimization` | 80 | 0 | 1 |
| `dominicusin/neoallunity` | 66 | 0 | 2 |
| `dominicusin/AllUnitySitemap` | 56 | 0 | 2 |
| `surypus/surypus` | 11 | 33 | 100 |
| `surypus/Ergonomicguiforerpcrm` | 21 | 0 | 2 |
| `dominicusin/astro-experiment` | 18 | 0 | 7 |
| `dominicusin/spring-fleet-sapphire-monarch` | 10 | 0 | 1 |
| `dominicusin/Layerstructureforfigma` | 9 | 0 | 2 |
| `dominicusin/vite-react` | 6 | 0 | 2 |
| `dominicusin/dominicusin.dev-portfolio` | 2 | 0 | 2 |
| `dominicusin/package-maximizer` | 2 | 0 | 100 |

## Priority 2 — archived/fork and inactive

These require `admin:repo_hook` scope to dismiss; currently blocked (issue #7). Dismissal reason must be `not_used`, never `fix_available` or `inaccurate`.

| Repository | Dependabot | Code scanning | Active |
|---|---:|---:|---|
| `dominicusin/carma-public` | 100 | 0 | yes |
| `dominicusin/deepsite-locally` | 100 | 0 | yes |
| `dominicusin/DokanCloudFS` | 9 | 0 | yes |
| `dominicusin/onionshare` | 62 | 0 | yes |
| `dominicusin/rails_sample_app` | 100 | 0 | yes |
