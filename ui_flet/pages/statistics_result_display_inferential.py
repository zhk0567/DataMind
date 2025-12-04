"""
统计分析页面 - 推断统计结果展示
整合所有推断统计分析结果展示Mixin
"""
from ui_flet.pages.statistics_result_display_inferential_ttest import StatisticsResultDisplayInferentialTTestMixin
from ui_flet.pages.statistics_result_display_inferential_chisquare import StatisticsResultDisplayInferentialChiSquareMixin
from ui_flet.pages.statistics_result_display_inferential_anova import StatisticsResultDisplayInferentialAnovaMixin
from ui_flet.pages.statistics_result_display_inferential_mannwhitney import StatisticsResultDisplayInferentialMannWhitneyMixin
from ui_flet.pages.statistics_result_display_inferential_kruskalwallis import StatisticsResultDisplayInferentialKruskalWallisMixin


class StatisticsResultDisplayInferentialMixin(
    StatisticsResultDisplayInferentialTTestMixin,
    StatisticsResultDisplayInferentialChiSquareMixin,
    StatisticsResultDisplayInferentialAnovaMixin,
    StatisticsResultDisplayInferentialMannWhitneyMixin,
    StatisticsResultDisplayInferentialKruskalWallisMixin
):
    """推断统计分析结果展示Mixin - 整合所有子模块"""
