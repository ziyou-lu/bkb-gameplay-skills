---
name: gameplay-motion-deformation
description: "在受击、落地、弹跳、后坐或角色运动中增加 squash/stretch、回弹与跟随运动；以既有运动和判定为基线，不套用于无游戏语境的泛动画。"
---

# 压缩拉伸与次级运动

本文件是从来源案例提炼的迁移流程，不是作者源码复刻，也未在目标游戏中执行。下面的验收项是实施后要做的检查，不是已经通过的测试。

## 触发条件

- 接触、弹跳或移动像刚体平移，缺少受力方向。
- 表现层形变误改碰撞体、或跟随物出现跳变。

## 先确认的输入

原始姿势/缩放、受力方向、着地点或持握点、碰撞体是否继承缩放、当前动画混合方式。

## 分步机制

1. 选定视觉子节点或独立表现层，先确认缩放不会无意改变碰撞盒、移动距离或伤害。
2. 以接触/固定点为支点压缩；离开接触或加速时沿运动方向拉伸，随后回到基准姿态。上压下扁只是例子，不是所有材质规律。
3. 为预备、冲击、回弹设可识别相位；先调单个回弹，再加入少量 overshoot，避免持续震荡盖过操作。
4. 武器后坐以枪口/持握锚点合理偏移，比较不同强度；装饰跟随以父节点驱动和受控滞后表现，不延迟真实角色朝向。
5. 头发/链状装饰可参考 DbS8p3VuhkL 的锚点、距离约束和弹簧/阻尼，节点数按项目需要。传送、转向翻面和帧率变化时重置或稳定积分。
6. 复位时回到保存的基础姿态；处理取消、死亡、重复触发与动画混合，避免比例或弹簧速度无限叠加。

## 适用限制

- DcXJwumOuBK 的弹球碰撞只确认 Tween Scale 标签，具体缩放对象、形变方式和幅度未清楚捕获；不能把标签当成已核验的球体 squash/stretch 做法，仍需先明确视觉节点和碰撞体关系。
- 五点链、递减圆形是该头发案例方案，不是通用骨骼架构。
- 踩头中“更高反弹”可能是玩法变化；仅做视觉优化时不能未经说明改跳高。

## 验收

- [ ] 形变开关 A/B 下碰撞和操作目标保持一致，任何预期玩法变化单列；弹球等物理场景使用相同初始条件比较接触位置和反弹轨迹，不能只比较外观。
- [ ] 转身、连续落地、传送、打断后无反向翻折和残留缩放。
- [ ] 强度与速度/高度的映射有上限，小事件不会像终结技。

## 组合而不复制

只在需要相应机制时读取，沿用其事件与预算约束：

- [移动、冲刺与落地反馈](../gameplay-movement-feedback/SKILL.md)
- [镜头冲击与短促聚焦](../gameplay-camera-feedback/SKILL.md)

## 来源证据

完整观察、证据类型、未证项和参数 provenance 见 [来源登记](../../sources/posts.json)。来源只支持下列案例内容，不证明本文件新增工程建议已在原帖实现。

- [Deuo1C7TfMW](https://www.instagram.com/p/Deuo1C7TfMW/)：踩头五层与连续奖励。
- [DerbjhXTzfy](https://www.instagram.com/reel/DerbjhXTzfy/)：落地反馈。
- [DXZ35VuEx0e](https://www.instagram.com/mii_misan/reel/DXZ35VuEx0e/)：方块落地同物理对照。
- [DbS8p3VuhkL](https://www.instagram.com/p/DbS8p3VuhkL/)：角色头发跟随运动。
- [DVGe1E9iDdi](https://www.instagram.com/p/DVGe1E9iDdi/)：炮塔后坐强度 A/B/C。
- [DejFnl2Ru9N](https://www.instagram.com/p/DejFnl2Ru9N/)：实体按钮反馈。
- [DeXJvO9kg94](https://www.instagram.com/reel/DeXJvO9kg94/)：法力宝石 UI。
- [DerYowOhdHs](https://www.instagram.com/p/DerYowOhdHs/)：NeonBlade 动作调整。
- [DcCF3ZmBNl2](https://www.instagram.com/p/DcCF3ZmBNl2/)：3D 击打灰盒增强。
- [DcXJwumOuBK](https://www.instagram.com/p/DcXJwumOuBK/)：弹球碰撞展示含 Tween Scale 标签；对象、具体形变和参数未核清，仅作有限证据。
