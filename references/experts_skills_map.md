# 专家 / 技能映射表

| 生成环节 | 专家（Expert） | 技能（Skill） | 工具 / 接口 | 备注 |
|---|---|---|---|---|
| 课文定位·教学设计总调度 | 企鹅教师助手（teaching-design-expert） | — | — | 识别域、路由到下层技能 |
| 写规范教案 | — | **teacher-lesson-plan** | docx 生成 | 目标/重难点/过程/板书/分层作业 |
| 互动课件结构·提问链 | — | **interactive-courseware-designer** | — | 互动点、ABT 叙事、评估 |
| VR 场景图·自动生成 | — | 内置 **ImageGen** 工具 | WorkBuddy 图片生成 | 每张 5–10 credits |
| VR 场景图·AI Hive 生成 | — | **nano-banana** | AI Hive OpenAPI（`public_model_nano_banana_2`） | 需 `sk-api-*` Key |
| VR 场景图·Gemini 网页生成 | — | 打开 gemini.google.com/app | 手动粘贴提示词 | 备选，见 VR生图提示词.md |
| VR 场景图·Gemini API 生成 | — | 本技能 `gen_gemini_vr.py` | Google Generative Language API | 需 `GEMINI_API_KEY` |
| 3D 全景 VR 框架 | — | **threejs-3d-scene** | Three.js（r128 圆柱全景） | 模板在 assets/template.html |
| 注入打包 | — | 本技能 `inject.py` | Python 标准库 + Pillow | 产出单文件 HTML |

## 使用边界
- 本技能固定 **6 个场景顺序**（长廊→万寿山脚下→万寿山→昆明湖→十七孔桥→石舫），对应《颐和园》课文；换课文需同步改写 `template.html` 里的 `SCENES` 数据与提示词。
- 自动生成图无法保证严格 360° 等距全景；要做可环视全景，请走选项 2 并加 `equirectangular` 前缀。
- 二维码（gate-qr.jpg）与背景音乐（1.mp3）为可选附属文件，缺失时课件仍能正常运行（二维码弹窗显示空白、音乐按钮提示未找到）。
