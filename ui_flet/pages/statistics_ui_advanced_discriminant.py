"""
统计分析页面 - 高级分析UI控制 - 判别分析
"""
import flet as ft
import pandas as pd
from ui_flet.components.fluent_components import FluentButton, FluentDropdown, FluentTextField
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES


class StatisticsUIAdvancedDiscriminantMixin:
    """高级分析UI控制 - 判别分析"""

    def _create_discriminant_analysis_controls(self, df):
        """创建判别分析控制"""
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if not numeric_cols or not categorical_cols:
            self.control_area.controls.append(
                ft.Text(
                    "需要至少1个数值型变量和1个分类型变量",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                )
            )
            return
        
        y_dropdown = FluentDropdown(
            label="分组变量（Y）",
            options=[ft.dropdown.Option(col) for col in categorical_cols],
            value=categorical_cols[0] if categorical_cols else None,
            width=380,
        )
        self.discriminant_y_dropdown = y_dropdown
        
        x_checkboxes = ft.Column(
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
        for i, row in enumerate(x_checkboxes.controls):
            row.label_text = numeric_cols[i]
            row.checkbox = row.controls[0]
        self.discriminant_x_checkboxes = x_checkboxes
        
        btn_analyze = FluentButton(
            text="开始分析",
            on_click=self._run_discriminant_analysis,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            y_dropdown,
            ft.Container(height=SPACING['md']),
            ft.Text(
                "预测变量（X，可多选）",
                size=FONT_SIZES['md'],
                weight=ft.FontWeight.BOLD,
                color=FLUENT_COLORS['text_primary']
            ),
            x_checkboxes,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])

