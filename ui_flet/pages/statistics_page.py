"""
统计分析页面 - Flet版本
高标准视觉规范
重构后版本：使用Mixin类分离功能
"""
import flet as ft
import os
from ui_flet.components.fluent_components import FluentCard, FluentButton, PageHeader
from ui_flet.styles import (
    FLUENT_COLORS, SPACING, FONT_SIZES, PAGE_LAYOUT,
    COMPONENT_SIZES, MIN_TOUCH_TARGET
)
from ui_flet.utils.message_helper import show_snackbar
from core.statistics import StatisticsAnalyzer
from core.reporting import ReportGenerator, ResultInterpreter
from ui_flet.pages.statistics_constants import ANALYSIS_CATEGORIES, ANALYSIS_NAMES
from ui_flet.pages.statistics_ui_controls import StatisticsUIControlsMixin
from ui_flet.pages.statistics_analyzers import StatisticsAnalyzersMixin
from ui_flet.pages.statistics_result_display import StatisticsResultDisplayMixin


class StatisticsPage(
    StatisticsUIControlsMixin,
    StatisticsAnalyzersMixin,
    StatisticsResultDisplayMixin
):
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
            scroll=ft.ScrollMode.ADAPTIVE,
        )
        
        return ft.Container(
            content=content,
            expand=True,
        )
    
    def _create_category_panel(self):
        """创建分类菜单面板 - 统一样式，增强视觉层次"""
        category_list = ft.Column(
            controls=[],
            spacing=SPACING['xs'],
            scroll=ft.ScrollMode.ADAPTIVE,
        )
        
        # 创建分类项
        for category_name, subcategories in ANALYSIS_CATEGORIES.items():
            category_item = self._create_category_item(category_name, subcategories)
            category_list.controls.append(category_item)
        
        category_card = FluentCard(
            title="分析分类",
            content=category_list,
            padding=COMPONENT_SIZES['card_padding'],
        )
        
        return ft.Container(
            content=category_card,
            width=320,
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
                bgcolor='#00000000',
                shape=ft.RoundedRectangleBorder(radius=COMPONENT_SIZES['input_border_radius']),
                padding=ft.padding.symmetric(horizontal=SPACING['md'], vertical=SPACING['md']),
                text_style=ft.TextStyle(
                    size=FONT_SIZES['xl'],
                    weight=ft.FontWeight.W_600,
                ),
            ),
            width=280,
            height=max(44, MIN_TOUCH_TARGET['height']),
            tooltip=f"点击展开/收起 {category_name}",
        )
        
        # 存储按钮引用以便更新图标
        category_title.data = {'category_name': category_name, 'expand_icon': expand_icon}
        
        # 子分类列表
        subcategory_list = ft.Column(
            controls=[],
            spacing=SPACING['sm'],
            visible=self.category_expansion.get(category_name, False),
        )
        
        for sub_name, sub_key in subcategories.items():
            sub_btn = ft.ElevatedButton(
                text=sub_name,
                data=sub_key,
                on_click=self._handle_analysis_select,
                style=ft.ButtonStyle(
                    color=FLUENT_COLORS['text_primary'],
                    bgcolor='#00000000',
                    shape=ft.RoundedRectangleBorder(radius=COMPONENT_SIZES['input_border_radius']),
                    padding=ft.padding.symmetric(horizontal=SPACING['xl'], vertical=SPACING['md']),
                    text_style=ft.TextStyle(
                        size=FONT_SIZES['md'],
                        weight=ft.FontWeight.W_500,
                    ),
                ),
                width=260,
                height=max(40, MIN_TOUCH_TARGET['height']),
            )
            subcategory_list.controls.append(sub_btn)
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    category_title,
                    subcategory_list,
                ],
                spacing=SPACING['xs'],
            ),
            padding=ft.padding.symmetric(horizontal=SPACING['md'], vertical=SPACING['sm']),
        )
    
    def _toggle_category(self, category_name: str):
        """切换分类展开/收起"""
        current_state = self.category_expansion.get(category_name, False)
        self.category_expansion[category_name] = not current_state
        
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
        # 分析标题
        self.analysis_title = ft.Text(
            "请选择分析类型",
            size=FONT_SIZES['title'],
            weight=ft.FontWeight.BOLD,
            color=FLUENT_COLORS['text_primary']
        )
        
        # 控制区域
        self.control_area = ft.Column(
            controls=[
                ft.Text(
                    "请从左侧选择分析类型",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary'],
                ),
            ],
            spacing=SPACING['lg'],
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )
        
        # 结果展示区域
        self.result_area = ft.Column(
            controls=[
                ft.Text(
                    "分析结果将显示在这里",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary'],
                    text_align=ft.TextAlign.LEFT,
                ),
            ],
            spacing=SPACING['lg'],
            horizontal_alignment=ft.CrossAxisAlignment.START,
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
        
        # 结果标题
        result_header = ft.Row(
            controls=[
                ft.Text(
                    "📊 分析结果",
                    size=FONT_SIZES['title'],
                    weight=ft.FontWeight.BOLD,
                    color=FLUENT_COLORS['text_primary']
                ),
                ft.Container(expand=True),
                self.btn_export,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        # 分析面板内容
        analysis_content = ft.Column(
            controls=[
                self.analysis_title,
                ft.Container(height=PAGE_LAYOUT['header_spacing']),
                self.control_area,
                ft.Container(height=PAGE_LAYOUT['section_spacing']),
                result_header,
                ft.Container(height=SPACING['lg']),
                self.result_area,
            ],
            spacing=0,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            scroll=ft.ScrollMode.ADAPTIVE,
        )
        
        return ft.Container(
            content=analysis_content,
            expand=True,
            padding=ft.padding.only(right=SPACING['md']),
        )
    
    def _update_analysis_panel(self):
        """更新分析面板"""
        if not self.current_analysis:
            return
        
        # 更新标题
        title_name = ANALYSIS_NAMES.get(self.current_analysis, self.current_analysis)
        self.analysis_title.value = f"📊 {title_name}"
        
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
            
            # 根据分析类型调用对应的_create_*方法（这些方法现在在Mixin类中）
            if self.current_analysis == 'descriptive':
                self._create_descriptive_controls(df)
            elif self.current_analysis == 'frequency':
                self._create_frequency_controls(df)
            elif self.current_analysis == 'crosstab':
                self._create_crosstab_controls(df)
            elif self.current_analysis == 't_test_one':
                self._create_t_test_one_controls(df)
            elif self.current_analysis == 't_test_independent':
                self._create_t_test_independent_controls(df)
            elif self.current_analysis == 't_test_paired':
                self._create_t_test_paired_controls(df)
            elif self.current_analysis == 'chi_square':
                self._create_chi_square_controls(df)
            elif self.current_analysis == 'anova':
                self._create_anova_controls(df)
            elif self.current_analysis == 'mann_whitney':
                self._create_mann_whitney_controls(df)
            elif self.current_analysis == 'kruskal_wallis':
                self._create_kruskal_wallis_controls(df)
            elif self.current_analysis == 'correlation':
                self._create_correlation_controls(df)
            elif self.current_analysis == 'partial_correlation':
                self._create_partial_correlation_controls(df)
            elif self.current_analysis == 'regression':
                self._create_regression_controls(df)
            elif self.current_analysis == 'stepwise_regression':
                self._create_stepwise_regression_controls(df)
            elif self.current_analysis == 'logistic_regression':
                self._create_logistic_regression_controls(df)
            elif self.current_analysis == 'pca':
                self._create_pca_controls(df)
            elif self.current_analysis == 'kmeans':
                self._create_kmeans_controls(df)
            elif self.current_analysis == 'hierarchical_clustering':
                self._create_hierarchical_clustering_controls(df)
            elif self.current_analysis == 'decision_tree':
                self._create_decision_tree_controls(df)
            elif self.current_analysis == 'factor_analysis':
                self._create_factor_analysis_controls(df)
            elif self.current_analysis == 'discriminant_analysis':
                self._create_discriminant_analysis_controls(df)
            elif self.current_analysis == 'trend_seasonality':
                self._create_trend_seasonality_controls(df)
            elif self.current_analysis == 'arima':
                self._create_arima_controls(df)
            elif self.current_analysis == 'exponential_smoothing':
                self._create_exponential_smoothing_controls(df)
            else:
                self.control_area.controls.append(
                    ft.Text(
                        f"{title_name} 功能开发中...",
                        size=FONT_SIZES['md'],
                        color=FLUENT_COLORS['text_secondary']
                    )
                )
        
        self.analysis_title.update()
        self.control_area.update()
    
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

