---
name: gameplay-camera-feedback
description: "在单次击打、落地、后坐或爆炸缺少重量，或现有震动漂移、影响瞄准时调整临时 shake、impulse 与 punch-in；持续速度视野及完成镜头交接使用独立入口。"
---

# 镜头冲击与短促聚焦

本文件是从来源案例提炼的迁移流程，不是作者源码复刻，也未在目标游戏中执行。下面的验收项是实施后要做的检查，不是已经通过的测试。

本入口只拥有事件驱动的临时镜头偏移。持续高速表现转到[速度镜头](../gameplay-speed-camera/SKILL.md)；完成后交接给另一活动镜头转到[完成事件组合](../gameplay-completion-sequences/SKILL.md)，不强制把完成镜头复位成已结束的追随状态。

## 触发条件

- 事件有特效但重量感弱，需要一次短促镜头确认。
- 现有镜头抖动过强、累积漂移、推近过度或影响瞄准。

## 先确认的输入

基础跟随/瞄准驱动、事件位置与强度/方向、玩家控制方式、屏幕比例、重复触发频率，以及减少镜头运动选项。先区分临时反馈偏移和真实玩法后坐。

## 分步机制

1. 把反馈偏移与基础跟随/瞄准解耦，以可归零的临时偏移叠加，不直接累计到相机世界坐标。
2. 匹配事件方向：着地偏向下，后坐沿武器反向，击打沿攻击方向；推近可用于稀有重击而非替代所有震动。
3. 在同一段动作中做无/小/大三档单变量对照，选择能够读出事件的最小强度，避免把最强档自动定为成品。
4. 给幅度、频率、衰减和重复触发上限独立控制；多目标同帧事件按最高强度或预算合成，策略按项目决定。
5. 区分画面震动与改变实际瞄准/碰撞的玩法后坐；除非用户明确需要，不借视觉优化改命中判定。
6. 测试推近后的视野边缘、快速转向、场景切换与中断，支持关闭/减弱并恢复基础镜头。

## 适用限制

- Ddvr0NYNkNF 的 SHAKE = TRAUMA² 是作者演示标签，可作为项目评估非线性强度映射的候选，不是已核算法；trauma 范围、叠加与衰减、具体相机位移均未测。±8% 音高变化只有文字，未核听，不能据此声称相机/音频组合收益。

- DVGe1E9iDdi 是后坐强度对照，DYfFEpzIa-H 是爆炸加震动对照，均没有通用最佳数值。
- DcXJwumOuBK 的弹球案例在 Camera Shake 标签下可见棋盘背景位移；没有验证震动算法、方向、幅度或衰减，不将背景位移解释成实际球速或反弹规则改变。
- 爆炸帖的可复用 shake 脚本是作者声称，不代表已取得或验证脚本；声音仍属未来计划。来源中的音效文字和展示代码不等于核听或执行验证。

## 验收

- [ ] 临时镜头效果结束、打断和切场后回到原基准，不累积漂移。
- [ ] 连续命中、多目标同帧和重复推近不会让镜头无限放大，减少运动设置有效。
- [ ] 准星、危险边界、落点和下一步路径仍可读；弹球场景检查连续碰撞后的球位、下一接触面和运动方向。记录对照结论而非仅评价更炫。

## 组合而不复制

只在需要相应机制时读取，沿用其事件与预算约束：

- [接触停顿](../gameplay-hitstop/SKILL.md)
- [攻击预警与反制可读性](../gameplay-attack-readability/SKILL.md)
- [持续速度视野与边缘效果](../gameplay-speed-camera/SKILL.md)
- [完成事件与镜头尾声](../gameplay-completion-sequences/SKILL.md)

## 来源证据

完整观察、证据类型、未证项和参数 provenance 见 [来源登记](../../sources/posts.json)。来源只支持下列案例内容，不证明本文件新增工程建议已在原帖实现。

- [DYfFEpzIa-H](https://www.instagram.com/rabaldusgames/reel/DYfFEpzIa-H/)：爆炸镜头震动对照。
- [Ddy_-6wDMkn](https://www.instagram.com/reel/Ddy_-6wDMkn/)：像素拳击五层。
- [Deidw81hnmg](https://www.instagram.com/vasilev.yegor/reel/Deidw81hnmg/)：动漫重击五层。
- [DerbjhXTzfy](https://www.instagram.com/reel/DerbjhXTzfy/)：落地反馈。
- [Dekh5vBzqhG](https://www.instagram.com/reel/Dekh5vBzqhG/)：枪械射击。
- [DecdQ9ltnjf](https://www.instagram.com/p/DecdQ9ltnjf/)：剑击五层。
- [DVGe1E9iDdi](https://www.instagram.com/p/DVGe1E9iDdi/)：炮塔后坐强度 A/B/C。
- [Deo9lu7tzCT](https://www.instagram.com/p/Deo9lu7tzCT/)：宝箱七步反馈。
- [DcXJwumOuBK](https://www.instagram.com/p/DcXJwumOuBK/)：弹球碰撞的粒子、缩放、镜头与文字反馈展示。

- [Ddvr0NYNkNF](https://www.instagram.com/p/Ddvr0NYNkNF/)：trauma² 镜头标签，算法与位移未核；不把声效文字当已听结果。
