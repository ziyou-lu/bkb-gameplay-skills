---
name: gameplay-motion-deformation
description: "在接触、弹跳、按钮反馈或快速出招缺少受力和轮廓时设计 squash/stretch、回弹、视觉后坐与 smear；只管理事件形变，持续跟随、瞄准组合、动作时序和物理接触使用独立入口。"
---

# 事件形变、回弹与视觉后坐

本文件是从来源案例提炼的迁移流程，不是作者源码复刻，也未在目标游戏中执行。下面的验收项是实施后要做的检查，不是已经通过的测试。

原入口中的持续装饰跟随、方向瞄准、动作时序和物理接触已独立；按下方链接选择对应工作流，不再要求所有动画需求经过压缩拉伸步骤。

## 触发条件

- 接触、弹跳或短促反馈像刚体平移，缺少受力方向或回弹。
- 表现形变误改碰撞体，或事件结束后残留缩放/偏移。
- 快速出招的关键轮廓不清，过渡 smear 掩盖了实际攻击方向。

## 先确认的输入

原始姿势/缩放、事件与受力方向、着地点或持握点、碰撞体是否继承缩放、动画混合方式，以及关键姿态和真实开火/命中时刻。只改表现时保留真实动作规则。

## 分步机制

1. 选定视觉子节点或独立表现层，先确认缩放不会无意改变碰撞盒、移动距离或伤害。若问题其实是物理接触过硬，转到接触响应诊断，不在此放宽碰撞容差。
2. 以接触/固定点为支点压缩；离开接触或加速时沿运动方向拉伸，随后回到基准姿态。上压下扁只是例子，不是所有材质规律。
3. 为预备、冲击、回弹保留可辨认的形状变化，再决定是否需要少量 overshoot；这里不负责删减真实前后摇或重定动作生效时刻。
4. 快速出招先保证关键姿态的方向与轮廓，再选择性用 smear 连接过渡并回收到可读姿态。DP53MiuDIpH 可见更展开的反身双臂、躯干/武器横向拉伸过渡与立姿收尾；固定美术与真实动作时序，分别比较姿态和 smear，不把大轮廓当成更快开火或更大命中范围。枪口细灰烟线不是动作轨迹。
5. 武器后坐以枪口/持握锚点合理偏移，比较不同强度，不默认最强档最好。
6. 复位时回到保存的基础姿态；处理取消、死亡、重复触发与动画混合，避免比例和偏移无限叠加。

## 适用限制

- Ddvr0NYNkNF 显示视觉 mesh 变化、collider 遥测 (1.00, 1.00) 和边框，作者声明同输入/固定碰撞。它增强了表现与碰撞分离的设计约束，但遥测不是实际引擎碰撞审计；视觉子节点是本页实施建议，未核源工程层级。细小形变倍率未读清，不给精确值。

- DcXJwumOuBK 只确认 Tween Scale 标签，具体缩放对象、形变方式和幅度未清楚捕获；不能把标签当作已核验的球体 squash/stretch 做法。
- DP53MiuDIpH 两版体型与美术也不同，不是单变量或有序教程；无速度、帧数和代码验证。DISTANCE 字样、评论中的更快/snappier 不是测得参数或作者已证结论。
- 踩头中“更高反弹”可能是玩法变化；仅做视觉优化时不能未经说明改跳高。
- 按钮、法力宝石和落地来源支持各自的形变表现，不证明所有场景的碰撞、资源或输入逻辑已验证；声音未核听。

## 验收

- [ ] 形变开关 A/B 下碰撞和操作目标保持一致，任何预期玩法变化单列；物理场景使用相同初始条件比较接触位置和反弹轨迹。
- [ ] 低顶与窄缝中分别开关形变，核对真实碰撞接触和可通过空间；只改变表现层时不让拉伸侵入天花板或移动物理根节点。
- [ ] 转身、连续落地、重复反馈和打断后无反向翻折、残留缩放或累计偏移。
- [ ] 强度与速度/高度的映射有上限，小事件不会像终结技。
- [ ] 相同美术/动作时序下分别开关姿态放大与 smear，过渡和收尾仍能辨认武器朝向；真实开火、受击范围和恢复时刻不被外形拉伸误导。

## 组合而不复制

- 车轮需要真正压弯/压缩且持续受支撑时，转到[可变形承载面](../gameplay-deformable-support/SKILL.md)，不是把本页视觉缩放套到物理根节点。

只在需要相应机制时读取，沿用其事件与预算约束：

- [装饰跟随与次级运动](../gameplay-secondary-motion/SKILL.md)
- [方向瞄准与分件姿态](../gameplay-aim-pose/SKILL.md)
- [输入响应与动作相位](../gameplay-action-timing/SKILL.md)
- [视觉损伤与接触响应诊断](../gameplay-contact-response/SKILL.md)
- [落地反馈](../gameplay-landing-feedback/SKILL.md)与[冲刺反馈](../gameplay-dash-feedback/SKILL.md)
- [射击反馈](../gameplay-shooting-feedback/SKILL.md)与[法术生命周期](../gameplay-projectile-spells/SKILL.md)

## 来源证据

完整观察、证据类型、未证项和参数 provenance 见 [来源登记](../../sources/posts.json)。来源只支持下列案例内容，不证明本文件新增工程建议已在原帖实现。

- [Deuo1C7TfMW](https://www.instagram.com/p/Deuo1C7TfMW/)：踩头五层与连续奖励。
- [DerbjhXTzfy](https://www.instagram.com/reel/DerbjhXTzfy/)：落地反馈。
- [DXZ35VuEx0e](https://www.instagram.com/mii_misan/reel/DXZ35VuEx0e/)：方块落地同物理对照。
- [DVGe1E9iDdi](https://www.instagram.com/p/DVGe1E9iDdi/)：炮塔后坐强度 A/B/C。
- [DejFnl2Ru9N](https://www.instagram.com/p/DejFnl2Ru9N/)：实体按钮反馈。
- [DeXJvO9kg94](https://www.instagram.com/reel/DeXJvO9kg94/)：法力宝石 UI。
- [DcCF3ZmBNl2](https://www.instagram.com/p/DcCF3ZmBNl2/)：3D 击打灰盒增强。
- [DcXJwumOuBK](https://www.instagram.com/p/DcXJwumOuBK/)：弹球碰撞的粒子、缩放、镜头与文字反馈展示。
- [DP53MiuDIpH](https://www.instagram.com/p/DP53MiuDIpH/)：后向开枪动作的姿态轮廓与 smear 前后对照。

- [Ddvr0NYNkNF](https://www.instagram.com/p/Ddvr0NYNkNF/)：视觉 mesh 形变/固定 collider 遥测的简化对照；同物理是作者声明，不是独立实测。
