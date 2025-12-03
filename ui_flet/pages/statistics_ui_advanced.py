"""
统计分析页面 - UI控制创建方法
将_create_*方法提取到此模块
"""
import flet as ft
import pandas as pd
from ui_flet.components.fluent_components import FluentButton, FluentDropdown, FluentTextField
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES


class StatisticsUIAdvancedMixin:
    """UI控制创建方法Mixin - advanced"""

    def _create_pca_controls(self, df):
        """创建主成分分析控�?""
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
        
        var_checkboxes = ft.Column(
            controls=[
                ft.Checkbox(label=col, value=True)
                for col in numeric_cols[:15]
            ],
            spacing=SPACING['xs'],
        )
        self.pca_var_checkboxes = var_checkboxes
        
        n_components_field = FluentTextField(
            label="主成分数量（留空自动选择�?,
            value="",
            width=380,
        )
        self.pca_n_components_field = n_components_field
        
        btn_analyze = FluentButton(
            text="开始分�?,
            on_click=self._run_pca,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            ft.Text(
                "选择变量（可多选）�?,
                size=FONT_SIZES['md'],
                weight=ft.FontWeight.BOLD
            ),
            var_checkboxes,
            ft.Container(height=SPACING['md']),
            n_components_field,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])
    

    def _create_kmeans_controls(self, df):
        """创建K-means聚类控制"""
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
        
        var_checkboxes = ft.Column(
            controls=[
                ft.Checkbox(label=col, value=True)
                for col in numeric_cols[:15]
            ],
            spacing=SPACING['xs'],
        )
        self.kmeans_var_checkboxes = var_checkboxes
        
        n_clusters_field = FluentTextField(
            label="聚类数量",
            value="3",
            width=380,
        )
        self.kmeans_n_clusters_field = n_clusters_field
        
        btn_analyze = FluentButton(
            text="开始分�?,
            on_click=self._run_kmeans,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            ft.Text(
                "选择变量（可多选）�?,
                size=FONT_SIZES['md'],
                weight=ft.FontWeight.BOLD
            ),
            var_checkboxes,
            ft.Container(height=SPACING['md']),
            n_clusters_field,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])
    

    def _create_hierarchical_clustering_controls(self, df):
        """创建层次聚类控制"""
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
        
        var_checkboxes = ft.Column(
            controls=[
                ft.Checkbox(label=col, value=True)
                for col in numeric_cols[:15]
            ],
            spacing=SPACING['xs'],
        )
        self.hierarchical_var_checkboxes = var_checkboxes
        
        n_clusters_field = FluentTextField(
            label="聚类数量",
            value="3",
            width=380,
        )
        self.hierarchical_n_clusters_field = n_clusters_field
        
        linkage_dropdown = FluentDropdown(
            label="链接方法",
            options=[
                ft.dropdown.Option("ward", "Ward"),
                ft.dropdown.Option("complete", "完全链接"),
                ft.dropdown.Option("average", "平均链接"),
                ft.dropdown.Option("single", "单链�?),
            ],
            value="ward",
            width=380,
        )
        self.hierarchical_linkage_dropdown = linkage_dropdown
        
        btn_analyze = FluentButton(
            text="开始分�?,
            on_click=self._run_hierarchical_clustering,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            ft.Text(
                "选择变量（可多选）�?,
                size=FONT_SIZES['md'],
                weight=ft.FontWeight.BOLD
            ),
            var_checkboxes,
            ft.Container(height=SPACING['md']),
            n_clusters_field,
            ft.Container(height=SPACING['md']),
            linkage_dropdown,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])
    

    def _create_decision_tree_controls(self, df):
        """创建决策树分类控�?""
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
        
        y_dropdown = FluentDropdown(
            label="目标变量（Y�?,
            options=[ft.dropdown.Option(col) for col in categorical_cols],
            value=categorical_cols[0] if categorical_cols else None,
            width=380,
        )
        self.decision_tree_y_dropdown = y_dropdown
        
        x_checkboxes = ft.Column(
            controls=[
                ft.Checkbox(label=col, value=True)
                for col in numeric_cols[:10]
            ],
            spacing=SPACING['xs'],
        )
        self.decision_tree_x_checkboxes = x_checkboxes
        
        max_depth_field = FluentTextField(
            label="最大深度（留空不限制）",
            value="",
            width=380,
        )
        self.decision_tree_max_depth_field = max_depth_field
        
        btn_analyze = FluentButton(
            text="开始分�?,
            on_click=self._run_decision_tree,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            y_dropdown,
            ft.Container(height=SPACING['md']),
            ft.Text(
                "特征变量（X，可多选）�?,
                size=FONT_SIZES['md'],
                weight=ft.FontWeight.BOLD
            ),
            x_checkboxes,
            ft.Container(height=SPACING['md']),
            max_depth_field,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])
    

    def _create_factor_analysis_controls(self, df):
        """创建因子分析控制"""
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
        
        var_checkboxes = ft.Column(
            controls=[
                ft.Checkbox(label=col, value=True)
                for col in numeric_cols[:15]
            ],
            spacing=SPACING['xs'],
        )
        self.factor_var_checkboxes = var_checkboxes
        
        n_factors_field = FluentTextField(
            label="因子数量（留空自动选择�?,
            value="",
            width=380,
        )
        self.factor_n_factors_field = n_factors_field
        
        btn_analyze = FluentButton(
            text="开始分�?,
            on_click=self._run_factor_analysis,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            ft.Text(
                "选择变量（可多选）�?,
                size=FONT_SIZES['md'],
                weight=ft.FontWeight.BOLD
            ),
            var_checkboxes,
            ft.Container(height=SPACING['md']),
            n_factors_field,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])
    

    def _create_discriminant_analysis_controls(self, df):
        """创建判别分析控制"""
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
        
        y_dropdown = FluentDropdown(
            label="分组变量（Y�?,
            options=[ft.dropdown.Option(col) for col in categorical_cols],
            value=categorical_cols[0] if categorical_cols else None,
            width=380,
        )
        self.discriminant_y_dropdown = y_dropdown
        
        x_checkboxes = ft.Column(
            controls=[
                ft.Checkbox(label=col, value=True)
                for col in numeric_cols[:10]
            ],
            spacing=SPACING['xs'],
        )
        self.discriminant_x_checkboxes = x_checkboxes
        
        btn_analyze = FluentButton(
            text="开始分�?,
            on_click=self._run_discriminant_analysis,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            y_dropdown,
            ft.Container(height=SPACING['md']),
            ft.Text(
                "预测变量（X，可多选）�?,
                size=FONT_SIZES['md'],
                weight=ft.FontWeight.BOLD
            ),
            x_checkboxes,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])
    

