# 来源、纠偏与机制边界

## 主来源支持什么

- 主来源：[Da5c59STLtg · @lab_lasagna](https://www.instagram.com/p/Da5c59STLtg/)，亦有[作者 reel 路径](https://www.instagram.com/lab_lasagna/reel/Da5c59STLtg/)。作品 Star Lane，作者介绍为 Android 像素 roguelike。两种 URL 归一为 Da5c59STLtg，只登记一条主来源。
- 已有研究记录的核读日期为 2026-10-23；本入口复用该记录，没有重新浏览或开展外部研究。全文 caption 讨论像素画法线贴图，以及同一精灵可能需要多个法线图。画面采样见编辑器中宇航员与暖橙灯、选中精灵及可能翻面的字幕、方向色轮、宇航员与紫/青法线图并列。
- “NORMAL MAPS MAY NOT BE FLIPPED!” 是作者工作流内的警告。它不证明所有引擎均不能正确翻面，更不能推导每个镜像方向必须新增资产。
- 没有音频核听、项目或 shader/纹理文件检查、源码执行或目标引擎实测。原帖未给出完整着色公式、法线空间/编码、引擎版本、方向资产数量、材质切换、过滤/压缩或性能结果。
- 对应[来源登记](../../../sources/posts.json)中的 Da5c59STLtg。保留公开机制与归因，不复制媒体或私人数据。

## 作者交叉发布与独立技术佐证

1. [作者 LinkedIn 开发日志](https://www.linkedin.com/posts/benjamin-blas-381467198_ive-been-building-a-roguelike-on-the-side-activity-7483904420485816321-TQ5G)在已有研究中被只读打开，链接 instagram.com/lab_lasagna 并指认同一 Star Lane 法线日志。作者称翻面/旋转精灵需要方向法线图。它佐证作者的表述与身份关联，不是第二套运行实验，也不证明该资产方案普遍必要。
2. [Godot 官方 issue #70517](https://github.com/godotengine/godot/issues/70517)记录 Godot 4.0 beta10 的 Sprite2D 水平/垂直翻面导致反向受光，并讨论对应法线分量随翻面改变的渲染器修正。这是特定历史版本问题的公开文本，不是原帖实际引擎/版本的证据。
3. [Godot 官方 PR #71382](https://github.com/godotengine/godot/pull/71382)的合并状态在已有研究中核到，合并日期为 2023-01-17。它说明渲染器侧修正可以解决这一类 Sprite2D 问题，足以否定“镜像总需另一张法线图”的普遍断言。PR 文件 diff 获取失败，不能称已审计精确实现、已测覆盖旋转/父级负缩放，或据此指定当前项目最低支持版本。
4. [Unity 6000.7 官方 secondary textures 指南](https://docs.unity.com/en-us/engine/6000.7/manual/unity2d/2d-urp/2d-index/secondary-textures)是独立实现补充：将法线作为精灵的 secondary texture，并让 2D light 使用；文档提示额外深度预处理/每层批次全尺寸纹理的性能成本。它不是原视频的 Unity 管线证明，不构成对翻面修正、实际耗时或其他版本行为的验证。该版本号仅标识所读文档，不作本技能通用运行要求。

以上链接与内容来自已提供的研究记录；本次只核读本地材料。官方历史 issue/PR 和 Unity 设置指导分别说明可修复性与接入/成本考虑，不拼接成作者已实现的完整算法。

## 工程指导与未验证运行

执行正文提出的诊断场景、已知倾斜法线、平面基线、法线空间审计、唯一纠正层、逐帧成对绑定、实例隔离、缺失回退和目标设备验收，均是迁移到项目的工程指导，不是原作者已披露的代码。

本入口没有提供通用通道反相公式、引擎 API、推荐版本或固定数值。正确路径取决于 UV 与几何如何翻面、法线编码/空间、渲染器是否已变换基及材质是否额外纠正；即使作者使用方向图，也可能在另一个引擎中只需一张镜像复用图。不同方向原画不一定互为镜像，独立表面信息仍可能需要独立创作。

新增的方向、灯位、图集、动画、组合变换、对象复用和性能检查均待目标项目实际执行。静态格式/关系检查通过不代表画面、运行或性能验收已通过。未核听音频，未执行项目代码，没有基准数据。

## 去重与独立 owner 决策

机制 owner：gameplay-sprite-normal-orientation；路由：sprite-normal-orientation；机制：sprite-normal-orientation。

2026-10-24 初次核读 catalog.json 的 96 个 owner、来源文件全部 164 条记录；隔离验证时来源已增为 165 条，复扫完整文件仍无该来源或机制重复。用仓库 post_id_from_url 归一两种来源路径，均得到 Da5c59STLtg，现有来源 ID/URL 无重复。对完整来源序列化内容检索 normal-map/normal map/normal basis/法线贴图和该 ID 均无已有命中，并审查所有 owner 的机制清单和相关 task_routes。近邻的“法线”主要用于附着/相机/卷曲，不拥有精灵贴图朝向修正。

新入口依据不是多一篇帖子，而是独立任务契约：触发为姿态正常但受光随翻面/旋转错误；输入为颜色/法线配对、编码与坐标空间、渲染路径、有效朝向和灯；每次显示状态把帧/纹理/变换/唯一纠正策略同步送到渲染；失败为反向高光、双纠正、错帧、组合变换失效或跨实例污染。

| 相邻 owner / route | 其任务与输入/状态 | 不同的失败验收 |
| --- | --- | --- |
| gameplay-movement-feedback / movement-feedback | 运动向量、速度、方向区间与方向帧，切换显示姿态 | 斜向错帧、方向边界抖动或停止朝向错误；姿态已经正确时仍可有法线受光错误，不接管贴图空间与渲染器纠正。 |
| gameplay-aim-pose / aim-pose | 真实瞄准、分件、锚点与绘制层级，组织肩/手/枪关系 | 接缝、持握脱节、错层；即使锚点不变，本项仍需要独立光照空间诊断，不将贴图修正混入持握逻辑。 |
| gameplay-facing-relative-light-aim / facing-relative-light-aim | 移动面向、鼠标、允许角域与灯开关，限制灯的方向 | 越界、背后跳变、开关旧状态；本项固定灯也会触发，不能通过改灯方向掩盖表面法线错误。 |
| gameplay-state-driven-surface-motion / state-driven-surface-motion | 权威转速、表面槽与 UV，累积每实例相位 | 皮带不动、错速、串实例或接缝；虽同用材质，任务是动画速度映射而非法线方向空间，不能一并拥有。 |
| gameplay-sheet-curl / sheet-curl | 原始网格、长度轴、阈值与半径，重映射卷曲顶点并更新法线 | 固定边漂移、几何接缝/自穿、形变后着色错误；其几何导数/切线更新仍归形变 owner，本项只处理现成精灵朝向与纹理。 |

五条边界均登记双向 distinct_from 和 related_skills，不迁移现有 owner，不建立 Godot/Unity 或每个方向各一个技能。
