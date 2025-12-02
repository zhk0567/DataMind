"""
基础统计分析模块
"""
import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Any, List, Optional


class BasicStatistics:
    """基础统计分析类"""
    
    def descriptive_statistics(
        self, df: pd.DataFrame, columns: List[str]
    ) -> Dict[str, Any]:
        """描述性统计"""
        numeric_cols = [
            col for col in columns
            if col in df.columns and df[col].dtype in ['int64', 'float64']
        ]
        
        if not numeric_cols:
            return {"error": "所选列中没有数值型数据"}
        
        result = {}
        for col in numeric_cols:
            data = df[col].dropna()
            if len(data) == 0:
                continue
            
            result[col] = {
                "count": int(data.count()),
                "mean": float(data.mean()),
                "std": float(data.std()),
                "min": float(data.min()),
                "25%": float(data.quantile(0.25)),
                "50%": float(data.median()),
                "75%": float(data.quantile(0.75)),
                "max": float(data.max()),
                "skewness": float(data.skew()) if len(data) > 2 else 0.0,
                "kurtosis": float(data.kurtosis()) if len(data) > 2 else 0.0,
                "variance": float(data.var()),
                "range": float(data.max() - data.min()),
                "cv": float(data.std() / data.mean() * 100) if data.mean() != 0 else 0.0,
            }
        
        return result
    
    def frequency_analysis(
        self, df: pd.DataFrame, columns: List[str]
    ) -> Dict[str, Any]:
        """频数分析"""
        result = {}
        for col in columns:
            if col not in df.columns:
                continue
            
            value_counts = df[col].value_counts()
            total = len(df[col].dropna())
            
            freq_data = []
            cumulative = 0
            for value, count in value_counts.items():
                percent = (count / total * 100) if total > 0 else 0.0
                cumulative += percent
                freq_data.append({
                    "value": str(value),
                    "frequency": int(count),
                    "percent": float(percent),
                    "valid_percent": float(percent),
                    "cumulative_percent": float(cumulative)
                })
            
            result[col] = {
                "total": total,
                "missing": int(df[col].isnull().sum()),
                "frequencies": freq_data
            }
        
        return result
    
    def crosstab_analysis(
        self, df: pd.DataFrame, row_col: str, col_col: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """交叉表分析"""
        if options is None:
            options = {}
        
        if row_col not in df.columns or col_col not in df.columns:
            return {"error": "指定的列不存在"}
        
        crosstab = pd.crosstab(df[row_col], df[col_col], margins=True)
        
        chi2, p_value, dof, expected = stats.chi2_contingency(
            pd.crosstab(df[row_col], df[col_col])
        )
        
        result = {
            "crosstab": crosstab.to_dict(),
            "chi2_statistic": float(chi2),
            "p_value": float(p_value),
            "degrees_of_freedom": int(dof),
            "significant": p_value < 0.05,
            "expected_frequencies": expected.tolist() if expected is not None else []
        }
        
        return result

