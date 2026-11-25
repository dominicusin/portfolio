# Surypus Docker/CI review — verdict

Three pasted drafts proposed a new Dockerfile, `docker.yml` and GHC pinning. Verdict against the live repository:

**Rejected as written (would break the build):**
- `COPY surypus.cabal` — the file is `Surypus.cabal`.
- `COPY cabal.project cabal.project.freeze*` — both are in `.dockerignore`, so the dependency layer would be empty.
- `cabal install exe:surypus` — no such executable; only `surypus-server` exists.
- A second GHCR-publish workflow — `docker-publish.yml` already publishes on `release: published` and `workflow_dispatch`, with provenance attestation. Adding another workflow conflicts with SUR-011 (82 → ≤15 workflows).

**Already present and better than the drafts:**
- Multi-stage Stack-based Dockerfile with non-root runtime, `dumb-init`, `HEALTHCHECK /api/v1/health`, cached dependency layer.
- `docker-lint.yml` (Hadolint), `.dockerignore`, `docker-compose.yml`, `flake.nix` devShell.

**Real defects, fixed in `surypus/surypus#264`:**
1. `PORT: 443` + `8080:443` mapping contradicted the healthcheck on `:8080` → now `PORT=8080`, `8080:8080`.
2. `worker` service ran `surypus-job-worker`, which is not in `Surypus.cabal` → service removed; Redis Streams work remains in the server.
3. `.gitattributes` marks `package-lock.json` as generated for repository language statistics.

**Deferred deliberately:**
- Base image `haskell:9.14.1` plus `stack setup --install-ghc` installs GHC 9.6.5 from lts-22.21; it works but carries an extra compiler layer. Pinning the builder base must be tested with a real Docker build (no Docker daemon in this environment), so it is not changed blindly.
- `docker-compose.yml` still builds locally; switching production to `image: ghcr.io/surypus/surypus:<tag>` is a deployment decision and needs a published release tag.
