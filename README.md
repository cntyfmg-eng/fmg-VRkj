# VR场景互动课件生成器

输入语文课文的教案+教材+生图提示词，自动生成适合 VR 场景的 6 张方位图（自动用内置图片生成 / 或进入 gemini.google.com/app 手动生成），并复用 Three.js 全景课件框架产出可离线运行的 VR 互动教学课件（支持场景缩放进入切换 + 滚轮镜头拉远拉近）。

一个 WorkBuddy Skill，把可复用的工作流固化下来，供随时调用。

## 文件结构

```
fmg-VRkj/
├── SKILL.md            # Skill 定义(入口, 含 front matter)
├── icon.png            # 图标
├── references/         # 参考模板 / 资料 / 数据
├── scripts/            # 自动化脚本(若有)
├── README.md
├── LICENSE
└── .gitignore
```

## 安装

将本仓库内容放入 WorkBuddy 的 skills 目录(`~/.workbuddy/skills/fmg-VRkj/`), 重启或刷新即可。

## License

MIT © cntyfmg-eng
