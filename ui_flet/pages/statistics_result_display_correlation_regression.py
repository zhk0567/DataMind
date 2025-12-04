"""
相关分析结果展示 - 回归分析
"""
import flet as ft
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, COMPONENT_SIZES


class StatisticsResultDisplayCorrelationRegressionMixin:
    """相关分析结果展示 - 回归分析"""

    def _display_regression_result(self, result: dict):
        """显示回归分析结果"""
        if 'r_squared' in result:
            # 显示主要统计量
            stats_data = [
                ("R²", result.get('r_squared', 0)),
                ("调整R²", result.get('adjusted_r_squared', 0)),
                ("F统计量", result.get('f_statistic', 0)),
                ("F p值", result.get('f_p_value', 0)),
            ]
            
            stats_rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(key, size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
                        ft.DataCell(ft.Text(f"{val:.4f}" if isinstance(val, (int, float)) else str(val), size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
                    ],
                    color=FLUENT_COLORS['bg_card']
                )
                for key, val in stats_data
            ]
            
            stats_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("统计量", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])),
                    ft.DataColumn(ft.Text("值", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])),
                ],
                rows=stats_rows,
                border=ft.border.all(1, FLUENT_COLORS['border']),
                border_radius=COMPONENT_SIZES['input_border_radius'],
                bgcolor=FLUENT_COLORS['bg_card'],
                heading_row_color=FLUENT_COLORS['bg_tertiary'],
                data_row_color={ft.ControlState.DEFAULT: FLUENT_COLORS['bg_card']},
            )
            
            self.result_area.controls.append(
                ft.Text(
                    "回归统计",
                    size=FONT_SIZES['lg'],
                    weight=ft.FontWeight.BOLD,
                    color=FLUENT_COLORS['text_primary']
                )
            )
            self.result_area.controls.append(ft.Container(height=SPACING['md']))
            self.result_area.controls.append(stats_table)
            
            # 显示系数
            if 'coefficients' in result:
                self.result_area.controls.append(ft.Container(height=SPACING['lg']))
                
                self.result_area.controls.append(
                    ft.Text(
                        "回归系数",
                        size=FONT_SIZES['lg'],
                        weight=ft.FontWeight.BOLD,
                        color=FLUENT_COLORS['text_primary']
                    )
                )
                self.result_area.controls.append(ft.Container(height=SPACING['md']))
                
                coeff_rows = []
                for var_name, coeff_data in result['coefficients'].items():
                    coeff_rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(var_name, size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
                                ft.DataCell(ft.Text(f"{coeff_data.get('coefficient', 0):.4f}", size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
                                ft.DataCell(ft.Text(f"{coeff_data.get('p_value', 0):.4f}", size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
                                ft.DataCell(
                                    ft.Text(
                                        "显著" if coeff_data.get('significant', False) else "不显著",
                                        size=FONT_SIZES['sm'],
                                        color=FLUENT_COLORS['success'] if coeff_data.get('significant', False) else FLUENT_COLORS['text_secondary']
                                    )
                                ),
                            ],
                            color=FLUENT_COLORS['bg_card']
                        )
                    )
                
                if coeff_rows:
                    coeff_table = ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("变量", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])),
                            ft.DataColumn(ft.Text("系数", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])),
                            ft.DataColumn(ft.Text("p值", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])),
                            ft.DataColumn(ft.Text("显著", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])),
                        ],
                        rows=coeff_rows,
                        border=ft.border.all(1, FLUENT_COLORS['border']),
                        border_radius=COMPONENT_SIZES['input_border_radius'],
                        bgcolor=FLUENT_COLORS['bg_card'],
                        heading_row_color=FLUENT_COLORS['bg_tertiary'],
                        data_row_color={ft.ControlState.DEFAULT: FLUENT_COLORS['bg_card']},
                    )
                    self.result_area.controls.append(coeff_table)
        else:
            self.result_area.controls.append(
                ft.Text(
                    "结果中缺少回归统计信息",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                )
            )

