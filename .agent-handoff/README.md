# Agent Handoff

This directory is not software-sensor runtime code. It is the repository-owned handoff channel used to share the latest verified development state between Codex, ChatGPT, and other maintainers.

- `latest.md` is the human- and ChatGPT-readable report.
- `latest.json` is the machine-readable state used by repository validation.
- Both files must be updated when a Phase/PR reaches a handoff point.
- Every value must come from actual git, test, benchmark, package or GitHub results. Guesses and estimated test counts are prohibited; unavailable measurements must say `not measured` or use `null` where defined.
- Historical evidence belongs in versioned docs, benchmark reports, upgrade records and pull requests. `latest.*` is overwritten and represents only the newest phase.

## Commit SHA finalization

A tracked file cannot contain the SHA of the commit that contains that same file: changing the SHA text changes the Git tree and therefore changes the commit SHA. During development, `git.head_sha` must equal the current HEAD exactly. For a clean published handoff tip, validation permits one explicit, auditable exception: `git.head_relation` may be `parent-of-handoff-commit`, `head_sha` must then equal `HEAD^`, and the tip commit may change only `.agent-handoff/latest.md` and `.agent-handoff/latest.json`. This records the exact tested implementation snapshot; the current PR tip is still independently resolved from GitHub and reported to the user.

The exception must never be used for an implementation change, and it does not allow a guessed SHA.
