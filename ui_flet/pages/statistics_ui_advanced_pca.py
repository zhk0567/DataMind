"""
统计分析页面 - 高级分析UI控制 - 主成分分析
"""
import flet as ft
import pandas as pd
from ui_flet.components.fluent_components import FluentButton, FluentDropdown, FluentTextField
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES


class StatisticsUIAdvancedPCAMixin:
    """高级分析UI控制 - 主成分分析"""

    def _create_pca_controls(self, df):
        """创建主成分分析控制"""
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
                for col in numeric_cols[:15]
            ],
            spacing=SPACING['xs'],
        )
        # 为每个Row添加label_text属性，方便后续访问
        for i, row in enumerate(var_checkboxes.controls):
            row.label_text = numeric_cols[i]
            row.checkbox = row.controls[0]
        self.pca_var_checkboxes = var_checkboxes
        
        n_components_field = FluentTextField(
            label="主成分数量（留空自动选择）",
            value="",
            width=380,
        )
        self.pca_n_components_field = n_components_field
        
        btn_analyze = FluentButton(
            text="开始分析",
            on_click=self._run_pca,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            ft.Text(
                "选择变量（可多选）",
                size=FONT_SIZES['md'],
                weight=ft.FontWeight.BOLD,
                color=FLUENT_COLORS['text_primary']
            ),
            var_checkboxes,
            ft.Container(height=SPACING['md']),
            n_components_field,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])

