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

## 使用 uv 启动 JupyterLab
1. 在仓库根目录同步依赖：
   ```bash
   uv sync
   ```
2. 在隔离环境中启动 JupyterLab（默认打开当前目录）：
   ```bash
   uv run jupyter lab
   ```
3. 若需指定 lims2_sdk_quickstart 目录，可添加 `--notebook-dir` 参数：
   ```bash
   uv run jupyter lab --notebook-dir lims2_sdk_quickstart
   ```

## 常用命令
- `uv run python main.py`：运行项目的 CLI 入口。
- `uv run pytest`：执行测试套件，可配合 `-k "pattern"` 过滤测试。
- `uv add <package>`：添加依赖并同步更新 `pyproject.toml` 与 `uv.lock`。
