# Evidence and Maturity

**English** | [简体中文](evidence-and-maturity.zh-CN.md) | [日本語](evidence-and-maturity.ja.md)

<!-- section:evidence -->
## Evidence levels

| Level | Meaning |
| --- | --- |
| E0 | Contract/schema only |
| E1 | Deterministic synthetic or recorded replay |
| E2 | Fixed-source compatibility/golden comparison |
| E3 | Real OCR/CV/runtime on controlled pixels |
| E4 | Named real device/lab setup and reproducible dataset |
| E5 | Pinned downstream project integration with rollback |

Recorded output is not a real runtime. Synthetic pixels are not a real device. Missing evidence is `not measured`, never zero.

<!-- section:maturity -->
## Maturity

- `contract-only`: no repository implementation is required.
- `experimental`: adapter and deterministic tests exist; important validation may remain pending.
- `validated`: applicable real-world, metrics and supported-path licensing gates passed.
- `stable`: validated public API plus downstream pinned reuse, rollback and compatibility commitments.

<!-- section:separation -->
## Evidence Level ≠ Maturity

Evidence records what ran. Maturity is a release decision across implementation, reproducibility, metrics, licensing, documentation and reuse. E3 does not automatically mean validated. All seven current Sensors remain experimental; none has E4 or E5.

Maintainer details: [evidence levels](evidence-levels.md) · [maturity gates](maturity-gates.md).
