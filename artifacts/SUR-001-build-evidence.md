# SUR-001 — clean build and real tests (verified 2026-11-25)

Evidence: `surypus/surypus` main-branch CI run `45519684668` (`status=completed`, `conclusion=success`, head `73c6aa4`).

Jobs/steps: `Install system build dependencies` success; `Setup GHC and Stack via haskell-actions` success; `Use the system GHC` success; `Build library and tests` success; `Run tests` success.

Real test output from job log: **`1188 examples, 0 failures, 4 pending`** (includes QuickCheck `+++ OK, passed 100 tests.` property runs).

Toolchain: GHC 9.6.5 via haskell-actions + Stack, system linker; the previously broken bindist sanity check (`collect2: cannot find ld`) is bypassed.

Caveat: the four pending examples are declared pending in the suite; they are not failures but are not evidence of those behaviours. No clean local GHC 9.6.5 environment exists on the operator host (local GHC 9.10.3), so CI is the authoritative build evidence.
