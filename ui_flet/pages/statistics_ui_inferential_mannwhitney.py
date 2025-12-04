"""
推断统计分析UI控制 - Mann-Whitney检验
"""
import flet as ft
import pandas as pd
from ui_flet.components.fluent_components import FluentButton, FluentDropdown, FluentTextField
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES


class StatisticsUIInferentialMannWhitneyMixin:
    """推断统计分析UI控制 - Mann-Whitney检验"""

    def _create_mann_whitney_controls(self, df):
        """创建Mann-Whitney检验控制"""
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
        
        group_dropdown = FluentDropdown(
            label="分组变量",
            options=[ft.dropdown.Option(col) for col in categorical_cols],
            value=categorical_cols[0] if categorical_cols else None,
            width=380,
        )
        self.mw_group_dropdown = group_dropdown
        
        value_dropdown = FluentDropdown(
            label="数值变量",
            options=[ft.dropdown.Option(col) for col in numeric_cols],
            value=numeric_cols[0] if numeric_cols else None,
            width=380,
        )
        self.mw_value_dropdown = value_dropdown
        
        btn_analyze = FluentButton(
            text="开始分析",
            on_click=self._run_mann_whitney,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            group_dropdown,
            ft.Container(height=SPACING['md']),
            value_dropdown,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])

