"""
推断统计分析UI控制 - 单样本t检验
"""
import flet as ft
import pandas as pd
from ui_flet.components.fluent_components import FluentButton, FluentDropdown, FluentTextField
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES


class StatisticsUIInferentialTTestOneMixin:
    """推断统计分析UI控制 - 单样本t检验"""

    def _create_t_test_one_controls(self, df):
        """创建单样本t检验控制"""
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if not numeric_cols:
            self.control_area.controls.append(
                ft.Text(
                    "没有数值型变量",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                )
            )
            return
        
        var_dropdown = FluentDropdown(
            label="选择变量",
            options=[ft.dropdown.Option(col) for col in numeric_cols],
            value=numeric_cols[0] if numeric_cols else None,
            width=380,
        )
        self.var_dropdown = var_dropdown
        
        test_value_field = FluentTextField(
            label="检验值（默认0）",
            value="0",
            width=380,
        )
        self.test_value_field = test_value_field
        
        btn_analyze = FluentButton(
            text="开始分析",
            on_click=self._run_t_test_one,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            var_dropdown,
            ft.Container(height=SPACING['md']),
            test_value_field,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])

