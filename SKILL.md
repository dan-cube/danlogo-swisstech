---
name: danlogo-swisstech
description: >-
  DanLogo · Swiss Tech 静几何：以字为标——中英文字形从零构造到可以当图形看，再从字标里取一处或几处组合、改造成符号（字成一体，取字成符）；
  修正几何（圆与方之间的曲线）、模数与基准、大静小响的色彩分离、墨阱式的修正细节，带来现代、潮流、科技的气质。
  按九个阶段推进：简报 → 概念（每轮 5 套）→ 原型（每个概念 ≥3 套）→ 图形精修 → 定稿（定制字 + 配色）→ 体系 → 场景 → 提案 → 总结。
  Use this skill when the user wants to design, redesign, refine, extend or present a logo, wordmark, 标志, 字标, 中英文组合标,
  品牌视觉, VI or brand identity led by custom lettering in a Swiss / rational / precise spirit — 字体设计, 定制字体, 字标设计, 字母标,
  瑞士风格, 理性, 精密, 科技感, 潮流, 硅谷大厂气质, custom type, logotype, lettermark, Swiss style, modular, superellipse — when they name danlogo-swisstech,
  or when they continue a project whose decisions.md names it. For a logo request that names no style, use it unless another
  installed danlogo style fits better; if several danlogo styles are installed, ask the user which one first.
---

# DanLogo · Swiss Tech 静几何

> 字是图形，取字成符；安静、准确，像一句话说到最后一个字。

danlogo 系列的静几何方向，一种**以字为标**的风格：中英文字形从零构造，整个词被当作一个图形经营；图标从字标里取一处或几处组合、改造而成。它锁定的是形式语言——构造字、修正几何、模数与基准、大静小响的色彩分离、修正即性格——不规定用哪几个字母、怎么组合、什么颜色，也不限行业。思想来自包豪斯的构造字、具体诗、瑞士国际主义、现代主义经典字标、字体的视觉修正与参数化，以及功能主义产品的信号色。它从 EonPoint「首尾」方案反向拆解而来（`cases/`），但每个新品牌都要从自己的名字里找到新的做法。

## 先读

开始任何项目之前，按顺序读完前三章风格章；第四章到第 6 阶段再读：

1. `references/philosophy.md` —— 思想坐标：为什么这样设计
2. `references/style-dna.md` —— 风格基因、旋钮与试金石：看起来是什么气质
3. `references/creative-methods.md` —— 创意方法与防同质化：每次怎么想出新的
4. `references/style-extension.md` —— 风格延展：体系、场景、提案长什么样（第 6–8 阶段）

`references/exemplars.md`（参照作品）和 `cases/index.md`（已用过的组合与旋钮）**等第 2 阶段列完组合候选再读**，用它们划掉惯性答案和撞题的母题——先读会被它们带着走。完整案例只在需要参照“做到什么程度”时读，并且只借方法、不借形式。其余文件在对应阶段读（见下表）。

## 三层要求

| 层 | 内容 | 能否改变 |
|---|---|---|
| 质量关卡（系列共用） | `references/quality-gates.md`；“首先是图形”一关按本风格的“字形图形化”标准判断（`style-dna.md`） | 每个项目都必须通过 |
| 风格基因（本风格） | `style-dna.md` + `philosophy.md` 的自检 | 默认遵守；用户明确要求调整时照做，并记入 decisions.md |
| 创意自由区 | 取哪几处、怎么组合、大小写、方度、字重字宽、签名修正、信号色、材料 | 每个项目重新推导；至少两个“旋钮”与所有已有案例明显不同 |

三句提醒：
- **以字为标，字要成图形。** 选用本风格即视为用户明确要求以字为标（共用章的替换见下节，记入 decisions.md）。字标要读成一个被设计的形，符号要是一块有分量、能独立成物的面；判断用 `style-dna.md` 的“字形图形化四问”。不要把字拆成几根线。
- **按气质判断，不按元素判断。** 案例里的具体形状、颜色、字形都是那个品牌的答案，不是本风格的规定。
- **符号从字里来。** 本风格最容易被误解成“选一款好看的字体，首字母放进方块”。字要从零构造，符号要由字标里的元素组合或改造而成（几处元素组合，或一个字形切开改造），被点亮的正是取用的地方；其中的关系由规则算出。

## 本风格对共用章的替换

共用五章按图形标志写成。本风格以字为标，下面几条按右栏执行，其余照共用章：

| 共用章的说法 | 本风格 |
|---|---|
| 标志首先是图形；默认不做字形标志（`quality-gates.md`、`craft.md`） | 字标与符号都要过“字形图形化四问”（`style-dna.md`），同样严 |
| 辨识度清单要与字母、数字、标点区分（`quality-gates.md`） | 字母可以认得出，但不能像常见字体打出的字或现成的字母组合 |
| 图形不要向字借结构（`craft.md`） | 符号正是向字借结构：取字成符 |
| 整个字标只有一处与众不同的细节（`craft.md`） | 同样只留一处签名；组合、信号、签名尽量落在同一处，中文里重现同一个签名仍算一处 |
| 主体叫“图形”，不叫“符号” | 本风格的“符号”就是图形标志（图标），同样要有面、能独立成物 |
| 每轮来自字形的概念最多 1 个（`workflow.md` 第 2 阶段） | 每个概念都来自名字的字形；10 个以上候选覆盖至少三类素材；5 张卡至少三种组合方式、同一种最多两张 |
| 第 3 阶段先只做图形，不做字；定制字在第 5 阶段 | 第 3 阶段先定字的语法，画关键字母、中文关键字与符号；第 4 阶段完成英文与中文字标；第 5 阶段推到 a–z 与完整中文，定配色 |
| 原型至少两种外轮廓、不能是母题的直接图解 | 同一概念的 ≥3 个原型在具体做法上不同（位置、比例、关系、切法、粗细），不必换组合方式，也不为凑外轮廓做弱原型；“直接图解”指常规字体打出的字、首字母放进方块 |
| 换名测试 | 换一个名字，这个组合和它的关系还成立吗？单个字母的变形要靠一条关系或名字的意思绑定这个名字；任何同字母的品牌都能照搬的，换掉 |
| 只做名字里用到的字母 | 第 5 阶段推到 a–z 与中文字标，证明是一套字 |

用户授权 AI 代为选择、锁定时，照流程往下走，每个代定的决定在 decisions.md 标【AI 代定】，等用户回来复核；问不到的事项（例如有没有同期项目）记【假设】。

## 九个阶段

细则、编号规则、出口条件见 `references/workflow.md`。每个阶段都以用户的明确确认结束；用户可以随时回退、增加、修改、合并。

| 阶段 | 做什么 | 每轮产出 | 读 |
|---|---|---|---|
| 1 简报 | 用户提供信息；AI 一次性追问缺口（≤10 问） | 简报卡 | `workflow.md` |
| 2 概念 | 读名字的字形与意思，找组合 | **5 张概念卡**（每张一种组合），可改、可加、可合并 | `creative-methods.md`、`philosophy.md`、`workflow.md`、`quality-gates.md` |
| 3 原型 | 每个锁定概念：先定字的语法，画关键字母、中文关键字与符号；黑白为主，附双色版（中性 + 暂定信号色） | **每个概念 ≥3 个原型** + 初步查重（含现成字母组合） | `style-dna.md`、`craft.md`、`quality-gates.md` |
| 4 图形 | 精修符号与完整的英文、中文字标：构造规则、视觉修正、小尺寸版（字标按实际高度测）、构造图 | 精修的字标与符号 | `craft.md`、`quality-gates.md`、`style-dna.md` |
| 5 定稿 | 语法推到 a–z 与完整中文；配色 | 每套字标 2–3 套配色 + 完整查重 | `craft.md`、`style-dna.md` |
| 6 体系 | 组合、变色、留白、最小尺寸、错误用法、动态 | SVG / PNG 全套 | `deliverables.md`、`style-extension.md` |
| 7 场景 | 按行业选 6–10 个场景 | 场景示意 | `deliverables.md`、`style-extension.md` |
| 8 提案 | 提报文档 + 演讲备注 + 源文件包 + 查重复查 | 提案 | `deliverables.md`、`style-extension.md`、`adapters/` |
| 9 总结 | 主动询问是否用这个项目优化 skill | 修改建议，用户批准后写入 | `workflow.md` 第 9 节 |

## 贯穿全程

- **项目存档**：每个项目一个文件夹和一份 `decisions.md`（第一行写 `skill: danlogo-swisstech v<版本>`），记录每轮展示了什么、用户原话、锁定和否定了什么。接手已有项目先读它。
- **结构先行**：第 5 阶段之前以黑白审结构。本风格声明**色彩参与结构**：第 3 阶段起每个黑白原型旁附一版双色版（中性色 + 一个标“暂定”的信号色），只把被组合的那几处标出；黑白版仍要靠形与纯度保住它们。
- **先算后画**：先写基准、方度、端头与刀口参数，再生成字；组合的关系由规则推出。
- **字要成套**：不只画名字里的字母；第 5 阶段把规则推到 a–z 与中文字标，确认是一家人。
- **被否就退回，不加东西**：换母题或换原型，不在原图上加装饰。
- **查重三次**：原型初查、定稿全查、提案前复查（`quality-gates.md`）；同时查“行业头部品牌的颜色 + 首字母”这类组合。
- **亲眼看渲染图**：判断好不好看，一律基于渲染出的图片，包括 16 px 小图。
- **沟通**：用用户的语言。每轮先一句话说做了什么，再编号列方案和一句话理念，给一个推荐和理由，问锁定、修改还是继续。简短反馈先查 `references/feedback-playbook.md`。
- **客户资料只放在项目文件夹里**，不写进 skill。

## 多个 danlogo 风格并存时

用户点名了某个风格，就用那个 skill。项目的 `decisions.md` 写了用哪个 skill，就沿用。都没有指定、又装了多个 danlogo 风格时，先列出已安装的风格，请用户选，再开始。

## 工具与文件

- `scripts/`：通用工具——几何与 SVG 生成（`geom.py`）、多图对比审看图（`sheet.py`）、图形感与辨识度审看板（`review.py`）、SVG 转 PNG（`render.sh`）、场景示意（`mockup.py`）。说明见 `scripts/README.md`。使用时复制到项目的 `src/`。
- `examples/eonpoint-shouwei/src/`：案例的完整生成代码（字母表、中文字标、体系与场景图）。**从零造字用它的工具链**：`setup.sh` 装好超椭圆、布尔运算与不裁切的渲染（`geo.py`、`render.mjs`）。学它的工程写法，不要复用它的造型和字形。
- `adapters/for-claude.md`、`adapters/for-codex.md`：不同 AI 工具在看图、做演示文稿、预览网页上的差异。
- `PROMPT-CARD.md`：没有安装 skill 时，贴给任何 AI 的风格提示词卡。
- `evals/briefs.md`：用于检验本 skill 不会把所有品牌做成同一个样子的测试简报。

`references/` 中带 `danlogo-core` 标记的五个文件（workflow、quality-gates、craft、deliverables、feedback-playbook）是 danlogo 系列共用章节，所有风格保持一致；本风格专属的是 philosophy、style-dna、creative-methods、style-extension 四章：前三章管标志本身，第四章管体系、场景和提案的审美，让整套设计和标志出自同一种气质。
