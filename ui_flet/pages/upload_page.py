"""
数据上传页面 - Flet版本
高标准视觉规范
重构后版本：使用Mixin类分离AI分析功能
"""
import flet as ft
import pandas as pd
import os
from ui_flet.components.fluent_components import FluentCard, FluentButton, PageHeader
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, PAGE_LAYOUT, COMPONENT_SIZES
from ui_flet.styles import (
    FONT_WEIGHT_NORMAL, FONT_WEIGHT_MEDIUM, FONT_WEIGHT_BOLD,
    get_text_kwargs
)
from ui_flet.utils.message_helper import show_snackbar
from ui_flet.utils.file_helper import read_dataframe
from ui_flet.pages.upload_ai_analysis import UploadAIAnalysisMixin


class UploadPage(UploadAIAnalysisMixin):
    """数据上传页面"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.content = None
        self.file_picker = None
        self.file_label = None
        self.info_label = None
        self.data_table = None
        self.ai_analyzer = None  # 延迟初始化，避免导入错误
        self.ai_analysis_card = None
        self.is_analyzing = False
        self.streaming_text = ""  # 流式响应文本
        self.basic_stats = None  # 基本统计信息（用于流式显示）
    
    def get_content(self):
        """获取页面内容"""
        if self.content is None:
            self.content = self._create_content()
        return self.content
    
    def _create_content(self):
        """创建页面内容"""
        # 标题区域 - 使用统一组件
        header = PageHeader(
            title="📤 数据上传",
            subtitle="上传CSV或Excel格式的数据文件"
        )
        
        # 文件选择器
        self.file_picker = ft.FilePicker(
            on_result=self._handle_file_selected
        )
        
        # 上传卡片 - 统一间距和样式
        self.file_label = ft.Text(
            "未选择文件",
            **get_text_kwargs(
                size=FONT_SIZES['md'],
                weight=FONT_WEIGHT_MEDIUM,
                color=FLUENT_COLORS['text_primary']
            )
        )
        
        self.info_label = ft.Text(
            "",
            **get_text_kwargs(
                size=FONT_SIZES['md'],
                weight=FONT_WEIGHT_NORMAL,
                color=FLUENT_COLORS['text_secondary']
            )
        )
        
        upload_card = FluentCard(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            FluentButton(
                                text="📁 选择文件上传",
                                on_click=self._handle_file_picker_click,
                                bg_color=FLUENT_COLORS['primary'],
                            ),
                            ft.Container(expand=True),
                            self.file_label,
                        ],
                        spacing=SPACING['lg'],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Container(height=SPACING['sm']),
                    self.info_label,
                ],
                spacing=0,
            ),
            padding=COMPONENT_SIZES['card_padding'],
        )
        
        # 数据预览卡片 - 统一样式
        preview_card = FluentCard(
            title="📋 数据预览",
            content=ft.Container(
                content=ft.Text(
                    "请先上传数据文件",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary'],
                    text_align=ft.TextAlign.CENTER,
                ),
                padding=SPACING['xl'],
                alignment=ft.alignment.center,
            ),
            padding=COMPONENT_SIZES['card_padding'],
        )
        self.preview_card = preview_card
        
        # AI分析卡片 - 统一样式
        self.ai_analysis_card = FluentCard(
            title="🤖 AI自动分析",
            content=ft.Container(
                content=ft.Text(
                    "上传数据后将自动进行AI分析",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary'],
                    text_align=ft.TextAlign.CENTER,
                ),
                padding=SPACING['xl'],
                alignment=ft.alignment.center,
            ),
            padding=COMPONENT_SIZES['card_padding'],
        )
        
        # 主内容 - 统一间距
        content = ft.Column(
            controls=[
                header,
                ft.Container(height=PAGE_LAYOUT['header_spacing']),
                upload_card,
                ft.Container(height=SPACING['lg']),
                preview_card,
                ft.Container(height=SPACING['lg']),
                self.ai_analysis_card,
            ],
            spacing=0,
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
        )
        
        return ft.Container(
            content=content,
            expand=True,
        )
    
    def _handle_file_picker_click(self, e):
        """处理文件选择器按钮点击"""
        # 确保 FilePicker 已添加到页面 overlay
        if self.file_picker and self.file_picker not in self.main_window.page.overlay:
            self.main_window.page.overlay.append(self.file_picker)
            self.main_window.page.update()
        
        # 打开文件选择对话框
        if self.file_picker:
            self.file_picker.pick_files(
                allowed_extensions=["csv", "xlsx", "xls"],
                dialog_title="选择数据文件"
            )
    
    def _handle_file_selected(self, e: ft.FilePickerResultEvent):
        """处理文件选择"""
        if e.files and len(e.files) > 0:
            file_path = e.files[0].path
            
            # 显示加载状态
            self.file_label.value = "正在读取文件..."
            self.file_label.update()
            
            try:
                # 使用工具函数读取文件（支持多种编码）
                df = read_dataframe(file_path)
                
                if df is None:
                    raise Exception("无法读取文件，请检查文件格式和编码")
                
                # 保存数据
                self.main_window.data = df
                self.main_window.processed_data = df.copy()
                
                # 更新界面
                self.file_label.value = f"✅ 已选择: {os.path.basename(file_path)}"
                self.file_label.color = FLUENT_COLORS['success']
                
                missing_count = df.isnull().sum().sum()
                self.info_label.value = (
                    f"📊 数据维度: {df.shape[0]:,} 行 × {df.shape[1]:,} 列 | "
                    f"⚠️ 缺失值: {missing_count:,} 个"
                )
                
                # 显示数据预览
                self._display_data_preview(df)
                
                # 通知其他页面数据已更新
                if hasattr(self.main_window, 'pages'):
                    for page_key, page in self.main_window.pages.items():
                        if hasattr(page, 'on_data_changed'):
                            page.on_data_changed()
                
                # 显示成功消息
                show_snackbar(
                    self.main_window.page,
                    f"数据加载成功！共 {df.shape[0]:,} 行数据，正在启动AI分析...",
                    "success"
                )
                
                # 更新页面
                self.main_window.page.update()
                
                # 自动启动AI分析（延迟一点确保UI已更新）
                import time
                import threading
                
                def start_analysis():
                    time.sleep(0.3)  # 短暂延迟，确保页面已更新
                    print(f"准备启动AI分析，数据形状: {df.shape}")
                    self._start_ai_analysis(df)
                
                # 在新线程中延迟启动，避免阻塞
                thread = threading.Thread(target=start_analysis, daemon=True)
                thread.start()
                
            except Exception as ex:
                # 显示错误
                self.file_label.value = f"❌ 文件读取失败: {str(ex)}"
                self.file_label.color = FLUENT_COLORS['error']
                self.file_label.update()
                
                show_snackbar(
                    self.main_window.page,
                    f"文件读取失败: {str(ex)}",
                    "error",
                    duration=5000
                )
    
    def _display_data_preview(self, df):
        """显示数据预览"""
        try:
            # 创建数据表格
            columns = df.columns.tolist()
            
            if len(columns) == 0:
                # 如果没有列，显示提示
                self.preview_card.content.content = ft.Container(
                    content=ft.Text(
                        "数据为空",
                        size=FONT_SIZES['md'],
                        color=FLUENT_COLORS['text_secondary'],
                        text_align=ft.TextAlign.CENTER,
                    ),
                    padding=SPACING['xl'],
                    alignment=ft.alignment.center,
                )
                # 更新整个页面而不是单个控件
                self.main_window.page.update()
                return
            
            max_cols = min(10, len(columns))  # 最多显示10列
            max_rows = min(100, len(df))  # 最多显示100行
            
            # 创建表格列
            data_columns = [
                ft.DataColumn(
                    ft.Text(
                        col,
                        **get_text_kwargs(
                            size=FONT_SIZES['sm'],
                            weight=FONT_WEIGHT_BOLD,
                            color=FLUENT_COLORS['text_primary']
                        )
                    ),
                    numeric=False
                )
                for col in columns[:max_cols]
            ]
            
            # 创建数据行
            data_rows = []
            for idx, row in df.head(max_rows).iterrows():
                cells = [
                    ft.DataCell(
                        ft.Text(
                            str(val)[:50] if pd.notna(val) else "",  # 限制显示长度
                            size=FONT_SIZES['sm'],
                            color=FLUENT_COLORS['text_primary']
                        )
                    )
                    for val in row[:max_cols]
                ]
                data_rows.append(ft.DataRow(cells=cells))
            
            data_table = ft.DataTable(
                columns=data_columns,
                rows=data_rows,
                border=ft.border.all(1, FLUENT_COLORS['border']),
                border_radius=COMPONENT_SIZES['input_border_radius'],
                heading_row_color=FLUENT_COLORS['bg_tertiary'],
                heading_text_style=ft.TextStyle(
                    size=FONT_SIZES['sm'],
                    weight=ft.FontWeight.BOLD,
                    color=FLUENT_COLORS['text_primary']
                ),
                data_row_max_height=40,
            )
            
            # 更新预览卡片
            scroll_view = ft.Container(
                content=data_table,
                padding=SPACING['xl'],
            )
            
            scroll_column = ft.Column(
                controls=[scroll_view],
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True,
            )
            
            self.preview_card.content.content = scroll_column
            # 更新整个页面而不是单个控件，确保所有控件都已添加到页面树中
            self.main_window.page.update()
            
        except Exception as ex:
            # 如果更新失败，显示错误但不中断流程
            show_snackbar(
                self.main_window.page,
                f"预览更新失败: {str(ex)}",
                "error",
                duration=3000
            )

