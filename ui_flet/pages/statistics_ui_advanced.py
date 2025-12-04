"""
统计分析页面 - 高级分析UI控制
整合所有高级分析UI控制Mixin
"""
from ui_flet.pages.statistics_ui_advanced_pca import StatisticsUIAdvancedPCAMixin
from ui_flet.pages.statistics_ui_advanced_kmeans import StatisticsUIAdvancedKMeansMixin
from ui_flet.pages.statistics_ui_advanced_hierarchical import StatisticsUIAdvancedHierarchicalMixin
from ui_flet.pages.statistics_ui_advanced_decisiontree import StatisticsUIAdvancedDecisionTreeMixin
from ui_flet.pages.statistics_ui_advanced_factor import StatisticsUIAdvancedFactorMixin
from ui_flet.pages.statistics_ui_advanced_discriminant import StatisticsUIAdvancedDiscriminantMixin


class StatisticsUIAdvancedMixin(
    StatisticsUIAdvancedPCAMixin,
    StatisticsUIAdvancedKMeansMixin,
    StatisticsUIAdvancedHierarchicalMixin,
    StatisticsUIAdvancedDecisionTreeMixin,
    StatisticsUIAdvancedFactorMixin,
    StatisticsUIAdvancedDiscriminantMixin
):
    """高级分析UI控制Mixin - 整合所有子模块"""
