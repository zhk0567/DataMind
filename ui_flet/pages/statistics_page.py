"""
统计分析页面 - Flet版本
高标准视觉规范
"""
import flet as ft
import pandas as pd
import os
from ui_flet.components.fluent_components import FluentCard, FluentButton, PageHeader, FluentDropdown
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, PAGE_LAYOUT, COMPONENT_SIZES, MIN_TOUCH_TARGET
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, PAGE_LAYOUT, COMPONENT_SIZES, FONT_FAMILY, FONT_WEIGHT_NORMAL, FONT_WEIGHT_MEDIUM, FONT_WEIGHT_BOLD, get_text_style
from ui_flet.utils.message_helper import show_snackbar
from core.statistics import StatisticsAnalyzer
from core.reporting import ReportGenerator, ResultInterpreter

# 分析分类结构
ANALYSIS_CATEGORIES = {
    "描述性分析": {
        "描述性统计": "descriptive",
        "频数分析": "frequency",
        "交叉表分析": "crosstab"
    },
    "差异性分析": {
        "单样本t检验": "t_test_one",
        "独立样本t检验": "t_test_independent",
        "配对样本t检验": "t_test_paired",
        "卡方检验": "chi_square",
        "方差分析": "anova"
    },
    "非参数检验": {
        "Mann-Whitney检验": "mann_whitney",
        "Kruskal-Wallis检验": "kruskal_wallis"
    },
    "相关性分析": {
        "相关分析": "correlation",
        "偏相关分析": "partial_correlation"
    },
    "预测模型": {
        "线性回归": "regression",
        "逐步回归": "stepwise_regression",
        "逻辑回归": "logistic_regression"
    },
    "高级分析": {
        "主成分分析": "pca",
        "K-means聚类": "kmeans",
        "层次聚类": "hierarchical_clustering",
        "决策树分类": "decision_tree"
    },
    "多变量分析": {
        "因子分析": "factor_analysis",
        "判别分析": "discriminant_analysis"
    },
    "时间序列": {
        "趋势与季节性分析": "trend_seasonality",
        "ARIMA模型": "arima",
        "指数平滑": "exponential_smoothing"
    },
}


class StatisticsPage:
    """统计分析页面"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.content = None
        self.analyzer = StatisticsAnalyzer()
        self.report_generator = ReportGenerator()
        self.interpreter = ResultInterpreter()
        self.current_analysis = None
        self.current_result = None
        self.category_expansion = {}  # 记录分类展开状态
    
    def get_content(self):
        """获取页面内容"""
        if self.content is None:
            self.content = self._create_content()
        return self.content
    
    def _create_content(self):
        """创建页面内容"""
        # 标题区域 - 使用统一组件
        header = PageHeader(
            title="📈 统计分析",
            subtitle="选择分析类型和变量，进行专业的统计分析"
        )
        
        # 主内容区域 - 统一间距
        main_row = ft.Row(
            controls=[],
            spacing=SPACING['md'],
            expand=True,
        )
        
        # 左侧分类菜单
        category_panel = self._create_category_panel()
        main_row.controls.append(category_panel)
        
        # 右侧分析面板
        analysis_panel = self._create_analysis_panel()
        main_row.controls.append(analysis_panel)
        
        # 主内容 - 统一间距
        content = ft.Column(
            controls=[
                header,
                ft.Container(height=PAGE_LAYOUT['header_spacing']),
                main_row,
            ],
            spacing=0,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )
        
        return ft.Container(
            content=content,
            expand=True,
        )
    
    def _create_category_panel(self):
        """创建分类菜单面板 - 统一样式，增强视觉层次"""
        category_list = ft.Column(
            controls=[],
            spacing=SPACING['xs'],  # 减小分类项之间的间距
            scroll=ft.ScrollMode.AUTO,
        )
        
        # 创建分类项
        for category_name, subcategories in ANALYSIS_CATEGORIES.items():
            category_item = self._create_category_item(category_name, subcategories)
            category_list.controls.append(category_item)
        
        category_card = FluentCard(
            title="分析分类",
            content=category_list,
            padding=COMPONENT_SIZES['card_padding'],  # 使用标准padding（从small改为标准）
        )
        
        return ft.Container(
            content=category_card,
            width=320,  # 稍微增加宽度，给内容更多空间
            padding=0,
        )
    
    def _create_category_item(self, category_name: str, subcategories: dict):
        """创建分类项（可展开/收起） - 整个标题区域可点击"""
        # 展开/收起图标
        is_expanded = self.category_expansion.get(category_name, False)
        expand_icon = ft.Icon(
            ft.Icons.EXPAND_MORE if is_expanded else ft.Icons.CHEVRON_RIGHT,
            size=20,
            color=FLUENT_COLORS['primary'],
        )
        
        # 分类标题文字
        category_text = ft.Text(
            category_name,
            size=FONT_SIZES['xl'],
            weight=ft.FontWeight.W_600,
            color=FLUENT_COLORS['text_primary']
        )
        
        # 整个标题区域作为可点击的按钮（包括图标和文字）
        category_title = ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    expand_icon,
                    category_text,
                ],
                spacing=SPACING['sm'],
                alignment=ft.MainAxisAlignment.START,
            ),
            on_click=lambda e, name=category_name: self._toggle_category(name),
            style=ft.ButtonStyle(
                color=FLUENT_COLORS['text_primary'],
                bgcolor='#00000000',  # 透明背景
                shape=ft.RoundedRectangleBorder(radius=COMPONENT_SIZES['input_border_radius']),
                padding=ft.padding.symmetric(horizontal=SPACING['md'], vertical=SPACING['md']),
                text_style=ft.TextStyle(
                    size=FONT_SIZES['xl'],
                    weight=ft.FontWeight.W_600,
                ),
            ),
            width=280,
            height=max(44, MIN_TOUCH_TARGET['height']),  # 确保最小点击区域（WCAG AAA级标准）
            tooltip=f"点击展开/收起 {category_name}",
        )
        
        # 存储按钮引用以便更新图标
        category_title.data = {'category_name': category_name, 'expand_icon': expand_icon}
        
        # 子分类列表 - 增大间距
        subcategory_list = ft.Column(
            controls=[],
            spacing=SPACING['sm'],  # 增大子项间距（从xs改为sm）
            visible=self.category_expansion.get(category_name, False),
        )
        
        for sub_name, sub_key in subcategories.items():
            sub_btn = ft.ElevatedButton(
                text=sub_name,
                data=sub_key,
                on_click=self._handle_analysis_select,
                style=ft.ButtonStyle(
                    color=FLUENT_COLORS['text_primary'],
                    bgcolor='#00000000',  # 透明
                    shape=ft.RoundedRectangleBorder(radius=COMPONENT_SIZES['input_border_radius']),
                    padding=ft.padding.symmetric(horizontal=SPACING['xl'], vertical=SPACING['md']),  # 增大内边距
                    # 统一字体样式
                    text_style=ft.TextStyle(
                        size=FONT_SIZES['md'],
                        weight=ft.FontWeight.W_500,  # 中等粗细
                    ),
                ),
                width=260,
                height=max(40, MIN_TOUCH_TARGET['height']),  # 确保最小点击区域
            )
            subcategory_list.controls.append(sub_btn)
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    category_title,
                    subcategory_list,
                ],
                spacing=SPACING['xs'],  # 减小分类项之间的间距
            ),
            padding=ft.padding.symmetric(horizontal=SPACING['md'], vertical=SPACING['sm']),  # 减小垂直内边距
        )
    
    def _toggle_category(self, category_name: str):
        """切换分类展开/收起"""
        self.category_expansion[category_name] = not self.category_expansion.get(category_name, False)
        
        # 重新创建分类面板以更新展开状态和图标
        if hasattr(self, 'content') and self.content:
            # 找到主内容区域
            main_row = None
            for control in self.content.content.controls:
                if isinstance(control, ft.Row) and len(control.controls) >= 2:
                    main_row = control
                    break
            
            if main_row:
                # 重新创建分类面板
                new_category_panel = self._create_category_panel()
                # 替换第一个控件（分类面板）
                main_row.controls[0] = new_category_panel
                self.content.update()
    
    def _handle_analysis_select(self, e):
        """处理分析选择"""
        analysis_key = e.control.data
        self.current_analysis = analysis_key
        self._update_analysis_panel()
    
    def _create_analysis_panel(self):
        """创建分析面板 - 统一间距和样式，左对齐"""
        # 分析标题 - 统一字体大小和样式
        self.analysis_title = ft.Text(
            "请选择分析类型",
            size=FONT_SIZES['title'],  # 统一使用title大小
            weight=ft.FontWeight.BOLD,
            color=FLUENT_COLORS['text_primary']
        )
        
        # 控制区域（变量选择等）- 移除内部滚动，由外层统一滚动
        self.control_area = ft.Column(
            controls=[
                ft.Text(
                    "请从左侧选择分析类型",
                    size=FONT_SIZES['md'],  # 统一使用md大小
                    color=FLUENT_COLORS['text_secondary'],  # 使用次要文字颜色
                ),
            ],
            spacing=SPACING['lg'],
            horizontal_alignment=ft.CrossAxisAlignment.START,  # 左对齐
        )
        
        # 结果展示区域 - 移除内部滚动，由外层统一滚动
        self.result_area = ft.Column(
            controls=[
                ft.Text(
                    "分析结果将显示在这里",
                    size=FONT_SIZES['md'],  # 统一使用md大小
                    color=FLUENT_COLORS['text_secondary'],
                    text_align=ft.TextAlign.LEFT,  # 改为左对齐，而不是居中
                ),
            ],
            spacing=SPACING['lg'],
            horizontal_alignment=ft.CrossAxisAlignment.START,  # 左对齐
        )
        
        # 导出按钮
        self.btn_export = FluentButton(
            text="导出报告",
            on_click=self._export_report,
            bg_color=FLUENT_COLORS['secondary'],
            width=120,
            size='sm',
        )
        self.btn_export.visible = False
        
        # 结果标题 - 统一字体大小和样式
        result_header = ft.Row(
            controls=[
                ft.Text(
                    "📊 分析结果",
                    size=FONT_SIZES['title'],  # 统一使用title大小，与上方标题一致
                    weight=ft.FontWeight.BOLD,
                    color=FLUENT_COLORS['text_primary']
                ),
                ft.Container(expand=True),
                self.btn_export,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,  # 垂直居中对齐
        )
        
        # 分析面板内容 - 统一间距，左对齐，添加右侧padding避免与滚动条重叠
        analysis_content = ft.Column(
            controls=[
                self.analysis_title,
                ft.Container(height=PAGE_LAYOUT['header_spacing']),  # 使用统一的标题间距
                self.control_area,
                ft.Container(height=PAGE_LAYOUT['section_spacing']),  # 使用统一的区块间距
                result_header,
                ft.Container(height=SPACING['lg']),
                self.result_area,
            ],
            spacing=0,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.START,  # 整体左对齐
            scroll=ft.ScrollMode.AUTO,
        )
        
        return ft.Container(
            content=analysis_content,
            expand=True,
            padding=ft.padding.only(
                right=SPACING['md'],  # 右侧padding，为滚动条留出空间
            ),
        )
    
    def _update_analysis_panel(self):
        """更新分析面板"""
        if not self.current_analysis:
            return
        
        # 更新标题
        analysis_names = {
            'descriptive': '描述性统计',
            'correlation': '相关分析',
            'regression': '线性回归',
            't_test_independent': '独立样本t检验',
            'anova': '方差分析',
        }
        self.analysis_title.value = f"📊 {analysis_names.get(self.current_analysis, self.current_analysis)}"
        
        # 清空控制区域
        self.control_area.controls.clear()
        
        # 根据分析类型创建控制界面
        if self.main_window.processed_data is None:
            self.control_area.controls.append(
                ft.Text(
                    "请先上传数据",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                )
            )
        else:
            df = self.main_window.processed_data
            
            if self.current_analysis == 'descriptive':
                self._create_descriptive_controls(df)
            elif self.current_analysis == 'correlation':
                self._create_correlation_controls(df)
            elif self.current_analysis == 'regression':
                self._create_regression_controls(df)
            else:
                self.control_area.controls.append(
                    ft.Text(
                        f"{self.current_analysis} 功能开发中...",
                        size=FONT_SIZES['md']
                    )
                )
        
        self.analysis_title.update()
        self.control_area.update()
    
    def _create_descriptive_controls(self, df):
        """创建描述性统计控制 - 统一样式"""
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if not numeric_cols:
            self.control_area.controls.append(
                ft.Text(
                    "没有数值型变量",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_primary']
                )
            )
            return
        
        # 变量选择
        var_dropdown = FluentDropdown(
            label="选择变量",
            options=[ft.dropdown.Option(col) for col in numeric_cols],
            value=numeric_cols[0] if numeric_cols else None,
            width=380,
        )
        
        self.var_dropdown = var_dropdown
        
        # 分析按钮
        btn_analyze = FluentButton(
            text="开始分析",
            on_click=self._run_descriptive_analysis,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            var_dropdown,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])
    
    def _create_correlation_controls(self, df):
        """创建相关分析控制 - 统一样式"""
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if len(numeric_cols) < 2:
            self.control_area.controls.append(
                ft.Text(
                    "至少需要2个数值型变量",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                )
            )
            return
        
        # 多选变量
        var_checkboxes = ft.Column(
            controls=[
                ft.Checkbox(label=col, value=True)
                for col in numeric_cols[:10]  # 最多显示10个
            ],
            spacing=SPACING['xs'],
        )
        
        self.var_checkboxes = var_checkboxes
        
        # 方法选择
        method_dropdown = FluentDropdown(
            label="相关方法",
            options=[
                ft.dropdown.Option("pearson"),
                ft.dropdown.Option("spearman"),
                ft.dropdown.Option("kendall"),
            ],
            value="pearson",
            width=380,
        )
        
        self.method_dropdown = method_dropdown
        
        # 分析按钮
        btn_analyze = FluentButton(
            text="开始分析",
            on_click=self._run_correlation_analysis,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            ft.Text(
                "选择变量（至少2个）：",
                size=FONT_SIZES['md'],
                weight=ft.FontWeight.BOLD
            ),
            var_checkboxes,
            ft.Container(height=SPACING['md']),
            method_dropdown,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])
    
    def _create_regression_controls(self, df):
        """创建回归分析控制 - 统一样式"""
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if len(numeric_cols) < 2:
            self.control_area.controls.append(
                ft.Text(
                    "至少需要2个数值型变量",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                )
            )
            return
        
        # 因变量选择
        y_dropdown = FluentDropdown(
            label="因变量（Y）",
            options=[ft.dropdown.Option(col) for col in numeric_cols],
            value=numeric_cols[-1] if numeric_cols else None,
            width=380,
        )
        
        self.y_dropdown = y_dropdown
        
        # 自变量选择
        x_checkboxes = ft.Column(
            controls=[
                ft.Checkbox(label=col, value=(col != numeric_cols[-1]))
                for col in numeric_cols
            ],
            spacing=SPACING['xs'],
        )
        
        self.x_checkboxes = x_checkboxes
        
        # 分析按钮
        btn_analyze = FluentButton(
            text="开始分析",
            on_click=self._run_regression_analysis,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            y_dropdown,
            ft.Container(height=SPACING['md']),
            ft.Text(
                "自变量（X，可多选）：",
                size=FONT_SIZES['md'],
                weight=ft.FontWeight.BOLD
            ),
            x_checkboxes,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])
    
    def _run_descriptive_analysis(self, e):
        """运行描述性统计"""
        if not hasattr(self, 'var_dropdown') or not self.var_dropdown.value:
            show_snackbar(self.main_window.page, "请选择变量", "warning")
            return
        
        df = self.main_window.processed_data
        column = self.var_dropdown.value
        
        # 显示加载状态
        self.result_area.controls.clear()
        self.result_area.controls.append(
            ft.Row(
                controls=[
                    ft.ProgressRing(width=40, height=40),
                    ft.Text("正在分析...", size=FONT_SIZES['md'], color=FLUENT_COLORS['text_secondary'])
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=SPACING['md'],
            )
        )
        self.result_area.update()
        
        try:
            result = self.analyzer.descriptive_statistics(df, [column])
            self.current_result = result
            self._display_result(result, 'descriptive')
            show_snackbar(self.main_window.page, "分析完成", "success")
        except Exception as ex:
            self._show_error(f"分析失败: {str(ex)}")
            show_snackbar(self.main_window.page, f"分析失败: {str(ex)}", "error", duration=5000)
    
    def _run_correlation_analysis(self, e):
        """运行相关分析"""
        if not hasattr(self, 'var_checkboxes'):
            return
        
        selected_vars = [
            cb.label for cb in self.var_checkboxes.controls
            if cb.value
        ]
        
        if len(selected_vars) < 2:
            show_snackbar(self.main_window.page, "请至少选择2个变量", "warning")
            self._show_error("请至少选择2个变量")
            return
        
        df = self.main_window.processed_data
        method = self.method_dropdown.value if hasattr(self, 'method_dropdown') else 'pearson'
        
        # 显示加载状态
        self.result_area.controls.clear()
        self.result_area.controls.append(
            ft.Row(
                controls=[
                    ft.ProgressRing(width=40, height=40),
                    ft.Text("正在分析...", size=FONT_SIZES['md'], color=FLUENT_COLORS['text_secondary'])
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=SPACING['md'],
            )
        )
        self.result_area.update()
        
        try:
            result = self.analyzer.correlation_analysis(df, selected_vars, method)
            self.current_result = result
            self._display_result(result, 'correlation')
            show_snackbar(self.main_window.page, "分析完成", "success")
        except Exception as ex:
            self._show_error(f"分析失败: {str(ex)}")
            show_snackbar(self.main_window.page, f"分析失败: {str(ex)}", "error", duration=5000)
    
    def _run_regression_analysis(self, e):
        """运行回归分析"""
        if not hasattr(self, 'y_dropdown') or not self.y_dropdown.value:
            return
        
        if not hasattr(self, 'x_checkboxes'):
            return
        
        y_col = self.y_dropdown.value
        x_cols = [
            cb.label for cb in self.x_checkboxes.controls
            if cb.value and cb.label != y_col
        ]
        
        if not x_cols:
            show_snackbar(self.main_window.page, "请至少选择1个自变量", "warning")
            self._show_error("请至少选择1个自变量")
            return
        
        df = self.main_window.processed_data
        columns = x_cols + [y_col]
        
        # 显示加载状态
        self.result_area.controls.clear()
        self.result_area.controls.append(
            ft.Row(
                controls=[
                    ft.ProgressRing(width=40, height=40),
                    ft.Text("正在分析...", size=FONT_SIZES['md'], color=FLUENT_COLORS['text_secondary'])
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=SPACING['md'],
            )
        )
        self.result_area.update()
        
        try:
            result = self.analyzer.regression_analysis(df, columns, {})
            self.current_result = result
            self._display_result(result, 'regression')
            show_snackbar(self.main_window.page, "分析完成", "success")
        except Exception as ex:
            self._show_error(f"分析失败: {str(ex)}")
            show_snackbar(self.main_window.page, f"分析失败: {str(ex)}", "error", duration=5000)
    
    def _display_result(self, result: dict, analysis_type: str):
        """显示分析结果 - 统一样式"""
        self.result_area.controls.clear()
        
        if 'error' in result:
            self.result_area.controls.append(
                ft.Text(
                    f"错误: {result['error']}",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['error']
                )
            )
        else:
            # 格式化显示结果
            if analysis_type == 'descriptive':
                self._display_descriptive_result(result)
            elif analysis_type == 'correlation':
                self._display_correlation_result(result)
            elif analysis_type == 'regression':
                self._display_regression_result(result)
        
        self.btn_export.visible = True
        self.result_area.update()
        self.btn_export.update()
    
    def _display_descriptive_result(self, result: dict):
        """显示描述性统计结果 - 统一样式"""
        if isinstance(result, dict) and len(result) > 0:
            # 获取第一个变量的结果
            var_name = list(result.keys())[0]
            stats = result[var_name]
            
            # 创建结果表格
            data_rows = []
            for key, value in stats.items():
                if isinstance(value, (int, float)):
                    data_rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(key), size=FONT_SIZES['sm'])),
                                ft.DataCell(ft.Text(f"{value:.4f}", size=FONT_SIZES['sm'])),
                            ]
                        )
                    )
            
            if data_rows:
                result_table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("统计量", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                        ft.DataColumn(ft.Text("值", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                    ],
                    rows=data_rows,
                    border=ft.border.all(1, FLUENT_COLORS['border']),
                    border_radius=COMPONENT_SIZES['input_border_radius'],
                )
                
                self.result_area.controls.append(
                    ft.Text(
                        f"变量: {var_name}",
                        size=FONT_SIZES['lg'],
                        weight=ft.FontWeight.BOLD
                    )
                )
                self.result_area.controls.append(
                    ft.Container(height=SPACING['md'])
                )
                self.result_area.controls.append(result_table)
    
    def _display_correlation_result(self, result: dict):
        """显示相关分析结果 - 统一样式"""
        if 'correlation_matrix' in result:
            corr_matrix = result['correlation_matrix']
            if isinstance(corr_matrix, pd.DataFrame):
                # 创建相关矩阵表格
                columns = corr_matrix.columns.tolist()
                data_rows = []
                
                for idx, row in corr_matrix.iterrows():
                    cells = [
                        ft.DataCell(ft.Text(f"{val:.4f}" if isinstance(val, (int, float)) else str(val)[:8], size=FONT_SIZES['sm']))
                        for val in row
                    ]
                    data_rows.append(ft.DataRow(cells=cells))
                
                result_table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text(col, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD))
                        for col in columns
                    ],
                    rows=data_rows,
                    border=ft.border.all(1, FLUENT_COLORS['border']),
                    border_radius=COMPONENT_SIZES['input_border_radius'],
                )
                
                self.result_area.controls.append(
                    ft.Text(
                        "相关矩阵",
                        size=FONT_SIZES['lg'],
                        weight=ft.FontWeight.BOLD
                    )
                )
                self.result_area.controls.append(
                    ft.Container(height=SPACING['md'])
                )
                self.result_area.controls.append(result_table)
    
    def _display_regression_result(self, result: dict):
        """显示回归分析结果 - 统一样式"""
        if 'r_squared' in result:
            # 显示主要统计量
            stats_data = [
                ("R²", result.get('r_squared', 0)),
                ("调整R²", result.get('adjusted_r_squared', 0)),
                ("F统计量", result.get('f_statistic', 0)),
                ("F p值", result.get('f_p_value', 0)),
            ]
            
            stats_rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(key, size=FONT_SIZES['sm'])),
                        ft.DataCell(ft.Text(f"{val:.4f}" if isinstance(val, (int, float)) else str(val), size=FONT_SIZES['sm'])),
                    ]
                )
                for key, val in stats_data
            ]
            
            stats_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("统计量", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("值", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                ],
                rows=stats_rows,
                border=ft.border.all(1, FLUENT_COLORS['border']),
                border_radius=COMPONENT_SIZES['input_border_radius'],
            )
            
            self.result_area.controls.append(
                ft.Text(
                    "回归统计",
                    size=FONT_SIZES['lg'],
                    weight=ft.FontWeight.BOLD
                )
            )
            self.result_area.controls.append(
                ft.Container(height=SPACING['md'])
            )
            self.result_area.controls.append(stats_table)
            
            # 显示系数
            if 'coefficients' in result:
                self.result_area.controls.append(
                    ft.Container(height=SPACING['lg'])
                )
                self.result_area.controls.append(
                    ft.Text(
                        "回归系数",
                        size=FONT_SIZES['lg'],
                        weight=ft.FontWeight.BOLD
                    )
                )
                self.result_area.controls.append(
                    ft.Container(height=SPACING['md'])
                )
                
                coeff_rows = []
                for var_name, coeff_data in result['coefficients'].items():
                    coeff_rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(var_name, size=FONT_SIZES['sm'])),
                                ft.DataCell(ft.Text(f"{coeff_data.get('coefficient', 0):.4f}", size=FONT_SIZES['sm'])),
                                ft.DataCell(ft.Text(f"{coeff_data.get('p_value', 0):.4f}", size=FONT_SIZES['sm'])),
                                ft.DataCell(
                                    ft.Text(
                                        "是" if coeff_data.get('significant', False) else "否",
                                        size=FONT_SIZES['sm'],
                                        color=FLUENT_COLORS['success'] if coeff_data.get('significant', False) else FLUENT_COLORS['text_secondary']
                                    )
                                ),
                            ]
                        )
                    )
                
                if coeff_rows:
                    coeff_table = ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("变量", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                            ft.DataColumn(ft.Text("系数", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                            ft.DataColumn(ft.Text("p值", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                            ft.DataColumn(ft.Text("显著", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                        ],
                        rows=coeff_rows,
                        border=ft.border.all(1, FLUENT_COLORS['border']),
                        border_radius=COMPONENT_SIZES['input_border_radius'],
                    )
                    self.result_area.controls.append(coeff_table)
    
    def _export_report(self, e):
        """导出报告"""
        if not self.current_result:
            show_snackbar(self.main_window.page, "没有可导出的结果", "warning")
            return
        
        # 生成报告文本
        try:
            report_lines = []
            report_lines.append("=" * 60)
            report_lines.append(f"DataMind 分析报告 - {self.current_analysis}")
            report_lines.append("=" * 60)
            report_lines.append("")
            
            if isinstance(self.current_result, dict):
                for key, value in self.current_result.items():
                    if isinstance(value, (int, float)):
                        report_lines.append(f"{key}: {value:.4f}")
                    else:
                        report_lines.append(f"{key}: {value}")
            
            report_text = "\n".join(report_lines)
            
            # 保存文件
            if not hasattr(self, 'save_picker') or self.save_picker is None:
                self.save_picker = ft.FilePicker(
                    on_result=lambda e: self._handle_save_report(e, report_text)
                )
                # 确保 FilePicker 已添加到页面 overlay
                if self.save_picker not in self.main_window.page.overlay:
                    self.main_window.page.overlay.append(self.save_picker)
                    self.main_window.page.update()
            
            self.save_picker.save_file(
                dialog_title="保存分析报告",
                file_name="analysis_report.txt",
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["txt", "md"],
            )
            
        except Exception as ex:
            show_snackbar(
                self.main_window.page,
                f"导出失败: {str(ex)}",
                "error",
                duration=5000
            )
    
    def _handle_save_report(self, e: ft.FilePickerResultEvent, report_text: str):
        """处理报告保存"""
        if e.path:
            try:
                with open(e.path, 'w', encoding='utf-8') as f:
                    f.write(report_text)
                show_snackbar(
                    self.main_window.page,
                    f"报告已保存到: {os.path.basename(e.path)}",
                    "success"
                )
            except Exception as ex:
                show_snackbar(
                    self.main_window.page,
                    f"保存失败: {str(ex)}",
                    "error",
                    duration=5000
                )
    
    def _show_error(self, message: str):
        """显示错误消息"""
        self.result_area.controls.append(
            ft.Text(
                f"❌ {message}",
                size=FONT_SIZES['md'],
                color=FLUENT_COLORS['error']
            )
        )
        self.result_area.update()
    
    def on_data_changed(self):
        """数据变化时调用"""
        pass
