"""
统计分析页面 - 结果显示方法
将_display_*方法提取到此模块
"""
import flet as ft
import pandas as pd
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, COMPONENT_SIZES


class StatisticsResultDisplayCorrelationMixin:
    """结果显示方法Mixin - correlation"""

    def _display_correlation_result(self, result: dict):
        """显示相关分析结果 - 统一样式"""
        if 'correlation_matrix' in result:
            corr_matrix = result['correlation_matrix']
            if isinstance(corr_matrix, pd.DataFrame):
                # 创建相关矩阵表格
                columns = corr_matrix.columns.tolist()
                data_rows = []
                
                for idx, row in corr_matrix.iterrows():
                    cells = [
                        ft.DataCell(ft.Text(f"{val:.4f}" if isinstance(val, (int, float)) else str(val)[:8], size=FONT_SIZES['sm']))
                        for val in row
                    ]
                    data_rows.append(ft.DataRow(cells=cells))
                
                if data_rows:
                    result_table = ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text(col, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD))
                            for col in columns
                        ],
                        rows=data_rows,
                        border=ft.border.all(1, FLUENT_COLORS['border']),
                        border_radius=COMPONENT_SIZES['input_border_radius'],
                    )
                    
                    self.result_area.controls.append(
                        ft.Text(
                            "相关矩阵",
                            size=FONT_SIZES['lg'],
                            weight=ft.FontWeight.BOLD
                        )
                    )
                    self.result_area.controls.append(
                        ft.Container(height=SPACING['md'])
                    )
                    self.result_area.controls.append(result_table)
                else:
                    self.result_area.controls.append(
                        ft.Text(
                            "相关矩阵为空",
                            size=FONT_SIZES['md'],
                            color=FLUENT_COLORS['text_secondary']
                        )
                    )
            else:
                self.result_area.controls.append(
                    ft.Text(
                        "相关矩阵格式错误",
                        size=FONT_SIZES['md'],
                        color=FLUENT_COLORS['text_secondary']
                    )
                )
        else:
            self.result_area.controls.append(
                ft.Text(
                    "结果中缺少相关矩�?,
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                )
            )
    

    def _display_partial_correlation_result(self, result):
        """显示偏相关分析结�?""
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
            corr_value = result.get('partial_correlation', 0)
            p_value = result.get('p_value', 0)
            
            self.result_area.controls.append(
                ft.Text(
                    f"偏相关系�? {corr_value:.4f}",
                    size=FONT_SIZES['md'],
                    weight=ft.FontWeight.BOLD
                )
            )
            self.result_area.controls.append(
                ft.Text(
                    f"p�? {p_value:.4f}",
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
    

    def _display_regression_result(self, result: dict):
        """显示回归分析结果 - 统一样式"""
        if 'r_squared' in result:
            # 显示主要统计�?
            stats_data = [
                ("R²", result.get('r_squared', 0)),
                ("调整R²", result.get('adjusted_r_squared', 0)),
                ("F统计�?, result.get('f_statistic', 0)),
                ("F p�?, result.get('f_p_value', 0)),
            ]
            
            stats_rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(key, size=FONT_SIZES['sm'])),
                        ft.DataCell(ft.Text(f"{val:.4f}" if isinstance(val, (int, float)) else str(val), size=FONT_SIZES['sm'])),
                    ]
                )
                for key, val in stats_data
            ]
            
            stats_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("统计�?, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("�?, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                ],
                rows=stats_rows,
                border=ft.border.all(1, FLUENT_COLORS['border']),
                border_radius=COMPONENT_SIZES['input_border_radius'],
            )
            
            self.result_area.controls.append(
                ft.Text(
                    "回归统计",
                    size=FONT_SIZES['lg'],
                    weight=ft.FontWeight.BOLD
                )
            )
            self.result_area.controls.append(
                ft.Container(height=SPACING['md'])
            )
            self.result_area.controls.append(stats_table)
            
            # 显示系数
            if 'coefficients' in result:
                self.result_area.controls.append(
                    ft.Container(height=SPACING['lg'])
                )
                self.result_area.controls.append(
                    ft.Text(
                        "回归系数",
                        size=FONT_SIZES['lg'],
                        weight=ft.FontWeight.BOLD
                    )
                )
                self.result_area.controls.append(
                    ft.Container(height=SPACING['md'])
                )
                
                coeff_rows = []
                for var_name, coeff_data in result['coefficients'].items():
                    coeff_rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(var_name, size=FONT_SIZES['sm'])),
                                ft.DataCell(ft.Text(f"{coeff_data.get('coefficient', 0):.4f}", size=FONT_SIZES['sm'])),
                                ft.DataCell(ft.Text(f"{coeff_data.get('p_value', 0):.4f}", size=FONT_SIZES['sm'])),
                                ft.DataCell(
                                    ft.Text(
                                        "�? if coeff_data.get('significant', False) else "�?,
                                        size=FONT_SIZES['sm'],
                                        color=FLUENT_COLORS['success'] if coeff_data.get('significant', False) else FLUENT_COLORS['text_secondary']
                                    )
                                ),
                            ]
                        )
                    )
                
                if coeff_rows:
                    coeff_table = ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("变量", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                            ft.DataColumn(ft.Text("系数", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                            ft.DataColumn(ft.Text("p�?, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                            ft.DataColumn(ft.Text("显著", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                        ],
                        rows=coeff_rows,
                        border=ft.border.all(1, FLUENT_COLORS['border']),
                        border_radius=COMPONENT_SIZES['input_border_radius'],
                    )
                    self.result_area.controls.append(coeff_table)
        else:
            self.result_area.controls.append(
                ft.Text(
                    "结果中缺少回归统计信�?,
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                )
            )
    

    def _display_logistic_regression_result(self, result):
        """显示逻辑回归结果"""
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
            # 显示主要统计�?
            if 'accuracy' in result:
                self.result_area.controls.append(
                    ft.Text(
                        f"准确�? {result['accuracy']:.4f}",
                        size=FONT_SIZES['md'],
                        weight=ft.FontWeight.BOLD
                    )
                )
            
            # 显示系数
            if 'coefficients' in result:
                self.result_area.controls.append(ft.Container(height=SPACING['md']))
                self.result_area.controls.append(
                    ft.Text(
                        "回归系数",
                        size=FONT_SIZES['lg'],
                        weight=ft.FontWeight.BOLD
                    )
                )
                self.result_area.controls.append(ft.Container(height=SPACING['sm']))
                
                coeff_rows = []
                for var_name, coeff_value in result['coefficients'].items():
                    coeff_rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(var_name, size=FONT_SIZES['sm'])),
                                ft.DataCell(ft.Text(f"{coeff_value:.4f}", size=FONT_SIZES['sm'])),
                            ]
                        )
                    )
                
                if coeff_rows:
                    coeff_table = ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("变量", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                            ft.DataColumn(ft.Text("系数", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                        ],
                        rows=coeff_rows,
                        border=ft.border.all(1, FLUENT_COLORS['border']),
                        border_radius=COMPONENT_SIZES['input_border_radius'],
                    )
                    self.result_area.controls.append(coeff_table)
        
        self.btn_export.visible = True
        self.result_area.update()
        self.btn_export.update()
        # 确保页面更新以显示结�?
        try:
            if hasattr(self.main_window, 'page'):
                self.main_window.page.update()
        except Exception:
            pass
    

