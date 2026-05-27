# Jupyter Work

Plotly/Cytoscape 图表生成、预览与上传工作区。

## 前置条件

安装 [uv](https://docs.astral.sh/uv/getting-started/installation/)（Python 包管理器）。

## 项目结构

```
plotly_quickstart/          # Plotly/Cytoscape 图表生成、预览与上传
  plotly_python.ipynb       # Python 生成 Plotly JSON + SDK 上传
  plotly_r.ipynb            # R (ggplot2) 生成 Plotly JSON
  thumbnail.ipynb           # 从 Plotly JSON 生成缩略图
  plotly_viewer_v2.html     # 图表查看器（支持拖拽）
  lims2_sdk.md              # lims2-sdk 完整文档
```

## 使用 uv 启动 JupyterLab
1. 在仓库根目录同步依赖：
   ```bash
   uv sync
   ```
2. 启动 JupyterLab：
   ```bash
   uv run jupyter lab
   ```

## 常用命令
- `uv add <package>`：添加依赖并同步更新 `pyproject.toml` 与 `uv.lock`。
