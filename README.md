# BKB Gameplay Skills

把游戏玩法与效果优化案例整理成可复用中文技能。按独立工作流维护，不按帖子复制，也不把同一大类下的独立任务强行合并。

当前：**52 个任务入口（51 个内容工作流 + 1 个维护），101 个主来源（98 纳入、3 排除）**。原 14 入口已全面重整；后续容错、输入映射与物理承载等按独立任务增量维护，重复机制融合。结构沿革与理由见[迁移说明](docs/MIGRATION.md)。

## 使用

1. 根据实际问题从下方选入口。相邻任务的触发示例、owner 和能力边界见 [catalog.task_routes](catalog.json)。
2. 组合技能只负责事件编排，形变、数值、镜头等共享机制只在各自 owner 中详述。不同场景可复用同一流程，不等于所有“移动”或“UI”都是同一流程。
3. 所有步骤都是迁移建议，不是已经在目标游戏运行的实现。画面、作者文字、代码静态阅读与实际运行严格区分；本批未运行作者代码或完整核听音效。
4. 保留整个目录关系；旧 14 个路径都仍可打开，并有迁出入口链接。尚未安装到任一具体游戏项目。

## 按实际任务选择

### 接触、形变与空间可读性

- [命中停顿与表现节奏](skills/gameplay-hitstop/SKILL.md)：在命中缺少接触感、或发射/翻牌揭示缺少节奏时设计接触 hit-stop 与非接触表现停顿；不把冰冻状态或全局暂停混为一谈。
- [接触闪光、冲击帧与粒子](skills/gameplay-impact-visuals/SKILL.md)：改善接触闪光、冲击帧、粒子与碰撞文字的可读性；常驻特效遮挡时优先删减，贴地余效的地形生成使用独立工作流。
- [事件形变、回弹与视觉后坐](skills/gameplay-motion-deformation/SKILL.md)：在接触、弹跳、按钮反馈或快速出招缺少受力和轮廓时设计 squash/stretch、回弹、视觉后坐与 smear；只管理事件形变，持续跟随、瞄准组合、动作时序和物理接触使用独立入口。
- [装饰跟随与次级运动](skills/gameplay-secondary-motion/SKILL.md)：在头发、眼部或链状装饰跟随运动僵硬、翻面跳变或传送后残留速度时设计持续次级运动；区分父对象真实运动与装饰滞后，不延迟实际朝向。
- [方向瞄准与分件姿态](skills/gameplay-aim-pose/SKILL.md)：在持枪方向改变时角色像整张纸片旋转，或肩部、持握点、遮挡与真实瞄准不协调时组织分件 sprite、方向帧或 stack 表示；不新增自动瞄准或改变射击规则。
- [输入响应与动作相位](skills/gameplay-action-timing/SKILL.md)：在输入后动作看起来迟迟不响应，或整体加速让动作失去重量时定位冗余准备段、主体和收势；独立核对可见响应、真实生效与恢复时刻，不一律删除前摇。
- [视觉损伤与接触响应诊断](skills/gameplay-contact-response/SKILL.md)：在车体等已显示变形但碰撞仍过硬时分离视觉网格与真实接触问题，并仅在明确允许改变物理时做局部可回退实验；不是软体教程或通用穿透/容差建议。
- [表面余效的贴地与边界适配](skills/gameplay-surface-aftermath/SKILL.md)：处理倾倒或碰撞后水洼等表面余效的贴地、阶梯高低与边界适配；区分承载面/阻挡约束、作者描述的生成管线与视觉证据，不把网格贴合当成真实流体或玩法碰撞。
- [世界目标发现与角色遮挡可读性](skills/gameplay-world-readability/SKILL.md)：改善世界目标发现性与角色遮挡可读性；按既定允许信息比较目标尺寸/位置、临时识别模式、局部透视和轮廓，不扩大检测或交互范围，也不处理操作投影、卡牌或机关反馈。

- [可弯曲与压缩的交互承载面](skills/gameplay-deformable-support/SKILL.md)：当车轮等载荷需要在可弯曲、可压缩的承载面上保持接触时，设计连接刚体层与层间弹簧的局部原型及稳定性验收；不是固定碰撞体的视觉压扁、通用软体算法或物性标定教程。

### 镜头与结果展示

- [镜头冲击与短促聚焦](skills/gameplay-camera-feedback/SKILL.md)：在单次击打、落地、后坐或爆炸缺少重量，或现有震动漂移、影响瞄准时调整临时 shake、impulse 与 punch-in；持续速度视野及完成镜头交接使用独立入口。
- [持续速度视野与边缘效果](skills/gameplay-speed-camera/SKILL.md)：在钩爪、冲刺或跑酷已有高速运动，但速度线、动态 FOV 与径向模糊缺少协调或妨碍路径判断时设计持续速度表现；不把镜头变化当成角色实际加速。
- [完成事件、结算与动作尾声](skills/gameplay-completion-sequences/SKILL.md)：当完成界面、计数动画和终点镜头互相打断时，编排一次权威完成事件到可结束的收尾流程；引用数值与镜头机制，不复制它们或把演出当真实结算。
- [结果总分递增计数](skills/gameplay-result-counting/SKILL.md)：在完成/结算界面需要把已确认总分递增显示时设计只读计数动画；验证终值、支持的跳过和重开，不把动画刷新当成逐次得分或奖励发放。

### 战斗、射击与法术

- [攻击预警与反制可读性](skills/gameplay-attack-readability/SKILL.md)：在敌人招式、Boss 区域攻击或危险路径难读时改善姿态、前摇、落点与窗口；将可读性修改与伤害、碰撞、难度修改分开验收。
- [近战命中、受击与暴击编排](skills/gameplay-melee-feedback/SKILL.md)：为普通近战命中、受击与暴击组合共享反馈；剑轨迹、弹反、踩踏、攻击方向规则和受击脱身使用独立入口，不凭视觉改变判定。
- [攻击方向规则与输入判定一致性](skills/gameplay-attack-direction/SKILL.md)：当四向限制妨碍斜向攻击或出招方向与输入意图不一致时，评估攻击方向规则及显示/判定对齐；只在明确需要时改玩法，不推断自动瞄准或任意角算法。
- [剑刃轨迹采样与网格拖尾](skills/gameplay-blade-trails/SKILL.md)：当挥剑方向不清或拖尾断裂、串段和残留时，组织剑尖采样、弧形网格、尾端渐隐与纹理遮罩；轨迹只表达动作，不替代攻击判定。
- [弹反窗口、成功确认与反击反馈](skills/gameplay-parry-feedback/SKILL.md)：当弹反预备、成功和反击机会难以区分时，按真实判定窗口与结果组织反馈；不因特效示例自动新增宽容窗口、击退或反击加伤。
- [踩踏反弹与连续命中确认](skills/gameplay-stomp-combos/SKILL.md)：为踩头成功、主角反弹和连续踩踏组织反馈，区分接触确认、实际反弹与连击结算；不从拉伸或递增分数推断跳高和经济规则。
- [连续受击恢复与脱身策略边界](skills/gameplay-hit-recovery/SKILL.md)：当连续受击使角色难以恢复操作时，评估一段时间内受击阈值脱身及其状态提示；单次受击后的免疫窗口另用独立入口，不将阈值脱身当作无敌。
- [射击、持续喷射与来源对齐](skills/gameplay-shooting-feedback/SKILL.md)：为重复射击组织枪口光、视觉后坐和弹壳，并核对弹丸或持续喷射与可见发射源对齐；发射不等于命中，视觉连接不证明碰撞正确。
- [多阶段法术生命周期与形状层级](skills/gameplay-projectile-spells/SKILL.md)：在蓄力、释放、持续运动、接触和消散脱节时组织法术生命周期；用事件和主体形状区分阶段，枪械发射与枪口对齐改用独立射击入口。
- [Boss 入场、转阶段与终结](skills/gameplay-boss-sequences/SKILL.md)：为 Boss 入场、阶段转换和死亡高潮编排可中断的反馈序列；战斗预警复用共享技能，不凭 Final Hit 标题推断保命机制。
- [低血量伤害缩放与生存余量](skills/gameplay-low-health-damage-reduction/SKILL.md)：在残血时下一次普通命中立即结束尝试、希望增加有限生存机会时，设计按生命状态缩放伤害的规则与边界测试；不负责固定 1 HP 保命、血条显示或受击无敌窗口。
- [小于视觉轮廓的受伤区域](skills/gameplay-hurtbox-tolerance/SKILL.md)：当擦过角色边缘的攻击仍造成伤害、项目希望增加空间闪避余量时，设计小于可见形象的受伤区域并验证命中边界；不把受伤区域等同于世界移动碰撞体，也不提供时间无敌。
- [受击后的短时保护](skills/gameplay-post-hit-protection/SKILL.md)：当密集命中在玩家反应前连续扣血时，设计一次有效受击后的短时伤害免疫、计时边界和状态提示；不负责残血减伤、缩小受伤区域或累计受击次数后的阈值脱身。

### 移动与车辆控制

- [移动方向动画与姿态一致性](skills/gameplay-movement-feedback/SKILL.md)：当四向/八向移动动画或跑姿与真实运动朝向不一致时校对方向表现；冲刺、落地、跳跃许可和车辆物理使用独立入口，不宣称方向帧增加就降低输入延迟。
- [冲刺路径与残像反馈](skills/gameplay-dash-feedback/SKILL.md)：当冲刺速度存在但路径、起止或角色轮廓难读时，组合方向形变、残像与速度线并做样式对照；不因幽灵外观新增无敌或改变实际移动规则。
- [落地事件与强度分级反馈](skills/gameplay-landing-feedback/SKILL.md)：当落地缺少重量或每帧接地重复播反馈时，绑定真实着地边沿并按高度/接触速度分级；不改跳高、接触物理或落地伤害。
- [离地跳跃宽限](skills/gameplay-jump-forgiveness/SKILL.md)：当角色刚离开平台便无法起跳时，评估 coyote time 的窗口、消费与重置规则；不处理落地前命令缓冲、顶角纠偏或防止离台。
- [移动交互的停留与接续](skills/gameplay-traversal-transitions/SKILL.md)：当平台边缘或抓杆交互的停留、释放选择不符合目标移动节奏时，设计防误落或连续接续状态；保留自主控制取舍，不以动画快慢替代规则设计。
- [车辆转向辅助与直接控制](skills/gameplay-steering-assistance/SKILL.md)：当车辆直接转向突兀、整体平滑输入又迟滞时，评估状态相关 self-steer 辅助及可关闭的直接控制对照；不负责轮胎碰撞或视觉后坐。
- [移动部件的接触表示](skills/gameplay-locomotion-contacts/SKILL.md)：当轮胎等移动部件漏掉路缘或侧面接触时，比较线采样与体积表示的覆盖、稳定性和成本；区分接触物理、网格外观与转向辅助。
- [落地前跳跃输入缓冲](skills/gameplay-jump-input-buffer/SKILL.md)：当落地前略早按跳被丢弃时，设计有限期的跳跃命令保留、合法时机执行与一次性消费；不同于离地后延长起跳许可，不声称已有可直接移植的输入实现。
- [上升碰撞的顶角宽容](skills/gameplay-ceiling-corner-correction/SKILL.md)：当上升角色轻擦顶角便被截断跳跃时，评估受限的横向角落修正及目标位置可达性；不处理输入早晚、缩小受伤区域或允许穿过实体。

- [鼠标轨迹曲率到转向输入](skills/gameplay-pointer-curvature-steering/SKILL.md)：当项目用鼠标画圈的轨迹曲率控制车辆转向时，设计位置流平滑、历史取样与转向映射的诊断和验收；不是光标位置直接瞄准、跳跃命令缓冲或基于车辆行进方向的 self-steer。

### 数值与资源状态

- [生命血条与损失残影](skills/gameplay-health-damage-ui/SKILL.md)：在 HP 变化突兀、损失量难读或低血量提示不清时设计血条平滑、延迟损失段和生命分级；此旧入口保留兼容路由，瞬时浮字与结果总分计数各有独立 owner。
- [伤害、治疗与得分浮字](skills/gameplay-floating-numbers/SKILL.md)：在瞬时伤害、治疗或得分数字缺少层次、遮挡对象或无法区分事件类型/暴击时设计浮字实例与密集事件布局；共享表现，不混同业务结算或结果总分计数。
- [法力与体力的实时资源读数](skills/gameplay-resource-ui/SKILL.md)：当法力/体力消耗、恢复或耗尽难读时，将真实资源量与显示动画对齐；成长徽章与实时读数分层，冷却时钟和按住输入改走专用入口。
- [冷却时钟与就绪反馈](skills/gameplay-cooldown-ui/SKILL.md)：当技能倒计时、填充和实际可用时刻不一致时，校对冷却时钟与就绪状态；不把恢复动画结束作为技能规则，也不处理资源量或按住蓄力。

### 交互与场景状态

- [游戏内交互状态与提交反馈](skills/gameplay-contextual-ui/SKILL.md)：为游戏内按钮、按住操作、拾取提示和指令选择区分可用、焦点、执行中、成功/失败；卡牌布局、对话、机关、连接和切场使用独立入口。
- [手牌布局与卡牌选择](skills/gameplay-card-interaction/SKILL.md)：当手牌跟随、扇形布局、翻面或升级卡选择缺少清晰状态时，设计卡牌交互反馈；不把奖励揭示或实际卡牌战斗规则混为布局动画。
- [对话文字进度与强调](skills/gameplay-dialogue-presentation/SKILL.md)：当逐字对话、标点节奏、情绪强调或结束提示不清时组织文本显示；区分字形动画、句子进度和真正继续操作，不推断未证的跳过功能。
- [世界内操作指示与深度对齐](skills/gameplay-worldspace-indicators/SKILL.md)：当世界内目标圈、鱼钩或操作指示与真实目标深度/投影错位时校对空间反馈；不同于仅让资源更显眼，不从动画推断成功判定。
- [机关驱动与通行反馈](skills/gameplay-mechanical-interactions/SKILL.md)：当压板、开关与门体运动/通行状态不一致时，组织触发、机械位移和接地反馈；分段变化不等于已知错峰算法。
- [连接关系与挂脱轨迹](skills/gameplay-connection-transitions/SKILL.md)：当挂钩、绳端连接/脱开的过程不可读或与真实关系不同步时，组织锚点和过渡状态；不由弯曲绳形推断牵引物理或抛物线算法。
- [切场遮蔽与就绪恢复](skills/gameplay-scene-transitions/SKILL.md)：当场景切换突显出生点或相机跳变时，组织遮蔽到就绪再恢复显示的流程；视觉过渡不是加载/出生点修复，不把未证淡出写成事实。

### 破坏与奖励

- [破坏、死亡与采集产物过程](skills/gameplay-breakables-loot/SKILL.md)：为可破坏物、敌人死亡和资源采集组织受击到终态/产物的可见过程；奖励揭示与拾取另行处理，不把倒伏、碎片或图标当作结算证明。
- [宝箱、卡牌与加工结果揭示](skills/gameplay-reward-reveal/SKILL.md)：当宝箱、稀有卡、合并或升级结果缺少清楚揭示时，绑定既有过程/成功事件组织预备、显现与结果确认；不把演出结束当结算或实际领取。
- [掉落物吸附与拾取确认](skills/gameplay-loot-pickup/SKILL.md)：当金币或掉落物的来源、引导和实际领取不清时，区分生成、可拾取、吸附与成功确认；吸附只在既有规则允许时使用，不猜半径、穿障或经济值。

### 持续维护

- [新案例去重与技能升级](skills/gameplay-skill-ingestion/SKILL.md)：把新的游戏效果优化案例归入此库，按帖子 ID 和机制双重去重，升级已有技能而非一帖一文件；仅在任务要求维护此库时使用。

## 证据边界与去重

- [来源清单](sources/INDEX.md) 与 [机器可读登记](sources/posts.json) 保留每条观察、参数出处、署名与缺口。源码/音频核验状态不因迁移升级。
- 新的简化对照补充早按缓冲、顶角纠偏、低血减伤、小受伤区域与受击后保护。它们提供设计/验收入口，不是已运行实现；旧 Celeste 缓冲来源和旧 Mercy Frames 标题的缺口仍以限定来源的 evidence_only 路由保留，不用新帖参数补旧帖。Boss 屏障材质仍不包装成通用 shader 能力。
- Ddvr0NYNkNF 的 hitstop 主段 55 ms 与开头 60 ms 标签存在冲突，均保留为未测示例。各来源给出的毫秒、像素、倍率和百分比都不是本库默认参数。
- [入库流程](skills/gameplay-skill-ingestion/SKILL.md)：同 ID 的 URL 变体去重；同工作流新证据融合；独立触发、状态或关键失败验收应有独立入口。同一大类不等于同一工作流，新作者、参数、颜色也不构成拆分理由。
- 排除项继续保留：终端工具、泛美术展示和未达证据要求的 Director 概述；不转载视频/音频/代码，不含私人账户或认证信息。

## 校验与集成

    python scripts/validate.py
    python -m unittest discover -s tests -v

另用安装环境的 skill-creator quick_validate.py 检查 skills/*。结构校验覆盖 owner、双向来源、路由与已审定 distinct_from 边界；它不自动理解自然语言，不替代实际请求演练或游戏测试。详见[验证记录](docs/VALIDATION.md)。当前未配置仓库 CI workflow，本地校验通过不等于远端 CI 通过。

维护目标：[GitHub 仓库](https://github.com/ziyou-lu/bkb-gameplay-skills)。[集成说明](docs/INTEGRATION.md)要求保留已有历史、普通提交与非强制更新，分别核对本地提交、发布和远端 SHA。
