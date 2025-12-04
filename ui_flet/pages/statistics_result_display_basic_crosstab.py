"""
基本统计分析结果展示 - 交叉表分析
"""
import flet as ft
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, COMPONENT_SIZES


class StatisticsResultDisplayBasicCrosstabMixin:
    """基本统计分析结果展示 - 交叉表分析"""

    def _display_crosstab_result(self, result):
        """显示交叉表分析结果"""
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
            
            # 创建交叉表
            rows = []
            for idx, row in crosstab_df.iterrows():
                cells = [
                    ft.DataCell(ft.Text(str(idx), size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary']))
                ]
                for val in row:
                    cells.append(ft.DataCell(ft.Text(str(val), size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])))
                rows.append(ft.DataRow(cells=cells, color=FLUENT_COLORS['bg_card']))
            
            columns = [
                ft.DataColumn(ft.Text("", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary']))
            ]
            for col in crosstab_df.columns:
                columns.append(ft.DataColumn(ft.Text(str(col), size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])))
            
            table = ft.DataTable(
                columns=columns,
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
        
        # 确保页面更新以显示结果
        try:
            if hasattr(self.main_window, 'page'):
                self.main_window.page.update()
        except Exception:
            pass

