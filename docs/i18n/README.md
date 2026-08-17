# i18n maintenance

- [`terminology.json`](terminology.json) is the machine-readable trilingual glossary; [`terminology.md`](terminology.md) explains sensitive choices.
- [`document-map.json`](document-map.json) lists every Tier A translation set and the exact section order.
- [`style-guide.md`](style-guide.md) defines language quality and fact-preservation rules.
- `python3 tools/validate_i18n.py` checks files, language navigation, section order, Sensor IDs, versions, maturity, evidence, release links and terminology structure.

Tier B maintainer details remain single-source and are not mechanically translated.
