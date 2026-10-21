---
name: gameplay-movement-feedback
description: "当四向/八向移动动画或跑姿与真实运动朝向不一致时校对方向表现；冲刺、落地、跳跃许可和车辆物理使用独立入口，不宣称方向帧增加就降低输入延迟。"
---

# 移动方向动画与姿态一致性

本文件是从来源案例提炼的迁移流程，不是作者源码复刻，也未在目标游戏中执行。下面的验收项是实施后要做的检查，不是已经通过的测试。

## 触发条件

- 斜向移动只显示正交姿势，或跑姿/朝向修正与实际运动脱节。

## 先确认的输入

真实移动方向/速度、可用方向帧、动画选择状态和视觉层级；瞄准方向若独立于移动应单独处理。

## 分步机制

1. 先固定路线与速度，记录四向等原始方向表现，不将输入规则变化混入动画对照。
2. 按已有方向帧选择与实际运动一致的姿态；Ddb6gDmzmAE 展示四向到八向对照，未提供通用角度阈值。
3. 检查转向、停止与方向切换边界，避免快速抖动或错误翻面；阈值/过渡由项目实现测试，不从视频补状态机。
4. 装饰跟随复用次级运动，真实角色应先响应；冲刺/落地等不同事件从下方专用入口读取，不在这里复制工作流。

## 适用限制

- DerYowOhdHs 引擎标签不一致，不能由帖子决定引擎；敌人等待首击只是案例行为，不作为此处方向动画能力。
- 方向帧增加是表现改变，不能声称输入延迟降低或攻击从四向自动变全向。

## 验收

- [ ] 正交、斜向、快速反向和停止时姿态对应实际方向，速度与碰撞未意外改变。
- [ ] 方向边界不闪跳，转场/传送后不保留旧朝向；装饰不拖延真实角色响应。

## 兼容旧入口

原“移动、冲刺与落地反馈”仍通过此路径进入；现仅拥有方向动画，其他独立需求由下面的链接分流。新早按跳跃演示支持独立[输入缓冲设计与验收](../gameplay-jump-input-buffer/SKILL.md)；[顶角纠偏](../gameplay-ceiling-corner-correction/SKILL.md)另有空间碰撞入口。二者都不是已运行的引擎实现。

程序化腿部在启动/转向时需要选腿和先脚后髋调度，转到[程序步态调度](../gameplay-gait-step-scheduling/SKILL.md)；本入口仍只处理方向姿态，不复制脚步状态机。

## 组合而不复制

- [冲刺反馈](../gameplay-dash-feedback/SKILL.md)：路径/残像生命周期
- [落地反馈](../gameplay-landing-feedback/SKILL.md)：着地事件与强度分级
- [次级跟随](../gameplay-secondary-motion/SKILL.md)：眼部/头发持续跟随
- [离地跳跃宽限](../gameplay-jump-forgiveness/SKILL.md)：离台后起跳许可
- [移动交互状态](../gameplay-traversal-transitions/SKILL.md)：边缘停留/抓杆离开
- [车辆转向辅助](../gameplay-steering-assistance/SKILL.md)：输入映射
- [移动接触表示](../gameplay-locomotion-contacts/SKILL.md)：地形接触覆盖

## 来源证据

完整观察、证据类型、未证项和参数 provenance 见 [来源登记](../../sources/posts.json)。来源不证明本文件工程建议已在原帖实现。

- [Ddb6gDmzmAE](https://www.instagram.com/cheese_eyes_games/reel/Ddb6gDmzmAE/)：四向改八向动画。
- [DerYowOhdHs](https://www.instagram.com/p/DerYowOhdHs/)：NeonBlade 动作调整。
