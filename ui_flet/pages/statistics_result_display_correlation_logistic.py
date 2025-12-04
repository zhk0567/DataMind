"""
相关分析结果展示 - 逻辑回归
"""
import flet as ft
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, COMPONENT_SIZES


class StatisticsResultDisplayCorrelationLogisticMixin:
    """相关分析结果展示 - 逻辑回归"""

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
            # 显示主要统计量
            if 'accuracy' in result:
                self.result_area.controls.append(
                    ft.Text(
                        f"准确率: {result['accuracy']:.4f}",
                        size=FONT_SIZES['md'],
                        weight=ft.FontWeight.BOLD,
                        color=FLUENT_COLORS['text_primary']
                    )
                )
            
            # 显示系数
            if 'coefficients' in result:
                self.result_area.controls.append(ft.Container(height=SPACING['md']))
                
                self.result_area.controls.append(
                    ft.Text(
                        "回归系数",
                        size=FONT_SIZES['lg'],
                        weight=ft.FontWeight.BOLD,
                        color=FLUENT_COLORS['text_primary']
                    )
                )
                self.result_area.controls.append(ft.Container(height=SPACING['sm']))
                
                coeff_rows = []
                for var_name, coeff_value in result['coefficients'].items():
                    coeff_rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(var_name, size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
                                ft.DataCell(ft.Text(f"{coeff_value:.4f}", size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
                            ],
                            color=FLUENT_COLORS['bg_card']
                        )
                    )
                
                if coeff_rows:
                    coeff_table = ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("变量", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])),
                            ft.DataColumn(ft.Text("系数", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])),
                        ],
                        rows=coeff_rows,
                        border=ft.border.all(1, FLUENT_COLORS['border']),
                        border_radius=COMPONENT_SIZES['input_border_radius'],
                        bgcolor=FLUENT_COLORS['bg_card'],
                        heading_row_color=FLUENT_COLORS['bg_tertiary'],
                        data_row_color={ft.ControlState.DEFAULT: FLUENT_COLORS['bg_card']},
                    )
                    self.result_area.controls.append(coeff_table)
        
        self.btn_export.visible = True
        self.result_area.update()
        self.btn_export.update()
        
        # 确保页面更新以显示结果
        try:
            if hasattr(self.main_window, 'page'):
                self.main_window.page.update()
        except Exception:
            pass

