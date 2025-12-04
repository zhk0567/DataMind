"""
数据处理页面 - 数据处理逻辑模块
将数据处理相关方法提取到此模块
"""
import flet as ft
import pandas as pd
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, COMPONENT_SIZES
from ui_flet.utils.message_helper import show_snackbar


class ProcessDataHandlerMixin:
    """数据处理逻辑Mixin类"""
    
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
        # 确保预览面板已初始化
        if not hasattr(self, 'preview_main_content'):
            return
        
        if self.main_window.processed_data is None:
            # 没有数据时，显示提示文本
            if hasattr(self, 'preview_main_content'):
                self.preview_main_content.controls.clear()
                if hasattr(self, 'preview_placeholder'):
                    self.preview_main_content.controls.append(self.preview_placeholder)
            return
        
        df = self.main_window.processed_data
        columns = df.columns.tolist()
        
        if len(columns) == 0:
            # 如果没有列，显示提示
            if hasattr(self, 'preview_main_content'):
                self.preview_main_content.controls.clear()
                if hasattr(self, 'preview_placeholder'):
                    self.preview_main_content.controls.append(self.preview_placeholder)
            return
        
        # 有数据时，显示表格
        # 显示所有列，不限制列数
        max_cols = len(columns)
        max_rows = min(50, len(df))
        
        # 创建列 - 为每列设置合适的宽度
        data_columns = []
        for col in columns:
            # 计算列宽：根据列名长度和数据类型
            col_width = max(80, min(150, len(str(col)) * 8 + 20))
            data_columns.append(
                ft.DataColumn(
                    ft.Text(
                        col, 
                        size=FONT_SIZES['sm'], 
                        weight=ft.FontWeight.BOLD,
                        color=FLUENT_COLORS['text_primary']
                    ),
                    numeric=pd.api.types.is_numeric_dtype(df[col]) if col in df.columns else False,
                )
            )
        
        # 创建行
        data_rows = []
        for idx, row in df.head(max_rows).iterrows():
            cells = []
            for i, val in enumerate(row):
                # 格式化数值显示
                if pd.api.types.is_numeric_dtype(df[columns[i]]):
                    if pd.notna(val):
                        # 数值类型：保留适当小数位
                        if isinstance(val, float):
                            display_val = f"{val:.2f}" if abs(val) < 1000 else f"{val:.0f}"
                        else:
                            display_val = str(val)
                    else:
                        display_val = ""
                else:
                    # 文本类型：截断过长的文本
                    display_val = str(val)[:50] if pd.notna(val) else ""
                
                cells.append(
                    ft.DataCell(
                        ft.Text(
                            display_val, 
                            size=FONT_SIZES['sm'],
                            color=FLUENT_COLORS['text_primary']
                        )
                    )
                )
            data_rows.append(
                ft.DataRow(
                    cells=cells,
                    color=FLUENT_COLORS['bg_card']
                )
            )
        
        # 重新创建DataTable
        new_table = ft.DataTable(
            columns=data_columns,
            rows=data_rows,
            border=ft.border.all(1, FLUENT_COLORS['border']),
            border_radius=COMPONENT_SIZES['input_border_radius'],
            heading_row_color=FLUENT_COLORS['bg_tertiary'],
            data_row_color={ft.ControlState.DEFAULT: FLUENT_COLORS['bg_card']},
            bgcolor=FLUENT_COLORS['bg_card'],
            heading_text_style=ft.TextStyle(
                size=FONT_SIZES['sm'],
                weight=ft.FontWeight.BOLD,
                color=FLUENT_COLORS['text_primary']
            ),
            data_text_style=ft.TextStyle(
                size=FONT_SIZES['sm'],
                color=FLUENT_COLORS['text_primary']
            ),
            data_row_max_height=40,
            column_spacing=20,
            horizontal_lines=ft.border.BorderSide(1, FLUENT_COLORS['border']),
            vertical_lines=ft.border.BorderSide(1, FLUENT_COLORS['border']),
        )
        
        # 更新preview_table引用
        self.preview_table = new_table
        
        # 创建可滚动的表格容器 - 使用Column包装以支持水平和垂直滚动
        scrollable_table = ft.Container(
            content=new_table,
            padding=SPACING['md'],
            alignment=ft.alignment.top_left,
        )
        
        # 外层容器，支持水平和垂直滚动
        scrollable_row = ft.Row(
            controls=[scrollable_table],
            scroll=ft.ScrollMode.ADAPTIVE,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
        
        new_table_container = ft.Container(
            content=scrollable_row,
            expand=True,
            alignment=ft.alignment.top_left,
            clip_behavior=ft.ClipBehavior.NONE,  # 允许内容溢出以显示滚动条
        )
        self.preview_table_container = new_table_container
        
        # 更新显示内容
        if hasattr(self, 'preview_main_content'):
            self.preview_main_content.controls.clear()
            self.preview_main_content.controls.append(new_table_container)
            
            # 更新preview_main_content的滚动设置
            self.preview_main_content.scroll = ft.ScrollMode.ADAPTIVE
            self.preview_main_content.horizontal_alignment = ft.CrossAxisAlignment.START
            
            # 更新preview_card的content
            if self.preview_card is not None:
                try:
                    if hasattr(self.preview_card, 'content') and hasattr(self.preview_card.content, 'content'):
                        column = self.preview_card.content.content
                        if isinstance(column, ft.Column):
                            column.scroll = ft.ScrollMode.ADAPTIVE
                            column.horizontal_alignment = ft.CrossAxisAlignment.START
                except Exception:
                    pass
        
        # 更新页面
        try:
            if hasattr(self.main_window, 'page') and self.main_window.page is not None:
                self.main_window.page.update()
        except Exception:
            pass
    
    def on_data_changed(self):
        """数据变化时调用"""
        if self.main_window.processed_data is not None:
            # 更新编码变量列表
            df = self.main_window.processed_data
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            
            # 检查encode_list是否已初始化
            if self.encode_list is not None:
                try:
                    new_controls = []
                    if categorical_cols:
                        for col in categorical_cols:
                            checkbox_row = ft.Row(
                                controls=[
                                    ft.Checkbox(value=False),
                                    ft.Text(
                                        col,
                                        size=FONT_SIZES['md'],
                                        color=FLUENT_COLORS['text_primary']
                                    ),
                                ],
                                spacing=SPACING['sm'],
                            )
                            new_controls.append(checkbox_row)
                    else:
                        new_controls.append(
                            ft.Container(
                                content=ft.Text(
                                    "没有分类型变量",
                                    size=FONT_SIZES['sm'],
                                    color=FLUENT_COLORS['text_secondary']
                                ),
                                padding=SPACING['sm'],
                            )
                        )
                    
                    # 清空并重新设置controls
                    self.encode_list.controls.clear()
                    self.encode_list.controls.extend(new_controls)
                    
                    # 更新encode_card的content
                    if self.encode_card is not None:
                        try:
                            if hasattr(self.encode_card, 'content') and hasattr(self.encode_card.content, 'content'):
                                column = self.encode_card.content.content
                                if isinstance(column, ft.Column) and len(column.controls) >= 4:
                                    encode_content_column = ft.Column(
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
                                    )
                                    column.controls[-1] = encode_content_column
                        except Exception:
                            pass
                    
                    # 尝试更新ListView
                    try:
                        if hasattr(self.encode_list, '_Control__attrs'):
                            self.encode_list.update()
                    except Exception:
                        pass
                except Exception:
                    pass
            
            # 更新概览和预览
            try:
                if self.overview_label is not None:
                    self._update_overview()
            except Exception:
                pass
            
            try:
                if self.preview_table is not None:
                    self._update_preview()
            except Exception:
                pass
            
            # 通过页面更新来刷新所有控件
            try:
                if hasattr(self.main_window, 'page') and self.main_window.page is not None:
                    self.main_window.page.update()
            except Exception:
                pass

