---
name: fmg-VRkj
version: 1.2.0
displayName: VR场景互动课件生成器
description: 输入语文课文的教案+教材+生图提示词，自动生成适合 VR 场景的 6 张方位图（自动用内置图片生成 / 或进入 gemini.google.com/app 手动生成），并复用 Three.js 全景课件框架产出可离线运行的 VR 互动教学课件（支持场景缩放进入切换 + 滚轮镜头拉远拉近）。
metadata:
  author: 冯萌刚
  tags: [语文, 教学课件, VR, Three.js, 互动课件, 数智化教学]
---

# fmg-VRkj · VR场景互动课件生成器

把「语文课文 → VR 全景互动教学课件」的全流程固化为一键技能，完全复用已验证的课件框架。

## 更新记录
- **v1.2.0**（2026-09-27）：在「操作说明」（游园须知）新增一条音乐播放提示——准备好的音乐文件改名为 1.mp3 并与课件放在同一文件夹即可正常播放。
- **v1.1.0**（2026-09-26）：① 场景切换由「淡入淡出」改为「缩放进入」（旧场景缩小淡出 + 新场景由小放大淡入）；② 新增鼠标滚轮「镜头拉远拉近」缩放，每个场景独立记忆远近；③ 同步更新首页游园须知文案。

## 触发场景
- 老师备好一篇写景/游记类课文（如《颐和园》）的教案、教材页，想把它做成 **可拖拽环视、场景互链、师生互动** 的 VR 课堂课件。
- 需要自动产出一批「不同方位、适合 VR 场景」的图片，并据此拼装单文件互动课件。

## 输入
- **教案**：规范教案 docx（决定 12 个教学热点的内容）
- **教材**：课文原文 + 教材页图片（核对生字词、段落、课后题）
- **提示词**：6 个方位的生图提示词（技能已附模板 `assets/VR生图提示词.md`，可据课文改写）

## 三步流程（每步精确对应专家/技能）

### 步骤 1 · 备课文案
- 专家：**企鹅教师助手**（教学设计专家）
- 技能：**teacher-lesson-plan**（写教案）、**interactive-courseware-designer**（设计互动点/提问链）
- 产出：教案 docx + 课件脚本 → 决定阶段三的 12 个教学热点。

### 步骤 2 · 生成 VR 场景图（二选一）
- **选项 A 自动生成**：调用 **内置 ImageGen** 工具（或 **nano-banana** 技能，需 AI Hive Key），把 `assets/VR生图提示词.md` 的 6 条提示词逐条出图，存为 `VR场景/01.jpg … 06.jpg`。
- **选项 B gemini.google.com/app 手动生成**：打开 https://gemini.google.com/app ，逐条粘贴提示词（想做 360° 全景请加 `equirectangular` 前缀），下载 6 张图同样命名放入 `VR场景/`。
  - 备选：有 `GEMINI_API_KEY` 时用 `assets/gen_gemini_vr.py` 一键批量出图。
- 场景顺序固定：①长廊 ②万寿山脚下 ③万寿山(俯瞰) ④昆明湖 ⑤十七孔桥(石狮) ⑥石舫。

### 步骤 3 · 生成 VR 互动课件
- 专家/技能：**threejs-3d-scene**（Three.js r128 圆柱全景），框架在 `assets/template.html`
- 打包：本技能 `assets/inject.py` 把 three.js + 6 图 + 二维码注入模板，产出单文件 HTML

```bash
python fmg-VRkj/assets/inject.py --img-dir VR场景 --out 第18课颐和园VR互动课件.html
# 可选：--qr gate-qr.jpg  --mp3 1.mp3  --lecturer "授课人：XXX"  --title "..."
```

成品能力：拖拽环视（阻尼惯性）、6 场景互链（画面箭头 + 底部路线 + 边缘快捷箭头）、12 个教学热点（选择题/比喻配对/小导游，含课文原句与教师提示）、集章徽章系统、可编辑署名、二维码、背景音乐开关。

## 目录结构
```
fmg-VRkj/
├─ SKILL.md
├─ assets/
│  ├─ template.html        # VR 课件框架（含占位符 __THREE_JS__ / __IMG_s1__..6__ / __IMG_QR__）
│  ├─ three.min.js         # Three.js r128（内联用）
│  ├─ inject.py            # 注入打包脚本（可配置）
│  ├─ gen_gemini_vr.py     # Gemini API 自动出图（备选）
│  └─ VR生图提示词.md       # 6 方位生图提示词模板
└─ references/
   ├─ workflow.md          # 详细三步流程
   └─ experts_skills_map.md # 每环节对应的专家/技能映射
```

## 使用边界
- 固定 6 场景顺序对应《颐和园》；换课文需同步改写 `template.html` 的 `SCENES` 与提示词。
- 自动生成图非严格 360° 全景；需真环视请走选项 B 加 `equirectangular` 前缀。
- 二维码 / 背景音乐为可选附属文件，缺失不影响主流程。
