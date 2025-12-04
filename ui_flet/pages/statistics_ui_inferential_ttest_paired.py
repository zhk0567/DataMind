"""
推断统计分析UI控制 - 配对样本t检验
"""
import flet as ft
import pandas as pd
from ui_flet.components.fluent_components import FluentButton, FluentDropdown, FluentTextField
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES


class StatisticsUIInferentialTTestPairedMixin:
    """推断统计分析UI控制 - 配对样本t检验"""

    def _create_t_test_paired_controls(self, df):
        """创建配对样本t检验控制"""
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
        
        col1_dropdown = FluentDropdown(
            label="变量1",
            options=[ft.dropdown.Option(col) for col in numeric_cols],
            value=numeric_cols[0] if numeric_cols else None,
            width=380,
        )
        self.paired_col1_dropdown = col1_dropdown
        
        col2_dropdown = FluentDropdown(
            label="变量2",
            options=[ft.dropdown.Option(col) for col in numeric_cols],
            value=numeric_cols[1] if len(numeric_cols) > 1 else None,
            width=380,
        )
        self.paired_col2_dropdown = col2_dropdown
        
        btn_analyze = FluentButton(
            text="开始分析",
            on_click=self._run_t_test_paired,
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

