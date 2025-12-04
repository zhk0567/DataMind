"""
推断统计分析UI控制 - 卡方检验
"""
import flet as ft
import pandas as pd
from ui_flet.components.fluent_components import FluentButton, FluentDropdown, FluentTextField
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES


class StatisticsUIInferentialChiSquareMixin:
    """推断统计分析UI控制 - 卡方检验"""

    def _create_chi_square_controls(self, df):
        """创建卡方检验控制"""
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if len(categorical_cols) < 2:
            self.control_area.controls.append(
                ft.Text(
                    "至少需要2个分类型变量",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                )
            )
            return
        
        col1_dropdown = FluentDropdown(
            label="变量1",
            options=[ft.dropdown.Option(col) for col in categorical_cols],
            value=categorical_cols[0] if categorical_cols else None,
            width=380,
        )
        self.chi_col1_dropdown = col1_dropdown
        
        col2_dropdown = FluentDropdown(
            label="变量2",
            options=[ft.dropdown.Option(col) for col in categorical_cols],
            value=categorical_cols[1] if len(categorical_cols) > 1 else None,
            width=380,
        )
        self.chi_col2_dropdown = col2_dropdown
        
        btn_analyze = FluentButton(
            text="开始分析",
            on_click=self._run_chi_square,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            col1_dropdown,
            ft.Container(height=SPACING['md']),
            col2_dropdown,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])

