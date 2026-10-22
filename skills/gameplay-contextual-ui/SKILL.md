---
name: gameplay-contextual-ui
description: "为游戏内按钮、按住操作、拾取提示和指令选择区分可用、焦点、执行中、成功/失败；卡牌布局、对话、机关、连接和切场使用独立入口。"
---

# 游戏内交互状态与提交反馈

## 触发条件

按钮、按住操作或指令焦点看似成功，却不符合真实交互结果。

## 输入与前置条件

可用、聚焦、按下、执行中、成功/失败事件；输入映射；目标/焦点归属；保持、释放及取消条件。

## 实施步骤

1. 建立状态到显示的映射，聚焦、按下和提交成功分别表示；显示订阅业务状态，不让动画结束调用一次额外提交。
2. 按钮按下可压缩、回弹和扩散波纹；成功提示仅由确认结果触发，失败/不可用采用可辨认的不同显示。
3. 按住操作绑定真实保持进度，松开或取消按规则清空/保留；满进度仍需确认结果，切换焦点不得把旧进度提交给新对象。
4. 拾取提示沿项目距离/朝向和输入映射显示；成功后同步持有状态及世界对象，等待确认时避免重复请求。
5. 战斗指令用焦点滑动、放大与说明框表达唯一选择和可执行性；卡牌布局、对话与机关执行交给独立入口。

## 参数调整

按下位移、回弹幅度与波纹寿命先小后大；保持时长属于输入规则，不能仅为动画好看改变。优先修焦点/状态错误，再调动效。

## 验收与失败处理

- [ ] 鼠标、键盘及适用手柄焦点唯一，按下/松开/取消不误提交。
- [ ] 重复点击、关闭重开与拾取竞态不双发结果；条件不足不播成功。
- [ ] 减少运动后仍读得懂结果，旧目标消失时焦点与待完成显示被撤销。

## 按需组合

- [奖励揭示](../gameplay-reward-reveal/SKILL.md)
- [事件形变](../gameplay-motion-deformation/SKILL.md)
- [卡牌交互](../gameplay-card-interaction/SKILL.md)
- [对话进度](../gameplay-dialogue-presentation/SKILL.md)
- [世界内指示](../gameplay-worldspace-indicators/SKILL.md)
- [目标可见性](../gameplay-world-readability/SKILL.md)
- [机关运动](../gameplay-mechanical-interactions/SKILL.md)
- [挂脱连接](../gameplay-connection-transitions/SKILL.md)
- [切场恢复](../gameplay-scene-transitions/SKILL.md)

需要核查出处、示例参数或证据限制时，读取[来源参考](references/sources.md)。
