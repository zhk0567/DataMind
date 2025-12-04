"""
统计分析页面 - 时间序列结果展示
整合所有时间序列分析结果展示Mixin
"""
from ui_flet.pages.statistics_result_display_timeseries_trend import StatisticsResultDisplayTimeseriesTrendMixin
from ui_flet.pages.statistics_result_display_timeseries_arima import StatisticsResultDisplayTimeseriesArimaMixin
from ui_flet.pages.statistics_result_display_timeseries_smoothing import StatisticsResultDisplayTimeseriesSmoothingMixin


class StatisticsResultDisplayTimeseriesMixin(
    StatisticsResultDisplayTimeseriesTrendMixin,
    StatisticsResultDisplayTimeseriesArimaMixin,
    StatisticsResultDisplayTimeseriesSmoothingMixin
):
    """时间序列分析结果展示Mixin - 整合所有子模块"""
