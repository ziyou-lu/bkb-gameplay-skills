---
name: gameplay-movement-feedback
description: "当四向/八向移动动画或跑姿与真实运动朝向不一致时校对方向表现；冲刺、落地、跳跃许可和车辆物理使用独立入口，不宣称方向帧增加就降低输入延迟。"
---

# 移动方向动画与姿态一致性

## 触发条件

角色斜向移动姿态不符，转向边界闪跳或装饰拖慢响应。

## 输入与前置条件

真实移动方向、速度、方向帧、翻面规则、停止朝向和输入/碰撞基线。

## 实施步骤

1. 固定同路线保留无新增动画基线，明确移动规则不随方向帧改变。
2. 按已有方向素材建立角度区间映射，正交和斜向选择对应姿态；缺少方向素材时先确定可接受的复用/翻面，不改真实移动向量补外形。
3. 明确低速/停止时保留最后方向还是使用独立 idle。方向边界有抖动时调整分区或稳定化，避免快速输入被过度平滑。
4. 先让真实角色响应，再按需添加头发/眼睛等次级跟随；冲刺、落地和步态选腿走独立入口。
5. 传送、切场、重启从当前运动状态重建方向，不携带旧帧或旧过渡。

## 参数调整

方向数量由素材和目标视角决定；调区间边界与切换稳定时间时同时测慢扫和快速反向。观察输入覆盖移动是控制契约问题，不用增加方向帧修复。

## 验收与失败处理

- [ ] 正交、斜向、反向和停止的显示对应真实运动。
- [ ] 边界不闪跳，控制响应无不期望延迟；速度/碰撞不变。
- [ ] 装饰关闭仍正确，重进/传送无旧方向残留。

## 按需组合

- [输入缓冲设计与验收](../gameplay-jump-input-buffer/SKILL.md)
- [顶角纠偏](../gameplay-ceiling-corner-correction/SKILL.md)
- [程序步态调度](../gameplay-gait-step-scheduling/SKILL.md)
- [移动与观察解耦](../gameplay-movement-look-decoupling/SKILL.md)
- [冲刺反馈](../gameplay-dash-feedback/SKILL.md)
- [落地反馈](../gameplay-landing-feedback/SKILL.md)
- [次级跟随](../gameplay-secondary-motion/SKILL.md)
- [离地跳跃宽限](../gameplay-jump-forgiveness/SKILL.md)
- [移动交互状态](../gameplay-traversal-transitions/SKILL.md)
- [车辆转向辅助](../gameplay-steering-assistance/SKILL.md)
- [移动接触表示](../gameplay-locomotion-contacts/SKILL.md)

需要核查出处、示例参数或证据限制时，读取[来源参考](references/sources.md)。

方向帧正确但翻面后的受光反向时，使用[精灵法线朝向](../gameplay-sprite-normal-orientation/SKILL.md)检查贴图与渲染变换；不要用更改角色面向掩盖光照问题。
