"""
统计分析页面 - 结果显示方法
整合所有结果显示Mixin
"""
from ui_flet.pages.statistics_result_display_basic import StatisticsResultDisplayBasicMixin
from ui_flet.pages.statistics_result_display_inferential import StatisticsResultDisplayInferentialMixin
from ui_flet.pages.statistics_result_display_correlation import StatisticsResultDisplayCorrelationMixin
from ui_flet.pages.statistics_result_display_advanced import StatisticsResultDisplayAdvancedMixin
from ui_flet.pages.statistics_result_display_timeseries import StatisticsResultDisplayTimeseriesMixin


class StatisticsResultDisplayMixin(
    StatisticsResultDisplayBasicMixin,
    StatisticsResultDisplayInferentialMixin,
    StatisticsResultDisplayCorrelationMixin,
    StatisticsResultDisplayAdvancedMixin,
    StatisticsResultDisplayTimeseriesMixin
):
    """结果显示方法Mixin - 整合所有子模块"""
