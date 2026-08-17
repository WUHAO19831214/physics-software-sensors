# Phase 4B planning scaffold: i18n and future Sensor intake

Status: **implemented in Draft PR #7; awaiting review**. No eighth Sensor, package/API change or source-project migration was performed.

## A. Internationalization / 国际化 / 国際化

Target languages:

- English (`en`)
- 简体中文 (`zh-CN`)
- 日本語 (`ja`)

Planned coverage:

- repository README and language-switch navigation;
- Sensor Catalog;
- all seven Sensor Pages;
- Installation, Download and Quick Start paths;
- a versioned terminology glossary shared by human pages;
- link, parity and untranslated-content checks.

Planning decisions still required:

- [x] Select English as canonical prose while machine JSON remains the technical fact source.
- [x] Use `README.md`, `README.zh-CN.md`, `README.ja.md` and preserve default English URLs.
- [x] Keep Sensor IDs, JSON fields, versions, units, coordinates, maturity and evidence unchanged.
- [x] Define terminology and review rules for physics, measurement and computer vision.
- [x] Add document-map metadata and an executable parity validator.
- [x] Apply the structure to root/public docs and all seven Sensor Pages.
- [x] Use explicit GitHub Markdown language links; English is fallback/default.

## B. Future Sensor intake workflow / 新 Sensor 长期接入

```text
project-local useful capability
    ↓
candidate sensor
    ↓
source/provenance
    ↓
adapter and dependency boundary
    ↓
tests/golden comparison
    ↓
benchmark and evidence
    ↓
Sensor Page and machine contract
    ↓
i18n review
    ↓
experimental
    ↓
validated / stable gates
```

Planning decisions still required:

- [x] Define candidate qualification, exclusions and ACCEPT/DEFER/REJECT.
- [x] Require repository, full SHA, file/symbol, use case, license and source comparison.
- [x] Require adapter isolation from UI/business/source-project coupling.
- [x] Add proposal/prompt/recipe and truthful trilingual scaffold templates.
- [x] Add document-map integration, i18n validation and optional handoff `sensor_intake` record.
- [x] Define privacy/model/dataset/license review gates.
- [x] Map intake lifecycle to existing evidence/maturity without changing contracts.
- [x] Require downstream old path and rollback until comparison succeeds.

## Explicit non-goals for this scaffold PR

- No eighth Sensor or candidate implementation.
- No contract redesign, package version bump or registry publication.
- No changes to the five historical source repositories.
- No movement of the immutable `v0.6.0` tag.

Implementation is complete for review. Phase 5 and downstream reuse validation remain out of scope.
