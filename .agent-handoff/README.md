# Agent Handoff

This directory is not software-sensor runtime code. It is the repository-owned handoff channel used to share the latest verified development state between Codex, ChatGPT, and other maintainers.

- `latest.md` is the human- and ChatGPT-readable report.
- `latest.json` is the machine-readable state used by repository validation.
- Both files must be updated when a Phase/PR reaches a handoff point.
- Every value must come from actual git, test, benchmark, package or GitHub results. Guesses and estimated test counts are prohibited; unavailable measurements must say `not measured` or use `null` where defined.
- Historical evidence belongs in versioned docs, benchmark reports, upgrade records and pull requests. `latest.*` is overwritten and represents only the newest phase.

## Commit SHA finalization (schema 1.1)

A tracked file cannot contain the SHA of the commit that contains that same file: changing the SHA text changes the Git tree and therefore changes the commit SHA. Schema 1.1 therefore separates three meanings instead of calling all of them `head_sha`:

- `git.tested_sha` is an actual full SHA for the implementation snapshot on which the reported tests and dry runs executed. It must be an ancestor of the handoff commit.
- `git.published_head_sha` is the resolver `{ "resolution": "branch-ref", "ref": "refs/heads/<branch>" }`. GitHub resolves it to the current published PR tip after push.
- `git.handoff_commit_sha` is the resolver `{ "resolution": "containing-commit" }`. Git resolves it to the commit containing `latest.json`.

Resolvers are intentional machine-readable instructions, not missing or guessed SHAs. The final user report must resolve and print both concrete SHAs after push. This survives squash merges because validation no longer assumes that a handoff-only parent relationship is retained.
