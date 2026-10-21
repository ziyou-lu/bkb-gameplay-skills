---
name: gameplay-attack-readability
description: "在敌人招式、Boss 区域攻击或危险路径难读时改善姿态、前摇、落点与窗口；将可读性修改与伤害、碰撞、难度修改分开验收。"
---

# 攻击预警与反制可读性

本文件是从来源案例提炼的迁移流程，不是作者源码复刻，也未在目标游戏中执行。下面的验收项是实施后要做的检查，不是已经通过的测试。

## 触发条件

- 玩家看不出下一招的方向、区域或时机。
- 外观像左侧攻击但实际打中中央，或警示与 hitbox 不一致。

## 先确认的输入

各招式真实有效区域/生效时刻、可反制动作、镜头与背景、既有难度和辅助选项。

## 分步机制

1. 列出每招的预备姿态、预警开始、生效、恢复窗口，标明真正改变判定的节点。未知逻辑先查项目，不从视频猜。
2. 先修姿态与方向一致性：不同招式使用可区分姿势，中央列攻击给中央指向。新增帧数不自动等于更低输入延迟。
3. 让落点/路径线、区域外缘与真实伤害一致；检视画面背景对比、危险格和形状编码，不能只靠色相。
4. 调整前摇以允许理解和反应，但不默认套用一秒；每次只改一个变量，保留原版同场景对照。
5. 若需改 hitbox、弱点、反击窗口或失衡机会，明确作为机制变更而非偷偷附带的特效改动。较小 hitbox 是原帖方案之一，不是统一要求。
6. 测试边界安全区、连续招式、被击倒/被墙堵时的可逃空间；记下未解决招式，不以某一可读性改进宣称整体公平。

## 适用限制

- 现有材料没有玩家研究或命中率统计；作者自测与观察者判断必须分开。
- DWFNHDmjT-H 明确 UFO 机制未改，最后星星仍可能有问题；DM-5jXrNy1f 缺已核验 URL，仅保留 ID 证据。

## 验收

- [ ] 静音/减少特效时仍能读出方向和区域。
- [ ] 实测特效边缘与判定一致，提示到生效延迟可记录。
- [ ] 普通、连续、墙角情境均有预期反制；未改动机制的对照保持同样判定结果。

受围困后的保护窗口和阈值脱身不是预警表现，分别转到[受击后保护](../gameplay-post-hit-protection/SKILL.md)或[受击阈值脱身](../gameplay-hit-recovery/SKILL.md)；弹反成功/失败的状态闭环转到[弹反反馈](../gameplay-parry-feedback/SKILL.md)。

## 组合而不复制

只在需要相应机制时读取，沿用其事件与预算约束：

- [生命血条与损失残影](../gameplay-health-damage-ui/SKILL.md)
- [Boss 入场、转阶段与终结](../gameplay-boss-sequences/SKILL.md)

## 来源证据

完整观察、证据类型、未证项和参数 provenance 见 [来源登记](../../sources/posts.json)。来源只支持下列案例内容，不证明本文件新增工程建议已在原帖实现。

- [DeqcYnUOte-](https://www.instagram.com/p/DeqcYnUOte-/)：公平 Boss 战十层。
- [Dc9h6SqNtPK](https://www.instagram.com/p/Dc9h6SqNtPK/)：九宫格 Boss 攻击可读性。
- [DbJe6rANpf-](https://www.instagram.com/p/DbJe6rANpf-/)：攻击动作四项改进。
- [DalHoK1t--K](https://www.instagram.com/beat.dash_game/reel/DalHoK1t--K/)：攻击姿势与方向对应。
- [DWFNHDmjT-H](https://www.instagram.com/beat.dash_game/reel/DWFNHDmjT-H/)：关卡攻击对比与路径提示。
- DM-5jXrNy1f（已知 ID，链接未核验）：Boss 招式专属手臂姿势。
- [DeGQTpgNFfF](https://www.instagram.com/solarfall_studios/reel/DeGQTpgNFfF/)：Boss 火焰可读性。
- [DenLEa4xApp](https://www.instagram.com/p/DenLEa4xApp/)：弹反反馈。
