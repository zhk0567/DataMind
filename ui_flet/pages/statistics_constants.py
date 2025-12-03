"""
统计分析页面常量定义
"""
# 分析分类结构
ANALYSIS_CATEGORIES = {
    "描述性分析": {
        "描述性统计": "descriptive",
        "频数分析": "frequency",
        "交叉表分析": "crosstab"
    },
    "差异性分析": {
        "单样本t检验": "t_test_one",
        "独立样本t检验": "t_test_independent",
        "配对样本t检验": "t_test_paired",
        "卡方检验": "chi_square",
        "方差分析": "anova"
    },
    "非参数检验": {
        "Mann-Whitney检验": "mann_whitney",
        "Kruskal-Wallis检验": "kruskal_wallis"
    },
    "相关性分析": {
        "相关分析": "correlation",
        "偏相关分析": "partial_correlation"
    },
    "预测模型": {
        "线性回归": "regression",
        "逐步回归": "stepwise_regression",
        "逻辑回归": "logistic_regression"
    },
    "高级分析": {
        "主成分分析": "pca",
        "K-means聚类": "kmeans",
        "层次聚类": "hierarchical_clustering",
        "决策树分类": "decision_tree"
    },
    "多变量分析": {
        "因子分析": "factor_analysis",
        "判别分析": "discriminant_analysis"
    },
    "时间序列": {
        "趋势与季节性分析": "trend_seasonality",
        "ARIMA模型": "arima",
        "指数平滑": "exponential_smoothing"
    },
}

# 分析类型中文名称映射
ANALYSIS_NAMES = {
    # 描述性分析
    'descriptive': '描述性统计',
    'frequency': '频数分析',
    'crosstab': '交叉表分析',
    # 差异性分析
    't_test_one': '单样本t检验',
    't_test_independent': '独立样本t检验',
    't_test_paired': '配对样本t检验',
    'chi_square': '卡方检验',
    'anova': '方差分析',
    # 非参数检验
    'mann_whitney': 'Mann-Whitney检验',
    'kruskal_wallis': 'Kruskal-Wallis检验',
    # 相关性分析
    'correlation': '相关分析',
    'partial_correlation': '偏相关分析',
    # 预测模型
    'regression': '线性回归',
    'stepwise_regression': '逐步回归',
    'logistic_regression': '逻辑回归',
    # 高级分析
    'pca': '主成分分析',
    'kmeans': 'K-means聚类',
    'hierarchical_clustering': '层次聚类',
    'decision_tree': '决策树分类',
    # 多变量分析
    'factor_analysis': '因子分析',
    'discriminant_analysis': '判别分析',
    # 时间序列
    'trend_seasonality': '趋势与季节性分析',
    'arima': 'ARIMA模型',
    'exponential_smoothing': '指数平滑',
}

