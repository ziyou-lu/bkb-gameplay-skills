# BKB Gameplay Skills

给游戏创建 Agent 使用的中文技能库：围绕游戏中的小型玩法与表现问题，直接指导实施、调参、排错和验收。来源研究是按需参考，不是 Agent 的执行流程。

当前：**88 个任务入口（87 个游戏内容工作流 + 1 个维护），154 个主来源（149 纳入、5 排除）**。保留独立任务边界与共享机制 owner，不按帖子复制，也不以大类相同强行合并。结构沿革见[迁移说明](docs/MIGRATION.md)。

## 使用

1. 按游戏里需要解决的症状选择下方入口，或查 [catalog.task_routes](catalog.json) 的真实请求示例和相邻边界。
2. 读取选中 SKILL.md，核对项目输入及前置条件，按实施顺序做最小可验证改动，再依机制参数调优、检查验收与失败路径。只在确实需要另一机制时读取组合链接。
3. 执行入口不依赖先读研究材料。需要核对案例、署名、原参数或实现证据时，按页尾链接打开 references/sources.md；机器映射由 catalog.evidence_path 和 sources/posts.json 维护。
4. 保留目录关系。组合技能编排事件，底层机制由唯一 owner 说明；已有路径与独立路由保留。本库尚未安装到任一具体游戏项目。

## 实施与证据的区别

正文包含从案例提炼的机制和为项目落地补充的工程操作，是待 Agent 在目标项目实施的指导，不是作者源码复刻或已通过的游戏测试。具体引擎 API、项目阈值和预算由当前项目决定；来源示例数值不是通用默认值。参考资料分别保留观察、作者说明、静态代码与未证项，不因正文新增实施步骤就升级来源事实。

Agent 完成任务时应报告实际修改、测过的场景与仍未验证的风险，不把文档复述或结构检查当作功能完成。

## 按实际任务选择

### 接触、形变与空间可读性

- [手柄视角边界减速](skills/gameplay-gamepad-pitch-limits/SKILL.md)：仅对手柄指向俯仰边界的输入减速并保留硬限制，鼠标绕过此边界缓动；不是事件震动、速度FOV或表面法线相机上方向。
- [房间焦点驱动的三维地图导航](skills/gameplay-room-map-navigation/SKILL.md)：地图独立选中房间与焦点，平滑切换房间并绕当前焦点旋转缩放；不是世界镜头冲击、完成事件镜头或普通菜单聚焦。

- [双缓冲移动历史场](skills/gameplay-surface-history-field/SKILL.md)：交换读写纹理积累表面交互，选择像素对齐与恢复规则，不把生成时间贴花当作所有历史场。

- [移动参数驱动的植被接触声](skills/gameplay-foliage-rustle-response/SKILL.md)：消费已有植被接触与移动速度/力度/方向调节响应，非倒伏阶段音层、视觉装饰摆动或已验证立体声算法。
- [下冲转滚与滚动冲刺的动量交接](skills/gameplay-dash-roll-momentum/SKILL.md)：仅明确要求真实移动规则时处理下冲接地到滚动再到临时推进的速度/状态交接；不是冲刺残影、落地震动或无条件能量守恒。

- [区域辅助下蹲与已有姿态控制复用](skills/gameplay-crouch-zone-assistance/SKILL.md)：关卡碰撞区贡献独立下蹲请求，复用原控制并处理重叠、手动输入和安全站起；不是第二套动画系统。

- [自定义光线投射器的墙面深度纠偏](skills/gameplay-raycaster-depth-correction/SKILL.md)：仅修正已有恒高墙体逐列raycaster的投影深度，不构建完整引擎、重写网格遍历或添加相机后处理。
- [创建时间纹理驱动的限时地面效果](skills/gameplay-timestamped-ground-effects/SKILL.md)：位置/形状写入数据纹理并保存创建时间，由贴花评估年龄；玩法网格独立权威，不是地形贴合网格生成、实体流体或普通UV滚动。

- [不转移液体体积的装饰瀑布](skills/gameplay-decorative-waterfall/SKILL.md)：合格湖水/半格边缘生成独立视觉水流，避免风景瀑布抽干水源或淹没下游；不替代实际液体模拟。

- [稀疏环境序列帧粒子与背景微动](skills/gameplay-ambient-flipbook-particles/SKILL.md)：逐帧绘制、贴图网格与SubUV格数一致，再以受控间隔出现于背景；不是战斗爆发或凝视AI。

- [固定相机插画投影与简化场景几何](skills/gameplay-fixed-camera-art-projection/SKILL.md)：固定参考相机的插画投影到简单几何，不是全向纹理展开、移动UV动画或角色方向姿态。
- [复用骨骼姿态的简化网格平面阴影](skills/gameplay-skeletal-planar-shadows/SKILL.md)：低面数骨骼副网格复用主姿态并在材质中投到已声明地面，非地面位置圆斑提示、任意地形贴合或物理光照求解。

- [角色面向内的有限角度手电瞄准](skills/gameplay-facing-relative-light-aim/SKILL.md)：移动方向决定角色面向，鼠标在相对允许弧内控制照明，开关独立；不是全向武器瞄准或阴影渲染教程。

- [物理阶段驱动的断裂、下落与触地音层](skills/gameplay-physics-stage-audio/SKILL.md)：由真实物理阶段驱动局部音频事件与变体，不改倒伏力学、不把预录时长当触地事件，也不自动增加枝条声。
- [枝条根部精确砍击与差异采集结果](skills/gameplay-precision-branch-cutting/SKILL.md)：仅显式玩法需求下按枝根命中位置分配脱离或减伤结果；不是纯视觉破坏、枝条地形碰撞覆盖、宽松受伤轮廓或切割时机对齐。
- [受击时启用道具动态物理](skills/gameplay-impact-physics-activation/SKILL.md)：显式允许静态待命的对象受击后进入动态模拟，保留碰撞、逻辑状态和首击；不是重心施力调参、自动休眠或直接进入破坏终态。

- [降雨的斜线、溅水与水洼涟漪](skills/gameplay-rain-surface-feedback/SKILL.md)：连续降雨的空中方向、接收面分类与短命涟漪编排；不是生成水洼网格、真实积水流体或整套天气模拟。
- [动态尺寸物件的持握锚点与径向贴合](skills/gameplay-dynamic-carry-alignment/SKILL.md)：几何可变的实体物件按重量组、局部锚点/轴与半径调整携带位置；不是固定工具挥动姿态、完整IK求解器或掉落物吸附后消失。

- [玩法驱动的薄片卷曲](skills/gameplay-sheet-curl/SKILL.md)：当纸张、卷轴或薄布需要随交互卷起/展开时，用物体空间长度阈值将自由段顶点映射到圆弧；保留固定段与锚边，不用骨骼蒙皮，不替代 UV 滚动、整体 squash/stretch 或布料物理。

- [命中停顿与表现节奏](skills/gameplay-hitstop/SKILL.md)：在命中缺少接触感、或发射/翻牌揭示缺少节奏时设计接触 hit-stop 与非接触表现停顿；不把冰冻状态或全局暂停混为一谈。
- [接触闪光、冲击帧与粒子](skills/gameplay-impact-visuals/SKILL.md)：改善接触闪光、冲击帧、粒子与碰撞文字，并管理既有战斗残留的寿命和遮挡预算；不把发射残留当命中，贴地余效生成与通用渲染实现不在本入口。
- [事件形变、回弹与视觉后坐](skills/gameplay-motion-deformation/SKILL.md)：在接触、弹跳、按钮反馈或快速出招缺少受力和轮廓时设计 squash/stretch、回弹、视觉后坐与 smear；只管理事件形变，持续跟随、瞄准组合、动作时序和物理接触使用独立入口。
- [角色装饰的次级运动](skills/gameplay-secondary-motion/SKILL.md)：在头发、眼部或链状装饰跟随运动僵硬、翻面跳变或传送后残留速度时设计持续次级运动；区分父对象真实运动与装饰滞后，不延迟实际朝向。
- [方向瞄准与分件姿态](skills/gameplay-aim-pose/SKILL.md)：在持枪方向改变时角色像整张纸片旋转，或肩部、持握点、遮挡与真实瞄准不协调时组织分件 sprite、方向帧或 stack 表示；不新增自动瞄准或改变射击规则。
- [输入响应与动作相位](skills/gameplay-action-timing/SKILL.md)：在输入后动作看起来迟迟不响应，或整体加速让动作失去重量时定位冗余准备段、主体和收势；独立核对可见响应、真实生效与恢复时刻，不一律删除前摇。
- [视觉材质感与接触响应诊断](skills/gameplay-contact-response/SKILL.md)：在网格损伤与碰撞硬度不符、或落地回弹不合材质目标时，隔离视觉表现与接触发生后的响应，做局部可回退实验；不接管倒伏前的重心/施力控制，也不是软体或通用容差教程。
- [表面余效的贴地与边界适配](skills/gameplay-surface-aftermath/SKILL.md)：为倾倒或碰撞后的水洼等表面余效实现承载面采样、边界截断与受控网格生成，修复悬空和穿边；不负责真实流体或玩法碰撞。
- [世界目标发现性与局部提示](skills/gameplay-world-readability/SKILL.md)：改善世界资源与交互目标发现性；按既定允许信息比较尺寸/位置、局部提示、方向线索和临时识别模式，不扩大检测或交互范围；角色遮挡检测与显露使用独立入口。

- [可弯曲与压缩的交互承载面](skills/gameplay-deformable-support/SKILL.md)：当车轮等载荷需要在可弯曲、可压缩的承载面上保持接触时，设计连接刚体层与层间弹簧的局部原型及稳定性验收；不是固定碰撞体的视觉压扁、通用软体算法或物性标定教程。

- [角色遮挡检测与局部显露](skills/gameplay-occlusion-reveal/SKILL.md)：当玩家角色被前景遮住难以跟踪，或轻微遮挡便误开大面积透视时，组织角色采样、遮挡聚合、局部显露与退出检查；不负责目标发现、相机改位、敌人视线 AI 或透视 shader 实现。

- [翻转视角下的重力方向线索](skills/gameplay-gravity-orientation-cues/SKILL.md)：当墙面/天花板攀爬或旋转视角让世界向下方向难辨时，设计与真实重力一致的轻量运动线索及覆盖验收；不旋转相机、不改变角色重力，也不把普通落地尘或目标提示当同一任务。

- [几何边界与离散事件触发对齐](skills/gameplay-geometric-event-alignment/SKILL.md)：当切断等离散事件早于或晚于可见物体经过操作边界时，明确几何参照、触发条件与一次性状态，再核对实际事件位置；不负责动画加速或切割网格算法。

- [运行状态驱动的局部表面动画](skills/gameplay-state-driven-surface-motion/SKILL.md)：当机器已运行但皮带等表面仍静止，或材质滚动与实际运行状态矛盾时，限定目标表面并将权威状态映射到可读的表面动画；不是实体皮带模拟、机关通行或任意背景 UV 装饰。

- [道具突出部的接触覆盖与响应](skills/gameplay-prop-appendage-contacts/SKILL.md)：当树枝等道具突出部随主体撞地却穿过表面时，检查局部碰撞覆盖、主体与部件的接触响应及分离边界；不负责整物倒伏演出、可断关节算法或通用软体模拟。

- [切割新表面的封口与材质边界](skills/gameplay-cut-surface-rendering/SKILL.md)：当游戏切割产生开放截面、错误外皮材质或圆形木芯不贴合不规则轮廓时，组织新暴露面的封口与材质边界校对；不提供切割触发、通用三角化或物理断裂算法。

- [道具倒伏的重心与施力诊断](skills/gameplay-prop-toppling-dynamics/SKILL.md)：当道具已有物理倒伏，但首次触地前的转动和重量感不合目标时，分开诊断重心参照与施力位置；不负责触地后的材质回弹、整套采集过程或通用刚体求解器。

### 镜头与结果展示

- [镜头冲击与短促聚焦](skills/gameplay-camera-feedback/SKILL.md)：在单次击打、落地、后坐或爆炸缺少重量，或现有震动漂移、影响瞄准时调整临时 shake、impulse 与 punch-in；持续速度视野及完成镜头交接使用独立入口。
- [持续速度视野与边缘效果](skills/gameplay-speed-camera/SKILL.md)：在钩爪、冲刺或跑酷已有高速运动，但速度线、动态 FOV 与径向模糊缺少协调或妨碍路径判断时设计持续速度表现；不把镜头变化当成角色实际加速。
- [完成事件、结算与动作尾声](skills/gameplay-completion-sequences/SKILL.md)：当完成界面、计数动画和终点镜头互相打断时，编排一次权威完成事件到可结束的收尾流程；引用数值与镜头机制，不复制它们或把演出当真实结算。
- [结果总分递增计数](skills/gameplay-result-counting/SKILL.md)：在完成/结算界面需要把已确认总分递增显示时设计只读计数动画；验证终值、支持的跳过和重开，不把动画刷新当成逐次得分或奖励发放。

- [表面感知的相机上方向](skills/gameplay-surface-camera-up/SKILL.md)：当贴壁角色经过地面小凸缘就把视角扭向地面时，以局部表面法线证据协调 world-up 与角色 up，保留真正攀墙时的视角旋转；不替代遮挡显露、相机碰撞、短促震动或速度 FOV。

### 战斗、射击与法术

- [工具动作与身体持握协调](skills/gameplay-tool-body-coordination/SKILL.md)：当第一人称挥动工具只见手在动、双手持握与身体参与脱节时，组织工具动作、持握约束与多部位姿态的协调及视角验收；不提供完整 IK 求解器、人体物理或伤害规则。

- [攻击预警与反制可读性](skills/gameplay-attack-readability/SKILL.md)：在敌人招式、Boss 区域攻击或危险路径难读时改善姿态、前摇、落点与窗口；将可读性修改与伤害、碰撞、难度修改分开验收。
- [近战命中、受击与暴击编排](skills/gameplay-melee-feedback/SKILL.md)：为普通近战命中、受击、暴击及重武器重量组合共享反馈；剑轨迹、弹反、踩踏、攻击方向规则和受击脱身使用独立入口，不凭视觉改变判定。
- [攻击方向规则与输入判定一致性](skills/gameplay-attack-direction/SKILL.md)：当四向限制妨碍斜向攻击或出招方向与输入意图不一致时，评估攻击方向规则及显示/判定对齐；只在明确需要时改玩法，不推断自动瞄准或任意角算法。
- [剑刃轨迹采样与网格拖尾](skills/gameplay-blade-trails/SKILL.md)：当挥剑方向不清或拖尾断裂、串段和残留时，组织剑尖采样、弧形网格、尾端渐隐与纹理遮罩；轨迹只表达动作，不替代攻击判定。
- [弹反窗口、成功确认与反击反馈](skills/gameplay-parry-feedback/SKILL.md)：当弹反预备、成功和反击机会难以区分时，按真实判定窗口与结果组织反馈；纯表现调整不新增宽容窗口、击退或反击加伤。
- [踩踏反弹与连续命中确认](skills/gameplay-stomp-combos/SKILL.md)：为踩头成功、主角反弹和连续踩踏组织反馈，区分接触确认、实际反弹与连击结算；不从拉伸或递增分数推断跳高和经济规则。
- [连续受击恢复与脱身策略边界](skills/gameplay-hit-recovery/SKILL.md)：当连续受击使角色难以恢复操作时，评估一段时间内受击阈值脱身及其状态提示；单次受击后的免疫窗口另用独立入口，不将阈值脱身当作无敌。
- [射击、持续喷射与发射源对齐](skills/gameplay-shooting-feedback/SKILL.md)：为重复射击组织枪口光、视觉后坐和弹壳，并核对弹丸或持续喷射与可见发射源对齐；发射不等于命中，视觉连接不证明碰撞正确。
- [多阶段法术生命周期与形状层级](skills/gameplay-projectile-spells/SKILL.md)：在蓄力、释放、持续运动、接触和消散脱节时组织法术生命周期；用事件和主体形状区分阶段，枪械发射与枪口对齐改用独立射击入口。
- [Boss 入场、转阶段与终结](skills/gameplay-boss-sequences/SKILL.md)：为 Boss 入场、阶段转换和死亡高潮编排可中断的反馈序列；战斗预警复用共享技能，不凭 Final Hit 标题推断保命机制。
- [低血量伤害缩放与生存余量](skills/gameplay-low-health-damage-reduction/SKILL.md)：在残血时下一次普通命中立即结束尝试、希望增加有限生存机会时，设计按生命状态缩放伤害的规则与边界测试；不负责固定 1 HP 保命、血条显示或受击无敌窗口。
- [贴合轮廓的受伤区域与擦边容差](skills/gameplay-hurtbox-tolerance/SKILL.md)：当攻击或危险障碍擦过角色边缘却命中、项目希望增加空间容差时，设计较小或贴合轮廓的受伤区域并验证命中边界；不把受伤区域等同于世界移动碰撞体，也不提供时间无敌。
- [受击后的短时保护](skills/gameplay-post-hit-protection/SKILL.md)：当密集命中在玩家反应前连续扣血时，设计一次有效受击后的短时伤害免疫、计时边界和状态提示；不负责残血减伤、缩小受伤区域或累计受击次数后的阈值脱身。

### 移动与车辆控制

- [坏落地的翻倒、掉物与恢复](skills/gameplay-landing-tumble-recovery/SKILL.md)：仅在项目明确要求坏落地的玩法后果时，以过快接触且不良接触角触发一次翻倒/布娃娃、短暂失控与持物掉落，再恢复控制和取回资格；不是普通落地特效，不自动添加伤害、敌人感知或噪声规则。

- [按住与松开控制跳跃高度](skills/gameplay-variable-jump-height/SKILL.md)：当轻点和长按跳跃需要不同顶点高度时，实现起跳后的松开截速或有限保持助力；只塑造一次合法跳跃的高度，不增加起跳许可、输入缓冲或下落重力规则。
- [升降非对称重力与有界顶点缓降](skills/gameplay-asymmetric-jump-gravity/SKILL.md)：当角色需要上升与下降不同重力、下落更快或有界的顶点缓降时，按运动相位配置加速度并处理相位边界；不按保持输入改变高度，不全程加重力，也不新增起跳许可。

- [环境跳板的弹射与腾空反馈](skills/gameplay-launch-pad-feedback/SKILL.md)：编排有效踩压、跳板回弹、权威弹射、上升跟随和落地复位；保留物理轨迹并防止一次接触重复弹射。

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

- [程序步态的预测迈步与髋部协调](skills/gameplay-gait-step-scheduling/SKILL.md)：当程序化步态在启动/转向时脚追赶身体，或多脚各自驱动髋部造成冲突时，协调预测迈步、选腿与共享髋运动；两分支按问题选用，不是方向换图、装饰跟随或物理平衡求解器。

- [移动朝向与观察输入解耦](skills/gameplay-movement-look-decoupling/SKILL.md)：当观察镜头强制决定角色移动/朝向、妨碍边走边看时，分离移动意图与观察输入，定义移动中及静止时的朝向契约；不是方向帧增加、攻击瞄准、自动转向或相机 up 稳定。

- [窄边缘攀附的支撑估计](skills/gameplay-surface-adhesion/SKILL.md)：当攀爬角色在窄凸缘或表面转折处找不到可靠支撑时，检查补充探测、命中位置/法线汇总与附着位姿更新；不把它当遮挡查询、轮胎碰撞形状、2D 顶角纠偏或完整攀爬控制器。

### 数值与资源状态

- [生命血条与损失残影](skills/gameplay-health-damage-ui/SKILL.md)：在 HP 变化突兀、损失量难读或低血量提示不清时设计血条平滑、延迟损失段和生命分级；此旧入口保留兼容路由，瞬时浮字与结果总分计数各有独立 owner。
- [伤害、治疗与得分浮字](skills/gameplay-floating-numbers/SKILL.md)：在瞬时伤害、治疗或得分数字缺少层次、遮挡对象或无法区分事件类型/暴击时设计浮字实例与密集事件布局；共享表现，不混同业务结算或结果总分计数。
- [法力与体力的实时资源读数](skills/gameplay-resource-ui/SKILL.md)：当法力/体力消耗、恢复或耗尽难读时，将真实资源量与显示动画对齐；成长徽章与实时读数分层，冷却时钟和按住输入改走专用入口。
- [冷却时钟与就绪反馈](skills/gameplay-cooldown-ui/SKILL.md)：当技能倒计时、填充和实际可用时刻不一致时，校对冷却时钟与就绪状态；不把恢复动画结束作为技能规则，也不处理资源量或按住蓄力。

### 交互与场景状态

- [游戏内交互状态与提交反馈](skills/gameplay-contextual-ui/SKILL.md)：为游戏内按钮、按住操作、拾取提示和指令选择区分可用、焦点、执行中、成功/失败；卡牌布局、对话、机关、连接和切场使用独立入口。
- [手牌布局与卡牌选择](skills/gameplay-card-interaction/SKILL.md)：当手牌跟随、扇形布局、翻面或升级卡选择缺少清晰状态时，设计卡牌交互反馈；不把奖励揭示或实际卡牌战斗规则混为布局动画。
- [对话文字进度与强调](skills/gameplay-dialogue-presentation/SKILL.md)：当逐字对话、标点节奏、情绪强调或重显后的文字进度不清时组织文本显示与动画生命周期；区分显隐、句子进度和真正继续操作，不接管剧情分支与 NPC 交互规则。
- [世界内位置参照与操作指示](skills/gameplay-worldspace-indicators/SKILL.md)：当世界内操作指示与目标深度错位，或腾空角色缺少当前地面位置参照时，明确标记的空间含义并校对锚点、投影与表面；不把当前投影当未来落点，不改操作判定或攀附物理。
- [机关驱动与通行反馈](skills/gameplay-mechanical-interactions/SKILL.md)：当压板、开关与门体运动/通行状态不一致时，组织触发、机械位移和接地反馈；分段运动、占用和中途反向按明确状态规则处理。
- [连接关系与挂脱轨迹](skills/gameplay-connection-transitions/SKILL.md)：当挂钩、绳端连接/脱开的过程不可读或与真实关系不同步时，组织锚点和过渡状态；不由弯曲绳形推断牵引物理或抛物线算法。
- [切场遮蔽与就绪恢复](skills/gameplay-scene-transitions/SKILL.md)：当场景切换突显出生点或相机跳变时，组织遮蔽到就绪再恢复显示的流程；以真实加载/出生点/相机就绪条件控制恢复，保留失败与取消出口。

### 破坏与奖励

- [破坏、死亡与采集产物过程](skills/gameplay-breakables-loot/SKILL.md)：为可破坏物、敌人死亡和资源采集组织受击到终态/产物的可见过程；奖励揭示与拾取另行处理，不把倒伏、碎片或图标当作结算证明。
- [宝箱、卡牌与加工结果揭示](skills/gameplay-reward-reveal/SKILL.md)：当宝箱、稀有卡、合并或升级结果缺少清楚揭示时，绑定既有过程/成功事件组织预备、显现与结果确认；不把演出结束当结算或实际领取。
- [掉落物吸附与拾取确认](skills/gameplay-loot-pickup/SKILL.md)：当金币或掉落物的来源、引导和实际领取不清时，区分生成、可拾取、吸附与成功确认；吸附只在既有规则允许时使用，不猜半径、穿障或经济值。

### 序列与随机规则

- [不放回洗牌袋与有界出场间隔](skills/gameplay-bag-randomizer/SKILL.md)：每袋各类型一份，洗牌后取完再补，控制缺席上界；含不消费预览和算法参考测试，不是奖励展示或加权掉落。

### 持续维护

- [把案例转成可执行的游戏制作技能](skills/gameplay-skill-ingestion/SKILL.md)：维护游戏创建 Agent 的技能库：把已研究案例转换为可实施的机制工作流，去重来源与机制，更新证据引用和验收；仅用于维护此库。

## 来源与持续维护

- [来源清单](sources/INDEX.md) 与 [机器登记](sources/posts.json) 保留观察、参数出处、署名和缺口；每个技能的参考文件解释其材料范围。只有来源问答需要 evidence_only 路由，不能把它们当新增实施能力。
- [入库流程](skills/gameplay-skill-ingestion/SKILL.md) 要求新旧技能都以 Agent 任务为中心：来源去重、相同工作流升级、独立状态与验收保持独立。新参数、作者或颜色不构成新技能。
- 排除来源继续保留原因，不复制原始视频/音频，不含私人账户或认证信息。源代码执行和音频核验状态以登记为准。

## 校验与集成

    python scripts/validate.py
    python -m unittest discover -s tests -v

另用安装环境的 skill-creator quick_validate.py 检查 skills/*。结构校验覆盖执行/参考分层、来源映射、owner、双向来源、路由与已审定 distinct_from 边界；它不自动理解自然语言，不替代实际请求演练或游戏测试。详见[验证记录](docs/VALIDATION.md)。当前未配置仓库 CI workflow，本地校验通过不等于远端 CI 通过。

维护目标：[GitHub 仓库](https://github.com/ziyou-lu/bkb-gameplay-skills)。[集成说明](docs/INTEGRATION.md)要求保留已有历史、普通提交与非强制更新，分别核对本地提交、发布和远端 SHA。
