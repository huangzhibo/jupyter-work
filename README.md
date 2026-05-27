# Jupyter Work

## 安装 uv
### macOS
- 使用 Homebrew：
  ```bash
  brew install uv
  ```
- 如果未安装 Homebrew，可使用官方安装脚本：
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### Windows
- 通过 Winget 安装（需 Windows 10/11 并启用 Winget）：
  ```powershell
  winget install astral-sh.uv
  ```
- 若无法使用 Winget，可在 PowerShell（管理员）中运行安装脚本：
  ```powershell
  powershell -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"
  ```

### Linux
- 大多数发行版可直接使用官方脚本安装：
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- 安装后将提示将 `~/.local/bin` 加入 `PATH`，按提示更新 shell 配置即可。

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
