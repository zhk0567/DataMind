"""
统计分析页面 - UI控制创建方法
将_create_*方法提取到此模块
"""
import flet as ft
import pandas as pd
from ui_flet.components.fluent_components import FluentButton, FluentDropdown, FluentTextField
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES


class StatisticsUIInferentialMixin:
    """UI控制创建方法Mixin - inferential"""

    def _create_t_test_one_controls(self, df):
        """创建单样本t检验控�?""
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
            label="检验值（默认0�?,
            value="0",
            width=380,
        )
        self.test_value_field = test_value_field
        
        btn_analyze = FluentButton(
            text="开始分�?,
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
    

    def _create_t_test_independent_controls(self, df):
        """创建独立样本t检验控�?""
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if not numeric_cols or not categorical_cols:
            self.control_area.controls.append(
                ft.Text(
                    "需要至�?个数值型变量�?个分类型变量",
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
        self.group_dropdown = group_dropdown
        
        value_dropdown = FluentDropdown(
            label="数值变�?,
            options=[ft.dropdown.Option(col) for col in numeric_cols],
            value=numeric_cols[0] if numeric_cols else None,
            width=380,
        )
        self.value_dropdown = value_dropdown
        
        btn_analyze = FluentButton(
            text="开始分�?,
            on_click=self._run_t_test_independent,
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
    

    def _create_t_test_paired_controls(self, df):
        """创建配对样本t检验控�?""
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if len(numeric_cols) < 2:
            self.control_area.controls.append(
                ft.Text(
                    "至少需�?个数值型变量",
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
            text="开始分�?,
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
    

    def _create_chi_square_controls(self, df):
        """创建卡方检验控�?""
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
            text="开始分�?,
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
    

    def _create_anova_controls(self, df):
        """创建方差分析控制"""
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if not numeric_cols or not categorical_cols:
            self.control_area.controls.append(
                ft.Text(
                    "需要至�?个数值型变量�?个分类型变量",
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
        self.anova_group_dropdown = group_dropdown
        
        value_dropdown = FluentDropdown(
            label="数值变�?,
            options=[ft.dropdown.Option(col) for col in numeric_cols],
            value=numeric_cols[0] if numeric_cols else None,
            width=380,
        )
        self.anova_value_dropdown = value_dropdown
        
        btn_analyze = FluentButton(
            text="开始分�?,
            on_click=self._run_anova,
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
    

    def _create_mann_whitney_controls(self, df):
        """创建Mann-Whitney检验控�?""
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if not numeric_cols or not categorical_cols:
            self.control_area.controls.append(
                ft.Text(
                    "需要至�?个数值型变量�?个分类型变量",
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
            label="数值变�?,
            options=[ft.dropdown.Option(col) for col in numeric_cols],
            value=numeric_cols[0] if numeric_cols else None,
            width=380,
        )
        self.mw_value_dropdown = value_dropdown
        
        btn_analyze = FluentButton(
            text="开始分�?,
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
    

    def _create_kruskal_wallis_controls(self, df):
        """创建Kruskal-Wallis检验控�?""
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if not numeric_cols or not categorical_cols:
            self.control_area.controls.append(
                ft.Text(
                    "需要至�?个数值型变量�?个分类型变量",
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
        self.kw_group_dropdown = group_dropdown
        
        value_dropdown = FluentDropdown(
            label="数值变�?,
            options=[ft.dropdown.Option(col) for col in numeric_cols],
            value=numeric_cols[0] if numeric_cols else None,
            width=380,
        )
        self.kw_value_dropdown = value_dropdown
        
        btn_analyze = FluentButton(
            text="开始分�?,
            on_click=self._run_kruskal_wallis,
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
    

