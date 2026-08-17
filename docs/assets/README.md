# Documentation Assets

`capability-showcase.png` is the root README aggregate for 7 Software Sensors and 1 Companion Processing Tool. It is generated entirely offline from the eight canonical detail assets listed in `tools/build_capability_showcase.py`:

```bash
python3 tools/build_capability_showcase.py
python3 tools/build_capability_showcase.py --check
```

Do not edit the PNG manually, move it to an external image host, or delete the per-capability source assets. Evidence boundaries are documented in the trilingual `docs/capability-showcase*.md` pages and `docs/demo-asset-inventory.md`.
