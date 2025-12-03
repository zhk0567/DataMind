"""
统计分析页面 - UI控制创建方法
整合所有UI控制Mixin
"""
from ui_flet.pages.statistics_ui_basic import StatisticsUIBasicMixin
from ui_flet.pages.statistics_ui_inferential import StatisticsUIInferentialMixin
from ui_flet.pages.statistics_ui_correlation import StatisticsUICorrelationMixin
from ui_flet.pages.statistics_ui_advanced import StatisticsUIAdvancedMixin
from ui_flet.pages.statistics_ui_timeseries import StatisticsUITimeseriesMixin


class StatisticsUIControlsMixin(
    StatisticsUIBasicMixin,
    StatisticsUIInferentialMixin,
    StatisticsUICorrelationMixin,
    StatisticsUIAdvancedMixin,
    StatisticsUITimeseriesMixin
):
    """UI控制创建方法Mixin - 整合所有子模块"""
