# fmg-VRkj 工作流程详解

本技能把「语文课文 → VR 互动教学课件」的完整链路固化为三步。每一步都精确对应一个专家 / 技能，便于追溯与二次改造。

## 前置输入
- **教案**：docx / 含教学目标、教学重难点、教学过程的规范教案（对应课文的一篇写景/游记类课文）
- **教材**：课文原文 + 教材页图片（用于核对生字词、段落、课后题）
- **提示词**：6 个方位的生图提示词（本技能附 `assets/VR生图提示词.md` 模板，可据课文改写）

---

## 阶段一：备课文案（专家/技能：教学设计）

| 环节 | 对应能力 | 产出 |
|---|---|---|
| 确定课文、学段、课时 | **企鹅教师助手** 专家 / 教学设计专家（teaching-design-expert） | 课文定位 |
| 写规范教案（目标·重难点·过程·板书·分层作业） | **teacher-lesson-plan** 技能 | 教案 docx |
| 设计互动课件结构（互动点·提问链） | **interactive-courseware-designer** 技能 | 课件脚本 |

> 本阶段产出的「教案 + 互动点」直接决定阶段三 VR 课件里 **12 个教学热点** 的内容（选择题/比喻配对/小导游任务等）。

## 阶段二：生成 VR 场景图（专家/技能：图片生成）

依据提示词生成 **6 张不同方位、适合 VR 场景底图** 的图片。提供两种选择：

### 选项 1 · 自动生成（推荐，最快）
- 调用 **WorkBuddy 内置 ImageGen 工具**（每张约 5–10 credits）。
- 直接把 `assets/VR生图提示词.md` 中的 6 条提示词逐条送入 ImageGen，生成 6 张 1536×1024 写实图。
- 也可用 **nano-banana** 技能（需 AI Hive 的 `sk-api-*` Key，模型 `public_model_nano_banana_2`）。
- 生成后按顺序命名为 `01.jpg … 06.jpg`（或 `01_场景名.jpg … 06_场景名.jpg`），放入 `VR场景/` 文件夹。

### 选项 2 · 进入 gemini.google.com/app 单独生成
- 打开 https://gemini.google.com/app ，把 `assets/VR生图提示词.md` 的 6 条提示词（建议用英文版）逐条粘贴生成。
- 想做真正 360° 等距全景，可在提示词最前加前缀：
  `360-degree equirectangular panorama, 2:1 aspect ratio, seamless wrap, immersive VR scene,`
- 下载 6 张图，同样命名 `01.jpg … 06.jpg` 放入 `VR场景/`。
- （备选）若你有 Google AI Studio Key，可用 `assets/gen_gemini_vr.py` 一键批量出图：
  `set GEMINI_API_KEY=sk-xxx && python gen_gemini_vr.py`

> 阶段二产出 = `VR场景/01.jpg … 06.jpg`，顺序须与技能固定场景顺序一致：
> ①长廊 ②万寿山脚下 ③万寿山(俯瞰) ④昆明湖 ⑤十七孔桥(石狮) ⑥石舫

## 阶段三：生成 VR 互动课件（专家/技能：Three.js 3D 场景）

| 环节 | 对应能力 | 说明 |
|---|---|---|
| 3D 全景 VR 框架 | **threejs-3d-scene** 技能（Three.js r128 圆柱全景） | `assets/template.html` |
| 注入打包 | 本技能 `assets/inject.py` | three.js + 6 图 + 二维码 → 单文件 HTML |

执行：
```bash
cd 项目目录
python fmg-VRkj/assets/inject.py --img-dir VR场景 --out 第18课颐和园VR互动课件.html
```
可选参数：`--qr gate-qr.jpg` `--mp3 1.mp3` `--lecturer "授课人：XXX"` `--title "..."`

> 成品为 **单文件、可离线、双击即用** 的 HTML：Three.js 内联、图片 base64 内嵌、课堂互动 + 路线跳转 + 印章系统全部可用。

---

## 成品能力清单
- 拖拽鼠标/触屏环视（Three.js 圆柱全景，阻尼惯性）
- 6 个场景相互跳转：画面绿色箭头 + 底部 6 站路线导航 + 拖到边缘快捷箭头
- 12 个教学热点（选择题 / 比喻句配对 / 小导游任务），均带课文原句与 👩‍🏫 教师提示
- 集满 12 枚游园印章 → “游园小达人”徽章（localStorage 持久化）
- 首页可编辑署名、右上角「更多资源」二维码、背景音乐开关
