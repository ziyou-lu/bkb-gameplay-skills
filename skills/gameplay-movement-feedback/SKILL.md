---
name: gameplay-movement-feedback
description: "优化游戏角色冲刺、落地、转向与装饰跟随，用同物理 A/B 区分视觉改善和操控改变；不处理脱离游戏行为的泛动画。"
---

# 移动、冲刺与落地反馈

本文件是从来源案例提炼的迁移流程，不是作者源码复刻，也未在目标游戏中执行。下面的验收项是实施后要做的检查，不是已经通过的测试。

## 触发条件

- 冲刺速度已有但看不出来，落地缺少重量感。
- 斜向移动姿势或头发/眼部跟随与操作不一致。

## 先确认的输入

角色实际速度/高度、着地事件、冲刺起止、方向状态、动画与碰撞层级。

## 分步机制

1. 先录制同一路线原版作为控制，保持移动速度、跳跃和碰撞不变。
2. 冲刺按可用证据选预备、纵向/方向性拉伸、残像与速度线；前摇若影响输入响应要明确，而非作为免费视觉增强。对样式选择，可在同场景同动作下做 Light trail / Heavy trail / Ghost dash 一类 A/B/C 对照，分别比较轨迹密度、角色轮廓与路径可读性；这不是从轻到重必然更好的累加升级。
3. 落地将压缩/回弹、脚边尘、向下镜头冲击绑定着地事件，避免每一帧接地都触发。用落下高度或接触速度驱动有上限的分级。
4. 在四向/八向动作选择中保证姿势与真实朝向一致，斜向动画的改善是方向表现，不声称降低控制延迟。
5. 头发/眼部次级运动引用形变技能，检验走、转、跳、冲刺和停止；真实角色应先响应，装饰随后跟随。
6. 按需要组合短停顿和白闪，但常规小跳应可轻量或完全不使用，避免每次落地抢镜头。

## 适用限制

- DerYowOhdHs 引擎标签不一致，不能由帖子决定项目引擎。
- 原帖未给冲刺风阻、角度阈值或高度映射；使用项目参数并标注新实现。
- DX6_8HIo_GT 的 Ghost dash 瞬间未完整捕捉，不编数量/透明度/时长。无敌帧或起步灰尘锚定建议只来自评论，不能计入作者已实现功能，也不能据此更改角色判定。

## 验收

- [ ] 同物理 A/B 不意外改变速度、距离、碰撞；若有玩法改动明确展示。
- [ ] 斜坡、台阶、连续跳、边缘落地、传送和高速转向无重复触发或残留。
- [ ] 不同帧率下装饰稳定，减少镜头运动/特效后仍可辨认角色状态。
- [ ] 拖尾样式对照保持动作、速度和场景一致；能指出各样式对角色轮廓、落点/路径及遮挡的影响，不以粒子或残影更多判定胜出。

## 组合而不复制

只在需要相应机制时读取，沿用其事件与预算约束：

- [压缩拉伸与次级运动](../gameplay-motion-deformation/SKILL.md)
- [镜头冲击与短促聚焦](../gameplay-camera-feedback/SKILL.md)
- [接触闪光、冲击帧与粒子](../gameplay-impact-visuals/SKILL.md)
- [命中停顿与表现节奏](../gameplay-hitstop/SKILL.md)

## 来源证据

完整观察、证据类型、未证项和参数 provenance 见 [来源登记](../../sources/posts.json)。来源只支持下列案例内容，不证明本文件新增工程建议已在原帖实现。

- [DehPnhjxUvB](https://www.instagram.com/reel/DehPnhjxUvB/)：冲刺反馈。
- [DerbjhXTzfy](https://www.instagram.com/reel/DerbjhXTzfy/)：落地反馈。
- [DXZ35VuEx0e](https://www.instagram.com/mii_misan/reel/DXZ35VuEx0e/)：方块落地同物理对照。
- [DbS8p3VuhkL](https://www.instagram.com/p/DbS8p3VuhkL/)：角色头发跟随运动。
- [Ddb6gDmzmAE](https://www.instagram.com/cheese_eyes_games/reel/Ddb6gDmzmAE/)：四向改八向动画。
- [DerYowOhdHs](https://www.instagram.com/p/DerYowOhdHs/)：NeonBlade 动作调整。
- [DX6_8HIo_GT](https://www.instagram.com/p/DX6_8HIo_GT/)：同场景冲刺三种拖尾样式对照，不是逐层累加升级。
