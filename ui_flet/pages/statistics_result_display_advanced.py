"""
统计分析页面 - 高级分析结果展示
"""
import flet as ft
import pandas as pd
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, COMPONENT_SIZES


class StatisticsResultDisplayAdvancedMixin:
    """高级分析结果展示Mixin"""

    def _display_pca_result(self, result):
        """显示主成分分析结果"""
        self.result_area.controls.clear()
        
        if 'error' in result:
            self.result_area.controls.append(
                ft.Text(
                    f"错误: {result['error']}",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['error']
                )
            )
        else:
            if 'explained_variance_ratio' in result:
                self.result_area.controls.append(
                    ft.Text(
                        "主成分方差解释比例",
                        size=FONT_SIZES['lg'],
                        weight=ft.FontWeight.BOLD,
                        color=FLUENT_COLORS['text_primary']
                    )
                )
                self.result_area.controls.append(ft.Container(height=SPACING['sm']))
                
                rows = []
                for i, ratio in enumerate(result['explained_variance_ratio'], 1):
                    rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(f"PC{i}", size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
                                ft.DataCell(ft.Text(f"{ratio:.4f}", size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
                            ],
                            color=FLUENT_COLORS['bg_card']
                        )
                    )
                
                table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("主成分", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])),
                        ft.DataColumn(ft.Text("方差解释比例", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])),
                    ],
                    rows=rows,
                    border=ft.border.all(1, FLUENT_COLORS['border']),
                    border_radius=COMPONENT_SIZES['input_border_radius'],
                    bgcolor=FLUENT_COLORS['bg_card'],
                    heading_row_color=FLUENT_COLORS['bg_tertiary'],
                    data_row_color={ft.ControlState.DEFAULT: FLUENT_COLORS['bg_card']},
                )
                self.result_area.controls.append(table)
        
        self.btn_export.visible = True
        self.result_area.update()
        self.btn_export.update()
        
        try:
            if hasattr(self.main_window, 'page'):
                self.main_window.page.update()
        except Exception:
            pass

    def _display_kmeans_result(self, result):
        """显示K-means聚类结果"""
        self.result_area.controls.clear()
        
        if 'error' in result:
            self.result_area.controls.append(
                ft.Text(
                    f"错误: {result['error']}",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['error']
                )
            )
        else:
            if 'n_clusters' in result:
                self.result_area.controls.append(
                    ft.Text(
                        f"聚类数量: {result['n_clusters']}",
                        size=FONT_SIZES['md'],
                        weight=ft.FontWeight.BOLD,
                        color=FLUENT_COLORS['text_primary']
                    )
                )
            
            if 'inertia' in result:
                self.result_area.controls.append(
                    ft.Text(
                        f"簇内平方和: {result['inertia']:.4f}",
                        size=FONT_SIZES['md'],
                        color=FLUENT_COLORS['text_primary']
                    )
                )
        
        self.btn_export.visible = True
        self.result_area.update()
        self.btn_export.update()
        
        try:
            if hasattr(self.main_window, 'page'):
                self.main_window.page.update()
        except Exception:
            pass

    def _display_hierarchical_clustering_result(self, result):
        """显示层次聚类结果"""
        self.result_area.controls.clear()
        
        if 'error' in result:
            self.result_area.controls.append(
                ft.Text(
                    f"错误: {result['error']}",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['error']
                )
            )
        else:
            if 'n_clusters' in result:
                self.result_area.controls.append(
                    ft.Text(
                        f"聚类数量: {result['n_clusters']}",
                        size=FONT_SIZES['md'],
                        weight=ft.FontWeight.BOLD,
                        color=FLUENT_COLORS['text_primary']
                    )
                )
        
        self.btn_export.visible = True
        self.result_area.update()
        self.btn_export.update()
        
        try:
            if hasattr(self.main_window, 'page'):
                self.main_window.page.update()
        except Exception:
            pass

    def _display_decision_tree_result(self, result):
        """显示决策树分类结果"""
        self.result_area.controls.clear()
        
        if 'error' in result:
            self.result_area.controls.append(
                ft.Text(
                    f"错误: {result['error']}",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['error']
                )
            )
        else:
            if 'accuracy' in result:
                self.result_area.controls.append(
                    ft.Text(
                        f"准确率: {result['accuracy']:.4f}",
                        size=FONT_SIZES['md'],
                        weight=ft.FontWeight.BOLD,
                        color=FLUENT_COLORS['text_primary']
                    )
                )
        
        self.btn_export.visible = True
        self.result_area.update()
        self.btn_export.update()
        
        try:
            if hasattr(self.main_window, 'page'):
                self.main_window.page.update()
        except Exception:
            pass

    def _display_factor_analysis_result(self, result):
        """显示因子分析结果"""
        self.result_area.controls.clear()
        
        if 'error' in result:
            self.result_area.controls.append(
                ft.Text(
                    f"错误: {result['error']}",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['error']
                )
            )
        else:
            if 'n_factors' in result:
                self.result_area.controls.append(
                    ft.Text(
                        f"因子数量: {result['n_factors']}",
                        size=FONT_SIZES['md'],
                        weight=ft.FontWeight.BOLD,
                        color=FLUENT_COLORS['text_primary']
                    )
                )
        
        self.btn_export.visible = True
        self.result_area.update()
        self.btn_export.update()
        
        try:
            if hasattr(self.main_window, 'page'):
                self.main_window.page.update()
        except Exception:
            pass

    def _display_discriminant_analysis_result(self, result):
        """显示判别分析结果"""
        self.result_area.controls.clear()
        
        if 'error' in result:
            self.result_area.controls.append(
                ft.Text(
                    f"错误: {result['error']}",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['error']
                )
            )
        else:
            if 'accuracy' in result:
                self.result_area.controls.append(
                    ft.Text(
                        f"准确率: {result['accuracy']:.4f}",
                        size=FONT_SIZES['md'],
                        weight=ft.FontWeight.BOLD,
                        color=FLUENT_COLORS['text_primary']
                    )
                )
        
        self.btn_export.visible = True
        self.result_area.update()
        self.btn_export.update()
        
        try:
            if hasattr(self.main_window, 'page'):
                self.main_window.page.update()
        except Exception:
            pass
