"""逐步回归分析UI控制"""
import flet as ft
import pandas as pd
from ui_flet.components.fluent_components import FluentButton, FluentDropdown
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES


class StatisticsUICorrelationStepwiseMixin:
    """逐步回归分析UI控制Mixin"""
    
    def _create_stepwise_regression_controls(self, df):
        """创建逐步回归控制"""
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
        
        y_dropdown = FluentDropdown(
            label="因变量（Y）",
            options=[ft.dropdown.Option(col) for col in numeric_cols],
            value=numeric_cols[-1] if numeric_cols else None,
            width=380,
        )
        self.control_area.controls.extend([y_dropdown])
        self.stepwise_y_dropdown = y_dropdown
        
        x_checkboxes = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Checkbox(value=(col != numeric_cols[-1])),
                        ft.Text(col, size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])
                    ],
                    spacing=SPACING['xs'],
                    tight=True,
                )
                for col in numeric_cols
            ],
            spacing=SPACING['xs'],
        )
        # 为每个Row添加label_text属性，方便后续访问
        for i, row in enumerate(x_checkboxes.controls):
            row.label_text = numeric_cols[i]
            row.checkbox = row.controls[0]
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
        self.control_area.controls.extend([direction_dropdown])
        self.stepwise_direction_dropdown = direction_dropdown
        
        btn_analyze = FluentButton(
            text="开始分析",
            on_click=self._run_stepwise_regression,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            y_dropdown,
            ft.Container(height=SPACING['md']),
            ft.Text(
                "自变量（X，可多选）",
                size=FONT_SIZES['md'],
                weight=ft.FontWeight.BOLD,
                color=FLUENT_COLORS['text_primary']
            ),
            x_checkboxes,
            ft.Container(height=SPACING['md']),
            direction_dropdown,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])

