"""
统计分析页面 - 分析执行方法
整合所有分析执行Mixin
"""
from ui_flet.pages.statistics_analyzers_basic import StatisticsAnalyzersBasicMixin
from ui_flet.pages.statistics_analyzers_inferential import StatisticsAnalyzersInferentialMixin
from ui_flet.pages.statistics_analyzers_correlation import StatisticsAnalyzersCorrelationMixin
from ui_flet.pages.statistics_analyzers_advanced import StatisticsAnalyzersAdvancedMixin
from ui_flet.pages.statistics_analyzers_timeseries import StatisticsAnalyzersTimeseriesMixin


class StatisticsAnalyzersMixin(
    StatisticsAnalyzersBasicMixin,
    StatisticsAnalyzersInferentialMixin,
    StatisticsAnalyzersCorrelationMixin,
    StatisticsAnalyzersAdvancedMixin,
    StatisticsAnalyzersTimeseriesMixin
):
    """分析执行方法Mixin - 整合所有子模块"""
