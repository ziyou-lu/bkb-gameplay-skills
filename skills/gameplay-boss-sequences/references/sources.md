# 来源与历史研究记录

本页仅供核对出处、参数来源和证据边界；不是执行入口。下列为改写前的研究记录，包含当时提出但未执行的迁移建议。当前实施步骤以 [SKILL.md](../SKILL.md) 为准；原始观察与验证状态以 [来源登记](../../../sources/posts.json) 为准。不得将历史建议、可见代码或作者说明当作已运行结果。

# Boss 入场、转阶段与终结

本文件是从来源案例提炼的迁移流程，不是作者源码复刻，也未在目标游戏中执行。下面的验收项是实施后要做的检查，不是已经通过的测试。

## 触发条件

- Boss 的入场、转阶段或击杀像普通事件，缺少阶段感。
- 演出隐藏危险、锁住控制或重复发奖励。

## 先确认的输入

Boss 状态机、入场触发、阶段阈值、玩家控制/镜头归属、死亡一次性标记、检查点与掉落规则。

## 分步机制

1. 明确演出阶段与可操作阶段，以及输入、碰撞、伤害和 UI 的归属；先保留现有游戏规则。
2. 入场可用铺垫、脚到脸揭示和音效提示形成尺度；封路是该帖设计，不默认给所有场景加锁门。
3. 转阶段让世界/角色变化与 HUD 状态对应，选用裂缝、火翼等项目合适的语汇；假胜利只是来源方案，不能作为强制套路。
4. 战斗阶段的预兆、危险区域和反制只调用[攻击可读性](../../gameplay-attack-readability/SKILL.md)，这里不重复招式流程。屏障材质 Dd0GSn2xC62 仅支持该场景的黑面板到煤灰/噪声、中心不透明/破碎边缘展示；高度裁切仍未修，不能据此提供通用 shader 或屏障系统能力。
5. 终结串联确认致命事件→节奏强调→崩解/熄灭→胜利与掉落，时间和视觉调用共享技能，奖励只由一次性业务事件处理。若终结确实进入关卡结果，引用[完成事件收尾](../../gameplay-completion-sequences/SKILL.md)；不是所有 Boss 死亡都必须进入整关结算。
6. 实现或保留跳过/打断/重开恢复路径时遵循项目需求，测试控制、镜头和音频状态回收；本条是工程迁移建议，不是原帖已展示功能。

## 适用限制

- DesK-ImRqfA 第 9 步仅 Final Hit 标题，不证明 1 HP 保护；不能添加这种机制并称源帖复现。
- 入场第 4/5/7 步缺失；声音未核听；屏障高度裁切是来源未解决点，不应称材质问题已全部修好。

## 验收

- [ ] 入场/转阶段/死亡不能重复触发，重开与中断后控制恢复。
- [ ] 特效边界与真实危险区一致，HUD 阶段和实际阶段一致。
- [ ] 致死、检查点、奖励各自实测；没有授权机制变化时不加锁门/保命/新奖励规则。

## 组合而不复制

只在需要相应机制时读取，沿用其事件与预算约束：

- [攻击预警与反制可读性](../../gameplay-attack-readability/SKILL.md)
- [命中停顿与表现节奏](../../gameplay-hitstop/SKILL.md)
- [接触闪光、冲击帧与粒子](../../gameplay-impact-visuals/SKILL.md)
- [镜头冲击与短促聚焦](../../gameplay-camera-feedback/SKILL.md)
- [生命血条与损失残影](../../gameplay-health-damage-ui/SKILL.md)

## 来源证据

完整观察、证据类型、未证项和参数 provenance 见 [来源登记](../../../sources/posts.json)。来源只支持下列案例内容，不证明本文件新增工程建议已在原帖实现。

- [DeozoT-xXrP](https://www.instagram.com/p/DeozoT-xXrP/)：Boss 入场。
- [DeohbEHTa7k](https://www.instagram.com/reel/DeohbEHTa7k/)：Boss 第二阶段。
- [DesK-ImRqfA](https://www.instagram.com/p/DesK-ImRqfA/)：Boss 击杀高潮。
- [DeqcYnUOte-](https://www.instagram.com/p/DeqcYnUOte-/)：公平 Boss 战十层。
- [Dd0GSn2xC62](https://www.instagram.com/p/Dd0GSn2xC62/)：Boss 屏障材质。
- [DeGQTpgNFfF](https://www.instagram.com/solarfall_studios/reel/DeGQTpgNFfF/)：Boss 火焰可读性。
