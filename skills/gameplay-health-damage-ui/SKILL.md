---
name: gameplay-health-damage-ui
description: "在 HP 变化突兀、损失量难读或低血量提示不清时设计血条平滑、延迟损失段和生命分级；此旧入口保留兼容路由，瞬时浮字与结果总分计数各有独立 owner。"
---

# 生命血条与损失残影

本文件是从来源案例提炼的迁移流程，不是作者源码复刻，也未在目标游戏中执行。下面的验收项是实施后要做的检查，不是已经通过的测试。

这是旧 gameplay-health-damage-ui 的兼容入口，现只拥有 HP 与残影状态。要做[伤害/治疗/得分浮字](../gameplay-floating-numbers/SKILL.md)或[结果总分递增](../gameplay-result-counting/SKILL.md)，直接读取对应入口，不再接入血条流程。

## 触发条件

- 生命值变化突兀、刚损失的血量不易理解，或残影等待/排空混乱。
- 治疗、最大生命变化、致死复活后，血条或生命分级提示与真实 HP 不一致。

## 先确认的输入

真实 HP/最大 HP 与变更事件、当前显示值/残影值、损失段等待时间与排空时长、治疗和死亡复活规则、UI 生命周期及并发 tween 归属。暴击文字是数值事件提示，不等于低血量分级。

## 分步机制

1. 将真实值与显示动画分离。真实扣血立即生效，前景条可平滑追随；残影条保留刚损失部分再追赶。
2. 将“受击后等待多久”与“开始追赶后花多久”设为两个独立参数，明确连续伤害分别如何重置等待和排空，避免混成一个时长。
3. 单独处理治疗、最大血量变化、死亡与复活；不要让损失残影错演成又受一次伤或显示超上限。
4. 按项目需要用局部受击/治疗确认和生命值分级提示帮助读数，保留低特效及非单一色相的识别方式；来源阈值不作为默认标准。
5. 若使用 Godot 且需要双层延迟血条，可参考 DcZxryBoCFw 的实见搭建顺序：准备边框/血量/暗底纹理，配置主 TextureProgressBar 的 over/progress，再以第二层 TextureProgressBar 显示延迟损失段，最后绑定真实生命变更。两层范围、值和布局须符合项目规则。
6. 检查现有 tween 归属、取消和重复扣血时的重启；不要把视频里的 tween.kill / create_tween 片段当作已验证的完整实现。

## 适用限制

- 0.75 秒 drain、0.4 秒 ghost/delay、50%/25% 颜色阈值来自特定例子，不是通用默认。Godot 的 ghost_delay=0.25 秒与 ghost_time=0.45 秒分别是等待和排空时长，不用新值覆盖其他来源参数。
- Godot 演示脚本未运行、未完整审计；正文 GitHub 项目未读取或测试，不能把界面截图或部分 API 名称当作实现正确性证明。
- DamtFQYxYtn 的自研 C++ 引擎/Lua 编排是作者声称，不是源码验证；没有据其“数字”一词推断浮动数值工作流。
- 不要补写 DemP6LfRbug 缺失的第 3/5/8 步。来源未验证完整伤害、无敌帧或资源规则，音频未核听。

## 验收

- [ ] 连续扣血、同帧治疗与受伤、致死/复活、最大生命改变后，两层血量正确收敛，不超上限或重复表现损失。
- [ ] 分别调等待时间和排空时长时只有对应阶段改变；等待中与排空中再次受伤、治疗及 tween 取消后仍能正确收敛。
- [ ] 低对比背景、低特效和色觉差异条件下仍能读出真实生命状态；动画不负责实际扣血或治疗结算。
- [ ] 关闭/重开和场景切换后没有旧 tween 或残影状态，当前显示重新对应真实 HP。

## 组合而不复制

- [低血量伤害缩放](../gameplay-low-health-damage-reduction/SKILL.md)与[受击后保护](../gameplay-post-hit-protection/SKILL.md)是独立伤害规则，不从血条长度或闪烁推导。

只在需要相应机制时读取，沿用其事件与预算约束：

- [伤害、治疗与得分浮字](../gameplay-floating-numbers/SKILL.md)
- [结果总分递增计数](../gameplay-result-counting/SKILL.md)
- [接触闪光与粒子](../gameplay-impact-visuals/SKILL.md)

## 来源证据

完整观察、证据类型、未证项和参数 provenance 见 [来源登记](../../sources/posts.json)。来源只支持下列案例内容，不证明本文件新增工程建议已在原帖实现。

- [DdhLtbTlTRG](https://www.instagram.com/reel/DdhLtbTlTRG/)：血条延迟扣血与残影。
- [DemP6LfRbug](https://www.instagram.com/p/DemP6LfRbug/)：血条与伤害数字。
- [DamtFQYxYtn](https://www.instagram.com/mii_misan/reel/DamtFQYxYtn/)：血条原型。
- [DelJO3qusJE](https://www.instagram.com/p/DelJO3qusJE/)：受击七步。
- [DejijtPzhYJ](https://www.instagram.com/reel/DejijtPzhYJ/)：组合战斗反馈。
- [DcZxryBoCFw](https://www.instagram.com/p/DcZxryBoCFw/)：Godot 双层延迟血条。
