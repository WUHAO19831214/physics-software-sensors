# GasLab 与 Core 支持能力收录

[English](gaslab-intake.md) | **简体中文** | [日本語](gaslab-intake.ja.md)

<!-- section:decision -->
## 判定

ACCEPT：作为实验性 Core 支持算法与无界面气体教学模型领域包，归入 MAINTENANCE。DEFER：晋级为具名 Sensor/Companion Tool。模拟值不是直接观测，领域包也不会因为与 FringeLab 并列就自动通过测量处理能力准入。目录仍为 9 个 Sensor + 4 个 Tool，共 13 项。Core 源码调整为未发布 0.3.1，gaslab 为未发布 0.1.0；不发布 registry/Release。

<!-- section:provenance -->
## 来源

[固定来源路径及 MIT 许可审查](../packages/gaslab/SOURCE.md)。原始 Core 分支提交 `6262fd87a032f2c665a476653f226496688b85f9`；后续 gaslab 分支提交 `5fbade46aa6a819e56c5cb360c87ab0bf9ca7eb5`。审查分支保留二者，原分支不改写。

<!-- section:review -->
## 审查与修正

原测试 Core 41/41、gaslab 17/17 通过，但未覆盖关键边界。复现了 -20 ℃ 变成 +20 ℃、NaN 被标有效、step(1) 仅推进 0.1 秒、旧快照被新步进改写、112/1000 个 Capsule 初始样本越界。已修正符号、转换后单位及原单位、缺失值/非有限数/时钟失序、常量序列过原点拟合 R²、完整步长、快照与配置隔离、seed reset、有效几何初态和角点独立壁面反射。无单位回退须显式启用专用 ROI。回放复制并验证输入，从首条时间戳开始，分段施加温度，支持暂停；显示压强与 SI 压强明确分开。

<!-- section:validation -->
## 验证边界

[验证记录](../benchmarks/results/gaslab-intake.json) · [可运行的无界面回放](../examples/headless-gaslab/README.md)。旧传感器契约与不可变 v0.6.0 下载不改动。合成测试和本地构建不是硬件精度证据。Capsule 指直筒加一个底部半球及平顶；壁面投影丢弃越界距离。模型无粒子间碰撞和移动活塞。

<!-- section:consumer -->
## 消费端状态

[查理定律本地复用](../integrations/charles-law-gaslab/README.md)。消费端当前测试和构建通过，但适配仍是未提交改动。实际复用的是抽样/变温和 Core 帮助函数；渲染粒子系统与回放 UI 仍在应用内部，不能宣称完整引擎/驱动器已远端闭环，也不提升 E5。新 tarball 在临时副本验证，原消费端依赖和改动保留。

<!-- section:rollback -->
## 回退及后续要求

固定先前源码/包提交或卸载新包。晋级公开目录前需明确可复用的测量输入、来源/失效契约，并完成正式准入；纯模拟不能变成 Sensor。消费端远端验收前需审查并提交适配，固定包哈希。旧草稿 PR #11 仍是独立的网站导航任务。
