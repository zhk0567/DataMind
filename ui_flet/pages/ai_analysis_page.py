"""
AI自动分析页面 - Flet版本
高标准视觉规范
"""
import flet as ft
import pandas as pd
from ui_flet.components.fluent_components import FluentCard, FluentButton, PageHeader
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, PAGE_LAYOUT, COMPONENT_SIZES, FONT_FAMILY, FONT_WEIGHT_NORMAL, FONT_WEIGHT_MEDIUM, FONT_WEIGHT_BOLD, get_text_style
from ui_flet.utils.message_helper import show_snackbar
from core.ai import AIAnalyzer
import threading


class AIAnalysisPage:
    """AI自动分析页面"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.content = None
        self.ai_analyzer = AIAnalyzer()
        self.analysis_result = None
        self.is_analyzing = False
        
        # UI控件
        self.btn_analyze = None
        self.analysis_display = None
        self.basic_stats_display = None
        self.loading_indicator = None
    
    def get_content(self):
        """获取页面内容"""
        if self.content is None:
            self.content = self._create_content()
        return self.content
    
    def _create_content(self):
        """创建页面内容"""
        # 标题区域
        header = PageHeader(
            title="🤖 AI自动分析",
            subtitle="使用AI智能分析数据特征，获取处理建议和可视化方案"
        )
        
        # 分析按钮
        self.btn_analyze = FluentButton(
            text="开始AI分析",
            on_click=self._start_analysis,
            bg_color=FLUENT_COLORS['primary'],
            width=300,
            size="large"
        )
        
        # 加载指示器
        self.loading_indicator = ft.Container(
            content=ft.Column(
                controls=[
                    ft.ProgressRing(width=50, height=50, stroke_width=3),
                    ft.Text(
                        "AI正在分析数据，请稍候...",
                        size=FONT_SIZES['md'],
                        color=FLUENT_COLORS['text_secondary']
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=SPACING['md']
            ),
            visible=False,
            padding=SPACING['xl']
        )
        
        # 基本统计信息显示
        self.basic_stats_display = FluentCard(
            title="📊 数据基本信息",
            content=ft.Column(
                controls=[
                    ft.Text(
                        "请先上传数据，然后点击\"开始AI分析\"按钮",
                        size=FONT_SIZES['md'],
                        color=FLUENT_COLORS['text_secondary']
                    )
                ],
                spacing=SPACING['md']
            ),
            padding=COMPONENT_SIZES['card_padding'],
        )
        
        # AI分析结果显示
        self.analysis_display = FluentCard(
            title="🤖 AI分析结果",
            content=ft.Column(
                controls=[
                    ft.Text(
                        "分析结果将显示在这里",
                        size=FONT_SIZES['md'],
                        color=FLUENT_COLORS['text_secondary']
                    )
                ],
                spacing=SPACING['md']
            ),
            padding=COMPONENT_SIZES['card_padding'],
        )
        
        # 主内容区域
        content = ft.Column(
            controls=[
                header,
                ft.Container(height=PAGE_LAYOUT['header_spacing']),
                # 操作区域
                ft.Container(
                    content=ft.Row(
                        controls=[
                            self.btn_analyze,
                            self.loading_indicator,
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=SPACING['md']
                    ),
                    padding=ft.padding.only(bottom=SPACING['xl'])
                ),
                # 基本统计信息
                self.basic_stats_display,
                ft.Container(height=SPACING['xl']),
                # AI分析结果
                self.analysis_display,
            ],
            spacing=0,
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
        )
        
        return ft.Container(
            content=content,
            expand=True,
            padding=ft.padding.only(right=SPACING['md']),  # 为滚动条留出空间
        )
    
    def _start_analysis(self, e):
        """开始AI分析"""
        if self.is_analyzing:
            show_snackbar(self.main_window.page, "分析正在进行中，请稍候...", "info")
            return
        
        if self.main_window.processed_data is None:
            show_snackbar(self.main_window.page, "请先上传数据", "error")
            return
        
        # 更新UI状态
        self.is_analyzing = True
        self.btn_analyze.disabled = True
        self.btn_analyze.text = "分析中..."
        self.loading_indicator.visible = True
        self.analysis_display.content.controls.clear()
        self.analysis_display.content.controls.append(
            ft.Text("正在分析，请稍候...", size=FONT_SIZES['md'], color=FLUENT_COLORS['text_secondary'])
        )
        
        try:
            self.main_window.page.update()
        except:
            pass
        
        # 在新线程中执行分析（避免阻塞UI）
        thread = threading.Thread(target=self._perform_analysis, daemon=True)
        thread.start()
    
    def _perform_analysis(self):
        """执行AI分析（在后台线程中）"""
        try:
            df = self.main_window.processed_data
            
            # 调用AI分析器
            result = self.ai_analyzer.analyze_dataframe(df)
            self.analysis_result = result
            
            # 更新UI（Flet的page.update()是线程安全的）
            self._update_analysis_ui(result)
            
        except Exception as ex:
            error_msg = str(ex)
            self._show_analysis_error(error_msg)
    
    def _update_analysis_ui(self, result):
        """更新分析结果UI（在主线程中执行）"""
        try:
            # 更新基本统计信息
            self._update_basic_stats(result)
            
            # 更新AI分析结果
            self._update_ai_analysis(result)
            
            # 恢复按钮状态
            self.is_analyzing = False
            self.btn_analyze.disabled = False
            self.btn_analyze.text = "重新分析"
            self.loading_indicator.visible = False
            
            # 更新页面
            self.main_window.page.update()
            
            show_snackbar(self.main_window.page, "AI分析完成！", "success")
            
        except Exception as e:
            self._show_analysis_error(str(e))
    
    def _update_basic_stats(self, result):
        """更新基本统计信息显示"""
        stats = result['basic_statistics']
        shape = stats['shape']
        missing = stats['missing_values']
        data_types = stats['data_types']
        
        controls = [
            ft.Row(
                controls=[
                    ft.Text(
                        f"数据维度: {shape['rows']:,} 行 × {shape['columns']:,} 列",
                        size=FONT_SIZES['md'],
                        weight=ft.FontWeight.BOLD,
                        color=FLUENT_COLORS['text_primary']
                    )
                ]
            ),
            ft.Divider(height=1),
            ft.Row(
                controls=[
                    ft.Text(
                        f"缺失值: {missing['total']:,} 个 ({missing['percentage']:.2f}%)",
                        size=FONT_SIZES['md'],
                        color=FLUENT_COLORS['text_primary']
                    )
                ]
            ),
            ft.Row(
                controls=[
                    ft.Text(
                        f"数值型列: {data_types['numeric_count']} 个",
                        size=FONT_SIZES['md'],
                        color=FLUENT_COLORS['text_primary']
                    ),
                    ft.Container(width=SPACING['xl']),
                    ft.Text(
                        f"分类型列: {data_types['categorical_count']} 个",
                        size=FONT_SIZES['md'],
                        color=FLUENT_COLORS['text_primary']
                    )
                ]
            )
        ]
        
        # 如果有缺失值的列，显示警告
        if missing['columns_with_missing']:
            controls.append(ft.Divider(height=1))
            controls.append(
                ft.Row(
                    controls=[
                        ft.Icon(ft.icons.WARNING, color=FLUENT_COLORS['warning'], size=20),
                        ft.Text(
                            f"包含缺失值的列: {', '.join(missing['columns_with_missing'][:5])}",
                            size=FONT_SIZES['sm'],
                            color=FLUENT_COLORS['warning']
                        )
                    ]
                )
            )
        
        self.basic_stats_display.content.controls = controls
    
    def _update_ai_analysis(self, result):
        """更新AI分析结果显示"""
        ai_response = result['ai_analysis']
        
        # 将AI响应文本转换为格式化的显示
        # 简单的文本格式化：将换行符转换为段落
        lines = ai_response.split('\n')
        
        controls = []
        current_paragraph = []
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_paragraph:
                    # 添加当前段落
                    paragraph_text = ' '.join(current_paragraph)
                    if paragraph_text:
                        controls.append(
                            ft.Text(
                                paragraph_text,
                                size=FONT_SIZES['md'],
                                color=FLUENT_COLORS['text_primary']
                            )
                        )
                    current_paragraph = []
                    controls.append(ft.Container(height=SPACING['sm']))
            elif line.startswith('#') or line.startswith('##') or line.startswith('###'):
                # 标题
                if current_paragraph:
                    paragraph_text = ' '.join(current_paragraph)
                    if paragraph_text:
                        controls.append(
                            ft.Text(
                                paragraph_text,
                                size=FONT_SIZES['md'],
                                color=FLUENT_COLORS['text_primary']
                            )
                        )
                    current_paragraph = []
                
                # 确定标题级别
                if line.startswith('###'):
                    title_size = FONT_SIZES['lg']
                    title_weight = ft.FontWeight.W_600
                elif line.startswith('##'):
                    title_size = FONT_SIZES['xl']
                    title_weight = ft.FontWeight.W_600
                else:
                    title_size = FONT_SIZES['title']
                    title_weight = ft.FontWeight.BOLD
                
                title_text = line.lstrip('#').strip()
                controls.append(
                    ft.Text(
                        title_text,
                        size=title_size,
                        weight=title_weight,
                        color=FLUENT_COLORS['primary']
                    )
                )
                controls.append(ft.Container(height=SPACING['sm']))
            elif line.startswith('-') or line.startswith('*'):
                # 列表项
                if current_paragraph:
                    paragraph_text = ' '.join(current_paragraph)
                    if paragraph_text:
                        controls.append(
                            ft.Text(
                                paragraph_text,
                                size=FONT_SIZES['md'],
                                color=FLUENT_COLORS['text_primary']
                            )
                        )
                    current_paragraph = []
                
                list_text = line.lstrip('-*').strip()
                controls.append(
                    ft.Row(
                        controls=[
                            ft.Text("•", size=FONT_SIZES['md'], color=FLUENT_COLORS['primary']),
                            ft.Container(width=SPACING['sm']),
                            ft.Text(
                                list_text,
                                size=FONT_SIZES['md'],
                                color=FLUENT_COLORS['text_primary'],
                                expand=True
                            )
                        ],
                        spacing=0
                    )
                )
            else:
                current_paragraph.append(line)
        
        # 添加最后一个段落
        if current_paragraph:
            paragraph_text = ' '.join(current_paragraph)
            if paragraph_text:
                controls.append(
                    ft.Text(
                        paragraph_text,
                        size=FONT_SIZES['md'],
                        color=FLUENT_COLORS['text_primary']
                    )
                )
        
        # 如果没有内容，显示默认文本
        if not controls:
            controls.append(
                ft.Text(
                    ai_response,
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_primary']
                )
            )
        
        self.analysis_display.content.controls = controls
    
    def _show_analysis_error(self, error_msg):
        """显示分析错误"""
        self.is_analyzing = False
        self.btn_analyze.disabled = False
        self.btn_analyze.text = "开始AI分析"
        self.loading_indicator.visible = False
        
        # 显示错误信息
        self.analysis_display.content.controls = [
            ft.Row(
                controls=[
                    ft.Icon(ft.icons.ERROR, color=FLUENT_COLORS['error'], size=24),
                    ft.Text(
                        f"分析失败: {error_msg}",
                        size=FONT_SIZES['md'],
                        color=FLUENT_COLORS['error']
                    )
                ],
                spacing=SPACING['sm']
            )
        ]
        
        try:
            self.main_window.page.update()
        except:
            pass
        
        show_snackbar(self.main_window.page, f"AI分析失败: {error_msg}", "error", duration=5000)
    
    def on_data_changed(self):
        """数据变化时调用"""
        # 重置分析结果
        self.analysis_result = None
        if hasattr(self, 'btn_analyze') and self.btn_analyze:
            self.btn_analyze.disabled = False
            self.btn_analyze.text = "开始AI分析"
        
        # 清空显示
        if hasattr(self, 'basic_stats_display') and self.basic_stats_display:
            self.basic_stats_display.content.controls = [
                ft.Text(
                    "数据已更新，请点击\"开始AI分析\"按钮",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                )
            ]
        
        if hasattr(self, 'analysis_display') and self.analysis_display:
            self.analysis_display.content.controls = [
                ft.Text(
                    "分析结果将显示在这里",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                )
            ]

