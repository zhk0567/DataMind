"""统计分析模块"""
from core.statistics.basic_stats import BasicStatistics
from core.statistics.inferential_stats import InferentialStatistics
from core.statistics.correlation import CorrelationAnalysis
from core.statistics.regression import RegressionAnalysis
from core.statistics.advanced import AdvancedAnalysis
from core.statistics.time_series import TimeSeriesAnalyzer
from core.statistics.multivariate import MultivariateAnalyzer
from core.statistics.nonparametric import NonparametricAnalyzer


class StatisticsAnalyzer:
    """统计分析类 - 统一接口"""
    
    def __init__(self):
        self.basic = BasicStatistics()
        self.inferential = InferentialStatistics()
        self.correlation = CorrelationAnalysis()
        self.regression = RegressionAnalysis()
        self.advanced = AdvancedAnalysis()
        self.time_series = TimeSeriesAnalyzer()
        self.multivariate = MultivariateAnalyzer()
        self.nonparametric = NonparametricAnalyzer()
    
    # 描述性统计
    def descriptive_statistics(self, df, columns):
        return self.basic.descriptive_statistics(df, columns)
    
    def frequency_analysis(self, df, columns):
        return self.basic.frequency_analysis(df, columns)
    
    def crosstab_analysis(self, df, row_col, col_col, options=None):
        return self.basic.crosstab_analysis(df, row_col, col_col, options)
    
    # 推断统计
    def t_test_one_sample(self, df, column, test_value=0.0):
        return self.inferential.t_test_one_sample(df, column, test_value)
    
    def t_test_independent(self, df, group_col, value_col):
        return self.inferential.t_test_independent(df, group_col, value_col)
    
    def t_test_paired(self, df, col1, col2):
        return self.inferential.t_test_paired(df, col1, col2)
    
    def chi_square_test(self, df, col1, col2):
        return self.inferential.chi_square_test(df, col1, col2)
    
    def mann_whitney_test(self, df, group_col, value_col):
        return self.inferential.mann_whitney_test(df, group_col, value_col)
    
    def kruskal_wallis_test(self, df, group_col, value_col):
        return self.inferential.kruskal_wallis_test(df, group_col, value_col)
    
    # 相关分析
    def correlation_analysis(self, df, columns, method="pearson"):
        return self.correlation.correlation_analysis(df, columns, method)
    
    def partial_correlation(self, df, x_col, y_col, control_cols):
        return self.correlation.partial_correlation(df, x_col, y_col, control_cols)
    
    # 方差分析
    def anova_analysis(self, df, columns, options):
        return self.inferential.anova_analysis(df, columns, options)
    
    # 回归分析
    def regression_analysis(self, df, columns, options):
        return self.regression.regression_analysis(df, columns, options)
    
    def stepwise_regression(self, df, y_col, x_cols, direction="forward",
                           alpha_enter=0.05, alpha_remove=0.10):
        return self.regression.stepwise_regression(
            df, y_col, x_cols, direction, alpha_enter, alpha_remove
        )
    
    def logistic_regression(self, df, y_col, x_cols):
        return self.regression.logistic_regression(df, y_col, x_cols)
    
    # 高级分析
    def principal_component_analysis(self, df, columns, n_components=None):
        return self.advanced.principal_component_analysis(df, columns, n_components)
    
    def kmeans_clustering(self, df, columns, n_clusters=3):
        return self.advanced.kmeans_clustering(df, columns, n_clusters)
    
    def hierarchical_clustering(self, df, columns, n_clusters=3, linkage="ward"):
        return self.advanced.hierarchical_clustering(df, columns, n_clusters, linkage)
    
    def decision_tree_classification(self, df, y_col, x_cols, max_depth=None):
        return self.advanced.decision_tree_classification(df, y_col, x_cols, max_depth)
    
    def random_forest_classification(self, df, y_col, x_cols, n_estimators=100):
        return self.advanced.random_forest_classification(df, y_col, x_cols, n_estimators)
    
    # 时间序列分析
    def time_series_trend_seasonality(self, df, time_column, value_column):
        return self.time_series.analyze_trend_seasonality(df, time_column, value_column)
    
    def test_stationarity(self, df, value_column, test_type='adf'):
        return self.time_series.test_stationarity(df, value_column, test_type)
    
    def fit_arima(self, df, value_column, order=(1, 1, 1), seasonal_order=None):
        return self.time_series.fit_arima(df, value_column, order, seasonal_order)
    
    def exponential_smoothing(self, df, value_column, trend=None, seasonal=None, seasonal_periods=None):
        return self.time_series.exponential_smoothing(df, value_column, trend, seasonal, seasonal_periods)
    
    def compute_acf_pacf(self, df, value_column, nlags=None):
        return self.time_series.compute_acf_pacf(df, value_column, nlags)
    
    def white_noise_test(self, df, value_column, lags=None):
        return self.time_series.white_noise_test(df, value_column, lags)
    
    # 多变量分析
    def factor_analysis(self, df, columns, n_factors=None, rotation='varimax'):
        return self.multivariate.factor_analysis(df, columns, n_factors, rotation)
    
    def linear_discriminant_analysis(self, df, target_column, feature_columns):
        return self.multivariate.linear_discriminant_analysis(df, target_column, feature_columns)
    
    def quadratic_discriminant_analysis(self, df, target_column, feature_columns):
        return self.multivariate.quadratic_discriminant_analysis(df, target_column, feature_columns)
    
    def canonical_correlation_analysis(self, df, x_columns, y_columns):
        return self.multivariate.canonical_correlation_analysis(df, x_columns, y_columns)
    
    # 非参数统计扩展
    def wilcoxon_signed_rank_test(self, df, var1, var2=None, zero_method='wilcox'):
        return self.nonparametric.wilcoxon_signed_rank_test(df, var1, var2, zero_method)
    
    def friedman_test(self, df, columns):
        return self.nonparametric.friedman_test(df, columns)
    
    def sign_test(self, df, var1, var2=None, median=0.0):
        return self.nonparametric.sign_test(df, var1, var2, median)
    
    def kolmogorov_smirnov_test(self, df, column, dist='norm'):
        return self.nonparametric.kolmogorov_smirnov_test(df, column, dist)
    
    def shapiro_wilk_test(self, df, column):
        return self.nonparametric.shapiro_wilk_test(df, column)
    
    def anderson_darling_test(self, df, column, dist='norm'):
        return self.nonparametric.anderson_darling_test(df, column, dist)

