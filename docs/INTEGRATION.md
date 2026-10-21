# 提交与持续集成

目标仓库：https://github.com/ziyou-lu/bkb-gameplay-skills

SSH 地址：git@github.com:ziyou-lu/bkb-gameplay-skills.git

官方 HTTPS 地址：https://github.com/ziyou-lu/bkb-gameplay-skills.git

本库维护的是公开游戏效果研究摘要，不包含原作者代码/媒体授权。不要加入私人账户、凭据或无关文件。

## 更新顺序

1. 使用现有受支持认证方式正常 clone/fetch，读取当前 AGENTS、分支状态与现有 skills。不要创建无关新历史或强推。
2. 对照 catalog.json 和 sources/posts.json。相同机制将新步骤/限制/证据融合到原 skill；同一帖子 ID 只补齐观察。读取 gameplay-skill-ingestion。
3. 更新来源登记与双向引用。执行 python scripts/update_index.py 刷新来源索引，然后执行 python scripts/validate.py 和 python -m unittest discover -s tests -v；如可用，另跑 skill-creator quick_validate。
4. 检查 git diff --check、完整 diff、来源证据和目标分支。保留其他人的修改，不以本批内容覆盖既有文件。
5. 在已授权的目标分支普通 commit/push。推送后比较该分支的远端 SHA 与预期提交，才能报告已发布。
6. 若远端变化导致拒绝，正常 fetch 并合并/重放、复验；不 force push。若缺认证，使用官方连接流程，不把密码、token 或私钥放进 URL、仓库、脚本或聊天。

## 证据与检查范围

文件校验不能证明游戏手感、碰撞、性能或无障碍测试已通过。引用视频中的代码没有实际执行；源帖声明、画面观察与新增工程建议必须保持区分。验证范围详见 VALIDATION.md。
