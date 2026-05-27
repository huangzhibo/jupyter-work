# Plotly 快速入门指南

## 概述
Plotly是一个强大的交互式数据可视化库，支持Python、R、JavaScript等多种语言。本指南提供最基础的入门示例。

##  使用Python版plotly （推荐）

### 安装
```bash
pip install plotly kaleido  # kaleido用于导出静态图片
```

### 基础示例 - 散点图
```python
import plotly.graph_objects as go
import numpy as np

# 生成示例数据
x = np.random.randn(50)
y = np.random.randn(50)

# 创建图表
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=x, 
    y=y, 
    mode='markers',
    name='Sample Data',
    marker=dict(size=10, color='blue')
))

# 设置标题和轴标签
fig.update_layout(
    title='My First Plotly Chart',
    xaxis_title='X Values',
    yaxis_title='Y Values'
)

# 显示图表
fig.show()

# 导出为JSON
json_str = fig.to_json()
with open('my_plot.json', 'w') as f:
    f.write(json_str)

# 保存为静态图片 (需要安装kaleido: pip install kaleido)
fig.write_image("my_plot.png")
fig.write_image("my_plot.pdf")
```

## R plotly快速入门

### 安装
```r
install.packages(c("plotly", "webshot2"))
```

### 基础示例 - 散点图
```r
library(plotly)

# 使用内置数据集
data <- mtcars

# 创建图表
fig <- plot_ly(data, 
               x = ~wt, 
               y = ~mpg, 
               type = 'scatter', 
               mode = 'markers',
               marker = list(size = 10, color = 'blue'),
               name = 'Car Data') %>%
  layout(title = "My First Plotly Chart",
         xaxis = list(title = "Weight"),
         yaxis = list(title = "Fuel Efficiency"))

# 显示图表
show(fig)

# 导出为JSON
json_str <- plotly_json(fig, pretty = TRUE， jsonedit = FALSE)
writeLines(json_str, "my_plot_r.json")

# 保存为静态图片 (需要安装kaleido: npm install -g electron@6.1.4 orca)
# 或者使用webshot2包
library(webshot2)
htmlwidgets::saveWidget(fig, "temp.html")
webshot2::webshot("temp.html", "my_plot.png")
file.remove("temp.html")
```

## R ggplot2导出为plotly json
```r
# 安装并加载
install.packages(c("ggplot2","plotly"))
library(ggplot2)
library(plotly)

# 1) 画一个 ggplot2 图
p_gg <- ggplot(mtcars, aes(x = wt, y = mpg, color = factor(cyl))) +
  geom_point(size = 3) +
  theme_minimal()

# 2) 转成 plotly 对象
p_plotly <- ggplotly(p_gg)

# 3) 同样用 plotly_json/jsonedit=FALSE 拿到字符
json_str <- plotly_json(
  p_plotly,
  pretty   = TRUE,
  jsonedit = FALSE
)

# 4) 写文件
writeLines(json_str, "ggplot2_plotly.json")
```

## 核心特性
- **交互性**: 自动支持缩放、平移、悬停等交互功能
- **响应式**: 图表自动适应容器大小
- **多格式输出**: 支持HTML、PNG、PDF、SVG等格式
- **Web就绪**: 生成的图表可直接嵌入网页

## 学习资源

### 官方文档
- **Python**: https://plotly.com/python/
- **R**: https://plotly.com/r/
- **图表参考**: https://plotly.com/python/reference/
- **生物图表**：[https://dash.plotly.com/dash-bio/ ](https://dash.plotly.com/dash-bio)

### 示例库
- **Python示例**: https://plotly.com/python/basic-charts/
- **R示例**: https://plotly.com/r/basic-charts/
- **其他示例**：[https://plotly.com/examples/](https://plotly.com/examples/)
- **社区**: https://community.plotly.com/
