---
name: gameplay-melee-feedback
description: "为普通近战命中、受击与暴击组合共享反馈；剑轨迹、弹反、踩踏、攻击方向规则和受击脱身使用独立入口，不凭视觉改变判定。"
---

# 近战命中、受击与暴击编排

本文件是从来源案例提炼的迁移流程，不是作者源码复刻，也未在目标游戏中执行。下面的验收项是实施后要做的检查，不是已经通过的测试。

## 触发条件

- 已有近战判定，需要让普通命中、受击、暴击或致命击的层级清楚。
- 普通击与暴击/致命击缺少对比，或多个系统重复播放同一次命中反馈。

## 先确认的输入

攻击相位、实际命中/受击事件、命中点与方向、受击者朝向、普通/暴击/致命结果，以及已有击退与控制恢复规则。

## 分步机制

1. 画出前摇→实际接触→受击→恢复链，绑定真实判定事件；挥空不能冒充命中。若输入后迟迟没有可见响应，复用[动作相位节奏](../gameplay-action-timing/SKILL.md)，不以整体倍速或删除敌人预兆代替定位。
2. 为已确认命中选择短停顿、局部闪光、定向粒子与受击姿势，分别调用共享 owner。DecdQ9ltnjf 的剑击分层与 DelJO3qusJE 的受击表现支持组合思路，不提供通用击退距离或无敌逻辑。
3. 将普通击与暴击/致命事件区分：DeqnlBQzbMY 展示冲击帧、金色火花、CRIT 字和眼部 cut-in；稀有强反馈不必每次普通击都出现。分数/伤害字由统一数值通道生成，显示不再结算伤害。
4. 对单次命中、多目标和连续命中设定项目合适的反馈预算，避免同一事件被攻击者、受击者和相机重复处理。DcCF3ZmBNl2 的姿态摆动、击飞烟迹与爆点是来源案例，把夸张反馈留给重击是迁移建议，不是作者明言。

## 适用限制

- 受击位移、恢复时间和伤害属于既有玩法规则，不能因增加反馈而自行更改。DelJO3qusJE 的 Mercy Frames 标题证据由[受击后保护入口](../gameplay-post-hit-protection/SKILL.md)保留，不能从受击动画推断实际免疫规则。
- DejijtPzhYJ 的 hitstop 3–5 帧与 DeqnlBQzbMY 的冲击帧 3 帧属于原帖示例，不是默认值；音效未核听。3D 灰盒案例并非完整有序步骤记录。

## 验收

- [ ] 接触点、受击方向与已确认命中一致；只改反馈时伤害和可命中方向不变。
- [ ] 挥空、普通命中、暴击与致命结果各自触发正确一次反馈，连续命中不重复结算。
- [ ] 多目标、打断与重开后相机/闪光/形变恢复，普通击与稀有事件仍有对比。
- [ ] 关闭表现层后伤害和位移符合原规则；获准修改的玩法另列验收。

## 原入口分流

- 四向/全方向攻击与输入、显示、判定对齐：[攻击方向规则](../gameplay-attack-direction/SKILL.md)。
- 剑尖采样、网格拖尾或拖尾残留：[剑刃轨迹](../gameplay-blade-trails/SKILL.md)。
- 弹反窗口、成功确认与反击机会：[弹反反馈](../gameplay-parry-feedback/SKILL.md)。
- 踩头反弹与连续踩踏：[踩踏连击](../gameplay-stomp-combos/SKILL.md)。
- 连续受击无法恢复控制：[受击恢复策略](../gameplay-hit-recovery/SKILL.md)。

## 组合而不复制

- [命中停顿](../gameplay-hitstop/SKILL.md)、[闪光与粒子](../gameplay-impact-visuals/SKILL.md)、[镜头反馈](../gameplay-camera-feedback/SKILL.md)：各自拥有表现流程。
- [事件形变](../gameplay-motion-deformation/SKILL.md)、[动作时序](../gameplay-action-timing/SKILL.md)、[事件浮字](../gameplay-floating-numbers/SKILL.md)与[生命血条](../gameplay-health-damage-ui/SKILL.md)：不在本页实现第二套。
- [攻击预警](../gameplay-attack-readability/SKILL.md)：处理敌人招式方向、区域与反制可读性，不代替独立的玩家攻击方向规则入口。

## 来源证据

完整观察、证据类型、未证项和参数 provenance 见 [来源登记](../../sources/posts.json)。来源只支持所注明的案例内容，不证明本文件工程建议已在原帖实现。

- [DecdQ9ltnjf](https://www.instagram.com/p/DecdQ9ltnjf/)：剑击五层。
- [DelJO3qusJE](https://www.instagram.com/p/DelJO3qusJE/)：受击七步。
- [DeqnlBQzbMY](https://www.instagram.com/reel/DeqnlBQzbMY/)：暴击反馈。
- [DejijtPzhYJ](https://www.instagram.com/reel/DejijtPzhYJ/)：组合战斗反馈。
- [DcCF3ZmBNl2](https://www.instagram.com/p/DcCF3ZmBNl2/)：3D 击打灰盒增强。
