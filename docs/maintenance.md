# Maintenance Guide

This repository now uses continuous maintenance tracks instead of automatically inventing a Phase 6 or Phase 7. Every task starts by identifying its type and preserving provenance, scientific boundaries and rollback.

## New Sensor

Use the [Sensor Intake workflow](sensor-intake.md), [proposal template](../templates/SENSOR_PROPOSAL.md), [naming rules](sensor-naming.md) and [Codex recipe](agent-recipes/add-new-sensor.md). ACCEPT, DEFER or REJECT the candidate before extraction. Do not add project UI, orchestration or unrelated helpers as Sensors.

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

Future handoffs use one of `NEW_SENSOR`, `SENSOR_UPGRADE`, `VALIDATION`, `DOWNSTREAM_INTEGRATION`, `RELEASE` or `MAINTENANCE`. Read [Current Project Status](project-status.md) before starting.
