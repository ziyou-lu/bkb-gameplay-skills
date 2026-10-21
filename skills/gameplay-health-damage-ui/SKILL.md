---
name: gameplay-health-damage-ui
description: "优化扣血、治疗、伤害数字和暴击标记的可读性；统一平滑、残影条与数字去拥挤，不另建每个作者版本。"
---

# 生命血条与伤害数字

本文件是从来源案例提炼的迁移流程，不是作者源码复刻，也未在目标游戏中执行。下面的验收项是实施后要做的检查，不是已经通过的测试。

## 触发条件

- 生命值变化突兀或损失量不易理解。
- 密集伤害数字遮挡角色，或普通/暴击无法区分。

## 先确认的输入

真实 HP/最大 HP 与变更事件、伤害类别/来源、显示空间、字号范围、同时发生事件的顺序。

## 分步机制

1. 将真实值与显示动画分离。真实扣血立即生效，前景条可平滑追随；残影条保留刚损失部分再追赶。将“受击后等待多久”与“开始追赶后花多久”分为两个独立参数，明确连续伤害对等待/排空各自如何重置，避免把延迟和动画时长混成一个数值。
2. 单独处理治疗、最大血量变化、死亡与复活；不要让损失残影错演成又受一次伤或显示超上限。
3. 在可读字体基础上增加数字弹出、短程运动和淡出；弧线/重力是可选轨迹，不以复杂运动代替识读。
4. 按伤害大小设有上下限的字号映射，按类型增加形状/文字或图标，颜色只作辅助；暴击用差异化标记而非把所有数字放大。
5. 选择错开、分区或合并策略。合并时清楚表示总量/命中数或短窗累计，避免把多次命中误读成一次；这属于迁移建议而非原作者已验证结论。
6. 同场景对比无数字/有数字及稀疏/密集伤害，确认 UI 不挡危险区。最后再叠加血条轻微闪光等反馈。

7. 若项目使用 Godot，可参考 DcZxryBoCFw 的实见搭建顺序：准备边框/血量/暗底纹理，配置主 TextureProgressBar 的 over/progress，再以第二层 TextureProgressBar 显示延迟损失段，最后绑定真实生命变更。两个层的范围、值和布局须与项目实际规则一致。视频展示了 tween.kill / create_tween，但未证明完整取消/重启逻辑，实施时应检查现有 tween 归属并做重复扣血测试，不照抄成已验证代码。

## 适用限制

- 0.75 秒 drain、0.4 秒 ghost/delay、50%/25% 颜色阈值只来自特定例子。Godot 案例的 ghost_delay=0.25 秒与 ghost_time=0.45 秒分别是等待与排空时长，同样不是默认最佳值，不用新数字覆盖其他来源的参数。
- Godot 演示脚本与正文提供的 GitHub 项目均未运行；后者未读取/审计，不能把界面截图或部分 API 名称当作实现正确性证明。
- 不要编补 DemP6LfRbug 第 3/5/8 步或 DcDs7f9uaqo 缺失淡出参数；引擎声明不等于实现验收。

## 验收

- [ ] 连续扣血、同帧治疗与受伤、致死/复活、最大生命改变都正确收敛。
- [ ] 最小字号、低对比背景、色觉差异与密集多人事件下仍可识别数值/类型。
- [ ] 取消动画或场景切换不残留数字；呈现总伤害与真实事件一致。
- [ ] 分别调等待时间和排空时长时只有对应阶段改变；等待中与排空中的再次受伤、治疗/致死，以及 tween 被取消后的两层血量都能正确收敛。

## 组合而不复制

只在需要相应机制时读取，沿用其事件与预算约束：

- [接触闪光、冲击帧与粒子](../gameplay-impact-visuals/SKILL.md)

## 来源证据

完整观察、证据类型、未证项和参数 provenance 见 [来源登记](../../sources/posts.json)。来源只支持下列案例内容，不证明本文件新增工程建议已在原帖实现。

- [DdhLtbTlTRG](https://www.instagram.com/reel/DdhLtbTlTRG/)：血条延迟扣血与残影。
- [DemP6LfRbug](https://www.instagram.com/p/DemP6LfRbug/)：血条与伤害数字。
- [DamtFQYxYtn](https://www.instagram.com/mii_misan/reel/DamtFQYxYtn/)：血条原型。
- [DcDs7f9uaqo](https://www.instagram.com/p/DcDs7f9uaqo/)：伤害数字十步。
- [Dcynt8ZoEoE](https://www.instagram.com/p/Dcynt8ZoEoE/)：战斗伤害数字 A/B。
- [DelJO3qusJE](https://www.instagram.com/p/DelJO3qusJE/)：受击七步。
- [DejijtPzhYJ](https://www.instagram.com/reel/DejijtPzhYJ/)：组合战斗反馈。
- [DcZxryBoCFw](https://www.instagram.com/p/DcZxryBoCFw/)：Godot 双层延迟血条与等待/排空两个时间参数；仅观察展示，没有代码执行验证。
