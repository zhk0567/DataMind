"""
统计分析页面 - 结果显示方法
将_display_*方法提取到此模块
"""
import flet as ft
import pandas as pd
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, COMPONENT_SIZES


class StatisticsResultDisplayBasicMixin:
    """结果显示方法Mixin - basic"""

    def _display_result(self, result: dict, analysis_type: str):
        """显示分析结果 - 统一样式"""
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
            # 格式化显示结�?
            if analysis_type == 'descriptive':
                self._display_descriptive_result(result)
            elif analysis_type == 'correlation':
                self._display_correlation_result(result)
            elif analysis_type == 'regression':
                self._display_regression_result(result)
        
        self.btn_export.visible = True
        self.result_area.update()
        self.btn_export.update()
        # 确保页面更新以显示结�?
        try:
            if hasattr(self.main_window, 'page'):
                self.main_window.page.update()
        except Exception:
            pass
    

    def _display_descriptive_result(self, result: dict):
        """显示描述性统计结�?- 统一样式"""
        if isinstance(result, dict) and len(result) > 0:
            # 获取第一个变量的结果
            var_name = list(result.keys())[0]
            stats = result[var_name]
            
            # 创建结果表格
            data_rows = []
            for key, value in stats.items():
                if isinstance(value, (int, float)):
                    data_rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(key), size=FONT_SIZES['sm'])),
                                ft.DataCell(ft.Text(f"{value:.4f}", size=FONT_SIZES['sm'])),
                            ]
                        )
                    )
            
            if data_rows:
                result_table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("统计�?, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                        ft.DataColumn(ft.Text("�?, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                    ],
                    rows=data_rows,
                    border=ft.border.all(1, FLUENT_COLORS['border']),
                    border_radius=COMPONENT_SIZES['input_border_radius'],
                )
                
                self.result_area.controls.append(
                    ft.Text(
                        f"变量: {var_name}",
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
                        "无有效统计数�?,
                        size=FONT_SIZES['md'],
                        color=FLUENT_COLORS['text_secondary']
                    )
                )
        else:
            self.result_area.controls.append(
                ft.Text(
                    "结果为空",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                )
            )
    

    def _display_frequency_result(self, result):
        """显示频数分析结果"""
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
            for col_name, freq_data in result.items():
                if isinstance(freq_data, dict) and 'frequency' in freq_data:
                    freq_df = freq_data['frequency']
                    
                    # 创建频数�?
                    rows = []
                    for idx, row in freq_df.iterrows():
                        rows.append(
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text(str(idx), size=FONT_SIZES['sm'])),
                                    ft.DataCell(ft.Text(str(row.iloc[0]), size=FONT_SIZES['sm'])),
                                ]
                            )
                        )
                    
                    table = ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("类别", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                            ft.DataColumn(ft.Text("频数", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                        ],
                        rows=rows,
                        border=ft.border.all(1, FLUENT_COLORS['border']),
                        border_radius=COMPONENT_SIZES['input_border_radius'],
                    )
                    
                    self.result_area.controls.append(
                        ft.Text(
                            f"变量: {col_name}",
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
    

    def _display_crosstab_result(self, result):
        """显示交叉表分析结�?""
        self.result_area.controls.clear()
        
        if 'error' in result:
            self.result_area.controls.append(
                ft.Text(
                    f"错误: {result['error']}",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['error']
                )
            )
        elif 'crosstab' in result:
            crosstab_df = result['crosstab']
            
            # 创建交叉�?
            rows = []
            for idx, row in crosstab_df.iterrows():
                cells = [
                    ft.DataCell(ft.Text(str(idx), size=FONT_SIZES['sm']))
                ]
                for val in row:
                    cells.append(ft.DataCell(ft.Text(str(val), size=FONT_SIZES['sm'])))
                rows.append(ft.DataRow(cells=cells))
            
            columns = [
                ft.DataColumn(ft.Text("", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD))
            ]
            for col in crosstab_df.columns:
                columns.append(ft.DataColumn(ft.Text(str(col), size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)))
            
            table = ft.DataTable(
                columns=columns,
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
    

