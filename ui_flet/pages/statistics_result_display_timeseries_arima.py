"""
时间序列分析结果展示 - ARIMA模型
"""
import flet as ft
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, COMPONENT_SIZES


class StatisticsResultDisplayTimeseriesArimaMixin:
    """时间序列ARIMA模型结果展示"""

    def _display_arima_result(self, result):
        """显示ARIMA模型结果"""
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
            # 显示模型信息
            self.result_area.controls.append(
                ft.Text(
                    f"模型类型: {result.get('model_type', 'ARIMA')}",
                    size=FONT_SIZES['lg'],
                    weight=ft.FontWeight.BOLD,
                    color=FLUENT_COLORS['text_primary']
                )
            )
            self.result_area.controls.append(ft.Container(height=SPACING['sm']))
            
            order = result.get('order', (1, 1, 1))
            
            self.result_area.controls.append(
                ft.Text(
                    f"ARIMA阶数: ({order[0]}, {order[1]}, {order[2]})",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_primary']
                )
            )
            
            # 显示模型评估指标
            self.result_area.controls.append(ft.Container(height=SPACING['md']))
            
            self.result_area.controls.append(
                ft.Text(
                    "模型评估",
                    size=FONT_SIZES['lg'],
                    weight=ft.FontWeight.BOLD,
                    color=FLUENT_COLORS['text_primary']
                )
            )
            self.result_area.controls.append(ft.Container(height=SPACING['sm']))
            
            metrics_data = [
                ("AIC", f"{result.get('aic', 0):.4f}"),
                ("BIC", f"{result.get('bic', 0):.4f}"),
            ]
            
            metrics_rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(key, size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
                        ft.DataCell(ft.Text(str(val), size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
                    ],
                    color=FLUENT_COLORS['bg_card']
                )
                for key, val in metrics_data
            ]
            
            metrics_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("指标", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])),
                    ft.DataColumn(ft.Text("值", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])),
                ],
                rows=metrics_rows,
                border=ft.border.all(1, FLUENT_COLORS['border']),
                border_radius=COMPONENT_SIZES['input_border_radius'],
                bgcolor=FLUENT_COLORS['bg_card'],
                heading_row_color=FLUENT_COLORS['bg_tertiary'],
                data_row_color={ft.ControlState.DEFAULT: FLUENT_COLORS['bg_card']},
            )
            self.result_area.controls.append(metrics_table)
            
            # 显示预测结果
            if 'forecast' in result and result['forecast']:
                self.result_area.controls.append(ft.Container(height=SPACING['lg']))
                
                self.result_area.controls.append(
                    ft.Text(
                        "预测结果（未来10期）",
                        size=FONT_SIZES['lg'],
                        weight=ft.FontWeight.BOLD,
                        color=FLUENT_COLORS['text_primary']
                    )
                )
                self.result_area.controls.append(ft.Container(height=SPACING['sm']))
                
                forecast = result['forecast'][:10]  # 只显示前10期
                
                forecast_rows = []
                for i, val in enumerate(forecast, 1):
                    forecast_rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(f"第{i}期", size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
                                ft.DataCell(ft.Text(f"{val:.4f}", size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
                            ],
                            color=FLUENT_COLORS['bg_card']
                        )
                    )
                
                forecast_table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("期数", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])),
                        ft.DataColumn(ft.Text("预测值", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary'])),
                    ],
                    rows=forecast_rows,
                    border=ft.border.all(1, FLUENT_COLORS['border']),
                    border_radius=COMPONENT_SIZES['input_border_radius'],
                    bgcolor=FLUENT_COLORS['bg_card'],
                    heading_row_color=FLUENT_COLORS['bg_tertiary'],
                    data_row_color={ft.ControlState.DEFAULT: FLUENT_COLORS['bg_card']},
                )
                self.result_area.controls.append(forecast_table)
        
        self.btn_export.visible = True
        self.result_area.update()
        self.btn_export.update()
        
        # 确保页面更新以显示结果
        try:
            if hasattr(self.main_window, 'page'):
                self.main_window.page.update()
        except Exception:
            pass

