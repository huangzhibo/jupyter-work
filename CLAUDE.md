# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Jupyter notebook 工作区，用于 Plotly/Cytoscape 图表生成、预览与通过 lims2-sdk 上传到生信云平台。

## Commands

```bash
uv sync                     # 安装/同步依赖
uv run jupyter lab          # 启动 JupyterLab
uv add <package>            # 添加依赖
```

## Architecture

- `plotly_quickstart/` — 所有 notebook、工具脚本和样例数据的单一目录
  - `plotly_python.ipynb` — Python 生成 Plotly JSON，末尾演示 lims2-sdk 上传
  - `plotly_r.ipynb` — R (ggplot2) 生成 Plotly JSON
  - `thumbnail.ipynb` — 从 Plotly JSON 生成缩略图（Kaleido + PIL）
  - `plotly_viewer_v2.html` — 独立 HTML 图表查看器（Plotly + Cytoscape，支持拖拽）
  - `PPINetwork.py` — PPI 网络 Cytoscape JSON 生成脚本
  - `lims2_sdk.md` — lims2-sdk CLI 和 Python API 文档

## Key Conventions

- **nbstripout** 已通过 `.gitattributes` 配置为 git filter，notebook 的 output 在 commit 时自动剥离，无需手动清理。
- 生成文件（`*.pdf`、`*.ipynb.html`）和大数据文件已在 `.gitignore` 中忽略，不要提交。
- Notebook 中不要硬编码 API token，使用环境变量 `LIMS2_API_TOKEN`。
- Python 3.13，依赖管理用 uv（不用 pip）。
