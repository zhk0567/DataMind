"""
推断统计分析结果展示 - t检验
"""
import flet as ft
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, COMPONENT_SIZES


class StatisticsResultDisplayInferentialTTestMixin:
    """推断统计分析t检验结果展示"""

    def _display_t_test_result(self, result, test_name):
        """显示t检验结果"""
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
                ("t统计量", result.get('t_statistic', 0)),
                ("p值", result.get('p_value', 0)),
                ("自由度", result.get('df', 0)),
            ]
            
            rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(key, size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
                        ft.DataCell(ft.Text(f"{val:.4f}" if isinstance(val, (int, float)) else str(val), size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
                    ],
                    color=FLUENT_COLORS['bg_card']
                )
                for key, val in stats_data
            ]
            
            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("统计量", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])),
                    ft.DataColumn(ft.Text("值", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])),
                ],
                rows=rows,
                border=ft.border.all(1, FLUENT_COLORS['border']),
                border_radius=COMPONENT_SIZES['input_border_radius'],
                bgcolor=FLUENT_COLORS['bg_card'],
                heading_row_color=FLUENT_COLORS['bg_tertiary'],
                data_row_color={ft.ControlState.DEFAULT: FLUENT_COLORS['bg_card']},
            )
            
            self.result_area.controls.append(
                ft.Text(
                    test_name,
                    size=FONT_SIZES['lg'],
                    weight=ft.FontWeight.BOLD,
                    color=FLUENT_COLORS['text_primary']
                )
            )
            self.result_area.controls.append(ft.Container(height=SPACING['md']))
            self.result_area.controls.append(table)
        
        self.btn_export.visible = True
        self.result_area.update()
        self.btn_export.update()
        
        # 确保页面更新以显示结果
        try:
            if hasattr(self.main_window, 'page'):
                self.main_window.page.update()
        except Exception:
            pass

