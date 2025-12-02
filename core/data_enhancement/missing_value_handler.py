"""
缺失值处理增强模块
提供插值法、前向/后向填充、基于模型的填充等方法
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from scipy import interpolate
try:
    from sklearn.impute import KNNImputer
    from sklearn.ensemble import RandomForestRegressor
    KNN_AVAILABLE = True
except ImportError:
    KNN_AVAILABLE = False


class MissingValueHandler:
    """缺失值处理增强类"""
    
    @staticmethod
    def interpolate_missing(
        df: pd.DataFrame,
        columns: List[str],
        method: str = 'linear',
        limit_direction: str = 'both'
    ) -> pd.DataFrame:
        """
        使用插值法填充缺失值
        
        参数:
            df: 数据框
            columns: 要处理的列
            method: 插值方法 ('linear', 'polynomial', 'spline', 'time')
            limit_direction: 限制方向 ('forward', 'backward', 'both')
        """
        result_df = df.copy()
        
        for col in columns:
            if col not in result_df.columns:
                continue
            
            if method == 'linear':
                result_df[col] = result_df[col].interpolate(
                    method='linear', limit_direction=limit_direction
                )
            elif method == 'polynomial':
                # 多项式插值
                valid_data = result_df[col].dropna()
                if len(valid_data) >= 2:
                    x_valid = valid_data.index.values
                    y_valid = valid_data.values
                    x_all = result_df[col].index.values
                    
                    # 使用numpy的多项式插值
                    if len(valid_data) >= 3:
                        poly = np.polyfit(x_valid, y_valid, min(2, len(valid_data)-1))
                        poly_func = np.poly1d(poly)
                        result_df[col] = result_df[col].fillna(
                            pd.Series(poly_func(x_all), index=result_df.index)
                        )
            elif method == 'spline':
                # 样条插值
                valid_data = result_df[col].dropna()
                if len(valid_data) >= 3:
                    x_valid = valid_data.index.values
                    y_valid = valid_data.values
                    x_all = result_df[col].index.values
                    
                    try:
                        spline = interpolate.UnivariateSpline(x_valid, y_valid, s=0)
                        result_df[col] = result_df[col].fillna(
                            pd.Series(spline(x_all), index=result_df.index)
                        )
                    except:
                        # 如果样条插值失败，使用线性插值
                        result_df[col] = result_df[col].interpolate(method='linear')
            elif method == 'time':
                # 时间序列插值
                result_df[col] = result_df[col].interpolate(
                    method='time', limit_direction=limit_direction
                )
        
        return result_df
    
    @staticmethod
    def forward_backward_fill(
        df: pd.DataFrame,
        columns: List[str],
        method: str = 'forward',
        limit: Optional[int] = None
    ) -> pd.DataFrame:
        """
        前向或后向填充
        
        参数:
            df: 数据框
            columns: 要处理的列
            method: 填充方法 ('forward', 'backward', 'both')
            limit: 最大连续填充数量
        """
        result_df = df.copy()
        
        for col in columns:
            if col not in result_df.columns:
                continue
            
            if method == 'forward':
                result_df[col] = result_df[col].fillna(method='ffill', limit=limit)
            elif method == 'backward':
                result_df[col] = result_df[col].fillna(method='bfill', limit=limit)
            elif method == 'both':
                result_df[col] = result_df[col].fillna(method='ffill', limit=limit)
                result_df[col] = result_df[col].fillna(method='bfill', limit=limit)
        
        return result_df
    
    @staticmethod
    def knn_impute(
        df: pd.DataFrame,
        columns: List[str],
        n_neighbors: int = 5
    ) -> pd.DataFrame:
        """
        使用KNN方法填充缺失值
        
        参数:
            df: 数据框
            columns: 要处理的列
            n_neighbors: KNN的邻居数量
        """
        if not KNN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用KNN填充")
        
        result_df = df.copy()
        numeric_cols = result_df.select_dtypes(include=[np.number]).columns.tolist()
        
        # 只处理数值列
        columns_to_impute = [col for col in columns if col in numeric_cols]
        if not columns_to_impute:
            return result_df
        
        # 使用KNN填充
        imputer = KNNImputer(n_neighbors=n_neighbors)
        result_df[columns_to_impute] = imputer.fit_transform(result_df[columns_to_impute])
        
        return result_df
    
    @staticmethod
    def model_based_impute(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str],
        model_type: str = 'random_forest'
    ) -> pd.DataFrame:
        """
        基于模型的填充（使用其他变量预测缺失值）
        
        参数:
            df: 数据框
            target_column: 目标列（有缺失值的列）
            feature_columns: 特征列（用于预测的列）
            model_type: 模型类型 ('random_forest', 'linear')
        """
        if not KNN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用基于模型的填充")
        
        result_df = df.copy()
        
        # 分离有缺失值和无缺失值的数据
        missing_mask = result_df[target_column].isnull()
        complete_mask = ~missing_mask
        
        if missing_mask.sum() == 0:
            return result_df
        
        # 准备特征和目标
        feature_cols = [col for col in feature_columns if col in result_df.columns]
        if not feature_cols:
            return result_df
        
        X_complete = result_df.loc[complete_mask, feature_cols].select_dtypes(include=[np.number])
        y_complete = result_df.loc[complete_mask, target_column]
        X_missing = result_df.loc[missing_mask, feature_cols].select_dtypes(include=[np.number])
        
        if len(X_complete) == 0 or len(X_missing) == 0:
            return result_df
        
        # 训练模型
        if model_type == 'random_forest':
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        else:
            from sklearn.linear_model import LinearRegression
            model = LinearRegression()
        
        model.fit(X_complete, y_complete)
        
        # 预测缺失值
        predictions = model.predict(X_missing)
        result_df.loc[missing_mask, target_column] = predictions
        
        return result_df
    
    @staticmethod
    def analyze_missing_pattern(df: pd.DataFrame) -> Dict[str, Any]:
        """
        分析缺失值模式
        
        返回:
            包含缺失值统计信息的字典
        """
        missing_count = df.isnull().sum()
        missing_pct = (missing_count / len(df)) * 100
        
        # 缺失值模式矩阵
        missing_matrix = df.isnull()
        
        # 完全缺失的列
        completely_missing = missing_count[missing_count == len(df)].index.tolist()
        
        # 无缺失的列
        no_missing = missing_count[missing_count == 0].index.tolist()
        
        # 部分缺失的列
        partially_missing = missing_count[
            (missing_count > 0) & (missing_count < len(df))
        ].index.tolist()
        
        return {
            'missing_count': missing_count.to_dict(),
            'missing_percentage': missing_pct.to_dict(),
            'completely_missing_columns': completely_missing,
            'no_missing_columns': no_missing,
            'partially_missing_columns': partially_missing,
            'total_missing': missing_count.sum(),
            'total_missing_pct': (missing_count.sum() / (len(df) * len(df.columns))) * 100
        }

