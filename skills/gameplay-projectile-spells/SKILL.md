---
name: gameplay-projectile-spells
description: "按蓄力、发射、飞行、命中和余效组织枪械、光束、冰刺与终极法术；先修空间一致性，再组合共享反馈。"
---

# 射击与法术生命周期

本文件是从来源案例提炼的迁移流程，不是作者源码复刻，也未在目标游戏中执行。下面的验收项是实施后要做的检查，不是已经通过的测试。

## 触发条件

- 弹丸看似从角色/炮塔中心出现，或法术各阶段脱节。
- 法术只是一团亮光，无法区分蓄力、路径、接触和消散。

## 先确认的输入

真实发射点、弹道与目标规则、蓄力/取消事件、命中判定、危险区、武器/角色姿态。

## 分步机制

1. 检查弹丸生成位置与可见枪口对齐，转身/不同朝向也成立；墙边出生点和碰撞需要实测，不能用特效掩盖穿墙。
2. 将法术拆成 charge、release/core、travel/trail、impact/reaction、aftermath，按既有事件连线，不因呈现顺序改变伤害时序。
3. 枪械发射可组合枪口光、视觉后坐、弹壳；只在真实命中时叠加命中反馈，不把每次开枪都当命中。
4. 冰刺参考从单排到尺寸/扇形变化、地裂、终端冰簇与霜雾；独立标注纯外观和实际 AOE/冰冻规则，视觉不能证明后两者。
5. 重法术可选聚光→短暂停顿/压暗→主体光束→冲击环→余效，用局部层级和受力反馈突出主要目标；屏幕裂纹只作表现。
6. 原帖声音的升调、静默、低音仅作为待制作/核听的声音设计提案；先保留静音可读的触发和阶段识别。

## 适用限制

- Dehz2z9Nc7F 只保留第 2–6 步已见这一事实，不提供未知第 1/7 步或未保存标题。
- 视频未给出的伤害、射速、弹丸速度、冰冻持续时间不补写。

## 验收

- [ ] 枪口朝向/翻转与出生点一致，墙边不会产生不预期的穿透。
- [ ] 蓄力取消、飞行中销毁、未命中、命中多目标、场景切换均清理正确。
- [ ] 玩家能辨认可躲避阶段与真正危险区；高强度特效仍不遮挡下一招。

## 组合而不复制

只在需要相应机制时读取，沿用其事件与预算约束：

- [压缩拉伸与次级运动](../gameplay-motion-deformation/SKILL.md)
- [接触闪光、冲击帧与粒子](../gameplay-impact-visuals/SKILL.md)
- [命中停顿与表现节奏](../gameplay-hitstop/SKILL.md)
- [镜头冲击与短促聚焦](../gameplay-camera-feedback/SKILL.md)
- [攻击预警与反制可读性](../gameplay-attack-readability/SKILL.md)

## 来源证据

完整观察、证据类型、未证项和参数 provenance 见 [来源登记](../../sources/posts.json)。来源只支持下列案例内容，不证明本文件新增工程建议已在原帖实现。

- [Deff1_AtlFi](https://www.instagram.com/reel/Deff1_AtlFi/)：法术的八层反馈。
- [Dehz2z9Nc7F](https://www.instagram.com/reel/Dehz2z9Nc7F/)：射击反馈分层。
- [Dekh5vBzqhG](https://www.instagram.com/reel/Dekh5vBzqhG/)：枪械射击。
- [DUYNtcoiCGS](https://www.instagram.com/rabaldusgames/reel/DUYNtcoiCGS/)：弹丸枪口发射点。
- [DVGe1E9iDdi](https://www.instagram.com/p/DVGe1E9iDdi/)：炮塔后坐强度 A/B/C。
- [DX_mL0Wo3vx](https://www.instagram.com/rabaldusgames/reel/DX_mL0Wo3vx/)：炮侧烟尘对照。
- [DetoueoNkIr](https://www.instagram.com/p/DetoueoNkIr/)：冰刺八层。
- [Depb7BiTAuG](https://www.instagram.com/reel/Depb7BiTAuG/)：终极法术。
