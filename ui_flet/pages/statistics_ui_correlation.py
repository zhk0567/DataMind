"""统计分析页面 - 相关分析UI控制"""
from ui_flet.pages.statistics_ui_correlation_correlation import StatisticsUICorrelationCorrelationMixin
from ui_flet.pages.statistics_ui_correlation_partial import StatisticsUICorrelationPartialMixin
from ui_flet.pages.statistics_ui_correlation_regression import StatisticsUICorrelationRegressionMixin
from ui_flet.pages.statistics_ui_correlation_stepwise import StatisticsUICorrelationStepwiseMixin
from ui_flet.pages.statistics_ui_correlation_logistic import StatisticsUICorrelationLogisticMixin


class StatisticsUICorrelationMixin(
    StatisticsUICorrelationCorrelationMixin,
    StatisticsUICorrelationPartialMixin,
    StatisticsUICorrelationRegressionMixin,
    StatisticsUICorrelationStepwiseMixin,
    StatisticsUICorrelationLogisticMixin
):
    """相关分析UI控制Mixin - 整合所有子模块"""
