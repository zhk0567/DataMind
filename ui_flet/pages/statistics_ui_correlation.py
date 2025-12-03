"""
统计分析页面 - UI控制创建方法
将_create_*方法提取到此模块
"""
import flet as ft
import pandas as pd
from ui_flet.components.fluent_components import FluentButton, FluentDropdown, FluentTextField
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES


class StatisticsUICorrelationMixin:
    """UI控制创建方法Mixin - correlation"""

    def _create_correlation_controls(self, df):
        """创建相关分析控制 - 统一样式"""
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if len(numeric_cols) < 2:
            self.control_area.controls.append(
                ft.Text(
                    "至少需�?个数值型变量",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                )
            )
            return
        
        # 多选变�?
        var_checkboxes = ft.Column(
            controls=[
                ft.Checkbox(label=col, value=True)
                for col in numeric_cols[:10]  # 最多显�?0�?
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
            text="开始分�?,
            on_click=self._run_correlation_analysis,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            ft.Text(
                "选择变量（至�?个）�?,
                size=FONT_SIZES['md'],
                weight=ft.FontWeight.BOLD
            ),
            var_checkboxes,
            ft.Container(height=SPACING['md']),
            method_dropdown,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])
    

    def _create_partial_correlation_controls(self, df):
        """创建偏相关分析控�?""
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if len(numeric_cols) < 3:
            self.control_area.controls.append(
                ft.Text(
                    "至少需�?个数值型变量",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                )
            )
            return
        
        x_dropdown = FluentDropdown(
            label="X变量",
            options=[ft.dropdown.Option(col) for col in numeric_cols],
            value=numeric_cols[0] if numeric_cols else None,
            width=380,
        )
        self.partial_x_dropdown = x_dropdown
        
        y_dropdown = FluentDropdown(
            label="Y变量",
            options=[ft.dropdown.Option(col) for col in numeric_cols],
            value=numeric_cols[1] if len(numeric_cols) > 1 else None,
            width=380,
        )
        self.partial_y_dropdown = y_dropdown
        
        control_checkboxes = ft.Column(
            controls=[
                ft.Checkbox(label=col, value=False)
                for col in numeric_cols[:10]
            ],
            spacing=SPACING['xs'],
        )
        self.partial_control_checkboxes = control_checkboxes
        
        btn_analyze = FluentButton(
            text="开始分�?,
            on_click=self._run_partial_correlation,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            x_dropdown,
            ft.Container(height=SPACING['md']),
            y_dropdown,
            ft.Container(height=SPACING['md']),
            ft.Text(
                "控制变量（可多选）�?,
                size=FONT_SIZES['md'],
                weight=ft.FontWeight.BOLD
            ),
            control_checkboxes,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])
    

    def _create_regression_controls(self, df):
        """创建回归分析控制 - 统一样式"""
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if len(numeric_cols) < 2:
            self.control_area.controls.append(
                ft.Text(
                    "至少需�?个数值型变量",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                )
            )
            return
        
        # 因变量选择
        y_dropdown = FluentDropdown(
            label="因变量（Y�?,
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
            text="开始分�?,
            on_click=self._run_regression_analysis,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            y_dropdown,
            ft.Container(height=SPACING['md']),
            ft.Text(
                "自变量（X，可多选）�?,
                size=FONT_SIZES['md'],
                weight=ft.FontWeight.BOLD
            ),
            x_checkboxes,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])
    

    def _create_stepwise_regression_controls(self, df):
        """创建逐步回归控制"""
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if len(numeric_cols) < 2:
            self.control_area.controls.append(
                ft.Text(
                    "至少需�?个数值型变量",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                )
            )
            return
        
        y_dropdown = FluentDropdown(
            label="因变量（Y�?,
            options=[ft.dropdown.Option(col) for col in numeric_cols],
            value=numeric_cols[-1] if numeric_cols else None,
            width=380,
        )
        self.stepwise_y_dropdown = y_dropdown
        
        x_checkboxes = ft.Column(
            controls=[
                ft.Checkbox(label=col, value=(col != numeric_cols[-1]))
                for col in numeric_cols
            ],
            spacing=SPACING['xs'],
        )
        self.stepwise_x_checkboxes = x_checkboxes
        
        direction_dropdown = FluentDropdown(
            label="方向",
            options=[
                ft.dropdown.Option("forward", "向前"),
                ft.dropdown.Option("backward", "向后"),
                ft.dropdown.Option("both", "双向"),
            ],
            value="forward",
            width=380,
        )
        self.stepwise_direction_dropdown = direction_dropdown
        
        btn_analyze = FluentButton(
            text="开始分�?,
            on_click=self._run_stepwise_regression,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            y_dropdown,
            ft.Container(height=SPACING['md']),
            ft.Text(
                "自变量（X，可多选）�?,
                size=FONT_SIZES['md'],
                weight=ft.FontWeight.BOLD
            ),
            x_checkboxes,
            ft.Container(height=SPACING['md']),
            direction_dropdown,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])
    

    def _create_logistic_regression_controls(self, df):
        """创建逻辑回归控制"""
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if not numeric_cols or not categorical_cols:
            self.control_area.controls.append(
                ft.Text(
                    "需要至�?个数值型变量�?个分类型变量",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                )
            )
            return
        
        y_dropdown = FluentDropdown(
            label="因变量（Y，二分类�?,
            options=[ft.dropdown.Option(col) for col in categorical_cols],
            value=categorical_cols[0] if categorical_cols else None,
            width=380,
        )
        self.logistic_y_dropdown = y_dropdown
        
        x_checkboxes = ft.Column(
            controls=[
                ft.Checkbox(label=col, value=True)
                for col in numeric_cols[:10]
            ],
            spacing=SPACING['xs'],
        )
        self.logistic_x_checkboxes = x_checkboxes
        
        btn_analyze = FluentButton(
            text="开始分�?,
            on_click=self._run_logistic_regression,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            y_dropdown,
            ft.Container(height=SPACING['md']),
            ft.Text(
                "自变量（X，可多选）�?,
                size=FONT_SIZES['md'],
                weight=ft.FontWeight.BOLD
            ),
            x_checkboxes,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])
    

