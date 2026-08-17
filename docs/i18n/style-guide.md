# Documentation i18n style guide

## Shared rules

- English is the default maintained prose language; machine facts come from `sensor.json`, benchmark indexes, release manifests and `terminology.json`.
- Keep Sensor IDs, API names, JSON fields, code, versions, units, URLs and commit SHAs unchanged.
- Preserve the same `<!-- section:... -->` markers and semantic order in each translation set.
- Never upgrade maturity or evidence in translation. Never turn pixels, OCR text, confidence or a bounding box into a calibrated physical quantity.
- Do not translate YOLO, ByteTrack, ModelArtifact, HOG, CSRT, KCF, MIL, Tesseract.js or OpenCV.
- A translation must be reviewed as technical prose; machine translation alone is not publication evidence.

## English

Use concise developer documentation. Lead with what the Sensor observes, then separate downstream physical derivation. Prefer short sentences and explicit limitations.

## 简体中文

面向物理教师、教育技术人员和开发者。先解释“实际测到什么”，再介绍算法；避免只堆叠计算机视觉术语。统一使用 terminology JSON 中的词汇。

## 日本語

自然な技術日本語を用い、中国語の語順を逐語的に移さない。必要に応じて「日本語説明（EnglishTerm）」の形で技術名を示す。物理・光学・画像処理・ソフトウェア工学の用語を文脈に合わせる。

## Review checklist

- Meaning, limitations, maturity, evidence and release link match across languages.
- Direct observation and derived physical quantities remain separated.
- Code examples are executable and identical where the API is identical.
- Links are relative where possible and resolve from each file location.
