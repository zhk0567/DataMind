"""
统计分析页面 - 结果显示方法
将_display_*方法提取到此模块
"""
import flet as ft
import pandas as pd
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, COMPONENT_SIZES


class StatisticsResultDisplayAdvancedMixin:
    """结果显示方法Mixin - advanced"""

    def _display_pca_result(self, result):
        """显示主成分分析结�?""
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
                        "主成分方差解释比�?,
                        size=FONT_SIZES['lg'],
                        weight=ft.FontWeight.BOLD
                    )
                )
                self.result_area.controls.append(ft.Container(height=SPACING['sm']))
                
                rows = []
                for i, ratio in enumerate(result['explained_variance_ratio'], 1):
                    rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(f"PC{i}", size=FONT_SIZES['sm'])),
                                ft.DataCell(ft.Text(f"{ratio:.4f}", size=FONT_SIZES['sm'])),
                            ]
                        )
                    )
                
                table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("主成�?, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                        ft.DataColumn(ft.Text("方差解释比例", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                    ],
                    rows=rows,
                    border=ft.border.all(1, FLUENT_COLORS['border']),
                    border_radius=COMPONENT_SIZES['input_border_radius'],
                )
                self.result_area.controls.append(table)
        
        self.btn_export.visible = True
        self.result_area.update()
        self.btn_export.update()
        # 确保页面更新以显示结�?
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
                        weight=ft.FontWeight.BOLD
                    )
                )
            
            if 'inertia' in result:
                self.result_area.controls.append(
                    ft.Text(
                        f"簇内平方�? {result['inertia']:.4f}",
                        size=FONT_SIZES['md']
                    )
                )
        
        self.btn_export.visible = True
        self.result_area.update()
        self.btn_export.update()
        # 确保页面更新以显示结�?
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
                        weight=ft.FontWeight.BOLD
                    )
                )
        
        self.btn_export.visible = True
        self.result_area.update()
        self.btn_export.update()
        # 确保页面更新以显示结�?
        try:
            if hasattr(self.main_window, 'page'):
                self.main_window.page.update()
        except Exception:
            pass
    

    def _display_decision_tree_result(self, result):
        """显示决策树分类结�?""
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
                        f"准确�? {result['accuracy']:.4f}",
                        size=FONT_SIZES['md'],
                        weight=ft.FontWeight.BOLD
                    )
                )
        
        self.btn_export.visible = True
        self.result_area.update()
        self.btn_export.update()
        # 确保页面更新以显示结�?
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
                        weight=ft.FontWeight.BOLD
                    )
                )
        
        self.btn_export.visible = True
        self.result_area.update()
        self.btn_export.update()
        # 确保页面更新以显示结�?
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
                        f"准确�? {result['accuracy']:.4f}",
                        size=FONT_SIZES['md'],
                        weight=ft.FontWeight.BOLD
                    )
                )
        
        self.btn_export.visible = True
        self.result_area.update()
        self.btn_export.update()
        # 确保页面更新以显示结�?
        try:
            if hasattr(self.main_window, 'page'):
                self.main_window.page.update()
        except Exception:
            pass
    
    # ========== 时间序列分析控制方法 ==========
    

