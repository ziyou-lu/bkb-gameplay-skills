# BKB Gameplay Skills

把游戏效果优化案例整理成可复用、可继续升级的中文技能库。按机制维护，不按帖子复制文件。

## 使用

1. 从下方分类选任务，读取对应 SKILL.md。需要命中停顿、镜头等基础机制时再读取它链接的共享技能。
2. 所有实施步骤是迁移建议，不是源帖代码或已通过的游戏测试。先核对目标项目，再逐层 A/B。
3. 原帖事实、缺口和示例参数集中在 sources/posts.json。画面、字幕、作者声称、静态读码和运行验证不能混写；本批没有运行作者代码或完整核听音效。
4. 保留整个仓库目录关系，技能中的共享引用需要同仓库文件。尚未将技能安装到任一具体游戏项目或执行器。

## 分类索引

### 共享机制

- [命中停顿与表现节奏](skills/gameplay-hitstop/SKILL.md)：在命中缺少接触感、或发射/翻牌揭示缺少节奏时设计接触 hit-stop 与非接触表现停顿；不把冰冻状态或全局暂停混为一谈。
- [接触闪光、冲击帧与粒子](skills/gameplay-impact-visuals/SKILL.md)：改善接触闪光、冲击帧、粒子、文字与表面余效的可读性和空间一致性；常驻特效遮挡时优先删减，不凭视觉推断伤害、流体物理或具体渲染实现。
- [镜头冲击与短促聚焦](skills/gameplay-camera-feedback/SKILL.md)：用方向性震动、短促推近及速度相关视野/屏幕效果强调接触或高速移动；先保证操作可读性与可减弱性，不把更多镜头运动当作更好或实际加速。
- [压缩拉伸与次级运动](skills/gameplay-motion-deformation/SKILL.md)：改善游戏动作的形变、回弹、跟随、瞄准姿态、快速过渡 smear 与相位节奏；区分视觉形变和物理响应、冗余表演和必要前后摇，不处理泛动画。
- [攻击预警与反制可读性](skills/gameplay-attack-readability/SKILL.md)：在敌人招式、Boss 区域攻击或危险路径难读时改善姿态、前摇、落点与窗口；将可读性修改与伤害、碰撞、难度修改分开验收。
- [生命血条与浮动数值](skills/gameplay-health-damage-ui/SKILL.md)：优化生命血条及伤害、治疗、得分浮字的可读性；共享数字动画但区分事件语义，统一平滑、残影条与去拥挤，不另建每个作者版本。

### 场景组合

- [近战、弹反与踩踏组合](skills/gameplay-melee-feedback/SKILL.md)：将共享反馈组合到剑击、受击、弹反、暴击和踩踏循环；不重复实现 hitstop、镜头、血条，不凭视觉改伤害规则。
- [射击与法术生命周期](skills/gameplay-projectile-spells/SKILL.md)：按蓄力、发射、飞行、命中和余效组织枪械、光束、冰刺、旋转火焰与终极法术；先修空间和主体运动可读性，再组合共享反馈。
- [移动、冲刺与落地反馈](skills/gameplay-movement-feedback/SKILL.md)：优化角色移动表现，并按需评估跳跃容错、边缘防误落、车辆转向辅助与接触表示；区分视觉反馈、控制规则和物理碰撞变更，不处理泛动画。
- [破坏、掉落与奖励揭示](skills/gameplay-breakables-loot/SKILL.md)：为破坏、死亡、掉落、宝箱、物品合并与升级装置设计事件到结果的反馈闭环；区分演出和真实结算，复用共享特效，未展示步骤不补齐。
- [Boss 入场、转阶段与终结](skills/gameplay-boss-sequences/SKILL.md)：为 Boss 入场、阶段转换和死亡高潮编排可中断的反馈序列；战斗预警复用共享技能，不凭 Final Hit 标题推断保命机制。
- [法力、体力、冷却与蓄力状态](skills/gameplay-resource-ui/SKILL.md)：用法力/体力消耗、冷却、恢复和蓄力反馈说明游戏资源状态；区分真实可用时刻与弹性动画，不误导玩家。
- [游戏内交互、卡牌与对话](skills/gameplay-contextual-ui/SKILL.md)：改善游戏内交互、机关、目标/角色可读性与切场过渡，以及卡牌、战斗菜单和对话反馈；校对真实状态、信息范围和就绪条件，不处理泛网站 UI 或泛动画。

### 持续入库

- [新案例去重与技能升级](skills/gameplay-skill-ingestion/SKILL.md)：把新的游戏效果优化案例归入此库，按帖子 ID 和机制双重去重，升级已有技能而非一帖一文件；仅在任务要求维护此库时使用。

## 证据与去重

- [来源清单](sources/INDEX.md)：原帖链接、观察和限制。JSON 是机器可读唯一登记。
- [机制与归属](catalog.json)：一个机制只有一个共享所有者；场景技能只组合，不再复制 hitstop/flash/camera/healthbar 的流程。
- 新案例遵循 [入库技能](skills/gameplay-skill-ingestion/SKILL.md)。同一 shortcode 的 /p/、/reel/、作者路由是同一帖；新作者、新参数、新美术风格通常只是原技能的新证据。
- 终端工具、泛美术风格和本批未验证的 Director 节奏概述保留排除理由，不混入效果优化技能。
- 对原帖只做原创摘要并链接，不转载原视频/音频/代码。未提供素材授权或项目代码许可证，不代表取得第三方素材再分发权。

## 校验与集成

运行：

    python scripts/validate.py
    python -m unittest discover -s tests -v

可另用安装环境提供的 skill-creator quick_validate.py 逐个检查 skills/*。
这些检查覆盖结构、来源 ID、机制归属与引用，不是游戏体验或作者代码执行测试。

维护目标为 [GitHub 仓库](https://github.com/ziyou-lu/bkb-gameplay-skills)。参见 [提交与持续集成](docs/INTEGRATION.md)：在现有历史上合并、校验、普通提交和推送，不强推、不重复新增机制技能。
