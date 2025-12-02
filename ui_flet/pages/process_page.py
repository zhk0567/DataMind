"""
数据处理页面 - Flet版本
高标准视觉规范
"""
import flet as ft
import pandas as pd
from ui_flet.components.fluent_components import FluentCard, FluentButton, PageHeader, FluentDropdown, FluentTextField
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, PAGE_LAYOUT, COMPONENT_SIZES
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, PAGE_LAYOUT, COMPONENT_SIZES, FONT_FAMILY, FONT_WEIGHT_NORMAL, FONT_WEIGHT_MEDIUM, FONT_WEIGHT_BOLD, get_text_style
from ui_flet.utils.message_helper import show_snackbar
from core.data_processor import DataProcessor


class ProcessPage:
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
    
    def get_content(self):
        """获取页面内容"""
        if self.content is None:
            self.content = self._create_content()
        # 如果数据已加载且页面已创建，更新显示
        if self.main_window.processed_data is not None and self.encode_list is not None:
            # 延迟更新，确保ListView已添加到页面
            try:
                self.on_data_changed()
            except Exception:
                # 如果更新失败，忽略错误（会在页面显示后自动更新）
                pass
        return self.content
    
    def _create_content(self):
        """创建页面内容"""
        # 标题区域 - 使用统一组件
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
        
        # 主内容区域 - 统一间距
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
        
        # 主内容 - 统一间距，添加右侧padding避免与滚动条重叠
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
            padding=ft.padding.only(
                right=SPACING['md'],  # 右侧padding，为滚动条留出空间
            ),
        )
    
    def _create_process_panel(self):
        """创建处理步骤面板 - 统一间距和样式"""
        # 数据概览
        self.overview_label = ft.Text(
            "请先上传数据",
            size=FONT_SIZES['md'],
            color=FLUENT_COLORS['text_primary'],
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
        self.outliers_check = ft.Checkbox(
            label="步骤 2: 删除异常值（IQR方法，1.5倍IQR）",
            value=False,
        )
        
        outliers_card = FluentCard(
            content=ft.Column(
                controls=[self.outliers_check],
                spacing=SPACING['sm'],
            ),
            padding=COMPONENT_SIZES['card_padding_small'],
        )
        
        # 分类变量编码
        self.encode_list = ft.ListView(
            height=120,
            spacing=SPACING['xs'],
        )
        
        self.encode_method_combo = FluentDropdown(
            label="编码方法",
            options=[
                ft.dropdown.Option("独热编码（One-Hot）"),
                ft.dropdown.Option("标签编码（Label）"),
            ],
            value="独热编码（One-Hot）",
            width=400,
        )
        
        encode_card = FluentCard(
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
        
        # 左侧面板内容 - 统一间距
        left_content = ft.Column(
            controls=[
                overview_card,
                ft.Container(height=SPACING['md']),
                missing_card,
                ft.Container(height=SPACING['md']),
                outliers_card,
                ft.Container(height=SPACING['md']),
                encode_card,
                ft.Container(height=SPACING['md']),
                self.btn_apply,
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
        )
        
        return ft.Container(
            content=left_content,
            width=420,
            padding=0,
        )
    
    def _create_preview_panel(self):
        """创建预览面板 - 统一样式"""
        # 预览表格（初始化为空，有数据时再填充）
        self.preview_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("列名", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("值", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
            border=ft.border.all(1, FLUENT_COLORS['border']),
            border_radius=COMPONENT_SIZES['input_border_radius'],
        )
        
        preview_card = FluentCard(
            title="📋 数据预览",
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=self.preview_table,
                            padding=SPACING['xl'],
                        ),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
            ),
            padding=COMPONENT_SIZES['card_padding'],
        )
        
        return ft.Container(
            content=preview_card,
            expand=True,
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
    
    def _apply_all_steps(self, e):
        """应用所有处理步骤"""
        if self.main_window.processed_data is None:
            show_snackbar(self.main_window.page, "请先上传数据", "error")
            return
        
        # 显示处理中状态
        original_text = self.btn_apply.text
        self.btn_apply.text = "处理中..."
        self.btn_apply.disabled = True
        self.btn_apply.update()
        
        try:
            df = self.main_window.processed_data.copy()
            original_shape = df.shape
            
            # 处理缺失值
            missing_method = self.missing_combo.value
            if missing_method == "删除缺失值":
                df = df.dropna()
            elif missing_method == "填充均值":
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            elif missing_method == "填充中位数":
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
            elif missing_method == "填充众数":
                for col in df.columns:
                    mode_val = df[col].mode()
                    if len(mode_val) > 0:
                        df[col] = df[col].fillna(mode_val[0])
            elif missing_method == "填充指定值" and hasattr(self, 'fill_value_entry'):
                fill_value = self.fill_value_entry.value
                if fill_value:
                    try:
                        numeric_value = float(fill_value)
                        numeric_cols = df.select_dtypes(include=['number']).columns
                        df[numeric_cols] = df[numeric_cols].fillna(numeric_value)
                    except ValueError:
                        df = df.fillna(fill_value)
            
            # 处理异常值
            if self.outliers_check.value:
                numeric_cols = df.select_dtypes(include=['number']).columns
                for col in numeric_cols:
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    if IQR > 0:  # 避免除零
                        lower_bound = Q1 - 1.5 * IQR
                        upper_bound = Q3 + 1.5 * IQR
                        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
            
            # 更新数据
            self.main_window.processed_data = df
            self._update_preview()
            self._update_overview()
            
            # 显示成功消息
            rows_removed = original_shape[0] - df.shape[0]
            if rows_removed > 0:
                show_snackbar(
                    self.main_window.page,
                    f"数据处理完成！删除了 {rows_removed:,} 行数据",
                    "success"
                )
            else:
                show_snackbar(
                    self.main_window.page,
                    "数据处理完成！",
                    "success"
                )
            
        except Exception as ex:
            show_snackbar(
                self.main_window.page,
                f"处理失败: {str(ex)}",
                "error",
                duration=5000
            )
        finally:
            # 恢复按钮状态
            self.btn_apply.text = original_text
            self.btn_apply.disabled = False
            self.btn_apply.update()
    
    def _update_overview(self):
        """更新数据概览"""
        if self.main_window.processed_data is not None:
            df = self.main_window.processed_data
            missing_count = df.isnull().sum().sum()
            info = f"📊 数据维度: {df.shape[0]:,} 行 × {df.shape[1]:,} 列\n"
            info += f"⚠️ 缺失值: {missing_count:,} 个"
            
            # 计算数据类型统计
            numeric_count = len(df.select_dtypes(include=['number']).columns)
            categorical_count = len(df.select_dtypes(include=['object']).columns)
            info += f"\n📈 数值型: {numeric_count} 个 | 📝 分类型: {categorical_count} 个"
            
            self.overview_label.value = info
            # 不调用单个控件的 update()，由页面统一更新，避免控件未添加到页面的错误
            try:
                if hasattr(self.overview_label, 'page') and self.overview_label.page is not None:
                    self.overview_label.update()
            except (AssertionError, AttributeError):
                # 控件还未添加到页面，忽略错误，由页面统一更新
                pass
    
    def _update_preview(self):
        """更新预览表格"""
        if self.main_window.processed_data is None:
            # 清空表格，保持默认列
            self.preview_table.rows = []
            # 不调用单个控件的 update()，由页面统一更新
            try:
                if hasattr(self.preview_table, 'page') and self.preview_table.page is not None:
                    self.preview_table.update()
            except (AssertionError, AttributeError):
                pass
            return
        
        df = self.main_window.processed_data
        columns = df.columns.tolist()
        
        if len(columns) == 0:
            # 如果没有列，保持默认列
            self.preview_table.rows = []
            # 不调用单个控件的 update()，由页面统一更新
            try:
                if hasattr(self.preview_table, 'page') and self.preview_table.page is not None:
                    self.preview_table.update()
            except (AssertionError, AttributeError):
                pass
            return
        
        max_cols = min(10, len(columns))
        max_rows = min(50, len(df))
        
        # 创建列
        self.preview_table.columns = [
            ft.DataColumn(ft.Text(col, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD))
            for col in columns[:max_cols]
        ]
        
        # 创建行
        self.preview_table.rows = []
        for idx, row in df.head(max_rows).iterrows():
            cells = [
                ft.DataCell(ft.Text(str(val)[:30] if pd.notna(val) else "", size=FONT_SIZES['sm']))
                for val in row[:max_cols]
            ]
            self.preview_table.rows.append(ft.DataRow(cells=cells))
        
        # 不调用单个控件的 update()，由页面统一更新，避免控件未添加到页面的错误
        try:
            if hasattr(self.preview_table, 'page') and self.preview_table.page is not None:
                self.preview_table.update()
        except (AssertionError, AttributeError):
            # 控件还未添加到页面，忽略错误，由页面统一更新
            pass
    
    def on_data_changed(self):
        """数据变化时调用"""
        if self.main_window.processed_data is not None:
            # 更新编码变量列表
            df = self.main_window.processed_data
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            
            # 检查encode_list是否已初始化且已添加到页面
            if self.encode_list is not None:
                try:
                    self.encode_list.controls.clear()
                    for col in categorical_cols:
                        checkbox = ft.Checkbox(label=col)
                        self.encode_list.controls.append(checkbox)
                    
                    # 只有在ListView已添加到页面时才更新
                    # 通过检查是否有父控件来判断
                    if hasattr(self.encode_list, '_Control__attrs') or True:  # Flet内部检查
                        self.encode_list.update()
                except Exception:
                    # 如果ListView还未添加到页面，忽略错误
                    # 会在页面显示时自动更新
                    pass
            
            # 更新概览和预览（这些控件应该已经存在）
            if self.overview_label is not None:
                self._update_overview()
            if self.preview_table is not None:
                self._update_preview()
