"""
统计分析页面 - 结果显示方法
将_display_*方法提取到此模块
"""
import flet as ft
import pandas as pd
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, COMPONENT_SIZES


class StatisticsResultDisplayInferentialMixin:
    """结果显示方法Mixin - inferential"""

    def _display_t_test_result(self, result, test_name):
        """显示t检验结�?""
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
            stats_data = [
                ("t统计�?, result.get('t_statistic', 0)),
                ("p�?, result.get('p_value', 0)),
                ("自由�?, result.get('df', 0)),
            ]
            
            rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(key, size=FONT_SIZES['sm'])),
                        ft.DataCell(ft.Text(f"{val:.4f}" if isinstance(val, (int, float)) else str(val), size=FONT_SIZES['sm'])),
                    ]
                )
                for key, val in stats_data
            ]
            
            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("统计�?, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("�?, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                ],
                rows=rows,
                border=ft.border.all(1, FLUENT_COLORS['border']),
                border_radius=COMPONENT_SIZES['input_border_radius'],
            )
            
            self.result_area.controls.append(
                ft.Text(
                    test_name,
                    size=FONT_SIZES['lg'],
                    weight=ft.FontWeight.BOLD
                )
            )
            self.result_area.controls.append(ft.Container(height=SPACING['md']))
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
    

    def _display_chi_square_result(self, result):
        """显示卡方检验结�?""
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
            stats_data = [
                ("卡方统计�?, result.get('chi2', 0)),
                ("p�?, result.get('p_value', 0)),
                ("自由�?, result.get('df', 0)),
            ]
            
            rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(key, size=FONT_SIZES['sm'])),
                        ft.DataCell(ft.Text(f"{val:.4f}" if isinstance(val, (int, float)) else str(val), size=FONT_SIZES['sm'])),
                    ]
                )
                for key, val in stats_data
            ]
            
            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("统计�?, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("�?, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
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
    

    def _display_anova_result(self, result):
        """显示方差分析结果"""
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
            stats_data = [
                ("F统计�?, result.get('f_statistic', 0)),
                ("p�?, result.get('p_value', 0)),
            ]
            
            rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(key, size=FONT_SIZES['sm'])),
                        ft.DataCell(ft.Text(f"{val:.4f}" if isinstance(val, (int, float)) else str(val), size=FONT_SIZES['sm'])),
                    ]
                )
                for key, val in stats_data
            ]
            
            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("统计�?, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("�?, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
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
    

    def _display_mann_whitney_result(self, result):
        """显示Mann-Whitney检验结�?""
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
            stats_data = [
                ("U统计�?, result.get('u_statistic', 0)),
                ("p�?, result.get('p_value', 0)),
            ]
            
            rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(key, size=FONT_SIZES['sm'])),
                        ft.DataCell(ft.Text(f"{val:.4f}" if isinstance(val, (int, float)) else str(val), size=FONT_SIZES['sm'])),
                    ]
                )
                for key, val in stats_data
            ]
            
            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("统计�?, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("�?, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
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
    

    def _display_kruskal_wallis_result(self, result):
        """显示Kruskal-Wallis检验结�?""
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
            stats_data = [
                ("H统计�?, result.get('h_statistic', 0)),
                ("p�?, result.get('p_value', 0)),
            ]
            
            rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(key, size=FONT_SIZES['sm'])),
                        ft.DataCell(ft.Text(f"{val:.4f}" if isinstance(val, (int, float)) else str(val), size=FONT_SIZES['sm'])),
                    ]
                )
                for key, val in stats_data
            ]
            
            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("统计�?, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("�?, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
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
    

