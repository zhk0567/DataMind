"""
相关分析结果展示 - 相关分析
"""
import flet as ft
import pandas as pd
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, COMPONENT_SIZES


class StatisticsResultDisplayCorrelationCorrelationMixin:
    """相关分析结果展示 - 相关分析"""

    def _display_correlation_result(self, result: dict):
        """显示相关分析结果"""
        if 'correlation_matrix' in result:
            corr_matrix = result['correlation_matrix']
            
            if isinstance(corr_matrix, pd.DataFrame):
                # 创建相关矩阵表格
                columns = corr_matrix.columns.tolist()
                data_rows = []
                
                for idx, row in corr_matrix.iterrows():
                    cells = [
                        ft.DataCell(ft.Text(f"{val:.4f}" if isinstance(val, (int, float)) else str(val)[:8], size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary']))
                        for val in row
                    ]
                    data_rows.append(ft.DataRow(cells=cells, color=FLUENT_COLORS['bg_card']))
                
                if data_rows:
                    result_table = ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text(col, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary']))
                            for col in columns
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
                            "相关矩阵",
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
                    "结果中缺少相关矩阵",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                )
            )

