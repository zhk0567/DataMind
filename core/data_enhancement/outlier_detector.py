"""
异常值检测增强模块
提供Z-score、DBSCAN、孤立森林等多种异常值检测方法
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from scipy import stats
try:
    from sklearn.cluster import DBSCAN
    from sklearn.ensemble import IsolationForest
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class OutlierDetector:
    """异常值检测增强类"""
    
    @staticmethod
    def detect_zscore(
        df: pd.DataFrame,
        columns: List[str],
        threshold: float = 3.0
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        使用Z-score方法检测异常值
        
        参数:
            df: 数据框
            columns: 要检测的列
            threshold: Z-score阈值（默认3.0）
        
        返回:
            (清理后的数据框, 检测结果字典)
        """
        result_df = df.copy()
        outlier_info = {}
        
        for col in columns:
            if col not in result_df.columns:
                continue
            
            data = result_df[col].dropna()
            if len(data) == 0:
                continue
            
            z_scores = np.abs(stats.zscore(data))
            outlier_mask = z_scores > threshold
            
            outlier_indices = data.index[outlier_mask].tolist()
            outlier_count = outlier_mask.sum()
            outlier_pct = (outlier_count / len(data)) * 100
            
            outlier_info[col] = {
                'count': outlier_count,
                'percentage': outlier_pct,
                'indices': outlier_indices,
                'values': data[outlier_mask].tolist()
            }
        
        return result_df, outlier_info
    
    @staticmethod
    def detect_modified_zscore(
        df: pd.DataFrame,
        columns: List[str],
        threshold: float = 3.5
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        使用修正Z-score方法检测异常值（对异常值更稳健）
        
        参数:
            df: 数据框
            columns: 要检测的列
            threshold: 修正Z-score阈值（默认3.5）
        """
        result_df = df.copy()
        outlier_info = {}
        
        for col in columns:
            if col not in result_df.columns:
                continue
            
            data = result_df[col].dropna()
            if len(data) < 2:
                continue
            
            median = np.median(data)
            mad = np.median(np.abs(data - median))  # 中位数绝对偏差
            
            if mad == 0:
                continue
            
            modified_z_scores = 0.6745 * (data - median) / mad
            outlier_mask = np.abs(modified_z_scores) > threshold
            
            outlier_indices = data.index[outlier_mask].tolist()
            outlier_count = outlier_mask.sum()
            outlier_pct = (outlier_count / len(data)) * 100
            
            outlier_info[col] = {
                'count': outlier_count,
                'percentage': outlier_pct,
                'indices': outlier_indices,
                'values': data[outlier_mask].tolist()
            }
        
        return result_df, outlier_info
    
    @staticmethod
    def detect_dbscan(
        df: pd.DataFrame,
        columns: List[str],
        eps: float = 0.5,
        min_samples: int = 5
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        使用DBSCAN聚类检测异常值
        
        参数:
            df: 数据框
            columns: 要检测的列
            eps: DBSCAN的eps参数
            min_samples: DBSCAN的min_samples参数
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用DBSCAN检测")
        
        result_df = df.copy()
        outlier_info = {}
        
        # 只处理数值列
        numeric_cols = [col for col in columns if col in result_df.select_dtypes(include=[np.number]).columns]
        if not numeric_cols:
            return result_df, outlier_info
        
        # 准备数据
        data = result_df[numeric_cols].dropna()
        if len(data) < min_samples:
            return result_df, outlier_info
        
        # 标准化数据
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data)
        
        # DBSCAN聚类
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(data_scaled)
        
        # 标记为-1的是异常值
        outlier_mask = labels == -1
        outlier_indices = data.index[outlier_mask].tolist()
        outlier_count = outlier_mask.sum()
        outlier_pct = (outlier_count / len(data)) * 100
        
        outlier_info['dbscan'] = {
            'count': outlier_count,
            'percentage': outlier_pct,
            'indices': outlier_indices,
            'columns': numeric_cols
        }
        
        return result_df, outlier_info
    
    @staticmethod
    def detect_isolation_forest(
        df: pd.DataFrame,
        columns: List[str],
        contamination: float = 0.1,
        random_state: int = 42
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        使用孤立森林检测异常值
        
        参数:
            df: 数据框
            columns: 要检测的列
            contamination: 异常值比例估计（0-1之间）
            random_state: 随机种子
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用孤立森林检测")
        
        result_df = df.copy()
        outlier_info = {}
        
        # 只处理数值列
        numeric_cols = [col for col in columns if col in result_df.select_dtypes(include=[np.number]).columns]
        if not numeric_cols:
            return result_df, outlier_info
        
        # 准备数据
        data = result_df[numeric_cols].dropna()
        if len(data) == 0:
            return result_df, outlier_info
        
        # 标准化数据
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data)
        
        # 孤立森林
        iso_forest = IsolationForest(
            contamination=contamination,
            random_state=random_state
        )
        predictions = iso_forest.fit_predict(data_scaled)
        
        # 标记为-1的是异常值
        outlier_mask = predictions == -1
        outlier_indices = data.index[outlier_mask].tolist()
        outlier_count = outlier_mask.sum()
        outlier_pct = (outlier_count / len(data)) * 100
        
        outlier_info['isolation_forest'] = {
            'count': outlier_count,
            'percentage': outlier_pct,
            'indices': outlier_indices,
            'columns': numeric_cols,
            'scores': iso_forest.score_samples(data_scaled).tolist()
        }
        
        return result_df, outlier_info
    
    @staticmethod
    def remove_outliers(
        df: pd.DataFrame,
        outlier_info: Dict[str, Any],
        method: str = 'zscore'
    ) -> pd.DataFrame:
        """
        根据检测结果移除异常值
        
        参数:
            df: 数据框
            outlier_info: 异常值检测结果
            method: 检测方法
        """
        result_df = df.copy()
        
        if method in ['zscore', 'modified_zscore']:
            # 移除所有检测到的异常值
            all_outlier_indices = set()
            for col_info in outlier_info.values():
                if isinstance(col_info, dict) and 'indices' in col_info:
                    all_outlier_indices.update(col_info['indices'])
            result_df = result_df.drop(index=list(all_outlier_indices))
        
        elif method == 'dbscan':
            if 'dbscan' in outlier_info and 'indices' in outlier_info['dbscan']:
                result_df = result_df.drop(index=outlier_info['dbscan']['indices'])
        
        elif method == 'isolation_forest':
            if 'isolation_forest' in outlier_info and 'indices' in outlier_info['isolation_forest']:
                result_df = result_df.drop(index=outlier_info['isolation_forest']['indices'])
        
        return result_df

