"""
统计分析页面 - 结果显示方法
将_display_*方法提取到此模块
"""
import flet as ft
import pandas as pd
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, COMPONENT_SIZES


class StatisticsResultDisplayTimeseriesMixin:
    """结果显示方法Mixin - timeseries"""

    def _display_trend_seasonality_result(self, result):
        """显示趋势与季节性分析结�?""
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
                        weight=ft.FontWeight.BOLD
                    )
                )
                self.result_area.controls.append(ft.Container(height=SPACING['sm']))
                
                trend_data = [
                    ("趋势方向", trend.get('direction', '')),
                    ("斜率", f"{trend.get('slope', 0):.4f}"),
                    ("截距", f"{trend.get('intercept', 0):.4f}"),
                    ("R²", f"{trend.get('r_squared', 0):.4f}"),
                    ("p�?, f"{trend.get('p_value', 0):.4f}"),
                ]
                
                trend_rows = [
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(key, size=FONT_SIZES['sm'])),
                            ft.DataCell(ft.Text(str(val), size=FONT_SIZES['sm'])),
                        ]
                    )
                    for key, val in trend_data
                ]
                
                trend_table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("指标", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                        ft.DataColumn(ft.Text("�?, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                    ],
                    rows=trend_rows,
                    border=ft.border.all(1, FLUENT_COLORS['border']),
                    border_radius=COMPONENT_SIZES['input_border_radius'],
                )
                self.result_area.controls.append(trend_table)
            
            # 显示季节性分析结�?
            if 'seasonality' in result and result['seasonality']:
                self.result_area.controls.append(ft.Container(height=SPACING['lg']))
                self.result_area.controls.append(
                    ft.Text(
                        "季节性分�?,
                        size=FONT_SIZES['lg'],
                        weight=ft.FontWeight.BOLD
                    )
                )
                self.result_area.controls.append(ft.Container(height=SPACING['sm']))
                
                seasonality = result['seasonality']
                if 'monthly_seasonality' in seasonality:
                    monthly = seasonality['monthly_seasonality']
                    has_seasonality = monthly.get('has_seasonality', False)
                    self.result_area.controls.append(
                        ft.Text(
                            f"月度季节�? {'存在' if has_seasonality else '不存�?}",
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
                        weight=ft.FontWeight.BOLD
                    )
                )
                self.result_area.controls.append(ft.Container(height=SPACING['sm']))
                
                stats = result['basic_stats']
                stats_data = [
                    ("均�?, f"{stats.get('mean', 0):.4f}"),
                    ("标准�?, f"{stats.get('std', 0):.4f}"),
                    ("最小�?, f"{stats.get('min', 0):.4f}"),
                    ("最大�?, f"{stats.get('max', 0):.4f}"),
                ]
                
                stats_rows = [
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(key, size=FONT_SIZES['sm'])),
                            ft.DataCell(ft.Text(str(val), size=FONT_SIZES['sm'])),
                        ]
                    )
                    for key, val in stats_data
                ]
                
                stats_table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("统计�?, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                        ft.DataColumn(ft.Text("�?, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                    ],
                    rows=stats_rows,
                    border=ft.border.all(1, FLUENT_COLORS['border']),
                    border_radius=COMPONENT_SIZES['input_border_radius'],
                )
                self.result_area.controls.append(stats_table)
        
        self.btn_export.visible = True
        self.result_area.update()
        self.btn_export.update()
        # 确保页面更新以显示结�?
        try:
            if hasattr(self.main_window, 'page'):
                self.main_window.page.update()
        except Exception:
            pass
    

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
                    weight=ft.FontWeight.BOLD
                )
            )
            self.result_area.controls.append(ft.Container(height=SPACING['sm']))
            
            order = result.get('order', (1, 1, 1))
            self.result_area.controls.append(
                ft.Text(
                    f"ARIMA阶数: ({order[0]}, {order[1]}, {order[2]})",
                    size=FONT_SIZES['md']
                )
            )
            
            # 显示模型评估指标
            self.result_area.controls.append(ft.Container(height=SPACING['md']))
            self.result_area.controls.append(
                ft.Text(
                    "模型评估",
                    size=FONT_SIZES['lg'],
                    weight=ft.FontWeight.BOLD
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
                        ft.DataCell(ft.Text(key, size=FONT_SIZES['sm'])),
                        ft.DataCell(ft.Text(str(val), size=FONT_SIZES['sm'])),
                    ]
                )
                for key, val in metrics_data
            ]
            
            metrics_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("指标", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("�?, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                ],
                rows=metrics_rows,
                border=ft.border.all(1, FLUENT_COLORS['border']),
                border_radius=COMPONENT_SIZES['input_border_radius'],
            )
            self.result_area.controls.append(metrics_table)
            
            # 显示预测结果
            if 'forecast' in result and result['forecast']:
                self.result_area.controls.append(ft.Container(height=SPACING['lg']))
                self.result_area.controls.append(
                    ft.Text(
                        "预测结果（未�?0期）",
                        size=FONT_SIZES['lg'],
                        weight=ft.FontWeight.BOLD
                    )
                )
                self.result_area.controls.append(ft.Container(height=SPACING['sm']))
                
                forecast = result['forecast'][:10]  # 只显示前10�?
                forecast_rows = []
                for i, val in enumerate(forecast, 1):
                    forecast_rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(f"第{i}�?, size=FONT_SIZES['sm'])),
                                ft.DataCell(ft.Text(f"{val:.4f}", size=FONT_SIZES['sm'])),
                            ]
                        )
                    )
                
                forecast_table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("期数", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                        ft.DataColumn(ft.Text("预测�?, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                    ],
                    rows=forecast_rows,
                    border=ft.border.all(1, FLUENT_COLORS['border']),
                    border_radius=COMPONENT_SIZES['input_border_radius'],
                )
                self.result_area.controls.append(forecast_table)
        
        self.btn_export.visible = True
        self.result_area.update()
        self.btn_export.update()
        # 确保页面更新以显示结�?
        try:
            if hasattr(self.main_window, 'page'):
                self.main_window.page.update()
        except Exception:
            pass
    

    def _display_exponential_smoothing_result(self, result):
        """显示指数平滑结果"""
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
                    f"模型类型: {result.get('model_type', 'Exponential Smoothing')}",
                    size=FONT_SIZES['lg'],
                    weight=ft.FontWeight.BOLD
                )
            )
            self.result_area.controls.append(ft.Container(height=SPACING['sm']))
            
            trend = result.get('trend', None)
            seasonal = result.get('seasonal', None)
            seasonal_periods = result.get('seasonal_periods', None)
            
            model_info = []
            if trend:
                model_info.append(f"趋势: {trend}")
            if seasonal:
                model_info.append(f"季节�? {seasonal}")
            if seasonal_periods:
                model_info.append(f"季节性周�? {seasonal_periods}")
            
            if model_info:
                self.result_area.controls.append(
                    ft.Text(
                        ", ".join(model_info),
                        size=FONT_SIZES['md']
                    )
                )
            
            # 显示模型评估指标
            self.result_area.controls.append(ft.Container(height=SPACING['md']))
            self.result_area.controls.append(
                ft.Text(
                    "模型评估",
                    size=FONT_SIZES['lg'],
                    weight=ft.FontWeight.BOLD
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
                        ft.DataCell(ft.Text(key, size=FONT_SIZES['sm'])),
                        ft.DataCell(ft.Text(str(val), size=FONT_SIZES['sm'])),
                    ]
                )
                for key, val in metrics_data
            ]
            
            metrics_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("指标", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("�?, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                ],
                rows=metrics_rows,
                border=ft.border.all(1, FLUENT_COLORS['border']),
                border_radius=COMPONENT_SIZES['input_border_radius'],
            )
            self.result_area.controls.append(metrics_table)
            
            # 显示预测结果
            if 'forecast' in result and result['forecast']:
                self.result_area.controls.append(ft.Container(height=SPACING['lg']))
                self.result_area.controls.append(
                    ft.Text(
                        "预测结果（未�?0期）",
                        size=FONT_SIZES['lg'],
                        weight=ft.FontWeight.BOLD
                    )
                )
                self.result_area.controls.append(ft.Container(height=SPACING['sm']))
                
                forecast = result['forecast'][:10]  # 只显示前10�?
                forecast_rows = []
                for i, val in enumerate(forecast, 1):
                    forecast_rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(f"第{i}�?, size=FONT_SIZES['sm'])),
                                ft.DataCell(ft.Text(f"{val:.4f}", size=FONT_SIZES['sm'])),
                            ]
                        )
                    )
                
                forecast_table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("期数", size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                        ft.DataColumn(ft.Text("预测�?, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD)),
                    ],
                    rows=forecast_rows,
                    border=ft.border.all(1, FLUENT_COLORS['border']),
                    border_radius=COMPONENT_SIZES['input_border_radius'],
                )
                self.result_area.controls.append(forecast_table)
        
        self.btn_export.visible = True
        self.result_area.update()
        self.btn_export.update()
    

