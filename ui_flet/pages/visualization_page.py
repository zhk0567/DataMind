"""
数据可视化页面 - Flet版本
高标准视觉规范
"""
import flet as ft
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import os
from ui_flet.components.fluent_components import FluentCard, FluentButton, PageHeader, FluentDropdown
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, PAGE_LAYOUT, COMPONENT_SIZES
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, PAGE_LAYOUT, COMPONENT_SIZES, FONT_FAMILY, FONT_WEIGHT_NORMAL, FONT_WEIGHT_MEDIUM, FONT_WEIGHT_BOLD, get_text_style
from ui_flet.utils.message_helper import show_snackbar
from ui_flet.utils.file_helper import export_chart_image
from core.visualization import BasicCharts, StatisticalCharts

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


class VisualizationPage:
    """数据可视化页面"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.content = None
        self.basic_charts = BasicCharts()
        self.statistical_charts = StatisticalCharts()
        self.current_figure = None
        self.chart_image = None
    
    def get_content(self):
        """获取页面内容"""
        if self.content is None:
            self.content = self._create_content()
        return self.content
    
    def _create_content(self):
        """创建页面内容"""
        # 标题区域 - 使用统一组件
        header = PageHeader(
            title="📉 数据可视化",
            subtitle="选择图表类型和变量，生成数据可视化图表"
        )
        
        # 主内容区域 - 统一间距
        main_row = ft.Row(
            controls=[],
            spacing=SPACING['md'],
            expand=True,
        )
        
        # 左侧控制面板
        control_panel = self._create_control_panel()
        main_row.controls.append(control_panel)
        
        # 右侧图表面板
        chart_panel = self._create_chart_panel()
        main_row.controls.append(chart_panel)
        
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
    
    def _create_control_panel(self):
        """创建控制面板 - 统一样式"""
        # 图表类型
        chart_types = [
            "柱状图", "分组柱状图", "折线图", "散点图",
            "饼图", "箱线图", "直方图", "热力图",
        ]
        
        self.chart_type_dropdown = FluentDropdown(
            label="图表类型",
            options=[ft.dropdown.Option(t) for t in chart_types],
            value=chart_types[0],
            width=350,
            on_change=self._on_chart_type_changed,
        )
        
        # 变量选择区域
        self.vars_area = ft.Column(
            controls=[
                ft.Text(
                    "请先上传数据",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_primary']
                ),
            ],
            spacing=SPACING['md'],
            scroll=ft.ScrollMode.ADAPTIVE,
        )
        
        # 生成按钮
        self.btn_generate = FluentButton(
            text="生成图表",
            on_click=self._generate_chart,
            bg_color=FLUENT_COLORS['primary'],
            width=350,
        )
        
        # 导出按钮
        self.btn_export = FluentButton(
            text="导出图表",
            on_click=self._export_chart,
            bg_color=FLUENT_COLORS['secondary'],
            width=350,
        )
        self.btn_export.disabled = True
        
        # 文件保存选择器
        self.save_file_picker = ft.FilePicker(
            on_result=self._handle_save_file
        )
        self.current_chart_bytes = None
        
        control_content = ft.Column(
            controls=[
                self.chart_type_dropdown,
                ft.Container(height=SPACING['xl']),
                self.vars_area,
                ft.Container(expand=True),
                self.btn_generate,
                ft.Container(height=SPACING['sm']),
                self.btn_export,
            ],
            spacing=0,
            expand=True,
        )
        
        control_card = FluentCard(
            content=control_content,
            padding=COMPONENT_SIZES['card_padding'],
        )
        
        return ft.Container(
            content=control_card,
            width=380,
            padding=0,
        )
    
    def _create_chart_panel(self):
        """创建图表面板 - 统一样式"""
        # 图表显示区域
        self.chart_display = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "图表将显示在这里",
                        size=FONT_SIZES['md'],
                        color=FLUENT_COLORS['text_secondary'],
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
            padding=SPACING['xl'],
            border=ft.border.all(1, FLUENT_COLORS['border']),
            border_radius=COMPONENT_SIZES['card_border_radius'],
            bgcolor=FLUENT_COLORS['bg_card'],
        )
        
        chart_card = FluentCard(
            title="📊 图表预览",
            content=self.chart_display,
            padding=COMPONENT_SIZES['card_padding'],
        )
        
        return ft.Container(
            content=chart_card,
            expand=True,
        )
    
    def _on_chart_type_changed(self, e):
        """图表类型改变"""
        self._update_vars_area()
    
    def _update_vars_area(self):
        """更新变量选择区域"""
        # 确保 vars_area 已初始化
        if not hasattr(self, 'vars_area') or self.vars_area is None:
            return
        
        self.vars_area.controls.clear()
        
        if self.main_window.processed_data is None:
            self.vars_area.controls.append(
                ft.Text(
                    "请先上传数据",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_primary']
                )
            )
            # 不调用 update()，由页面统一更新
            return
        
        df = self.main_window.processed_data
        chart_type = self.chart_type_dropdown.value
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        # 根据图表类型创建变量选择控件
        if chart_type in ["柱状图", "分组柱状图"]:
            if categorical_cols:
                x_dropdown = FluentDropdown(
                    label="分类变量（X轴）",
                    options=[ft.dropdown.Option(col) for col in categorical_cols],
                    value=categorical_cols[0] if categorical_cols else None,
                    width=350,
                )
                self.x_var_dropdown = x_dropdown
                self.vars_area.controls.append(x_dropdown)
            
            if numeric_cols:
                y_dropdown = FluentDropdown(
                    label="数值变量（Y轴）",
                    options=[ft.dropdown.Option(col) for col in numeric_cols],
                    value=numeric_cols[0] if numeric_cols else None,
                    width=350,
                )
                self.y_var_dropdown = y_dropdown
                self.vars_area.controls.append(y_dropdown)
        
        elif chart_type in ["折线图", "散点图"]:
            if len(numeric_cols) >= 2:
                x_dropdown = FluentDropdown(
                    label="X变量",
                    options=[ft.dropdown.Option(col) for col in numeric_cols],
                    value=numeric_cols[0],
                    width=350,
                )
                self.x_var_dropdown = x_dropdown
                self.vars_area.controls.append(x_dropdown)
                
                y_dropdown = FluentDropdown(
                    label="Y变量",
                    options=[ft.dropdown.Option(col) for col in numeric_cols],
                    value=numeric_cols[1] if len(numeric_cols) > 1 else None,
                    width=350,
                )
                self.y_var_dropdown = y_dropdown
                self.vars_area.controls.append(y_dropdown)
        
        elif chart_type == "饼图":
            if categorical_cols:
                cat_dropdown = FluentDropdown(
                    label="分类变量",
                    options=[ft.dropdown.Option(col) for col in categorical_cols],
                    value=categorical_cols[0] if categorical_cols else None,
                    width=350,
                )
                self.cat_var_dropdown = cat_dropdown
                self.vars_area.controls.append(cat_dropdown)
            
            if numeric_cols:
                val_dropdown = FluentDropdown(
                    label="数值变量",
                    options=[ft.dropdown.Option(col) for col in numeric_cols],
                    value=numeric_cols[0] if numeric_cols else None,
                    width=350,
                )
                self.val_var_dropdown = val_dropdown
                self.vars_area.controls.append(val_dropdown)
        
        elif chart_type in ["箱线图", "直方图"]:
            if numeric_cols:
                var_dropdown = FluentDropdown(
                    label="变量",
                    options=[ft.dropdown.Option(col) for col in numeric_cols],
                    value=numeric_cols[0] if numeric_cols else None,
                    width=350,
                )
                self.var_dropdown = var_dropdown
                self.vars_area.controls.append(var_dropdown)
    
    def _generate_chart(self, e):
        """生成图表"""
        if self.main_window.processed_data is None:
            show_snackbar(self.main_window.page, "请先上传数据", "error")
            return
        
        # 显示生成中状态
        self.btn_generate.text = "生成中..."
        self.btn_generate.disabled = True
        self.btn_generate.update()
        
        self.chart_display.content = ft.Column(
            controls=[
                ft.ProgressRing(width=40, height=40),
                ft.Text(
                    "正在生成图表...",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=SPACING['md'],
        )
        self.chart_display.update()
        
        try:
            df = self.main_window.processed_data
            chart_type = self.chart_type_dropdown.value
            
            # 创建图表
            fig, ax = plt.subplots(figsize=(10, 6))
            
            if chart_type == "柱状图":
                if hasattr(self, 'x_var_dropdown') and hasattr(self, 'y_var_dropdown'):
                    x_col = self.x_var_dropdown.value
                    y_col = self.y_var_dropdown.value
                    df.groupby(x_col)[y_col].mean().plot(kind='bar', ax=ax)
                    ax.set_xlabel(x_col)
                    ax.set_ylabel(y_col)
                    ax.set_title(f"{y_col} by {x_col}")
            
            elif chart_type == "折线图":
                if hasattr(self, 'x_var_dropdown') and hasattr(self, 'y_var_dropdown'):
                    x_col = self.x_var_dropdown.value
                    y_col = self.y_var_dropdown.value
                    df.plot(x=x_col, y=y_col, kind='line', ax=ax, marker='o')
                    ax.set_xlabel(x_col)
                    ax.set_ylabel(y_col)
                    ax.set_title(f"{y_col} vs {x_col}")
            
            elif chart_type == "散点图":
                if hasattr(self, 'x_var_dropdown') and hasattr(self, 'y_var_dropdown'):
                    x_col = self.x_var_dropdown.value
                    y_col = self.y_var_dropdown.value
                    ax.scatter(df[x_col], df[y_col], alpha=0.6)
                    ax.set_xlabel(x_col)
                    ax.set_ylabel(y_col)
                    ax.set_title(f"{y_col} vs {x_col}")
            
            elif chart_type == "饼图":
                if hasattr(self, 'cat_var_dropdown') and hasattr(self, 'val_var_dropdown'):
                    cat_col = self.cat_var_dropdown.value
                    val_col = self.val_var_dropdown.value
                    data = df.groupby(cat_col)[val_col].sum()
                    ax.pie(data.values, labels=data.index, autopct='%1.1f%%')
                    ax.set_title(f"{val_col} by {cat_col}")
            
            elif chart_type == "箱线图":
                if hasattr(self, 'var_dropdown'):
                    var_col = self.var_dropdown.value
                    ax.boxplot(df[var_col].dropna())
                    ax.set_ylabel(var_col)
                    ax.set_title(f"Boxplot of {var_col}")
            
            elif chart_type == "直方图":
                if hasattr(self, 'var_dropdown'):
                    var_col = self.var_dropdown.value
                    ax.hist(df[var_col].dropna(), bins=30, edgecolor='black')
                    ax.set_xlabel(var_col)
                    ax.set_ylabel('Frequency')
                    ax.set_title(f"Histogram of {var_col}")
            
            plt.tight_layout()
            
            # 转换为图片
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            buf.seek(0)
            img_bytes = buf.read()
            buf.close()
            plt.close(fig)
            
            # 保存图表字节数据
            self.current_chart_bytes = img_bytes
            
            # 显示图表
            self._display_chart(img_bytes)
            self.btn_export.disabled = False
            self.btn_export.update()
            
            show_snackbar(self.main_window.page, "图表生成成功", "success")
            
        except Exception as ex:
            show_snackbar(
                self.main_window.page,
                f"生成图表失败: {str(ex)}",
                "error",
                duration=5000
            )
            self.chart_display.content = ft.Column(
                controls=[
                    ft.Text(
                        f"生成失败: {str(ex)}",
                        size=FONT_SIZES['md'],
                        color=FLUENT_COLORS['error'],
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
            self.chart_display.update()
        finally:
            # 恢复按钮状态
            self.btn_generate.text = "生成图表"
            self.btn_generate.disabled = False
            self.btn_generate.update()
    
    def _display_chart(self, img_bytes: bytes):
        """显示图表"""
        # 将图片转换为base64
        img_base64 = base64.b64encode(img_bytes).decode()
        
        # 创建图片控件
        chart_image = ft.Image(
            src_base64=img_base64,
            width=800,
            fit=ft.ImageFit.CONTAIN,
        )
        
        self.chart_image = chart_image
        
        # 更新显示区域
        self.chart_display.content = ft.Column(
            controls=[chart_image],
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True,
        )
        
        self.chart_display.update()
    
    def _export_chart(self, e):
        """导出图表"""
        if self.current_chart_bytes is None:
            show_snackbar(self.main_window.page, "没有可导出的图表", "error")
            return
        
        # 确保 FilePicker 已添加到页面 overlay
        if self.save_file_picker and self.save_file_picker not in self.main_window.page.overlay:
            self.main_window.page.overlay.append(self.save_file_picker)
            self.main_window.page.update()
        
        # 打开文件保存对话框
        if self.save_file_picker:
            self.save_file_picker.save_file(
                dialog_title="保存图表",
                file_name="chart.png",
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["png", "jpg", "pdf"],
            )
    
    def _handle_save_file(self, e: ft.FilePickerResultEvent):
        """处理文件保存"""
        if e.path and self.current_chart_bytes:
            try:
                if export_chart_image(self.current_chart_bytes, e.path):
                    show_snackbar(
                        self.main_window.page,
                        f"图表已保存到: {os.path.basename(e.path)}",
                        "success"
                    )
                else:
                    show_snackbar(
                        self.main_window.page,
                        "保存失败，请检查文件路径",
                        "error"
                    )
            except Exception as ex:
                show_snackbar(
                    self.main_window.page,
                    f"保存失败: {str(ex)}",
                    "error",
                    duration=5000
                )
    
    def on_data_changed(self):
        """数据变化时调用"""
        # 确保页面内容已创建，vars_area 已初始化
        if hasattr(self, 'vars_area') and self.vars_area is not None:
            self._update_vars_area()
