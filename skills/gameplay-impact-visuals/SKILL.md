---
name: gameplay-impact-visuals
description: "在击打、弹球碰撞、爆炸、着地或消耗反馈难辨时编排 flash、impact frame、冲击线、局部粒子和接触文字；不凭特效推断伤害范围或 shader 实现。"
---

# 接触闪光、冲击帧与粒子

本文件是从来源案例提炼的迁移流程，不是作者源码复刻，也未在目标游戏中执行。下面的验收项是实施后要做的检查，不是已经通过的测试。

## 触发条件

- 命中或非战斗碰撞成立，但画面没有清楚的接触标记。
- 普通命中与暴击使用同样表现，或粒子遮挡判定。

## 先确认的输入

事件位置、接触法线/攻击方向、目标可见性、轻重级别、背景对比度与减少闪烁设置。

## 分步机制

1. 先以局部目标闪光或轮廓变化建立接触锚点，比较开启/关闭，而不是直接堆满屏粒子。
2. 重击可另选短时剪影、反相、冲击帧或爆发线。它们是可替换或分级的表达，不是每击必须叠加的清单。
3. 把火花、木屑、烟尘等放在接触点，按方向与材质分布。冲穿攻击可先仅在确认命中点增加沿穿透方向的爆发/拖长碎片，保持基础行动与判定不变做对照，再决定是否需要其他反馈；不要仅因原帖问题字幕而新增减速。区分冲击瞬间的硬边形状、向外传播的环/线和慢衰减余尘。
4. 为 burst、trail、aftermath 设不同生命期与遮挡层级，尾迹不得掩盖下一次攻击或伪装成仍有效的伤害区。需要漫画化碰撞确认时，可另选短促接触文字并及时淡出；DcXJwumOuBK 的弹球碰撞可见白色碎粒和 POW 淡出。这类文字是事件标记，不是伤害值或得分，不应凭其出现改变结算。
5. 先检查单目标，再检查多目标与高速连击。复用粒子/材质实例或采用项目已有预算方式，明确每类最大可见数量。
6. 保留减少闪烁/低特效替代，用轮廓、形状或局部亮度也能说明命中；清理临时材质状态与粒子。

## 适用限制

- 弹球案例展示若干标签层，但完整顺序和是否累加未全部核验；不把它重排成确定的逐层配方，也不据此宣称物理轨迹未改变。
- 教程字幕里的 Sound 不等于实际音效已核听；本技能不把视觉观察变成音频实现证据。
- 三帧冲击等是源帖示例，未知帧率不换算为通用参数。强反相、全屏闪烁与血液效果需按目标用户和内容要求取舍。

- DXNr6m4hSDk 只确证方向性粒子反馈；未完整核验停顿、减速和镜头震动。评论里的闪白/屏震建议不能记为作者已实现，No Friction 字幕不能当作物理参数证据。

## 验收

- [ ] 能指出接触位置与受力方向，粒子不从无关中心冒出；冲穿攻击的同地图/同动作对照中，视觉新增点应对应真实命中，而非凭残影误判接触。
- [ ] 连击场景仍能读出目标、危险区、生命值和下一招；连续弹球碰撞中，粒子与文字不遮挡球的去向，不把同一次接触回调重复显示为多次事件。
- [ ] 减少闪烁后仍有清楚反馈；结束/中断后材质和屏幕恢复。

## 组合而不复制

只在需要相应机制时读取，沿用其事件与预算约束：

- [命中停顿与表现节奏](../gameplay-hitstop/SKILL.md)
- [攻击预警与反制可读性](../gameplay-attack-readability/SKILL.md)

## 来源证据

完整观察、证据类型、未证项和参数 provenance 见 [来源登记](../../sources/posts.json)。来源只支持下列案例内容，不证明本文件新增工程建议已在原帖实现。

- [Deidw81hnmg](https://www.instagram.com/vasilev.yegor/reel/Deidw81hnmg/)：动漫重击五层。
- [DelJO3qusJE](https://www.instagram.com/p/DelJO3qusJE/)：受击七步。
- [DecdQ9ltnjf](https://www.instagram.com/p/DecdQ9ltnjf/)：剑击五层。
- [DeqnlBQzbMY](https://www.instagram.com/reel/DeqnlBQzbMY/)：暴击反馈。
- [DetftcbzGnS](https://www.instagram.com/reel/DetftcbzGnS/)：木箱破坏。
- [DerbjhXTzfy](https://www.instagram.com/reel/DerbjhXTzfy/)：落地反馈。
- [DX_mL0Wo3vx](https://www.instagram.com/rabaldusgames/reel/DX_mL0Wo3vx/)：炮侧烟尘对照。
- [Deuo1C7TfMW](https://www.instagram.com/p/Deuo1C7TfMW/)：踩头五层与连续奖励。
- [Dd0GSn2xC62](https://www.instagram.com/p/Dd0GSn2xC62/)：Boss 屏障材质。
- [DcCF3ZmBNl2](https://www.instagram.com/p/DcCF3ZmBNl2/)：3D 击打灰盒增强。
- [DXNr6m4hSDk](https://www.instagram.com/p/DXNr6m4hSDk/)：Lunar Crypt 冲穿攻击的方向性命中粒子对照；停顿/减速/屏震未证。
- [DcXJwumOuBK](https://www.instagram.com/p/DcXJwumOuBK/)：非战斗弹球碰撞的白色碎粒和 POW 淡出；层间累加顺序未完整核验。
