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
4. 查 catalog 中的机制唯一归属。相同机制更新原技能步骤、限制、验收和来源；场景差异只在现有 recipe 中增加条件分支并引用共享技能。
5. 只有新例子形成无法由现有触发条件/流程涵盖的独立任务才新增 skill，明确与邻近技能边界；单个作者、新参数和新风格不够。纯开发工具、泛艺术展示等记排除原因，不建效果 skill。
6. 新证据若冲突，保留范围与来源差异；已证补齐替换旧缺口并记录 evidence_updates，不能把另一帖子步骤移植成原帖事实。参数只进示例来源和迁移说明，不无证升级为默认值。
7. 更新 sources 与 catalog 的双向归属；运行 python scripts/update_index.py 刷新派生来源清单，再运行 python scripts/validate.py 和 python -m unittest discover -s tests -v，并用安装环境的 skill-creator quick_validate 校验各技能。查看 diff，确认无私人账号、凭据、复制素材或无关文件。
8. 按用户授权 commit/push 目标仓库，不 force push；在真实已有分支上集成，先确认远端当前历史，推送后比对 remote HEAD/目标分支 SHA。不能把本地准备、提交或失败推送说成已远端完成。

## 适用限制

- 本技能提供内容与合并流程，不授予登录、发帖、点赞、抓取账号信息、安装凭据或更改网络的权限。
- 来源补全与机制归纳不需要转载视频/音频原件；链接可失效，应保留已观察摘要与限制。

## 验收

- [ ] 同一 URL 的 /p/ 与 /reel/ 变体只增加一个 source，重复机制不产生第二个 owner。
- [ ] 新增案例能沿来源→机制→skill 双向定位，未知项与已补齐项不矛盾。
- [ ] 验证通过且 diff 仅含目标更新；只有远端 SHA 核对成功才报告 pushed。

## 组合而不复制

只在需要相应机制时读取，沿用其事件与预算约束：

- [命中停顿与表现节奏](../gameplay-hitstop/SKILL.md)
- [接触闪光、冲击帧与粒子](../gameplay-impact-visuals/SKILL.md)
- [镜头冲击与短促聚焦](../gameplay-camera-feedback/SKILL.md)
- [生命血条与浮动数值](../gameplay-health-damage-ui/SKILL.md)

## 来源证据

完整观察、证据类型、未证项和参数 provenance 见 [来源登记](../../sources/posts.json)。来源只支持下列案例内容，不证明本文件新增工程建议已在原帖实现。

- [DejijtPzhYJ](https://www.instagram.com/reel/DejijtPzhYJ/)：组合战斗反馈。
- [Ddy_-6wDMkn](https://www.instagram.com/reel/Ddy_-6wDMkn/)：像素拳击五层。
- [Deo9lu7tzCT](https://www.instagram.com/p/Deo9lu7tzCT/)：宝箱七步反馈。
- [DenLEa4xApp](https://www.instagram.com/p/DenLEa4xApp/)：弹反反馈。
- [DesK-ImRqfA](https://www.instagram.com/p/DesK-ImRqfA/)：Boss 击杀高潮。
