"""
统计分析页面 - UI控制创建方法
将_create_*方法提取到此模块
"""
import flet as ft
import pandas as pd
from ui_flet.components.fluent_components import FluentButton, FluentDropdown, FluentTextField
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES


class StatisticsUITimeseriesMixin:
    """UI控制创建方法Mixin - timeseries"""

    def _create_trend_seasonality_controls(self, df):
        """创建趋势与季节性分析控�?""
        # 检查是否有时间类型的列
        time_cols = []
        value_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        # 尝试识别时间列（datetime类型或可能是日期的字符串列）
        for col in df.columns:
            if df[col].dtype == 'datetime64[ns]':
                time_cols.append(col)
            elif df[col].dtype == 'object':
                # 尝试解析为日�?
                try:
                    pd.to_datetime(df[col].head(10))
                    time_cols.append(col)
                except:
                    pass
        
        if not time_cols:
            self.control_area.controls.append(
                ft.Text(
                    "未检测到时间列，请确保数据中包含日期/时间类型的列",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                )
            )
            return
        
        if not value_cols:
            self.control_area.controls.append(
                ft.Text(
                    "没有数值型变量",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                )
            )
            return
        
        time_dropdown = FluentDropdown(
            label="时间�?,
            options=[ft.dropdown.Option(col) for col in time_cols],
            value=time_cols[0] if time_cols else None,
            width=380,
        )
        self.trend_time_dropdown = time_dropdown
        
        value_dropdown = FluentDropdown(
            label="数值列",
            options=[ft.dropdown.Option(col) for col in value_cols],
            value=value_cols[0] if value_cols else None,
            width=380,
        )
        self.trend_value_dropdown = value_dropdown
        
        btn_analyze = FluentButton(
            text="开始分�?,
            on_click=self._run_trend_seasonality,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            time_dropdown,
            ft.Container(height=SPACING['md']),
            value_dropdown,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])
    

    def _create_arima_controls(self, df):
        """创建ARIMA模型控制"""
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if not numeric_cols:
            self.control_area.controls.append(
                ft.Text(
                    "没有数值型变量",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                )
            )
            return
        
        value_dropdown = FluentDropdown(
            label="数值列",
            options=[ft.dropdown.Option(col) for col in numeric_cols],
            value=numeric_cols[0] if numeric_cols else None,
            width=380,
        )
        self.arima_value_dropdown = value_dropdown
        
        p_field = FluentTextField(
            label="AR阶数 (p)",
            value="1",
            width=380,
        )
        self.arima_p_field = p_field
        
        d_field = FluentTextField(
            label="差分阶数 (d)",
            value="1",
            width=380,
        )
        self.arima_d_field = d_field
        
        q_field = FluentTextField(
            label="MA阶数 (q)",
            value="1",
            width=380,
        )
        self.arima_q_field = q_field
        
        btn_analyze = FluentButton(
            text="开始分�?,
            on_click=self._run_arima,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            value_dropdown,
            ft.Container(height=SPACING['md']),
            ft.Text(
                "ARIMA参数 (p, d, q):",
                size=FONT_SIZES['md'],
                weight=ft.FontWeight.BOLD
            ),
            p_field,
            ft.Container(height=SPACING['sm']),
            d_field,
            ft.Container(height=SPACING['sm']),
            q_field,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])
    

    def _create_exponential_smoothing_controls(self, df):
        """创建指数平滑控制"""
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if not numeric_cols:
            self.control_area.controls.append(
                ft.Text(
                    "没有数值型变量",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['text_secondary']
                )
            )
            return
        
        value_dropdown = FluentDropdown(
            label="数值列",
            options=[ft.dropdown.Option(col) for col in numeric_cols],
            value=numeric_cols[0] if numeric_cols else None,
            width=380,
        )
        self.es_value_dropdown = value_dropdown
        
        trend_dropdown = FluentDropdown(
            label="趋势类型",
            options=[
                ft.dropdown.Option("", "�?),
                ft.dropdown.Option("add", "加法"),
                ft.dropdown.Option("mul", "乘法"),
            ],
            value="",
            width=380,
        )
        self.es_trend_dropdown = trend_dropdown
        
        seasonal_dropdown = FluentDropdown(
            label="季节性类�?,
            options=[
                ft.dropdown.Option("", "�?),
                ft.dropdown.Option("add", "加法"),
                ft.dropdown.Option("mul", "乘法"),
            ],
            value="",
            width=380,
        )
        self.es_seasonal_dropdown = seasonal_dropdown
        
        seasonal_periods_field = FluentTextField(
            label="季节性周期（留空自动检测）",
            value="",
            width=380,
        )
        self.es_seasonal_periods_field = seasonal_periods_field
        
        btn_analyze = FluentButton(
            text="开始分�?,
            on_click=self._run_exponential_smoothing,
            bg_color=FLUENT_COLORS['primary'],
            width=380,
        )
        
        self.control_area.controls.extend([
            value_dropdown,
            ft.Container(height=SPACING['md']),
            trend_dropdown,
            ft.Container(height=SPACING['md']),
            seasonal_dropdown,
            ft.Container(height=SPACING['md']),
            seasonal_periods_field,
            ft.Container(height=SPACING['lg']),
            btn_analyze,
        ])
    

