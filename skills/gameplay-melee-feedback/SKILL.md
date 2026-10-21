---
name: gameplay-melee-feedback
description: "将共享反馈组合到剑击、受击、弹反、暴击和踩踏循环；不重复实现 hitstop、镜头、血条，不凭视觉改伤害规则。"
---

# 近战、弹反与踩踏组合

本文件是从来源案例提炼的迁移流程，不是作者源码复刻，也未在目标游戏中执行。下面的验收项是实施后要做的检查，不是已经通过的测试。

## 触发条件

- 已有近战判定，需要逐层改善手感。
- 弹反成功/失败、暴击/普通命中或连续踩踏的反馈缺少层次。

## 先确认的输入

攻击与受击事件、命中点/方向、弹反成功窗口、暴击/终结/连击事件及角色控制恢复规则。

## 分步机制

1. 先画出攻击前摇→接触→受击/反制→恢复链，绑定真实判定事件；剑轨迹支撑动作方向，不替代碰撞检测。
2. 需要剑刃拖尾时，参考已证五步：采样剑尖→连成弧→填成可贴纹理的网格→轨迹尾端渐隐→斩击纹理与遮罩组合。先确认采样坐标、重置条件和材质坐标方向；采样密度、网格拓扑、UV 和 shader 代码由项目决定，原帖没有证明。
3. 普通命中选用 hitstop、局部闪光、定向粒子与受击/击退姿势；调用下方共享技能逐项 A/B，避免重复触发同一事件。
4. 弹反区分预备、判定成功、攻击者 stagger 和反击奖励；仅对项目已有或明确要求的机制展示反馈，不因来源提及就自动加新击退或加伤。DenLEa4xApp 第 6 步已补齐为 STAGGER；字幕说击退并暴露，第 7 步反击 bonus damage，但距离/时长未核验。
5. 踩踏以目标压扁、接触停顿、烟星、主角拉伸反弹组成成功确认；连踩可递增分数/节奏。如果跳高或分值实际变化，把它列为玩法变更。
6. 为暴击/终结使用稀有的冲击帧、推近或 cut-in，保持普通击与大事件对比；分数/伤害字由统一 UI 通道生成。
7. 检视连续受击失控问题。Mercy Frames 和受击阈值吼叫是两种不同机制选项，不能仅因特效需求自动加无敌或脱身伤害。

## 适用限制

- 视频没有验证每个游戏的无敌帧、击退、反击加伤或连击经济；实现前核对现有规则。
- 剑拖尾五步标题现已补齐，但引擎代码与采样参数未见；不要让显示拖尾代替真实攻击判定。音高/挤压/金属音均未核听。

## 验收

- [ ] 挥空、格挡失败、成功弹反、普通/暴击/致死分别触发正确一次反馈。
- [ ] 连续踩踏、密集多目标和打断后状态恢复，连击/UI 不重复结算。
- [ ] 加入纯表现层前后伤害与位移保持预期；任何机制变动单列测试。

## 组合而不复制

只在需要相应机制时读取，沿用其事件与预算约束：

- [命中停顿与表现节奏](../gameplay-hitstop/SKILL.md)
- [接触闪光、冲击帧与粒子](../gameplay-impact-visuals/SKILL.md)
- [镜头冲击与短促聚焦](../gameplay-camera-feedback/SKILL.md)
- [压缩拉伸与次级运动](../gameplay-motion-deformation/SKILL.md)
- [生命血条与伤害数字](../gameplay-health-damage-ui/SKILL.md)
- [攻击预警与反制可读性](../gameplay-attack-readability/SKILL.md)

## 来源证据

完整观察、证据类型、未证项和参数 provenance 见 [来源登记](../../sources/posts.json)。来源只支持下列案例内容，不证明本文件新增工程建议已在原帖实现。

- [DemlZDhNoFi](https://www.instagram.com/p/DemlZDhNoFi/)：剑挥砍轨迹。
- [DecdQ9ltnjf](https://www.instagram.com/p/DecdQ9ltnjf/)：剑击五层。
- [DenLEa4xApp](https://www.instagram.com/p/DenLEa4xApp/)：弹反反馈。
- [DelJO3qusJE](https://www.instagram.com/p/DelJO3qusJE/)：受击七步。
- [DeqnlBQzbMY](https://www.instagram.com/reel/DeqnlBQzbMY/)：暴击反馈。
- [Deuo1C7TfMW](https://www.instagram.com/p/Deuo1C7TfMW/)：踩头五层与连续奖励。
- [DdAIJqcPzPn](https://www.instagram.com/p/DdAIJqcPzPn/)：受围困脱身机制。
- [DejijtPzhYJ](https://www.instagram.com/reel/DejijtPzhYJ/)：组合战斗反馈。
- [DcCF3ZmBNl2](https://www.instagram.com/p/DcCF3ZmBNl2/)：3D 击打灰盒增强。
