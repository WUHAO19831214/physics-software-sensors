# Maintenance Guide

This repository now uses continuous maintenance tracks instead of automatically inventing a Phase 6 or Phase 7. Every task starts by identifying its type and preserving provenance, scientific boundaries and rollback.

## New Sensor

Use the [Sensor Intake workflow](sensor-intake.md), [proposal template](../templates/SENSOR_PROPOSAL.md), [naming rules](sensor-naming.md) and [Codex recipe](agent-recipes/add-new-sensor.md). ACCEPT, DEFER or REJECT the candidate before extraction. Do not add project UI, orchestration or unrelated helpers as Sensors.

## New reusable Companion Tool

When a mature capability processes existing observations or measurements—such as mathematical composition, calibration, derived measurement or a renderer-neutral visualization adapter—it belongs in `processing/<tool-id>/`, not in the Sensor catalog. Record repository/commit/path/symbol provenance, the direct-observation boundary, clean extraction, deterministic golden/replay tests, EN/ZH-CN/JA Tool Pages, a small example, dependency/license review and `tool.json`. A Tool must not reuse `sensor.json`, emit a fictitious direct observation, or change the Sensor count. Reject project UI, lesson orchestration and miscellaneous helpers even if they are reusable code.

## Existing Sensor algorithm upgrade

Never silently overwrite released behavior. The default sequence is:

```text
current implementation
      ↓
candidate algorithm
      ↓
same-input old/new benchmark
      ↓
source golden and failure regression
      ↓
compatibility decision
      ↓
upgrade record + implementation version bump
```

Record the changed algorithm, reason, dependencies, source relationship, numeric tolerances, benchmark deltas and rollback. Keep the previous behavior available when compatibility or downstream risk requires it. Contract and implementation versions remain separate.

## Real-world validation

Add a reproducible dataset card, named device/runtime/OS/settings, protocol, raw result and limitations. Update the benchmark registry, [validation matrix](validation-matrix.md), Sensor Page and evidence level. Evidence does not automatically change maturity; missing measurements stay `not measured`.

## Downstream reuse

Create `integrations/<project>/` with a machine record, comparison summary and rollback instructions. Pin a public Release or exact commit, retain the old path, use a feature flag, compare identical inputs, run downstream regressions and verify rollback. Do not copy a downstream application into this repository.

## Release

Use the [Release checklist](../release/RELEASE_CHECKLIST.md), reproducible artifact build, checksums, clean-install consumers, dependency/license review and immutable tags. A documentation or evidence update does not require an immediate release. Never replace an existing Release attachment or move a published tag.

## Deprecation

Document the reason, replacement, compatibility impact, migration instructions and deprecation period. Add an upgrade/deprecation record and changelog entry. Keep aliases or adapters for the stated compatibility window; removal requires an explicit reviewed release decision.

## Maintenance task types

Future handoffs use one of `NEW_SENSOR`, `NEW_REUSABLE_TOOL`, `SENSOR_UPGRADE`, `VALIDATION`, `DOWNSTREAM_INTEGRATION`, `RELEASE` or `MAINTENANCE`. Read [Current Project Status](project-status.md) before starting.

## Homepage asset delivery incidents

Repository image validity and GitHub delivery availability are separate checks. If the GitHub Contents API returns `200`, the repository blob exists, and local decode passes while `raw.githubusercontent.com` returns `429`, classify the incident as an **external GitHub Raw/CDN delivery issue**, not a broken repository image. Preserve valid canonical assets, use text navigation as graceful degradation, and record the incident without moving assets to an external image host. See the [2026-08-17 homepage stabilization record](upgrades/2026-08-17-homepage-showcase-stabilization.md).

## Multilingual public-document delivery

When GitHub Web blob views are unavailable while Contents API and local UTF-8 checks pass, treat the issue as an **external GitHub Web file-view delivery issue**. Do not rewrite valid Markdown in an attempt to refresh GitHub. The Pages-ready reader under `docs/` is generated from canonical root READMEs; validate it with `tools/validate_public_docs.py`. See [Public Document Delivery](public-document-delivery.md) for the route matrix and no-Actions `main /docs` Pages enablement procedure.
