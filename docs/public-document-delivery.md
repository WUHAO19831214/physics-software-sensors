# Public Document Delivery

## Scope

This is a reading-delivery layer for the repository. It does not replace GitHub repository pages as the source of truth for code, provenance, Issues, Pull Requests or Releases.

## Repository multilingual content integrity

**PASS.** On 2026-08-17, all three root documents were verified to exist, decode as UTF-8 and retain the expected six cross-language Markdown source links:

| Source | Language |
| --- | --- |
| `README.md` | English |
| `README.zh-CN.md` | 简体中文 |
| `README.ja.md` | 日本語 |

The existing Markdown files are not regenerated to work around a GitHub Web delivery incident.

## Access-path diagnosis

The route probes below are delivery observations, not repository-content validation.

| Route | English | 简体中文 | 日本語 | Classification |
| --- | --- | --- | --- | --- |
| GitHub Web blob | 404 / unavailable | 404 / unavailable | 404 / unavailable | External GitHub Web file-view delivery issue |
| GitHub Raw | 429 | 429 | 429 | External GitHub Raw/CDN rate limiting |
| GitHub Contents API | 200 | 200 | 200 | Repository content available |
| GitHub Pages | 404 before setup | 404 before setup | 404 before setup | Not enabled yet |

Therefore a GitHub blob or Raw failure must not be described as broken Markdown, an encoding error or a missing repository file.

## Pages-ready static reader

The version-controlled reader is generated from the canonical root READMEs and `project-status.json`:

```text
docs/
├── index.html          English
├── zh-CN/index.html    简体中文
├── ja/index.html       日本語
├── site.css
└── assets/capability-showcase.png
```

`tools/build_multilingual_pages.py` uses the existing Markdown rather than maintaining a fourth set of facts. It writes a source SHA-256 and project-status SHA-256 into each HTML file; `tools/validate_public_docs.py` verifies that the generated pages are fresh.

The page navigation is relative and self-contained:

| Page | English | 简体中文 | 日本語 |
| --- | --- | --- | --- |
| `docs/index.html` | `./` | `zh-CN/` | `ja/` |
| `docs/zh-CN/index.html` | `../` | `./` | `../ja/` |
| `docs/ja/index.html` | `../` | `../zh-CN/` | `./` |

All pages expose 7 Software Sensors, 1 Companion Processing Tool and 8 public capabilities. They reuse the existing `capability-showcase.png`; no external image host or duplicate showcase is used.

## Local verification

```bash
python3 tools/validate_public_docs.py
.venv/bin/python tools/build_multilingual_pages.py --check
python3 -m http.server 8765 --directory docs
```

The three local routes are `/`, `/zh-CN/` and `/ja/`.

## GitHub Pages enablement

Current state: **PAGES_READY_FOR_ENABLEMENT**. The Pages API returned 404 because a Pages site is not yet configured. The repository viewer has `ADMIN` permission, but this maintenance branch is intentionally a Draft PR and the final Pages source must be `main /docs`, not a temporary branch.

After the PR is merged, enable the no-Actions deployment mode in the repository:

1. Open **Settings → Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**.
3. Select branch **`main`** and folder **`/docs`**.
4. Save and wait for the Pages URL `https://wuhao19831214.github.io/physics-software-sensors/`.
5. Verify `/`, `/zh-CN/` and `/ja/` return the expected language page.

Do not create a `gh-pages` branch and do not create an Actions workflow for this delivery path. When Pages is live, root README language navigation can be updated to prefer the Pages routes while retaining Markdown-source links for developers.
