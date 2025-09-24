import pandas as pd
import json
import os


class PPINetworkConverter:
    """
    蛋白质相互作用网络转换器

    功能：
    - 支持多种文件格式（CSV、TSV、TXT）
    - 自动检测文件分隔符
    - 生成Cytoscape.js兼容的JSON格式
    - 提供圆形布局和动态节点大小
    """

    def __init__(self):
        self.edges = []  # 存储边信息：每个边包含source、target、score等信息
        self.nodes = {}  # 存储节点信息：key为protein_id，value为节点属性字典

    def _detect_separator(self, file_path):
        """
        自动检测文件分隔符

        Args:
            file_path (str): 文件路径

        Returns:
            str: 分隔符字符（',' 或 '\t'）

        检测规则：
        - .csv文件使用逗号分隔
        - .tsv/.txt/.tab文件使用制表符分隔
        - 其他文件自动检测首行内容
        """
        _, ext = os.path.splitext(file_path.lower())

        if ext in ['.csv']:
            return ','
        elif ext in ['.tsv', '.txt', '.tab']:
            return '\t'
        else:
            # 尝试自动检测：读取首行判断分隔符类型
            with open(file_path, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                if '\t' in first_line:
                    return '\t'
                elif ',' in first_line:
                    return ','
                else:
                    return '\t'  # 使用一个或多个空白字符作为分隔符

    def load_file(self, file_path,
                  source_col='protein_a',
                  target_col='protein_b',
                  score_col='score',
                  separator=None):
        """
        加载网络数据文件，支持CSV、TSV、TXT格式

        Args:
            file_path (str): 数据文件路径
            source_col (str): 源蛋白质列名，默认'protein_a'
            target_col (str): 目标蛋白质列名，默认'protein_b'
            score_col (str): 相互作用分数列名，默认'score'
            separator (str, optional): 自定义分隔符，为None时自动检测

        Returns:
            bool: 加载成功返回True，失败返回False

        数据格式要求：
        - 必须包含source_col、target_col、score_col三列
        - score列应为数值类型（无法转换时设为0.0）
        """
        if separator is None:
            separator = self._detect_separator(file_path)

        try:
            df = pd.read_csv(file_path, sep=separator)
        except Exception as e:
            print(f"错误：无法读取文件 {file_path}")
            print(f"详细错误：{e}")
            return False

        # 检查必需的列是否存在
        required_cols = [source_col, target_col, score_col]
        missing_cols = [col for col in required_cols
                        if col not in df.columns]
        if missing_cols:
            print(f"错误：文件中缺少以下列: {missing_cols}")
            print(f"可用的列: {list(df.columns)}")
            return False

        # 逐行处理数据，构建节点和边
        for _, row in df.iterrows():
            source = str(row[source_col])
            target = str(row[target_col])

            # 安全转换分数值
            try:
                score = float(row[score_col])
            except (ValueError, TypeError):
                score = 0.0  # 如果分数无法转换为浮点数，设为0

            # 初始化节点信息（如果节点不存在）
            if source not in self.nodes:
                self.nodes[source] = {
                    'id': source,           # 节点唯一标识
                    'label': source,        # 节点显示标签
                    'type': 'protein'       # 节点类型标记
                }
            if target not in self.nodes:
                self.nodes[target] = {
                    'id': target,
                    'label': target,
                    'type': 'protein'
                }

            # 添加边信息到edges列表
            self.edges.append({
                'data': {
                    'id': f"{source}_{target}",     # 边的唯一标识
                    'source': source,               # 起始节点ID
                    'target': target,               # 终止节点ID
                    'score': score,                 # 相互作用强度分数
                    'interaction': 'PPI'            # 交互类型标记
                }
            })

        node_count = len(self.nodes)
        edge_count = len(self.edges)
        print(f"成功加载 {node_count} 个节点和 {edge_count} 条边")
        return True

    def add_protein_annotations(self, annotation_file,
                                protein_col='protein', **kwargs):
        """
        添加蛋白质注释信息到节点

        Args:
            annotation_file (str): 注释文件路径
            protein_col (str): 蛋白质ID列名
            **kwargs: 其他参数

        功能：
        - 读取注释文件，为现有节点添加额外属性
        - 支持任何列作为注释信息
        - 自动检测文件分隔符
        """
        if annotation_file and os.path.exists(annotation_file):
            try:
                separator = self._detect_separator(annotation_file)
                anno_df = pd.read_csv(annotation_file, sep=separator)
                annotation_dict = anno_df.set_index(protein_col).to_dict(
                    'index')

                # 更新节点信息：将注释数据合并到现有节点属性中
                for protein_id in self.nodes:
                    if protein_id in annotation_dict:
                        # 更新节点的注释信息
                        anno_data = annotation_dict[protein_id]
                        self.nodes[protein_id].update(anno_data)

                anno_count = len(annotation_dict)
                print(f"成功添加 {anno_count} 个蛋白质注释")
            except Exception as e:
                print(f"警告：无法加载注释文件 {annotation_file}: {e}")

    def _calculate_node_degrees(self, filtered_edges):
        """
        计算每个节点的度数（连接数）

        Args:
            filtered_edges (list): 过滤后的边列表

        Returns:
            dict: 节点ID -> 度数的映射字典

        说明：
        - 度数 = 与该节点相连的边的数量
        - 用于动态调整节点大小：连接越多的节点越重要，显示越大
        """
        degrees = {}
        for edge in filtered_edges:
            source = edge['data']['source']
            target = edge['data']['target']
            # 每条边为其两个端点节点各增加1个度数
            degrees[source] = degrees.get(source, 0) + 1
            degrees[target] = degrees.get(target, 0) + 1
        return degrees

    def _get_score_range(self):
        """
        获取所有边的分数范围，用于动态调整颜色映射

        Returns:
            tuple: (min_score, max_score)
        """
        if not self.edges:
            return 0.0, 1.0

        scores = [edge['data'].get('score', 0) for edge in self.edges]
        return min(scores), max(scores)

    def generate_json(self, score_threshold=0.0):
        """
        生成Cytoscape.js兼容的JSON数据

        Args:
            score_threshold (float): 分数阈值，低于此值的边将被过滤

        Returns:
            dict: 包含elements、style、layout的完整配置

        生成流程：
        1. 根据分数阈值过滤边
        2. 计算节点度数
        3. 创建节点元素（包含度数信息）
        4. 返回完整的Cytoscape配置

        边的颜色映射说明：
        - 边的颜色深浅反映分数高低：分数越高颜色越深
        - 边的宽度也根据分数调整：分数越高线条越粗
        - 边的透明度随分数变化：分数越高越不透明
        """
        # 过滤边：只保留分数大于等于阈值的边
        edge_elements = [e for e in self.edges
                         if e['data'].get('score', 0) >= score_threshold]

        edge_count = len(edge_elements)
        print(f"过滤后保留 {edge_count} 条边 (阈值: {score_threshold})")

        # 计算节点度数（基于过滤后的边）
        degrees = self._calculate_node_degrees(edge_elements)

        # 创建节点元素，添加度数信息用于样式映射
        node_elements = []
        for protein_id, node_data in self.nodes.items():
            node_copy = node_data.copy()
            node_copy['degree'] = degrees.get(protein_id, 0)  # 添加度数属性
            node_elements.append({
                'data': node_copy
            })

        # 获取分数范围用于动态调整样式
        min_score, max_score = self._get_score_range()

        return {
            'elements': node_elements + edge_elements,  # 图元素：节点+边
            'style': self._get_reference_style(min_score, max_score),  # 样式配置
            'layout': self._get_circular_layout()       # 布局配置
        }

    def _get_reference_style(self, min_score=0.0, max_score=1.0):
        """
        获取与参考图片一致的样式配置，支持基于分数的边颜色映射

        Args:
            min_score (float): 最小分数值，用于颜色映射的下限
            max_score (float): 最大分数值，用于颜色映射的上限

        Returns:
            list: Cytoscape样式规则列表

        样式说明：
        - 使用橙色主题，与参考图片保持一致
        - 节点大小根据度数动态调整（mapData函数）
        - 边的颜色、宽度、透明度根据分数动态调整
        - 提供选中状态的视觉反馈

        边的颜色映射原理：
        - 使用mapData(score, min, max, color1, color2)函数
        - 分数在[min_score, max_score]范围内线性映射到颜色范围
        - 低分数: 浅灰色(#e0e0e0) -> 高分数: 深蓝色(#2c5aa0)
        """
        return [
            {
                # === 节点基础样式 ===
                'selector': 'node',
                'style': {
                    # 颜色设置
                    'background-color': '#ff8c42',              # 主色：橙色
                    'border-color': '#d67635',                  # 边框：深橙色
                    'border-width': '1px',                      # 边框宽度：3像素
                    'opacity': 0.8,                             # 透明度：80%

                    # 尺寸设置（动态映射）
                    'width': 'mapData(degree, 0, 20, 20, 70)',   # 宽度：度数0-20映射到60-140px
                    'height': 'mapData(degree, 0, 20, 20, 70)',  # 高度：与宽度相同

                    # 标签设置
                    'label': 'data(label)',                     # 显示节点的label属性
                    'font-size': 'mapData(degree, 0, 20, 10, 18)',  # 字体：度数0-20映射到14-22px
                    'font-weight': 'bold',                      # 字体粗细：加粗
                    'color': '#333333',                         # 字体颜色：深灰色

                    # 文字轮廓（提高可读性）
                    'text-outline-width': '1px',               # 轮廓宽度：2像素
                    'text-outline-color': '#ffffff',           # 轮廓颜色：白色

                    # 文字位置
                    'text-valign': 'center',                    # 垂直居中
                    'text-halign': 'right'                     # 水平居中
                }
            },
            {
                # === 边的基础样式 ===
                'selector': 'edge',
                'style': {
                    # 边宽度根据分数动态调整
                    'width': f'mapData(score, {min_score}, {max_score}, 4, 7)',

                    # 边颜色根据分数映射：分数越高颜色越深
                    'line-color': f'mapData(score, {min_score}, {max_score}, #e0e0e0, #666666)',

                    # 透明度也根据分数调整：分数越高越不透明
                    'opacity': f'mapData(score, {min_score}, {max_score}, 0.2, 0.5)',

                    'curve-style': 'straight',                  # 边类型：直线
                    'target-arrow-shape': 'none'                # 箭头：无（无向图）
                }
            },
            {
                # === 选中节点的样式 ===
                'selector': 'node:selected',
                'style': {
                    'background-color': '#ff6b1a',              # 选中色：亮橙色
                    'border-color': '#cc5500',                  # 选中边框：深橙红色
                    'border-width': '5px'                       # 选中边框：5像素（更粗）
                }
            },
            {
                # === 选中边的样式 ===
                'selector': 'edge:selected',
                'style': {
                    'line-color': '#666666',                    # 选中边：深灰色
                    'width': '4px',                             # 选中边：4像素（更粗）
                    'opacity': 1.0                              # 选中透明度：100%
                }
            }
        ]

    def _get_circular_layout(self):
        """
        获取圆形布局参数配置

        Returns:
            dict: Cytoscape圆形布局配置

        布局说明：
        - 使用circle布局算法，节点按圆形排列
        - 自适应容器大小，避免节点重叠
        - 动态计算扫描角度，防止首尾节点重叠
        - 包含动画效果，提升用户体验
        """
        # 计算节点数量
        node_count = len(self.nodes)

        # 动态计算扫描角度：避免首尾节点重叠
        # 原理：如果使用完整的2π，首节点(0°)和尾节点(接近360°)会重叠
        # 解决：留出1/n的空隙，使用(n-1)/n * 2π的角度范围
        if node_count <= 1:
            sweep_angle = 6.28  # 单个或无节点时使用完整圆圈
        else:
            # 多个节点：sweep = 2π * (n-1)/n，避免重叠
            sweep_angle = 6.28 * (node_count - 1) / node_count

        # 动态计算半径：根据节点数量调整
        radius = min(280, max(120, node_count * 5))

        return {
            # === 基础布局设置 ===
            'name': 'circle',                       # 布局算法：圆形布局
            'fit': True,                            # 自适应：自动调整到容器大小
            'padding': 50,                          # 内边距：50像素

            # === 圆形布局特定参数 ===
            'boundingBox': {                        # 布局边界框
                'x1': 0, 'y1': 0,                  # 左上角坐标
                'w': 600, 'h': 600                 # 宽度和高度：600x600像素
            },

            # === 节点排列设置 ===
            'avoidOverlap': False,                   # 避免重叠：防止节点相互覆盖
            'nodeDimensionsIncludeLabels': False,   # 尺寸计算：不包含标签
            'spacingFactor': 1.7,                  # 间距因子：1.2倍标准间距

            # === 圆形参数 ===
            'radius': radius,                       # 圆形半径：动态计算
            'startAngle': 0,                        # 起始角度：0度（12点钟方向）
            'sweep': sweep_angle,                   # 扫描角度：动态计算，避免重叠
            'clockwise': True,                      # 排列方向：顺时针
            'sort': True,                           # 排序：按某种规则排序节点

            # === 动画设置 ===
            'animate': True,                        # 启用动画
            'animationDuration': 2000,              # 动画时长：2秒
            'animationEasing': 'ease-in-out'        # 动画缓动：先慢后快再慢
        }

    def get_network_stats(self):
        """
        获取网络统计信息

        Returns:
            dict: 包含节点数、边数、平均度数、网络密度等统计信息

        统计指标说明：
        - nodes: 节点总数
        - edges: 边总数
        - avg_degree: 平均度数 = 2 * 边数 / 节点数
        - density: 网络密度 = 实际边数 / 最大可能边数
        """
        node_count = len(self.nodes)
        edge_count = len(self.edges)

        # 计算平均度数：每条边贡献2个度数（两个端点各1个）
        avg_degree = round(2 * edge_count / max(node_count, 1), 2)

        # 计算网络密度：实际边数 / 最大可能边数
        # 无向图最大边数 = n*(n-1)/2，有向图为n*(n-1)
        max_edges = node_count * (node_count - 1)  # 假设为有向图
        density = round(2 * edge_count / max(max_edges, 1), 4)

        return {
            'nodes': node_count,
            'edges': edge_count,
            'avg_degree': avg_degree,
            'density': density
        }


# ========== 使用示例 ==========
if __name__ == "__main__":
    """
    主程序：演示如何使用PPINetworkConverter

    使用流程：
    1. 创建转换器实例
    2. 加载数据文件
    3. 生成网络图JSON
    4. 保存结果文件
    """

    # 创建网络转换器实例
    converter = PPINetworkConverter()

    # 尝试加载示例数据文件
    input_file = 'data/D_vs_E.network.xls.tmp'
    if os.path.exists(input_file):
        # 加载网络数据
        success = converter.load_file(
            input_file,
            source_col='protein1',      # 源蛋白质列名
            target_col='protein2',      # 目标蛋白质列名
            score_col='combined_score')  # 分数列名

        if success:
            # 可选：添加蛋白质功能注释
            # converter.add_protein_annotations(
            #     'protein_annotations.csv',
            #     protein_col='protein')

            # 生成Cytoscape.js格式的JSON数据
            # score_threshold=0 表示包含所有边
            result = converter.generate_json(score_threshold=0)

            # 输出网络统计信息
            stats = converter.get_network_stats()
            print(f"网络统计: {stats}")

            # 保存结果到JSON文件
            output_file = 'ppi_network.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            print(f"网络图数据已保存到: {output_file}")
            print("请将此文件内容复制到图表查看器中进行可视化")
        else:
            print("文件加载失败")
    else:
        print(f"文件不存在: {input_file}")
        print("请检查文件路径或使用以下示例：")
        example_text = ("converter.load_file('your_file.csv', "
                        "source_col='protein_a', "
                        "target_col='protein_b', score_col='score')")
        print(example_text)
