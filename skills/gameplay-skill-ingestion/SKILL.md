---
name: gameplay-skill-ingestion
description: "把新的游戏效果优化案例归入此库，按帖子 ID 和机制双重去重，升级已有技能而非一帖一文件；仅在任务要求维护此库时使用。"
---

# 新案例去重与技能升级

本文件是从来源案例提炼的迁移流程，不是作者源码复刻，也未在目标游戏中执行。下面的验收项是实施后要做的检查，不是已经通过的测试。

## 触发条件

- 新找到逐层改进、同场景前后对照或明确机制实验。
- 旧帖补齐缺失步骤，或新例子和已有 hitstop/flash/camera/healthbar 重复。

## 先确认的输入

公开来源链接或准确帖子 ID、已核验观察与未核验项、现有 catalog.json 与 sources/posts.json、当前仓库分支。

## 分步机制

1. 先读取目标仓库 AGENTS、catalog.json、sources/posts.json 和相关 SKILL.md；远端不可访问时仅准备待合并包，不能假设仓库空白。
2. 用 scripts/validate.py 的 post_id_from_url 规则识别 /p/、/reel/、/reels/ 及作者路由的同一 shortcode。URL 查询参数不构成新来源；只有 ID 没链接时保留 null，不臆造地址。
3. 记录实见画面、字幕/正文、可见代码、实际运行测试的区别；未核听声音不得标为听过，展示代码不得标为运行验证。先更正旧帖缺口，再汇总机制。
4. 查 catalog 的机制 owner 和 task_routes，用真实请求比较触发目标、所需输入、状态推进与失败验收。相同工作流的新证据/参数/风格升级原技能；相同视觉原语由组合引用。不能因为都属“移动”“UI”“奖励”就在旧 recipe 无限加分支，也不能把控制/物理规则改动写成表现层升级。
5. 若用途、输入/状态或关键失败验收形成可独立执行的任务，就新建精准入口并迁移 owner；不要先扩大旧触发条件再据此宣称无需新增。若多个场景复用同一状态流程则保留条件分支，数量不是目标。补一条正向请求、易混淆的相邻请求和边界；把已审定独立路由登记 distinct_from，保留旧路径的导航，不复制流程。证据只支持行为说明而无完整工作流时标 evidence_only，例如冻结来源中的输入缓冲说明；不能为了数量把它包装成已验证实现。纯工具/泛艺术等仍登记排除原因。
6. 新证据若冲突，保留范围与来源差异；已证补齐替换旧缺口并记录 evidence_updates，不能把另一帖子步骤移植成原帖事实。参数只进示例来源和迁移说明，不无证升级为默认值。
7. 更新 sources、catalog 的双向归属与 task_routes；审阅来源事实/缺口随迁移保留，纯结构变更不增加来源数；运行 python scripts/update_index.py 刷新派生来源清单，再运行 python scripts/validate.py 和 python -m unittest discover -s tests -v，并用安装环境的 skill-creator quick_validate 校验各技能。查看 diff，确认无私人账号、凭据、复制素材或无关文件。
8. 按用户授权 commit/push 目标仓库，不 force push；在真实已有分支上集成，先确认远端当前历史，推送后比对 remote HEAD/目标分支 SHA。不能把本地准备、提交或失败推送说成已远端完成。

## 适用限制

- 本技能提供内容与合并流程，不授予登录、发帖、点赞、抓取账号信息、安装凭据或更改网络的权限。
- 来源补全与机制归纳不需要转载视频/音频原件；链接可失效，应保留已观察摘要与限制。

## 验收

- [ ] 同一 URL 的 /p/ 与 /reel/ 变体只增加一个 source，重复机制不产生第二个 owner。
- [ ] 新增案例能沿来源→机制→skill 双向定位，未知项与已补齐项不矛盾。
- [ ] 用至少一条实际请求和易混淆请求检查入口能否被找到；独立状态/失败路径不因大类名相同而合并，同一原语也不产生多个 owner。
- [ ] 自动路由校验只检查声明完整性与已审边界，不等同自然语言检索质量；实质拆分须另做独立请求演练。
- [ ] 验证通过且 diff 仅含目标更新；只有远端 SHA 核对成功才报告 pushed。

## 组合而不复制

只在需要相应机制时读取，沿用其事件与预算约束：

- [命中停顿与表现节奏](../gameplay-hitstop/SKILL.md)
- [接触闪光、冲击帧与粒子](../gameplay-impact-visuals/SKILL.md)
- [镜头冲击与短促聚焦](../gameplay-camera-feedback/SKILL.md)
- [生命血条与损失残影](../gameplay-health-damage-ui/SKILL.md)

## 来源证据

完整观察、证据类型、未证项和参数 provenance 见 [来源登记](../../sources/posts.json)。来源只支持下列案例内容，不证明本文件新增工程建议已在原帖实现。

- [DejijtPzhYJ](https://www.instagram.com/reel/DejijtPzhYJ/)：组合战斗反馈。
- [Ddy_-6wDMkn](https://www.instagram.com/reel/Ddy_-6wDMkn/)：像素拳击五层。
- [Deo9lu7tzCT](https://www.instagram.com/p/Deo9lu7tzCT/)：宝箱七步反馈。
- [DenLEa4xApp](https://www.instagram.com/p/DenLEa4xApp/)：弹反反馈。
- [DesK-ImRqfA](https://www.instagram.com/p/DesK-ImRqfA/)：Boss 击杀高潮。
