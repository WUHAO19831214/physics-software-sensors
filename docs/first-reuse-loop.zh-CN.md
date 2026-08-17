# 首次完整复用闭环

[English](first-reuse-loop.md) | **简体中文** | [日本語](first-reuse-loop.ja.md)

<!-- section:loop -->
## 闭环路径

```text
光斑振动项目
      ↓
trackRedSpot 来源行为
      ↓
tracker.spot-centroid
      ↓
Physics Software Sensors v0.6.0
      ↓
公开 wheel
      ↓
已合并的光斑振动项目接入
      ↓
legacy/library 对比 + 回退
      ↓
E5 下游复用得到证明
```

<!-- section:meaning -->
## 它证明了什么

一个在物理项目中实际使用的能力，经过固定来源追溯、抽取和公开发布后，又被来源项目通过固定依赖和可回退适配器重新使用。合并后的下游路径默认仍是 `legacy`；`library` 和 `compare` 是明确选择的离线回放模式。

历史来源 commit `7f0d91cc73afafaecc54acc46b2b9d69375d994a` 说明算法来自哪里；下游 merge commit `172429fae463274ee354e54d56400096c2c6d375` 说明公开库在哪里被重新使用。这是两类不同证据，不能混淆。

<!-- section:boundary -->
## 科学边界

这是**软件复用闭环**，不是物理计量精度验证。七个 synthetic 同帧场景、下游计算回归和回退均通过；真实摄像头、受控光学位移、曝光鲁棒性、重复性和不确定度仍是 E4 缺口。因此即使已有 E5 复用证据，`tracker.spot-centroid` 仍保持 `experimental`。

详细证据：[光斑振动集成记录](../integrations/spot-vibration/README.md)。
