"""
统计分析页面 - 时间序列分析执行方法
"""
from ui_flet.pages.statistics_helpers import execute_analysis_with_loading
from ui_flet.pages.statistics_result_display_timeseries import StatisticsResultDisplayTimeseriesMixin


class StatisticsAnalyzersTimeseriesMixin(StatisticsResultDisplayTimeseriesMixin):
    """时间序列分析执行方法Mixin"""

    def _run_trend_seasonality(self, e):
        """执行趋势与季节性分析"""
        if not hasattr(self, 'timeseries_var_dropdown') or not self.timeseries_var_dropdown.value:
            return
        
        selected_var = self.timeseries_var_dropdown.value
        
        # 假设时间列是索引或第一列
        time_column = self.main_window.processed_data.index.name or 'index'
        if time_column == 'index':
            df = self.main_window.processed_data.reset_index()
            time_column = df.columns[0]
        else:
            df = self.main_window.processed_data
        
        def analyzer_func():
            return self.analyzer.time_series_trend_seasonality(
                df,
                time_column,
                selected_var
            )
        
        def display_func(result):
            self._display_trend_seasonality_result(result)
        
        execute_analysis_with_loading(
            self.result_area,
            self.main_window.page,
            analyzer_func,
            display_func,
            success_msg="趋势与季节性分析完成",
            error_prefix="趋势与季节性分析失败"
        )

    def _run_arima(self, e):
        """执行ARIMA模型分析"""
        if not hasattr(self, 'arima_var_dropdown') or not self.arima_var_dropdown.value:
            return
        
        selected_var = self.arima_var_dropdown.value
        
        order = (1, 1, 1)
        if hasattr(self, 'arima_order_field') and self.arima_order_field.value:
            try:
                parts = self.arima_order_field.value.split(',')
                if len(parts) == 3:
                    order = (int(parts[0].strip()), int(parts[1].strip()), int(parts[2].strip()))
            except ValueError:
                pass
        
        def analyzer_func():
            return self.analyzer.fit_arima(
                self.main_window.processed_data,
                selected_var,
                order
            )
        
        def display_func(result):
            self._display_arima_result(result)
        
        execute_analysis_with_loading(
            self.result_area,
            self.main_window.page,
            analyzer_func,
            display_func,
            success_msg="ARIMA模型分析完成",
            error_prefix="ARIMA模型分析失败"
        )

    def _run_exponential_smoothing(self, e):
        """执行指数平滑分析"""
        if not hasattr(self, 'smoothing_var_dropdown') or not self.smoothing_var_dropdown.value:
            return
        
        selected_var = self.smoothing_var_dropdown.value
        
        trend = None
        seasonal = None
        seasonal_periods = None
        
        if hasattr(self, 'smoothing_trend_dropdown') and self.smoothing_trend_dropdown.value:
            trend = self.smoothing_trend_dropdown.value
        if hasattr(self, 'smoothing_seasonal_dropdown') and self.smoothing_seasonal_dropdown.value:
            seasonal = self.smoothing_seasonal_dropdown.value
        if hasattr(self, 'smoothing_periods_field') and self.smoothing_periods_field.value:
            try:
                seasonal_periods = int(self.smoothing_periods_field.value)
            except ValueError:
                pass
        
        def analyzer_func():
            return self.analyzer.exponential_smoothing(
                self.main_window.processed_data,
                selected_var,
                trend=trend,
                seasonal=seasonal,
                seasonal_periods=seasonal_periods
            )
        
        def display_func(result):
            self._display_exponential_smoothing_result(result)
        
        execute_analysis_with_loading(
            self.result_area,
            self.main_window.page,
            analyzer_func,
            display_func,
            success_msg="指数平滑分析完成",
            error_prefix="指数平滑分析失败"
        )

