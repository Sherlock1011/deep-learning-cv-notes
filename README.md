# 深度学习 / CV / NLP / Agent 浏览器讲义

这是一个基于 [AccumulateMore/CV](https://github.com/AccumulateMore/CV) 学习资料整理出的浏览器阅读版讲义项目。原仓库提供了 PyTorch、深度学习、计算机视觉、NLP、Transformer、BERT 和大模型 Agent/RAG 相关的 Jupyter Notebook 笔记；本项目在此基础上做了学习路径重组、章节化阅读入口和 HTML 化排版，方便直接在浏览器中阅读。

> 说明：本项目为学习资料整理与阅读体验优化项目，内容来源请以原始仓库 [AccumulateMore/CV](https://github.com/AccumulateMore/CV) 为准。若继续学习和运行代码，建议同时查看原始 `.ipynb` 笔记。

## 项目来源

- 原始仓库：[AccumulateMore/CV](https://github.com/AccumulateMore/CV)
- 原始资料类型：Jupyter Notebook
- 原始课程覆盖：
  - 土堆 PyTorch 入门，对应笔记 `100-122`
  - 李沐《动手学深度学习》，对应笔记 `200-268`
  - 吴恩达深度学习专项课程，对应笔记 `300-354`
  - 大模型 Agent / RAG / API，对应笔记 `400-409`
- 本项目整理方式：
  - 将 notebook 转换为可直接打开的 HTML 页面
  - 按学习难度重组为章节讲义
  - 补充学习路径、阶段目标和 12 周学习计划
  - 对步骤说明、标题、图片、代码块做阅读排版优化

## 主要界面

### 1. 讲义首页

入口文件：[`index.html`](./index.html)

首页包含：

- 课程视频入口
- 数据集入口
- 10 章学习路径
- 每章学习目标
- 每章对应的原始 notebook 范围
- 每章对应的视频课程链接
- 学习路径流程图
- 12 周学习计划

### 2. Notebook 阅读页

目录：[`notebooks/`](./notebooks/)

每个 notebook 都被转换为一个独立 HTML 页面，例如：

- [`notebooks/100_配置版本.html`](./notebooks/100_配置版本.html)
- [`notebooks/101_Pytorch安装.html`](./notebooks/101_Pytorch安装.html)
- [`notebooks/263_Transformer.html`](./notebooks/263_Transformer.html)
- [`notebooks/405_使用LangChain构建RAG.html`](./notebooks/405_使用LangChain构建RAG.html)

阅读页功能：

- 顶部返回讲义目录
- 顶部跳转原始 notebook 仓库
- 自动识别章节标题
- 自动识别 `①②③...` 形式的步骤说明
- 将 notebook 内嵌图片转换为浏览器可显示图片
- 优化代码块、命令文本、截图和正文间距

### 3. 转换脚本

脚本文件：[`render_notebooks.py`](./render_notebooks.py)

该脚本用于从本地原始 notebook 重新生成 HTML 阅读页。它会处理：

- Markdown 渲染
- 代码块渲染
- notebook 图片附件转换
- 步骤卡片排版
- 页面顶部导航

如果你只想浏览讲义，不需要运行该脚本。

## 项目结构

```text
.
├── README.md
├── index.html
├── render_notebooks.py
└── notebooks/
    ├── 100_配置版本.html
    ├── 101_Pytorch安装.html
    ├── ...
    └── 409_多轮对话.html
```

## 本地预览

直接用浏览器打开：

```text
index.html
```

也可以使用一个简单的静态服务器：

```bash
python -m http.server 8000
```

然后访问：

```text
http://localhost:8000
```

## GitHub Pages 部署方式

### 方式一：通过 GitHub Pages 设置部署

1. 将本项目推送到 GitHub 仓库。
2. 打开仓库的 `Settings`。
3. 进入 `Pages`。
4. 在 `Build and deployment` 中选择：
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/ (root)`
5. 保存后等待 GitHub Pages 构建完成。
6. 访问 GitHub 生成的 Pages 地址。

### 方式二：本地直接部署到任意静态托管

本项目是纯静态文件，可以部署到：

- GitHub Pages
- Vercel
- Netlify
- Cloudflare Pages
- 任意支持静态 HTML 的服务器

部署时只需要上传整个项目目录即可。

## 注意事项

- `notebooks/` 目录中的 HTML 页面包含 notebook 原图的内嵌数据，因此文件体积会比普通 HTML 大。
- 本项目不包含原始 `.ipynb` 文件；如需运行代码，请前往 [AccumulateMore/CV](https://github.com/AccumulateMore/CV) 下载原始 notebook。
- 原仓库 README 中 `400-409` 大模型 Agent 部分没有提供具体视频 URL，因此本项目中对应章节标注为“原仓库未提供具体链接”。

## 致谢

感谢 [AccumulateMore/CV](https://github.com/AccumulateMore/CV) 原作者整理并公开深度学习相关学习资料。本项目仅在其基础上做浏览器阅读版整理、学习路径组织和排版优化。
