"""
数据处理页面 - Flet版本
高标准视觉规范
重构后版本：使用Mixin类分离数据处理逻辑
"""
import flet as ft
import pandas as pd
import threading
import time
from ui_flet.components.fluent_components import (
    FluentCard, FluentButton, PageHeader, FluentDropdown, FluentTextField
)
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, PAGE_LAYOUT, COMPONENT_SIZES
from ui_flet.utils.message_helper import show_snackbar
from core.data_processor import DataProcessor
from ui_flet.pages.process_data_handler import ProcessDataHandlerMixin


class ProcessPage(ProcessDataHandlerMixin):
    """数据处理页面"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.content = None
        self.processor = DataProcessor()
        self.missing_combo = None
        self.outliers_check = None
        self.encode_list = None
        self.encode_method_combo = None
        self.btn_apply = None
        self.overview_label = None
        self.preview_table = None
        self.encode_card = None
        self.preview_card = None
    
    def get_content(self):
        """获取页面内容"""
        if self.content is None:
            self.content = self._create_content()
        # 如果数据已存在，立即更新显示
        if self.main_window.processed_data is not None:
            def delayed_update():
                time.sleep(0.1)
                try:
                    if hasattr(self.main_window, 'page') and self.main_window.page is not None:
                        self.on_data_changed()
                except Exception:
                    pass
            thread = threading.Thread(target=delayed_update, daemon=True)
            thread.start()
        return self.content
    
    def _create_content(self):
        """创建页面内容"""
        # 标题区域
        reset_button = FluentButton(
            text="🔄 重置",
            on_click=self._reset_data,
            bg_color=FLUENT_COLORS['text_secondary'],
            width=100,
            size='sm',
        )
        
        header = PageHeader(
            title="🔧 数据处理工作流",
            subtitle="执行数据清洗、转换、编码等预处理操作",
            action=reset_button,
        )
        
        # 主内容区域
        main_row = ft.Row(
            controls=[],
            spacing=SPACING['md'],
            expand=True,
        )
        
        # 左侧处理面板
        left_panel = self._create_process_panel()
        main_row.controls.append(left_panel)
        
        # 右侧预览面板
        right_panel = self._create_preview_panel()
        main_row.controls.append(right_panel)
        
        # 主内容
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
            padding=ft.padding.only(right=SPACING['md']),
        )
    
    def _create_process_panel(self):
        """创建处理步骤面板"""
        # 数据概览
        self.overview_label = ft.Text(
            "请先上传数据",
            size=FONT_SIZES['md'],
            color=FLUENT_COLORS['text_primary'],
            weight=ft.FontWeight.NORMAL,
            selectable=True,
        )
        
        overview_card = FluentCard(
            title="📊 数据概览",
            content=ft.Column(
                controls=[self.overview_label],
                spacing=SPACING['md'],
            ),
            padding=COMPONENT_SIZES['card_padding_small'],
        )
        
        # 缺失值处理
        self.missing_combo = FluentDropdown(
            label="步骤 1: 缺失值处理",
            options=[
                ft.dropdown.Option("不处理"),
                ft.dropdown.Option("删除缺失值"),
                ft.dropdown.Option("填充均值"),
                ft.dropdown.Option("填充中位数"),
                ft.dropdown.Option("填充众数"),
                ft.dropdown.Option("填充指定值"),
            ],
            value="不处理",
            width=400,
            on_change=self._on_missing_method_changed,
        )
        
        # 填充指定值输入框
        self.fill_value_entry = FluentTextField(
            label="填充值",
            hint_text="输入要填充的值",
            width=400,
            visible=False,
        )
        
        missing_card = FluentCard(
            content=ft.Column(
                controls=[self.missing_combo, self.fill_value_entry],
                spacing=SPACING['sm'],
            ),
            padding=COMPONENT_SIZES['card_padding_small'],
        )
        
        # 异常值处理
        self.outliers_check = ft.Checkbox(value=False)
        
        outliers_content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        self.outliers_check,
                        ft.Text(
                            "删除异常值（IQR方法，1.5倍IQR）",
                            size=FONT_SIZES['md'],
                            color=FLUENT_COLORS['text_primary']
                        ),
                    ],
                    spacing=SPACING['sm'],
                )
            ],
            spacing=SPACING['sm'],
        )
        
        outliers_card = FluentCard(
            title="步骤 2: 异常值处理",
            content=outliers_content,
            padding=COMPONENT_SIZES['card_padding_small'],
        )
        
        # 分类变量编码
        self.encode_list = ft.ListView(
            height=120,
            spacing=SPACING['xs'],
        )
        
        self.encode_placeholder = ft.Text(
            "请先上传数据",
            size=FONT_SIZES['sm'],
            color=FLUENT_COLORS['text_secondary'],
        )
        self.encode_list.controls.append(self.encode_placeholder)
        
        self.encode_method_combo = FluentDropdown(
            label="编码方法",
            options=[
                ft.dropdown.Option("独热编码（One-Hot）"),
                ft.dropdown.Option("标签编码（Label）"),
            ],
            value="独热编码（One-Hot）",
            width=400,
        )
        
        self.encode_card = FluentCard(
            title="步骤 3: 分类变量编码",
            content=ft.Column(
                controls=[
                    ft.Text(
                        "选择分类变量：",
                        size=FONT_SIZES['md'],
                        color=FLUENT_COLORS['text_primary']
                    ),
                    self.encode_list,
                    self.encode_method_combo,
                ],
                spacing=SPACING['md'],
            ),
            padding=COMPONENT_SIZES['card_padding_small'],
        )
        
        # 应用按钮
        self.btn_apply = FluentButton(
            text="✅ 应用所有步骤",
            on_click=self._apply_all_steps,
            bg_color=FLUENT_COLORS['primary'],
            width=400,
        )
        
        # 左侧面板内容
        left_content = ft.Column(
            controls=[
                overview_card,
                ft.Container(height=SPACING['md']),
                missing_card,
                ft.Container(height=SPACING['md']),
                outliers_card,
                ft.Container(height=SPACING['md']),
                self.encode_card,
                ft.Container(height=SPACING['md']),
                self.btn_apply,
            ],
            spacing=0,
            scroll=ft.ScrollMode.ADAPTIVE,
        )
        
        return ft.Container(
            content=left_content,
            width=420,
            padding=0,
        )
    
    def _create_preview_panel(self):
        """创建预览面板"""
        # 预览表格
        self.preview_table = ft.DataTable(
            columns=[
                ft.DataColumn(
                    ft.Text("列名", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])
                ),
                ft.DataColumn(
                    ft.Text("值", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])
                ),
            ],
            rows=[],
            border=ft.border.all(1, FLUENT_COLORS['border']),
            border_radius=COMPONENT_SIZES['input_border_radius'],
            heading_row_color=FLUENT_COLORS['bg_tertiary'],
            heading_text_style=ft.TextStyle(
                size=FONT_SIZES['sm'],
                weight=ft.FontWeight.BOLD,
                color=FLUENT_COLORS['text_primary']
            ),
            data_text_style=ft.TextStyle(
                size=FONT_SIZES['sm'],
                color=FLUENT_COLORS['text_primary']
            ),
        )
        
        # 提示文本
        self.preview_placeholder = ft.Container(
            content=ft.Text(
                "请先上传数据文件",
                size=FONT_SIZES['md'],
                color=FLUENT_COLORS['text_secondary'],
                text_align=ft.TextAlign.CENTER,
            ),
            padding=SPACING['xl'],
            alignment=ft.alignment.center,
        )
        
        # 表格容器
        self.preview_table_container = ft.Container(
            content=self.preview_table,
            padding=SPACING['xl'],
            alignment=ft.alignment.top_left,
        )
        
        # 主内容容器
        self.preview_main_content = ft.Column(
            controls=[self.preview_placeholder],
            spacing=0,
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True,
        )
        
        # 外层Column用于滚动
        scroll_column = ft.Column(
            controls=[self.preview_main_content],
            spacing=0,
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )
        
        # FluentCard
        self.preview_card = FluentCard(
            title="📋 数据预览",
            content=scroll_column,
            padding=COMPONENT_SIZES['card_padding'],
        )
        
        return ft.Container(
            content=self.preview_card,
            expand=True,
            clip_behavior=ft.ClipBehavior.NONE,  # 允许内容溢出以显示滚动条
        )
    
    def _on_missing_method_changed(self, e):
        """缺失值处理方法改变"""
        if self.missing_combo.value == "填充指定值":
            self.fill_value_entry.visible = True
        else:
            self.fill_value_entry.visible = False
        self.fill_value_entry.update()
    
    def _reset_data(self, e):
        """重置数据"""
        if self.main_window.data is not None:
            self.main_window.processed_data = self.main_window.data.copy()
            self._update_preview()
            self._update_overview()
            show_snackbar(self.main_window.page, "数据已重置到原始状态", "info")
    
    # 注意：_apply_all_steps, _update_overview, _update_preview, on_data_changed
    # 这些方法现在在ProcessDataHandlerMixin中

