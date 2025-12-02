"""
特征工程模块
提供特征创建、特征选择、特征缩放等功能
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
try:
    from sklearn.preprocessing import (
        MinMaxScaler, RobustScaler, QuantileTransformer,
        PolynomialFeatures
    )
    from sklearn.feature_selection import (
        VarianceThreshold, SelectKBest, chi2, f_regression,
        RFE
    )
    from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
    from sklearn.linear_model import LinearRegression, LogisticRegression
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class FeatureEngineer:
    """特征工程类"""
    
    @staticmethod
    def create_polynomial_features(
        df: pd.DataFrame,
        columns: List[str],
        degree: int = 2,
        include_bias: bool = False
    ) -> pd.DataFrame:
        """
        创建多项式特征
        
        参数:
            df: 数据框
            columns: 要创建多项式特征的列
            degree: 多项式次数
            include_bias: 是否包含偏置项
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用多项式特征")
        
        result_df = df.copy()
        numeric_cols = [col for col in columns if col in result_df.select_dtypes(include=[np.number]).columns]
        
        if not numeric_cols:
            return result_df
        
        poly = PolynomialFeatures(degree=degree, include_bias=include_bias)
        poly_features = poly.fit_transform(result_df[numeric_cols])
        
        # 创建新列名
        feature_names = poly.get_feature_names_out(numeric_cols)
        poly_df = pd.DataFrame(poly_features, columns=feature_names, index=result_df.index)
        
        # 合并到原数据框
        result_df = pd.concat([result_df, poly_df], axis=1)
        
        return result_df
    
    @staticmethod
    def create_interaction_features(
        df: pd.DataFrame,
        columns: List[str]
    ) -> pd.DataFrame:
        """
        创建交互特征（两两相乘）
        
        参数:
            df: 数据框
            columns: 要创建交互特征的列
        """
        result_df = df.copy()
        numeric_cols = [col for col in columns if col in result_df.select_dtypes(include=[np.number]).columns]
        
        if len(numeric_cols) < 2:
            return result_df
        
        # 创建两两交互特征
        for i, col1 in enumerate(numeric_cols):
            for col2 in numeric_cols[i+1:]:
                interaction_name = f"{col1}_x_{col2}"
                result_df[interaction_name] = result_df[col1] * result_df[col2]
        
        return result_df
    
    @staticmethod
    def create_aggregation_features(
        df: pd.DataFrame,
        group_by: str,
        agg_columns: List[str],
        agg_functions: List[str] = ['mean', 'std', 'min', 'max']
    ) -> pd.DataFrame:
        """
        创建分组聚合特征
        
        参数:
            df: 数据框
            group_by: 分组列
            agg_columns: 要聚合的列
            agg_functions: 聚合函数列表
        """
        result_df = df.copy()
        
        if group_by not in result_df.columns:
            return result_df
        
        numeric_cols = [col for col in agg_columns if col in result_df.select_dtypes(include=[np.number]).columns]
        if not numeric_cols:
            return result_df
        
        # 分组聚合
        grouped = result_df.groupby(group_by)[numeric_cols].agg(agg_functions)
        
        # 展平列名
        grouped.columns = [f"{col}_{func}" for col, func in grouped.columns]
        
        # 合并回原数据框
        for col in grouped.columns:
            result_df[f"group_{col}"] = result_df[group_by].map(grouped[col])
        
        return result_df
    
    @staticmethod
    def select_features_by_variance(
        df: pd.DataFrame,
        columns: List[str],
        threshold: float = 0.0
    ) -> List[str]:
        """
        基于方差选择特征
        
        参数:
            df: 数据框
            columns: 要评估的列
            threshold: 方差阈值
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用方差选择")
        
        numeric_cols = [col for col in columns if col in df.select_dtypes(include=[np.number]).columns]
        if not numeric_cols:
            return []
        
        selector = VarianceThreshold(threshold=threshold)
        selector.fit(df[numeric_cols])
        
        selected_features = [numeric_cols[i] for i in range(len(numeric_cols)) if selector.variances_[i] > threshold]
        
        return selected_features
    
    @staticmethod
    def select_features_by_correlation(
        df: pd.DataFrame,
        target_column: str,
        columns: List[str],
        threshold: float = 0.1
    ) -> List[str]:
        """
        基于相关性选择特征
        
        参数:
            df: 数据框
            target_column: 目标列
            columns: 要评估的列
            threshold: 相关性阈值（绝对值）
        """
        if target_column not in df.columns:
            return []
        
        numeric_cols = [col for col in columns if col in df.select_dtypes(include=[np.number]).columns]
        if target_column not in numeric_cols:
            return []
        
        correlations = df[numeric_cols].corrwith(df[target_column]).abs()
        selected_features = correlations[correlations >= threshold].index.tolist()
        
        if target_column in selected_features:
            selected_features.remove(target_column)
        
        return selected_features
    
    @staticmethod
    def select_features_rfe(
        df: pd.DataFrame,
        target_column: str,
        columns: List[str],
        n_features: int = 10,
        model_type: str = 'regression'
    ) -> List[str]:
        """
        使用递归特征消除（RFE）选择特征
        
        参数:
            df: 数据框
            target_column: 目标列
            columns: 要评估的列
            n_features: 要选择的特征数量
            model_type: 模型类型 ('regression', 'classification')
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用RFE")
        
        numeric_cols = [col for col in columns if col in df.select_dtypes(include=[np.number]).columns]
        if target_column not in numeric_cols or len(numeric_cols) < 2:
            return []
        
        # 准备数据
        X = df[numeric_cols].drop(columns=[target_column]).dropna()
        y = df[target_column].dropna()
        
        # 对齐索引
        common_index = X.index.intersection(y.index)
        X = X.loc[common_index]
        y = y.loc[common_index]
        
        if len(X) == 0:
            return []
        
        # 选择模型
        if model_type == 'regression':
            model = LinearRegression()
        else:
            model = LogisticRegression(max_iter=1000)
        
        # RFE
        rfe = RFE(estimator=model, n_features_to_select=min(n_features, len(X.columns)))
        rfe.fit(X, y)
        
        selected_features = X.columns[rfe.support_].tolist()
        
        return selected_features
    
    @staticmethod
    def scale_features(
        df: pd.DataFrame,
        columns: List[str],
        method: str = 'minmax'
    ) -> pd.DataFrame:
        """
        特征缩放
        
        参数:
            df: 数据框
            columns: 要缩放的列
            method: 缩放方法 ('minmax', 'robust', 'quantile')
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用特征缩放")
        
        result_df = df.copy()
        numeric_cols = [col for col in columns if col in result_df.select_dtypes(include=[np.number]).columns]
        
        if not numeric_cols:
            return result_df
        
        # 选择缩放器
        if method == 'minmax':
            scaler = MinMaxScaler()
        elif method == 'robust':
            scaler = RobustScaler()
        elif method == 'quantile':
            scaler = QuantileTransformer(output_distribution='uniform')
        else:
            return result_df
        
        # 缩放
        result_df[numeric_cols] = scaler.fit_transform(result_df[numeric_cols])
        
        return result_df
    
    @staticmethod
    def get_feature_importance(
        df: pd.DataFrame,
        target_column: str,
        columns: List[str],
        model_type: str = 'regression'
    ) -> pd.Series:
        """
        获取特征重要性
        
        参数:
            df: 数据框
            target_column: 目标列
            columns: 特征列
            model_type: 模型类型 ('regression', 'classification')
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用特征重要性")
        
        numeric_cols = [col for col in columns if col in df.select_dtypes(include=[np.number]).columns]
        if target_column not in numeric_cols or len(numeric_cols) < 2:
            return pd.Series()
        
        # 准备数据
        X = df[numeric_cols].drop(columns=[target_column]).dropna()
        y = df[target_column].dropna()
        
        # 对齐索引
        common_index = X.index.intersection(y.index)
        X = X.loc[common_index]
        y = y.loc[common_index]
        
        if len(X) == 0:
            return pd.Series()
        
        # 选择模型
        if model_type == 'regression':
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        else:
            model = RandomForestClassifier(n_estimators=100, random_state=42)
        
        model.fit(X, y)
        
        # 获取特征重要性
        importance = pd.Series(model.feature_importances_, index=X.columns)
        importance = importance.sort_values(ascending=False)
        
        return importance

