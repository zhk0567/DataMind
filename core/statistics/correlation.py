"""
相关分析模块
"""
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
from typing import Dict, Any, List


class CorrelationAnalysis:
    """相关分析类"""
    
    def correlation_analysis(
        self, df: pd.DataFrame, columns: List[str], method: str = "pearson"
    ) -> Dict[str, Any]:
        """相关分析"""
        numeric_cols = [
            col for col in columns
            if col in df.columns and df[col].dtype in ['int64', 'float64']
        ]
        
        if len(numeric_cols) < 2:
            return {"error": "相关分析至少需要2个数值型变量"}
        
        if method == "pearson":
            corr_matrix = df[numeric_cols].corr(method='pearson')
        elif method == "spearman":
            corr_matrix = df[numeric_cols].corr(method='spearman')
        elif method == "kendall":
            corr_matrix = df[numeric_cols].corr(method='kendall')
        else:
            return {"error": f"不支持的相关分析方法: {method}"}
        
        # 计算p值
        n = len(df[numeric_cols].dropna())
        p_values = np.zeros_like(corr_matrix.values)
        for i in range(len(numeric_cols)):
            for j in range(len(numeric_cols)):
                if i != j:
                    col1_data = df[numeric_cols[i]].dropna()
                    col2_data = df[numeric_cols[j]].dropna()
                    common_idx = col1_data.index.intersection(col2_data.index)
                    
                    if len(common_idx) < 3:
                        p_values[i, j] = 1.0
                        continue
                    
                    if method == "pearson":
                        r, p = stats.pearsonr(
                            col1_data.loc[common_idx],
                            col2_data.loc[common_idx]
                        )
                    elif method == "spearman":
                        r, p = stats.spearmanr(
                            col1_data.loc[common_idx],
                            col2_data.loc[common_idx]
                        )
                    else:  # kendall
                        r, p = stats.kendalltau(
                            col1_data.loc[common_idx],
                            col2_data.loc[common_idx]
                        )
                    p_values[i, j] = p
        
        return {
            "correlation_matrix": corr_matrix.to_dict(),
            "p_value_matrix": pd.DataFrame(
                p_values, index=numeric_cols, columns=numeric_cols
            ).to_dict(),
            "method": method,
            "columns": numeric_cols,
            "n": int(n)
        }
    
    def partial_correlation(
        self, df: pd.DataFrame, x_col: str, y_col: str, control_cols: List[str]
    ) -> Dict[str, Any]:
        """偏相关分析"""
        all_cols = [x_col, y_col] + control_cols
        if not all(col in df.columns for col in all_cols):
            return {"error": "指定的列不存在"}
        
        valid_data = df[all_cols].dropna()
        
        if len(valid_data) < len(control_cols) + 3:
            return {"error": "数据不足"}
        
        from scipy.stats import pearsonr
        
        if len(control_cols) > 0:
            X_control = valid_data[control_cols].values
            y_x = valid_data[x_col].values
            y_y = valid_data[y_col].values
            
            model_x = LinearRegression().fit(X_control, y_x)
            model_y = LinearRegression().fit(X_control, y_y)
            
            residuals_x = y_x - model_x.predict(X_control)
            residuals_y = y_y - model_y.predict(X_control)
            
            partial_r, partial_p = pearsonr(residuals_x, residuals_y)
        else:
            partial_r, partial_p = pearsonr(valid_data[x_col], valid_data[y_col])
        
        zero_order_r, zero_order_p = pearsonr(valid_data[x_col], valid_data[y_col])
        
        return {
            "partial_correlation": float(partial_r),
            "partial_p_value": float(partial_p),
            "zero_order_correlation": float(zero_order_r),
            "zero_order_p_value": float(zero_order_p),
            "control_variables": control_cols,
            "n": int(len(valid_data)),
            "significant": partial_p < 0.05
        }

