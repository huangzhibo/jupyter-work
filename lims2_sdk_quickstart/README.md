# Lims2 SDK

[![Version](https://img.shields.io/badge/version-0.4.4-blue.svg)](https://github.com/huangzhibo/lims2-sdk)
[![Python](https://img.shields.io/badge/python-≥3.9-green.svg)](https://www.python.org/)

生信云平台 Python SDK，提供图表上传和文件存储功能。

**当前版本**: v0.4.4

## 功能特性

- **图表服务**：支持 Plotly、Cytoscape、图片、PDF 格式上传
- **文件存储**：通过 STS 凭证上传文件到阿里云 OSS，支持断点续传
- **命令行工具**：提供便捷的 CLI 命令
- **精度控制**：使用 decimal 库精确四舍五入，默认保留3位小数，减少 JSON 文件大小（可减少 15-60%）
- **连接优化**：自动重试机制处理网络不稳定问题，适合批量上传场景

## 安装配置

### 推荐方式：从 PyPI 安装
```bash
pip install lims2-sdk
```

### 设置环境变量：

```bash
export LIMS2_API_URL="your-api"
export LIMS2_API_TOKEN="your-api-token"
```

## 命令行使用

### 📖 获取帮助信息

```bash
# 查看所有可用命令
lims2 --help

# 查看图表上传帮助
lims2 chart --help
lims2 chart upload --help

# 查看存储服务帮助
lims2 storage --help
lims2 storage upload --help
lims2 storage upload-dir --help

# 查看文件操作帮助
lims2 storage exists --help
lims2 storage info --help
```

### 图表上传
```bash
# 上传图表文件（完整参数示例）
lims2 chart upload plot.json -p proj_001 -n "基因表达分析" -s sample_001 -t heatmap -d "差异表达热图" -c A_vs_B -a Expression_statistics --precision 3
```

### 文件存储
```bash
# 上传单个文件（简化）
lims2 storage upload results.csv -p proj_001

# 上传到指定路径
lims2 storage upload results.csv -p proj_001 --base-path analysis

# 上传目录（简化）
lims2 storage upload-dir output/ -p proj_001

# 上传目录到指定路径
lims2 storage upload-dir output/ -p proj_001 --base-path analysis
```

## Python SDK 使用
** 多个图表上传，推荐使用该方法，可复用链接池 **

### 推荐使用方式（v0.4.1+）

```python
from lims2 import Lims2Client

# 初始化客户端（推荐复用，避免重复创建连接）
client = Lims2Client()

# 批量上传时复用同一个客户端实例
charts = ["plot1.json", "plot2.json", "plot3.json"]
for chart_file in charts:
    client.chart.upload(
        data_source=chart_file,
        project_id="proj_001",
        chart_name=f"图表_{chart_file}",
        analysis_node="Expression_statistics",
        precision=3
    )
```

### 完整参数示例

```python
# 上传图表（完整参数示例）
client.chart.upload(
    data_source="plot.json",        # 图表数据源：字典、文件路径或 Path 对象
    project_id="proj_001",          # 项目 ID（必需）
    chart_name="基因表达分析",        # 图表名称（必需）
    sample_id="sample_001",         # 样本 ID（可选）
    chart_type="heatmap",           # 图表类型（可选）
    description="差异表达基因热图",   # 图表描述（可选）
    contrast="A_vs_B",              # 对比策略（可选）
    analysis_node="Expression_statistics",  # 分析节点名称（可选）
    precision=3                     # 浮点数精度：0-10位小数（默认3）
)

# 上传文件（最简）
client.storage.upload_file("results.csv", "proj_001")

# 上传文件到指定路径
client.storage.upload_file("results.csv", "proj_001", base_path="analysis")

# 上传目录（最简）
client.storage.upload_directory("output/", "proj_001")

# 上传目录到指定路径
client.storage.upload_directory("output/", "proj_001", base_path="analysis")
```

### 便捷函数（已弃用）

> ⚠️ **弃用警告**: 以下函数在 v0.4.1 中已弃用，将在 v0.5.0 中移除。推荐使用上述 `Lims2Client` 实例方法复用连接池，避免批量上传时的连接问题。

```python
# 不推荐：每次调用都创建新连接
from lims2 import upload_chart_from_file
upload_chart_from_file("图表名", "proj_001", "chart.json")
```

## 支持的数据格式

### 图表格式
- **Plotly**: 包含 `data` 和 `layout` 字段的字典
- **Cytoscape**: 包含 `elements` 或 `nodes`+`edges` 字段的字典
- **图片**: PNG, JPG, JPEG, SVG
- **其他**: PDF

### 文件格式
- 支持任意格式的文件上传
- 自动处理大文件（>10MB）的断点续传
- 提供进度回调支持
