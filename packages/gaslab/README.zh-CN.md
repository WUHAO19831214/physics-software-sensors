# GasLab 实验性领域包

[English](README.md) | **简体中文** | [日本語](README.ja.md)

`@physics-software-sensors/gaslab` 0.1.0 提供不依赖 UI、DOM、Three.js 的气体教学模型，运行时零依赖。导出 `.`, `./core`, `./physics`, `./simulation`, `./driver`，使用 NodeNext ESM，需要 Node >=22.13。尚未发布到 npm，也不在不可变的 v0.6.0 Release 中。

## 本地使用

```bash
npm ci --prefix packages/gaslab
npm --prefix packages/gaslab test
npm pack ./packages/gaslab --pack-destination /path/to/output
npm install /path/to/output/physics-software-sensors-gaslab-0.1.0.tgz
```

[完整 API 示例与语义](README.md) · [无界面示例](../../examples/headless-gaslab/README.md) · [来源记录](SOURCE.md) · [收录与审查](../../docs/gaslab-intake.zh-CN.md)。

## 模型与单位边界

麦克斯韦速度由三个独立高斯分量抽样；速率服从三自由度 chi 分布，归一化速率的平方才是卡方分布。变温比例为 `sqrt(T2/T1)`，输入须为正开尔文温度。

默认 `display` 模式使用显示尺度；微观冲量压强标为 `simulation`，不能当作 Pa。`pedagogicalPressureRatio = T/T0` 是理论教学倍率。使用 `unitSystem: 'si'` 时须输入米、千克、秒、开尔文，省略显示速度标定；引擎由粒子质量推导 RMS 速率，冲量/面积/时间的结果标为 Pa。真实装置精度尚未测量。外部压强以 kPa 驱动元数据保留，与模拟压强分开。

Box/Cylinder 以原点为中心。`capsule` 实际表示直筒长度 `cylinderHeight`、底部一个半球、平顶的容器，面积 `2*pi*r*h + 3*pi*r*r`，不是两端半球。模型仅包含静止壁面反射，不包含粒子间碰撞、移动活塞或玻意耳定律求解器。子步进和投影会丢弃碰撞越界距离，碰撞时刻和统计量属于数值近似；不宣称计量精度。

## 时间与失效语义

`step(dt)` 推进完整非负秒数，零步长不推进；无效温度、几何、质量、标定或步长显式抛错。超过一百万内部子步时拒绝，应缩短输入步长。快照独立复制，带种子的 `reset()` 可复现初态。

回放数据使用严格递增的有限秒数时间戳，起点取第一条记录，按记录边界分段施加温度。倍率同时影响回放与模拟时间；`setReplayPaused(true)` 暂停二者，末帧后保持最后输入。跳转只改变输入游标，不重建过去轨迹；需要完整轨迹时应 reset 后从起点回放。`live` 模式由调用者供给读数，不包含采集器。统计窗口在启动阶段包含尚无碰撞的时间，早期结果偏低。

这是一项独立仿真领域包收录，Sensor/Companion Tool 仍为 9/4，共 13 项。卸载新包或固定先前提交即可回退。
