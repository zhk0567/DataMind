"""
统计分析页面 - UI控制创建方法
将_create_*方法提取到此模块
"""
import flet as ft
import pandas as pd
from ui_flet.components.fluent_components import FluentButton, FluentDropdown, FluentTextField
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES


class StatisticsUIBasicMixin:
    """UI控制创建方法Mixin - basic"""

    def _create_descriptive_controls(self, df):
        """创建描述性统计控�?- 统一样式"""
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if not numeric_cols:
            self.control_area.controls.append(
                ft.Text(
                    "没有数值型变量",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_primary']
                )
            )
            return
        
        # 变量选择
        var_dropdown = FluentDropdown(
            label="选择变量",
            options=[ft.dropdown.Option(col) for col in numeric_cols],
            value=numeric_cols[0] if numeric_cols else None,
            width=380,
        )
        
        self.var_dropdown = var_dropdown
        
        # 分析按钮
        btn_analyze = FluentButton(
            text="开始分�?,
            on_click=self._run_descriptive_analysis,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            var_dropdown,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])
    

    def _create_frequency_controls(self, df):
        """创建频数分析控制"""
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if not categorical_cols:
            self.control_area.controls.append(
                ft.Text(
                    "没有分类型变�?,
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                )
            )
            return
        
        var_dropdown = FluentDropdown(
            label="选择变量",
            options=[ft.dropdown.Option(col) for col in categorical_cols],
            value=categorical_cols[0] if categorical_cols else None,
            width=380,
        )
        self.var_dropdown = var_dropdown
        
        btn_analyze = FluentButton(
            text="开始分�?,
            on_click=self._run_frequency_analysis,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            var_dropdown,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])
    

    def _create_crosstab_controls(self, df):
        """创建交叉表分析控�?""
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if len(categorical_cols) < 2:
            self.control_area.controls.append(
                ft.Text(
                    "至少需�?个分类型变量",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                )
            )
            return
        
        row_dropdown = FluentDropdown(
            label="行变�?,
            options=[ft.dropdown.Option(col) for col in categorical_cols],
            value=categorical_cols[0],
            width=380,
        )
        self.crosstab_row_dropdown = row_dropdown
        
        col_dropdown = FluentDropdown(
            label="列变�?,
            options=[ft.dropdown.Option(col) for col in categorical_cols],
            value=categorical_cols[1] if len(categorical_cols) > 1 else None,
            width=380,
        )
        self.crosstab_col_dropdown = col_dropdown
        
        btn_analyze = FluentButton(
            text="开始分�?,
            on_click=self._run_crosstab_analysis,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            row_dropdown,
            ft.Container(height=SPACING['md']),
            col_dropdown,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])
    

