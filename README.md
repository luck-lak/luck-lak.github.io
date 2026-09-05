# Aokun 的个人网站

[在线访问](https://luck-lak.github.io/) · [English](README.en.md)

这里放着我的项目、课程记录和博客。我是南京大学智能科学与技术专业本科生，最近的学习重心从 Web 开发和广泛的技术探索，逐渐转向数据挖掘与机器学习。

网站使用 HTML、CSS 和少量 JavaScript；博客由 Jekyll 生成，部署在 GitHub Pages。保持结构简单，是为了让我能看懂代码，也能自己继续维护。

## 从哪里开始改

| 想修改的内容 | 对应文件 |
| --- | --- |
| 自我介绍、当前方向、项目、学习轨迹、联系方式 | `index.html` |
| 学习记录总入口、未来 Notebook 入口 | `learning-records.html` |
| 页面宽度、文字大小、深色模式、手机布局 | `css/style.css`（各区域有注释） |
| 主题切换和记忆 | `js/main.js` |
| 博客首页简介 | `blog/index.html` |
| 博客文章 | `_posts/` |
| 博客导航、页面框架 | `_includes/`、`_layouts/` |
| 课程列表、课程详情 | 由 `tools/` 中的脚本生成，见下文 |

网站正文以英文介绍为主，课程笔记中英文混合，博客主要用中文。README 以本文件为准：**先改中文版，再同步 `README.en.md`**。GitHub 默认展示本文件。

## 本地预览

在网站根目录运行（需要已安装 Python）：

```powershell
python -m http.server 8000 --bind 127.0.0.1
```

打开 [本地首页](http://127.0.0.1:8000/)。如果电脑上的命令是 `py`，将 `python` 换成 `py`。

这个命令可以预览首页和学习记录，**不会构建 Jekyll 博客**。完整博客以 GitHub Pages 构建结果为准；配置了 Ruby/Jekyll 环境后也可以在本地构建。

## 更新首页

首页各部分都直接写在 `index.html` 中：

- `#about-me`：简短介绍。
- `#current-focus`：当前在学什么，以及下一步的学习计划。
- `#projects`：实际做过的项目。
- `#technical-journey`：简短的 Learning Journey。保留旧锚点名称，兼容已有链接。
- `#learning-records`：课程记录和未来数据 Notebook 的入口。
- `#contact-me`：联系方式。

添加项目时，在 `.project-list` 中复制一个 `<article class="project-card">`，修改标题、真实仓库链接和介绍即可，通常不用改 CSS。

数据 Notebook 仓库尚未放出，入口标记为 **Planned**。有第一批内容后，再把说明替换为实际仓库链接，并更新学习记录总页和 GitHub 个人主页。

文案尽量写清楚做过什么、正在学什么、打算学什么。课程接触不等于项目经验，计划也不当作已经完成的成果。

## 调整排版

`css/style.css` 里可以直接搜索类名和分区注释：

| 样式 | 作用 |
| --- | --- |
| `.home-page` | 首页整体宽度，目前上限 1200px，包含两侧内边距 |
| `#about-me`、`.personal-img` | 自我介绍和图片的两列布局 |
| `.focus-grid`、`.notes-grid` | 学习方向和笔记入口 |
| `.project-list` | 项目卡片网格 |
| `.journey-list` | 学习轨迹列表 |
| `.records-*`、`.record-*` | 课程列表和详情 |
| `.blog-*`、`.post-*` | 博客列表和文章 |
| `body.dark-mode` | 深色模式 |
| `@media` | 窄屏布局与减少动画的设置 |

导航使用 `position: sticky`，会占据正常页面空间。调整导航时，不需要给正文猜一个固定的顶部高度。首页可以宽一些，长篇博客仍保留较窄的阅读宽度。

修改后检查桌面 100% 缩放、手机宽度、深浅主题，以及导航跳转。

## 维护学习记录

`learning-records.html` 是手动维护的总入口；`learning/` 是按平台分类的列表页；`records/` 是课程或论文详情。

| 平台 | 生成脚本 | 原始笔记 |
| --- | --- | --- |
| DeepLearning.AI | `tools/build_learning_records.py` | 根目录的 `学习探索记录.docx` |
| Codecademy | `tools/build_codecademy_records.py` | 网站文件夹同级的 `codecademy/` |

正常更新时，先改原始笔记或生成脚本，再生成页面。直接改生成的 HTML，下一次重建时会被覆盖。原始文字、截图顺序和链接应保留；网站导语与导航在生成模板中维护。

Codecademy 的 `PLATFORM_INTRO` 是列表页导语，`PLATFORM_PREFACE` 保存原有的个人序言。新增课程时：

1. 把笔记放到同级 `codecademy/` 中。
2. 在脚本的 `RECORDS` 里添加 `file`、`title`、`slug`、`kind`；不同笔记格式参照已有条目。
3. 在 `assets/records/thumbnails/codecademy/` 添加对应编号的 SVG 封面。
4. 运行脚本，再检查列表、详情、上一条/下一条链接。
5. 手动更新 `learning-records.html` 中的平台记录数。

```powershell
python -m pip install python-docx Pillow
python tools/build_codecademy_records.py
# 更新 DeepLearning.AI 原始笔记时运行：
python tools/build_learning_records.py
```

如果网站仓库与 Codecademy 笔记目录不在同一级，可在运行生成器的终端中设置 `CODECADEMY_NOTES_DIR`，无需修改或硬编码脚本路径：

```powershell
$env:CODECADEMY_NOTES_DIR = "<Codecademy 笔记目录>"
python tools/build_codecademy_records.py
```

DeepLearning.AI 的封面在 `assets/records/thumbnails/`，按记录编号命名；特殊扩展名在脚本的 `RECORD_COVER_EXTENSIONS` 中配置。此平台提供原始 DOCX 下载；Codecademy 页面不提供 DOCX 下载。

`inspect_docx.py` 和 `list_record_links.py` 是检查用的小工具，不参与网页运行。

## 写博客

在 `_posts/` 新建 `YYYY-MM-DD-post-slug.md`：

```markdown
---
layout: post
title: "一次数据分析练习"
lang: zh
date: 2026-09-05 12:00:00 +0800
description: "这次练习的问题、过程和收获。"
---

正文从这里开始。
```

发布后的地址是 `/blog/post-slug/`。未来日期的文章默认暂不展示。

图片放在 `assets/images/blog/post-slug/`，正文中使用 `/assets/images/blog/post-slug/image.png`。可在文章头部加上 `cover` 和 `cover_alt` 来显示列表封面：

```yaml
cover: "/assets/images/blog/post-slug/cover.jpg"
cover_alt: "图片内容说明"
```

博客导航来自 `_includes/site-header.html`。首页与学习记录使用普通 HTML，相关导航变更需要同步到页面或生成脚本。

## 发布与两个仓库

提交并推送到网站仓库的 `main` 后，GitHub Pages 会运行 Jekyll。到仓库 Actions 查看构建结果，再检查线上页面。静态 HTML 页面会原样复制；博客模板和文章会经过处理。

`_config.yml` 排除生成工具与两份 README，但保留页面实际链接到的 DOCX 下载文件。

| 仓库 | 用途 |
| --- | --- |
| [luck-lak.github.io](https://github.com/luck-lak/luck-lak.github.io) | 网站源码；本 README 说明如何维护网站 |
| [luck-lak](https://github.com/luck-lak/luck-lak) | GitHub 个人主页 README；介绍个人近况和项目 |

学习方向变化时，检查首页、学习记录导语和个人主页 README 是否一致。两份网站 README 的维护说明也应同步更新。
