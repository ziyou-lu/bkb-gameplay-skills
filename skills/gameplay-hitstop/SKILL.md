---
name: gameplay-hitstop
description: "在命中缺少接触感、或发射/翻牌揭示缺少节奏时设计接触 hit-stop 与非接触表现停顿；不把冰冻状态或全局暂停混为一谈。"
---

# 命中停顿与表现节奏

本文件是从来源案例提炼的迁移流程，不是作者源码复刻，也未在目标游戏中执行。下面的验收项是实施后要做的检查，不是已经通过的测试。

## 触发条件

- 接触发生但玩家读不出撞击瞬间。
- 需要区分普通命中、重击、终结的时间权重，或为发射/奖励揭示设独立的演出停顿。

## 先确认的输入

确认这是接触事件还是蓄力释放/翻牌揭示等表现节点，及当前时钟、动画更新方式、触发频率、联网与输入要求。

## 分步机制

1. 先保留无停顿基线。接触支路绑定真实命中/落地，挥空不触发命中停顿；非接触支路绑定已确认的蓄力释放或翻牌揭示节点，不要求伪造接触事件。
2. 选择最窄的停顿范围：受击体、攻击体动画或表现层。全局 time scale 只在项目语义允许时使用，并明确 UI、输入、音频与相机哪些继续更新。
3. 接触支路在接触瞬间短停顿；非接触支路在指定表现节点局部停顿。两者分开配置/测试，不与冻结敌人的状态效果混用。先单独评估节奏，再组合闪白、镜头与粒子；该编排是迁移方法，不是原帖代码结构。
4. 用事件强度区分轻击/重击/终结；同时为密集命中设预算或合并策略，避免每次接触重新延长导致近似永久冻结。
5. 保存并恢复原有速度/时间状态，覆盖取消、死亡、场景切换和叠加慢动作；不要硬写恢复值为 1 覆盖原本合法慢动作。
6. 按真实时间与帧率分别测试。原帖按帧描述的值必须先确认其演示帧率，未知时不直接移植为固定毫秒。

## 适用限制

- Ddvr0NYNkNF 主 STEP 2/遥测标 55 ms，开头一次画面标 60 ms，两者冲突均保留，不平均或选成权威值。作者文字称接触后暂停物理再击退，但影响范围、精确时序和实际持续时间未核；不能把组合画面当作已测的 55 ms 冻结实现。

- 示例数值只在来源登记，不作为默认值。Ddy_-6wDMkn 中 5%/140 ms 是展示代码，未运行；DXZ35VuEx0e 的 0.07 秒是伪代码。
- 多人同步、物理与技能时钟的改动需要项目实现验证；视频只证明表现意图。

## 验收

- [ ] 单次命中停顿贴合接触且挥空不触发；非接触演出停顿只由指定揭示/释放事件触发，不误判成命中。
- [ ] 连续命中、同时命中多目标、取消后都能恢复，不吞合法输入或卡住 UI。
- [ ] 关闭停顿时游戏判定结果不被意外改变；对照轻/重击后能分辨权重且不拖累节奏。

## 组合而不复制

只在需要相应机制时读取，沿用其事件与预算约束：

- [接触闪光、冲击帧与粒子](../gameplay-impact-visuals/SKILL.md)
- [镜头冲击与短促聚焦](../gameplay-camera-feedback/SKILL.md)

## 来源证据

完整观察、证据类型、未证项和参数 provenance 见 [来源登记](../../sources/posts.json)。来源只支持下列案例内容，不证明本文件新增工程建议已在原帖实现。

- [DejijtPzhYJ](https://www.instagram.com/reel/DejijtPzhYJ/)：组合战斗反馈。
- [Deidw81hnmg](https://www.instagram.com/vasilev.yegor/reel/Deidw81hnmg/)：动漫重击五层。
- [DecdQ9ltnjf](https://www.instagram.com/p/DecdQ9ltnjf/)：剑击五层。
- [DenLEa4xApp](https://www.instagram.com/p/DenLEa4xApp/)：弹反反馈。
- [DelJO3qusJE](https://www.instagram.com/p/DelJO3qusJE/)：受击七步。
- [Ddy_-6wDMkn](https://www.instagram.com/reel/Ddy_-6wDMkn/)：像素拳击五层。
- [DXZ35VuEx0e](https://www.instagram.com/mii_misan/reel/DXZ35VuEx0e/)：方块落地同物理对照。
- [Depb7BiTAuG](https://www.instagram.com/reel/Depb7BiTAuG/)：终极法术。
- [Deuo1C7TfMW](https://www.instagram.com/p/Deuo1C7TfMW/)：踩头五层与连续奖励。
- [DemZuPozqeb](https://www.instagram.com/reel/DemZuPozqeb/)：传说卡牌揭示。
- [Deo9lu7tzCT](https://www.instagram.com/p/Deo9lu7tzCT/)：宝箱七步反馈。

- [Ddvr0NYNkNF](https://www.instagram.com/p/Ddvr0NYNkNF/)：接触暂停展示；55 ms/60 ms 标签不一致，均为未测示例。
