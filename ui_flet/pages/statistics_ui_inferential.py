"""
统计分析页面 - 推断统计UI控制
整合所有推断统计UI控制Mixin
"""
from ui_flet.pages.statistics_ui_inferential_ttest_one import StatisticsUIInferentialTTestOneMixin
from ui_flet.pages.statistics_ui_inferential_ttest_independent import StatisticsUIInferentialTTestIndependentMixin
from ui_flet.pages.statistics_ui_inferential_ttest_paired import StatisticsUIInferentialTTestPairedMixin
from ui_flet.pages.statistics_ui_inferential_chisquare import StatisticsUIInferentialChiSquareMixin
from ui_flet.pages.statistics_ui_inferential_anova import StatisticsUIInferentialAnovaMixin
from ui_flet.pages.statistics_ui_inferential_mannwhitney import StatisticsUIInferentialMannWhitneyMixin
from ui_flet.pages.statistics_ui_inferential_kruskalwallis import StatisticsUIInferentialKruskalWallisMixin


class StatisticsUIInferentialMixin(
    StatisticsUIInferentialTTestOneMixin,
    StatisticsUIInferentialTTestIndependentMixin,
    StatisticsUIInferentialTTestPairedMixin,
    StatisticsUIInferentialChiSquareMixin,
    StatisticsUIInferentialAnovaMixin,
    StatisticsUIInferentialMannWhitneyMixin,
    StatisticsUIInferentialKruskalWallisMixin
):
    """推断统计UI控制Mixin - 整合所有子模块"""
