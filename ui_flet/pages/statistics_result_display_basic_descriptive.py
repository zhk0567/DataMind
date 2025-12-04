"""
基本统计分析结果展示 - 描述性统计
"""
import flet as ft
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, COMPONENT_SIZES


class StatisticsResultDisplayBasicDescriptiveMixin:
    """基本统计分析结果展示 - 描述性统计"""

    def _display_descriptive_result(self, result: dict):
        """显示描述性统计结果"""
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
                                ft.DataCell(ft.Text(str(key), size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
                                ft.DataCell(ft.Text(f"{value:.4f}", size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
                            ],
                            color=FLUENT_COLORS['bg_card']
                        )
                    )
            
            if data_rows:
                result_table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("统计量", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])),
                        ft.DataColumn(ft.Text("值", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])),
                    ],
                    rows=data_rows,
                    border=ft.border.all(1, FLUENT_COLORS['border']),
                    border_radius=COMPONENT_SIZES['input_border_radius'],
                    bgcolor=FLUENT_COLORS['bg_card'],
                    heading_row_color=FLUENT_COLORS['bg_tertiary'],
                    data_row_color={ft.ControlState.DEFAULT: FLUENT_COLORS['bg_card']},
                )
                
                self.result_area.controls.append(
                    ft.Text(
                        f"变量: {var_name}",
                        size=FONT_SIZES['lg'],
                        weight=ft.FontWeight.BOLD,
                        color=FLUENT_COLORS['text_primary']
                    )
                )
                self.result_area.controls.append(ft.Container(height=SPACING['md']))
                self.result_area.controls.append(result_table)
            else:
                self.result_area.controls.append(
                    ft.Text(
                        "没有有效统计数",
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

