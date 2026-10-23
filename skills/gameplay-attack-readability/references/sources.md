# 来源与历史研究记录

本文件保留改写前的案例观察、归因、参数出处和未证项，供追溯时按需阅读；其中旧的迁移建议不作为当前执行入口。当前操作以 [SKILL.md](../SKILL.md) 为准，工程步骤不代表来源已经实现或通过测试。

# 攻击预警与反制可读性

本文件是从来源案例提炼的迁移流程，不是作者源码复刻，也未在目标游戏中执行。下面的验收项是实施后要做的检查，不是已经通过的测试。

## 触发条件

- 玩家看不出下一招的方向、区域或时机。
- 外观像左侧攻击但实际打中中央，或警示与 hitbox 不一致。

## 先确认的输入

各招式真实有效区域/生效时刻、可反制动作、镜头与背景、既有难度和辅助选项。

## 分步机制

1. 列出每招的预备姿态、预警开始、生效、恢复窗口，标明真正改变判定的节点。未知逻辑先查项目，不从视频猜。
2. 先修姿态与方向一致性：不同招式使用可区分姿势，中央列攻击给中央指向。新增帧数不自动等于更低输入延迟。
3. 让落点/路径线、区域外缘与真实伤害一致；检视画面背景对比、危险格和形状编码，不能只靠色相。
4. 调整前摇以允许理解和反应，但不默认套用一秒；每次只改一个变量，保留原版同场景对照。
5. 若需改 hitbox、弱点、反击窗口或失衡机会，明确作为机制变更而非偷偷附带的特效改动。较小 hitbox 是原帖方案之一，不是统一要求。
6. 测试边界安全区、连续招式、被击倒/被墙堵时的可逃空间；记下未解决招式，不以某一可读性改进宣称整体公平。

## 适用限制

- 现有材料没有玩家研究或命中率统计；作者自测与观察者判断必须分开。
- DWFNHDmjT-H 明确 UFO 机制未改，最后星星仍可能有问题；DM-5jXrNy1f 缺已核验 URL，仅保留 ID 证据。

## 验收

- [ ] 静音/减少特效时仍能读出方向和区域。
- [ ] 实测特效边缘与判定一致，提示到生效延迟可记录。
- [ ] 普通、连续、墙角情境均有预期反制；未改动机制的对照保持同样判定结果。

受围困后的保护窗口和阈值脱身不是预警表现，分别转到[受击后保护](../../gameplay-post-hit-protection/SKILL.md)或[受击阈值脱身](../../gameplay-hit-recovery/SKILL.md)；弹反成功/失败的状态闭环转到[弹反反馈](../../gameplay-parry-feedback/SKILL.md)。

## 组合而不复制

只在需要相应机制时读取，沿用其事件与预算约束：

- [生命血条与损失残影](../../gameplay-health-damage-ui/SKILL.md)
- [Boss 入场、转阶段与终结](../../gameplay-boss-sequences/SKILL.md)

## 来源证据

完整观察、证据类型、未证项和参数 provenance 见 [来源登记](../../../sources/posts.json)。来源只支持下列案例内容，不证明本文件新增工程建议已在原帖实现。

- [DeqcYnUOte-](https://www.instagram.com/p/DeqcYnUOte-/)：公平 Boss 战十层。
- [Dc9h6SqNtPK](https://www.instagram.com/p/Dc9h6SqNtPK/)：九宫格 Boss 攻击可读性。
- [DbJe6rANpf-](https://www.instagram.com/p/DbJe6rANpf-/)：攻击动作四项改进。
- [DalHoK1t--K](https://www.instagram.com/beat.dash_game/reel/DalHoK1t--K/)：攻击姿势与方向对应。
- [DWFNHDmjT-H](https://www.instagram.com/beat.dash_game/reel/DWFNHDmjT-H/)：关卡攻击对比与路径提示。
- DM-5jXrNy1f（已知 ID，链接未核验）：Boss 招式专属手臂姿势。
- [DeGQTpgNFfF](https://www.instagram.com/solarfall_studios/reel/DeGQTpgNFfF/)：Boss 火焰可读性。
- [DenLEa4xApp](https://www.instagram.com/p/DenLEa4xApp/)：弹反反馈。

## 新增：人群中选择性攻击者轮廓

- [DdATuwMSQe0 · solarfall_studios](https://www.instagram.com/p/DdATuwMSQe0/)，Ruins of Aloryith，2026-10-23 核看。作者说明在测试红色攻击轮廓以让围攻中的威胁可辨，并询问是否够快/过强，不能表述为已验证的玩家反应改善。
- 画面为第三人称角色被暗色敌人包围，部分敌人身体有明亮红色外缘，其他仍暗；后段多个对象选择性亮起。字幕只捕获 actually about to 等片段，准确起止时刻未转录。没有数值线宽、颜色/持续时间、渲染 API、代码或反应时实验。
- 正文将此补为现有攻击预警的状态选择性轮廓分支，不另立通用描边 owner。攻击实例门控、取消/池复用清理、多部件绑定、可访问冗余编码、遮挡约束和高拥挤验收为本库工程选择，不是已核作者实现。未核听音频或运行目标游戏。
- 相关 Ddl38IMNXy0 仅有相机/攻击旋转片段与泛称反馈改善，完整规则未知，不据此补转向算法或另计主来源。
