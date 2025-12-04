"""
时间序列分析结果展示 - 趋势与季节性分析
"""
import flet as ft
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, COMPONENT_SIZES


class StatisticsResultDisplayTimeseriesTrendMixin:
    """时间序列趋势与季节性分析结果展示"""

    def _display_trend_seasonality_result(self, result):
        """显示趋势与季节性分析结果"""
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
            # 显示趋势分析结果
            if 'trend' in result:
                trend = result['trend']
                
                self.result_area.controls.append(
                    ft.Text(
                        "趋势分析",
                        size=FONT_SIZES['lg'],
                        weight=ft.FontWeight.BOLD,
                        color=FLUENT_COLORS['text_primary']
                    )
                )
                self.result_area.controls.append(ft.Container(height=SPACING['sm']))
                
                trend_data = [
                    ("趋势方向", trend.get('direction', '')),
                    ("斜率", f"{trend.get('slope', 0):.4f}"),
                    ("截距", f"{trend.get('intercept', 0):.4f}"),
                    ("R²", f"{trend.get('r_squared', 0):.4f}"),
                    ("p值", f"{trend.get('p_value', 0):.4f}"),
                ]
                
                trend_rows = [
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(key, size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
                            ft.DataCell(ft.Text(str(val), size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
                        ],
                        color=FLUENT_COLORS['bg_card']
                    )
                    for key, val in trend_data
                ]
                
                trend_table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("指标", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])),
                        ft.DataColumn(ft.Text("值", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])),
                    ],
                    rows=trend_rows,
                    border=ft.border.all(1, FLUENT_COLORS['border']),
                    border_radius=COMPONENT_SIZES['input_border_radius'],
                    bgcolor=FLUENT_COLORS['bg_card'],
                    heading_row_color=FLUENT_COLORS['bg_tertiary'],
                    data_row_color={ft.ControlState.DEFAULT: FLUENT_COLORS['bg_card']},
                )
                self.result_area.controls.append(trend_table)
            
            # 显示季节性分析结果
            if 'seasonality' in result and result['seasonality']:
                self.result_area.controls.append(ft.Container(height=SPACING['lg']))
                
                self.result_area.controls.append(
                    ft.Text(
                        "季节性分析",
                        size=FONT_SIZES['lg'],
                        weight=ft.FontWeight.BOLD,
                        color=FLUENT_COLORS['text_primary']
                    )
                )
                self.result_area.controls.append(ft.Container(height=SPACING['sm']))
                
                seasonality = result['seasonality']
                
                if 'monthly_seasonality' in seasonality:
                    monthly = seasonality['monthly_seasonality']
                    has_seasonality = monthly.get('has_seasonality', False)
                    
                    self.result_area.controls.append(
                        ft.Text(
                            f"月度季节性: {'存在' if has_seasonality else '不存在'}",
                            size=FONT_SIZES['md'],
                            color=FLUENT_COLORS['primary'] if has_seasonality else FLUENT_COLORS['text_secondary']
                        )
                    )
            
            # 显示基本统计
            if 'basic_stats' in result:
                self.result_area.controls.append(ft.Container(height=SPACING['lg']))
                
                self.result_area.controls.append(
                    ft.Text(
                        "基本统计",
                        size=FONT_SIZES['lg'],
                        weight=ft.FontWeight.BOLD,
                        color=FLUENT_COLORS['text_primary']
                    )
                )
                self.result_area.controls.append(ft.Container(height=SPACING['sm']))
                
                stats = result['basic_stats']
                
                stats_data = [
                    ("均值", f"{stats.get('mean', 0):.4f}"),
                    ("标准差", f"{stats.get('std', 0):.4f}"),
                    ("最小值", f"{stats.get('min', 0):.4f}"),
                    ("最大值", f"{stats.get('max', 0):.4f}"),
                ]
                
                stats_rows = [
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(key, size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
                            ft.DataCell(ft.Text(str(val), size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
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
                self.result_area.controls.append(stats_table)
        
        self.btn_export.visible = True
        self.result_area.update()
        self.btn_export.update()
        
        # 确保页面更新以显示结果
        try:
            if hasattr(self.main_window, 'page'):
                self.main_window.page.update()
        except Exception:
            pass

