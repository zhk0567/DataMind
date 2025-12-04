"""偏相关分析UI控制"""
import flet as ft
import pandas as pd
from ui_flet.components.fluent_components import FluentButton, FluentDropdown
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES


class StatisticsUICorrelationPartialMixin:
    """偏相关分析UI控制Mixin"""
    
    def _create_partial_correlation_controls(self, df):
        """创建偏相关分析控制"""
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if len(numeric_cols) < 3:
            self.control_area.controls.append(
                ft.Text(
                    "至少需要3个数值型变量",
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
        self.control_area.controls.extend([x_dropdown])
        self.partial_x_dropdown = x_dropdown
        
        y_dropdown = FluentDropdown(
            label="Y变量",
            options=[ft.dropdown.Option(col) for col in numeric_cols],
            value=numeric_cols[1] if len(numeric_cols) > 1 else None,
            width=380,
        )
        self.control_area.controls.extend([y_dropdown])
        self.partial_y_dropdown = y_dropdown
        
        control_checkboxes = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Checkbox(value=False),
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
        for i, row in enumerate(control_checkboxes.controls):
            row.label_text = numeric_cols[i]
            row.checkbox = row.controls[0]
        self.control_area.controls.extend([control_checkboxes])
        self.partial_control_checkboxes = control_checkboxes
        
        btn_analyze = FluentButton(
            text="开始分析",
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
                "控制变量（可多选）",
                size=FONT_SIZES['md'],
                weight=ft.FontWeight.BOLD,
                color=FLUENT_COLORS['text_primary']
            ),
            control_checkboxes,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])

