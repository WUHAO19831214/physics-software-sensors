# 来源资产盘点

扫描日期：2026-08-16。扫描固定在 Phase 1 记录的五个完整 commit，匹配 `*.png`、`*.jpg`、`*.jpeg`、`*.gif`、`*.webp`，并检查 README、docs、public/assets 与 Markdown/HTML/CSS 图片引用。

## 结果

| Asset | Source Repo | Commit | Source Path | Relevant Sensor | Can Copy? | Target |
| --- | --- | --- | --- | --- | --- | --- |
| 校徽图片（1193×1193 PNG） | `ampere-force-visualizer-teacher-yanan` | `cb073e89d6d87129287030f1df08bd540504eb39` | `src/assets/school-logo.png` | 无；属于学校品牌/UI，不展示传感器效果 | 否：用途不相关，且来源仓库未声明许可证 | 不复制 |

## 未发现可用演示资产的仓库

| Source Repo | Commit | 扫描结果 |
| --- | --- | --- |
| `audio-visual-soundfield-tracker-stable` | `85740d686c67452a057540edb564d713e01ccc51` | 没有提交上述格式图片，也没有 README/docs 图片引用 |
| `spot-vibration-tracking-system-20260508-171952` | `7f0d91cc73afafaecc54acc46b2b9d69375d994a` | 没有提交上述格式图片，也没有 README/docs 图片引用 |
| `forced-vibration-af-analyzer-20260502-122715` | `c3f58175a09ff29cacdfb976a5055758c4eff619` | 没有提交上述格式图片，也没有 README/docs 图片引用 |
| `physics-experiment-bridge-mvp` | `8bba87df6475cae1e595fc925551db8bea83fb68` | 没有提交上述格式图片，也没有 README/docs 图片引用 |

## 许可证判断

五个来源仓库在固定 commit 均没有 `LICENSE*`、`COPYING*` 或 `NOTICE*` 文件；GitHub license metadata 均为 `NOASSERTION`。因此本轮：

- 不复制唯一发现的校徽；
- 不从网页、第三方说明或搜索结果补图；
- 不生成看似真实的 UI/实验截图；
- 七个页面统一标记 `demo asset pending`；
- 后续应从来源项目真实运行状态生成由维护者确认可发布的截图，再补充 SHA-256、采集环境和用途。

## 后续真实截图清单

1. `tracker.color-marker`：原始摄像头帧、HSV mask、带中心/轮廓的输出帧；
2. `ocr.number`：经授权屏幕帧、OCR ROI、预处理图和 rawText/value 调试结果；
3. 其余传感器：在进入对应 Phase 3 适配前，先记录来源 commit 和运行环境，再生成截图。
