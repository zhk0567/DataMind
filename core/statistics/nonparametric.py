"""
非参数统计模块
提供秩检验、分布检验等功能
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from scipy import stats
from scipy.stats import (
    wilcoxon, friedmanchisquare, mannwhitneyu, kruskal,
    kstest, shapiro, anderson
)


class NonparametricAnalyzer:
    """非参数统计分析类"""
    
    @staticmethod
    def wilcoxon_signed_rank_test(
        df: pd.DataFrame,
        var1: str,
        var2: Optional[str] = None,
        zero_method: str = 'wilcox'
    ) -> Dict[str, Any]:
        """
        Wilcoxon符号秩检验
        
        参数:
            df: 数据框
            var1: 第一个变量（或配对检验的差值）
            var2: 第二个变量（配对检验时使用）
            zero_method: 零处理方法
        """
        if var1 not in df.columns:
            return {'error': '变量1不存在'}
        
        if var2 is None:
            # 单样本检验（与0比较）
            data = df[var1].dropna().values
            if len(data) < 3:
                return {'error': '数据点不足'}
            
            statistic, p_value = wilcoxon(data, zero_method=zero_method)
        else:
            # 配对样本检验
            if var2 not in df.columns:
                return {'error': '变量2不存在'}
            
            data1 = df[var1].dropna()
            data2 = df[var2].dropna()
            common_index = data1.index.intersection(data2.index)
            
            if len(common_index) < 3:
                return {'error': '配对数据点不足'}
            
            diff = data1.loc[common_index] - data2.loc[common_index]
            statistic, p_value = wilcoxon(diff, zero_method=zero_method)
        
        return {
            'test_name': 'Wilcoxon符号秩检验',
            'statistic': float(statistic),
            'p_value': float(p_value),
            'significant': p_value < 0.05,
            'interpretation': '有显著差异' if p_value < 0.05 else '无显著差异'
        }
    
    @staticmethod
    def friedman_test(
        df: pd.DataFrame,
        columns: List[str]
    ) -> Dict[str, Any]:
        """
        Friedman检验（多个相关样本的非参数检验）
        
        参数:
            df: 数据框
            columns: 要比较的变量列
        """
        numeric_cols = [col for col in columns if col in df.select_dtypes(include=[np.number]).columns]
        if len(numeric_cols) < 3:
            return {'error': '至少需要3个变量'}
        
        # 准备数据（确保所有列有相同的索引）
        data_list = []
        common_index = df.index
        for col in numeric_cols:
            data_list.append(df[col].loc[common_index].dropna().values)
        
        # 找到所有列都有值的行
        valid_mask = ~df[numeric_cols].isnull().any(axis=1)
        if valid_mask.sum() < 3:
            return {'error': '有效数据点不足'}
        
        data_array = df.loc[valid_mask, numeric_cols].values.T
        
        if data_array.shape[1] < 3:
            return {'error': '有效数据点不足'}
        
        statistic, p_value = friedmanchisquare(*data_array)
        
        return {
            'test_name': 'Friedman检验',
            'statistic': float(statistic),
            'p_value': float(p_value),
            'significant': p_value < 0.05,
            'interpretation': '各组存在显著差异' if p_value < 0.05 else '各组无显著差异',
            'variables': numeric_cols
        }
    
    @staticmethod
    def sign_test(
        df: pd.DataFrame,
        var1: str,
        var2: Optional[str] = None,
        median: float = 0.0
    ) -> Dict[str, Any]:
        """
        符号检验
        
        参数:
            df: 数据框
            var1: 第一个变量
            var2: 第二个变量（配对检验时使用）
            median: 中位数（单样本检验时使用）
        """
        if var1 not in df.columns:
            return {'error': '变量1不存在'}
        
        if var2 is None:
            # 单样本符号检验
            data = df[var1].dropna().values
            if len(data) < 3:
                return {'error': '数据点不足'}
            
            positive = (data > median).sum()
            negative = (data < median).sum()
            zero = (data == median).sum()
        else:
            # 配对符号检验
            if var2 not in df.columns:
                return {'error': '变量2不存在'}
            
            data1 = df[var1].dropna()
            data2 = df[var2].dropna()
            common_index = data1.index.intersection(data2.index)
            
            if len(common_index) < 3:
                return {'error': '配对数据点不足'}
            
            diff = data1.loc[common_index] - data2.loc[common_index]
            positive = (diff > 0).sum()
            negative = (diff < 0).sum()
            zero = (diff == 0).sum()
        
        n = positive + negative
        if n == 0:
            return {'error': '没有有效的符号'}
        
        # 二项检验
        p_value = stats.binom_test(min(positive, negative), n, p=0.5, alternative='two-sided')
        
        return {
            'test_name': '符号检验',
            'positive': int(positive),
            'negative': int(negative),
            'zero': int(zero),
            'p_value': float(p_value),
            'significant': p_value < 0.05,
            'interpretation': '有显著差异' if p_value < 0.05 else '无显著差异'
        }
    
    @staticmethod
    def kolmogorov_smirnov_test(
        df: pd.DataFrame,
        column: str,
        dist: str = 'norm'
    ) -> Dict[str, Any]:
        """
        Kolmogorov-Smirnov检验（分布拟合检验）
        
        参数:
            df: 数据框
            column: 变量列
            dist: 分布类型 ('norm', 'uniform', 'expon')
        """
        if column not in df.columns:
            return {'error': '变量不存在'}
        
        data = df[column].dropna().values
        if len(data) < 3:
            return {'error': '数据点不足'}
        
        # 选择分布
        if dist == 'norm':
            dist_obj = stats.norm
            params = dist_obj.fit(data)
        elif dist == 'uniform':
            dist_obj = stats.uniform
            params = dist_obj.fit(data)
        elif dist == 'expon':
            dist_obj = stats.expon
            params = dist_obj.fit(data)
        else:
            return {'error': f'不支持的分布类型: {dist}'}
        
        # KS检验
        statistic, p_value = kstest(data, dist_obj.cdf, args=params)
        
        return {
            'test_name': 'Kolmogorov-Smirnov检验',
            'distribution': dist,
            'statistic': float(statistic),
            'p_value': float(p_value),
            'fitted_params': params,
            'fits_distribution': p_value > 0.05,
            'interpretation': f'数据符合{dist}分布' if p_value > 0.05 else f'数据不符合{dist}分布'
        }
    
    @staticmethod
    def shapiro_wilk_test(
        df: pd.DataFrame,
        column: str
    ) -> Dict[str, Any]:
        """
        Shapiro-Wilk正态性检验
        
        参数:
            df: 数据框
            column: 变量列
        """
        if column not in df.columns:
            return {'error': '变量不存在'}
        
        data = df[column].dropna().values
        if len(data) < 3:
            return {'error': '数据点不足'}
        if len(data) > 5000:
            data = data[:5000]  # Shapiro-Wilk检验最多支持5000个样本
        
        statistic, p_value = shapiro(data)
        
        return {
            'test_name': 'Shapiro-Wilk正态性检验',
            'statistic': float(statistic),
            'p_value': float(p_value),
            'is_normal': p_value > 0.05,
            'interpretation': '数据符合正态分布' if p_value > 0.05 else '数据不符合正态分布'
        }
    
    @staticmethod
    def anderson_darling_test(
        df: pd.DataFrame,
        column: str,
        dist: str = 'norm'
    ) -> Dict[str, Any]:
        """
        Anderson-Darling检验
        
        参数:
            df: 数据框
            column: 变量列
            dist: 分布类型 ('norm', 'expon', 'logistic', 'gumbel', 'gumbel_l', 'weibull_min')
        """
        if column not in df.columns:
            return {'error': '变量不存在'}
        
        data = df[column].dropna().values
        if len(data) < 3:
            return {'error': '数据点不足'}
        
        try:
            result = anderson(data, dist=dist)
            
            return {
                'test_name': 'Anderson-Darling检验',
                'distribution': dist,
                'statistic': float(result.statistic),
                'critical_values': result.critical_values.tolist(),
                'significance_levels': result.significance_level.tolist(),
                'fits_distribution': result.statistic < result.critical_values[-1],
                'interpretation': f'数据符合{dist}分布' if result.statistic < result.critical_values[-1] else f'数据不符合{dist}分布'
            }
        except Exception as e:
            return {'error': f'Anderson-Darling检验失败: {str(e)}'}

