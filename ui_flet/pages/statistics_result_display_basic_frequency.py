"""
基本统计分析结果展示 - 频率分析
"""
import flet as ft
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, COMPONENT_SIZES


class StatisticsResultDisplayBasicFrequencyMixin:
    """基本统计分析结果展示 - 频率分析"""

    def _display_frequency_result(self, result):
        """显示频率分析结果"""
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
                    
                    # 创建频率表
                    rows = []
                    for idx, row in freq_df.iterrows():
                        rows.append(
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text(str(idx), size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
                                    ft.DataCell(ft.Text(str(row.iloc[0]), size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
                                ],
                                color=FLUENT_COLORS['bg_card']
                            )
                        )
                    
                    table = ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("类别", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])),
                            ft.DataColumn(ft.Text("频率", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])),
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
                            f"变量: {col_name}",
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

