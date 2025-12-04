"""
统计分析页面 - 基本统计结果展示
整合所有基本统计结果展示Mixin
"""
from ui_flet.pages.statistics_result_display_basic_main import StatisticsResultDisplayBasicMainMixin
from ui_flet.pages.statistics_result_display_basic_descriptive import StatisticsResultDisplayBasicDescriptiveMixin
from ui_flet.pages.statistics_result_display_basic_frequency import StatisticsResultDisplayBasicFrequencyMixin
from ui_flet.pages.statistics_result_display_basic_crosstab import StatisticsResultDisplayBasicCrosstabMixin


class StatisticsResultDisplayBasicMixin(
    StatisticsResultDisplayBasicMainMixin,
    StatisticsResultDisplayBasicDescriptiveMixin,
    StatisticsResultDisplayBasicFrequencyMixin,
    StatisticsResultDisplayBasicCrosstabMixin
):
    """基本统计结果展示Mixin - 整合所有子模块"""
