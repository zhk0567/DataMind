"""
统计分析页面 - 高级分析UI控制 - 层次聚类
"""
import flet as ft
import pandas as pd
from ui_flet.components.fluent_components import FluentButton, FluentDropdown, FluentTextField
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES


class StatisticsUIAdvancedHierarchicalMixin:
    """高级分析UI控制 - 层次聚类"""

    def _create_hierarchical_clustering_controls(self, df):
        """创建层次聚类控制"""
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
                ft.dropdown.Option("single", "单链接"),
            ],
            value="ward",
            width=380,
        )
        self.hierarchical_linkage_dropdown = linkage_dropdown
        
        btn_analyze = FluentButton(
            text="开始分析",
            on_click=self._run_hierarchical_clustering,
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
            n_clusters_field,
            ft.Container(height=SPACING['md']),
            linkage_dropdown,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])

