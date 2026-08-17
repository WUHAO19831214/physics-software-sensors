# Phase 4B planning scaffold: i18n and future Sensor intake

Status: **planning only**. This document defines the next review surface; it does not authorize bulk translation, a new Sensor, package/API changes or source-project migration.

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

- [ ] Select canonical source language and translation ownership rules.
- [ ] Choose file layout without changing existing stable URLs unnecessarily.
- [ ] Define what must remain byte-identical across languages: Sensor IDs, JSON field names, versions, units, coordinates, maturity and evidence levels.
- [ ] Define a terminology review workflow for physics, measurement and computer-vision terms.
- [ ] Define parity metadata and validation without treating machine translation as reviewed publication.
- [ ] Pilot one repository page and one Sensor Page before translating all pages.
- [ ] Specify fallback and language-switch behavior on GitHub.

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

- [ ] Define candidate nomination and rejection criteria.
- [ ] Require repository, full commit SHA, file, symbol, use case, license state and source-output comparison before intake.
- [ ] Define adapter isolation checks that prohibit UI/business-store/source-project coupling.
- [ ] Design reusable Sensor Page, SOURCE, benchmark, golden-data and upgrade-record templates.
- [ ] Design a machine-readable intake record and validation command.
- [ ] Define privacy, model-artifact, dataset and third-party license gates.
- [ ] Define experimental→validated→stable promotion and rollback evidence.
- [ ] Define how downstream projects retain old paths until comparison succeeds.

## Explicit non-goals for this scaffold PR

- No bulk English or Japanese translation.
- No eighth Sensor or candidate implementation.
- No contract redesign, package version bump or registry publication.
- No changes to the five historical source repositories.
- No movement of the immutable `v0.6.0` tag.

The next task must review and approve the above decisions before implementation begins.
