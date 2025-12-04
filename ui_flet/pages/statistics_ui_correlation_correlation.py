"""相关分析UI控制"""
import flet as ft
import pandas as pd
from ui_flet.components.fluent_components import FluentButton, FluentDropdown
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES


class StatisticsUICorrelationCorrelationMixin:
    """相关分析UI控制Mixin"""
    
    def _create_correlation_controls(self, df):
        """创建相关分析控制"""
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
        
        var_checkboxes = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Checkbox(value=True),
                        ft.Text(col, size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])
                    ],
                    spacing=SPACING['xs'],
                    tight=True,
                )
                for col in numeric_cols[:10]
            ],
            spacing=SPACING['xs'],
        )
        # 为每个Row添加label_text属性，方便后续访问
        for i, row in enumerate(var_checkboxes.controls):
            row.label_text = numeric_cols[i]
            row.checkbox = row.controls[0]
        self.correlation_var_checkboxes = var_checkboxes
        
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
        
        self.control_area.controls.extend([
            ft.Text(
                "选择变量（至少2个）",
                size=FONT_SIZES['md'],
                weight=ft.FontWeight.BOLD,
                color=FLUENT_COLORS['text_primary']
            ),
            var_checkboxes,
            ft.Container(height=SPACING['md']),
            method_dropdown,
            ft.Container(height=SPACING['lg']),
        ])
        self.method_dropdown = method_dropdown
        
        btn_analyze = FluentButton(
            text="开始分析",
            on_click=self._run_correlation_analysis,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            btn_analyze,
        ])

