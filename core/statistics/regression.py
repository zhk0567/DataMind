"""
回归分析模块
"""
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any, List, Optional


class RegressionAnalysis:
    """回归分析类"""
    
    def regression_analysis(
        self, df: pd.DataFrame, columns: List[str], options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """回归分析（扩展版）"""
        if len(columns) < 2:
            return {"error": "回归分析需要至少2个变量"}
        
        y_col = columns[-1]
        x_cols = columns[:-1]
        
        numeric_x_cols = [
            col for col in x_cols
            if col in df.columns and df[col].dtype in ['int64', 'float64']
        ]
        
        if df[y_col].dtype not in ['int64', 'float64']:
            return {"error": "因变量必须是数值型"}
        
        if not numeric_x_cols:
            return {"error": "自变量中没有数值型变量"}
        
        all_cols = numeric_x_cols + [y_col]
        valid_data = df[all_cols].dropna()
        
        if len(valid_data) < len(numeric_x_cols) + 2:
            return {"error": "数据不足，无法进行回归分析"}
        
        X = valid_data[numeric_x_cols].values
        y = valid_data[y_col].values
        
        scaler = None
        if options.get("standardize", False):
            scaler = StandardScaler()
            X = scaler.fit_transform(X)
        
        model = LinearRegression()
        model.fit(X, y)
        
        r_squared = model.score(X, y)
        n = len(y)
        p = len(numeric_x_cols)
        adj_r_squared = (
            1 - (1 - r_squared) * (n - 1) / (n - p - 1)
            if n > p + 1 else r_squared
        )
        
        y_pred = model.predict(X)
        residuals = y - y_pred
        
        mse = np.sum(residuals ** 2) / (n - p - 1) if n > p + 1 else 0
        try:
            var_coef = mse * np.linalg.inv(X.T @ X) if n > p + 1 else np.zeros((p, p))
            se_coef = np.sqrt(np.diag(var_coef))
            t_stats = model.coef_ / se_coef if np.all(se_coef > 0) else np.zeros(p)
            p_values = 2 * (1 - stats.t.cdf(np.abs(t_stats), n - p - 1))
        except:
            se_coef = np.zeros(p)
            t_stats = np.zeros(p)
            p_values = np.ones(p)
        
        coefficients = {}
        for i, col in enumerate(numeric_x_cols):
            coefficients[col] = {
                "coefficient": float(model.coef_[i]),
                "std_error": float(se_coef[i]) if i < len(se_coef) else 0.0,
                "t_statistic": float(t_stats[i]) if i < len(t_stats) else 0.0,
                "p_value": float(p_values[i]) if i < len(p_values) else 1.0,
                "significant": float(p_values[i]) < 0.05 if i < len(p_values) else False
            }
        
        ss_reg = np.sum((y_pred - y.mean()) ** 2)
        ss_res = np.sum(residuals ** 2)
        f_stat = (
            (ss_reg / p) / (ss_res / (n - p - 1))
            if (n > p + 1 and ss_res > 0) else 0
        )
        f_p_value = (
            1 - stats.f.cdf(f_stat, p, n - p - 1) if f_stat > 0 else 1.0
        )
        
        return {
            "coefficients": coefficients,
            "intercept": {
                "value": float(model.intercept_),
                "std_error": 0.0,
                "t_statistic": 0.0,
                "p_value": 1.0
            },
            "r_squared": float(r_squared),
            "adj_r_squared": float(adj_r_squared),
            "f_statistic": float(f_stat),
            "f_p_value": float(f_p_value),
            "mse": float(mse),
            "rmse": float(np.sqrt(mse)),
            "n": int(n),
            "predictions": y_pred.tolist(),
            "residuals": residuals.tolist(),
            "x_columns": numeric_x_cols,
            "y_column": y_col
        }
    
    def stepwise_regression(
        self, df: pd.DataFrame, y_col: str, x_cols: List[str],
        direction: str = "forward", alpha_enter: float = 0.05,
        alpha_remove: float = 0.10
    ) -> Dict[str, Any]:
        """逐步回归"""
        if y_col not in df.columns:
            return {"error": "因变量不存在"}
        
        numeric_x_cols = [
            col for col in x_cols
            if col in df.columns and df[col].dtype in ['int64', 'float64']
        ]
        
        if len(numeric_x_cols) == 0:
            return {"error": "没有可用的自变量"}
        
        all_cols = numeric_x_cols + [y_col]
        valid_data = df[all_cols].dropna()
        
        if len(valid_data) < len(numeric_x_cols) + 2:
            return {"error": "数据不足"}
        
        selected_vars = []
        remaining_vars = numeric_x_cols.copy()
        
        if direction in ["forward", "both"]:
            while remaining_vars:
                best_var = None
                best_p = 1.0
                
                for var in remaining_vars:
                    test_vars = selected_vars + [var]
                    X = valid_data[test_vars].values
                    y = valid_data[y_col].values
                    
                    model = LinearRegression().fit(X, y)
                    y_pred = model.predict(X)
                    ss_res = np.sum((y - y_pred) ** 2)
                    ss_tot = np.sum((y - y.mean()) ** 2)
                    r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
                    
                    n = len(y)
                    p = len(test_vars)
                    if n > p + 1 and ss_res > 0:
                        f_stat = ((ss_tot - ss_res) / p) / (ss_res / (n - p - 1))
                        p_value = 1 - stats.f.cdf(f_stat, p, n - p - 1)
                    else:
                        p_value = 1.0
                    
                    if p_value < best_p and p_value < alpha_enter:
                        best_p = p_value
                        best_var = var
                
                if best_var:
                    selected_vars.append(best_var)
                    remaining_vars.remove(best_var)
                else:
                    break
        
        if selected_vars:
            X_final = valid_data[selected_vars].values
            y_final = valid_data[y_col].values
            final_model = LinearRegression().fit(X_final, y_final)
            r2_final = final_model.score(X_final, y_final)
            
            return {
                "selected_variables": selected_vars,
                "r_squared": float(r2_final),
                "coefficients": {
                    col: float(coef)
                    for col, coef in zip(selected_vars, final_model.coef_)
                },
                "intercept": float(final_model.intercept_),
                "direction": direction
            }
        else:
            return {"error": "没有变量被选中"}
    
    def logistic_regression(
        self, df: pd.DataFrame, y_col: str, x_cols: List[str]
    ) -> Dict[str, Any]:
        """逻辑回归"""
        if y_col not in df.columns:
            return {"error": "因变量不存在"}
        
        numeric_x_cols = [
            col for col in x_cols
            if col in df.columns and df[col].dtype in ['int64', 'float64']
        ]
        
        if len(numeric_x_cols) == 0:
            return {"error": "没有可用的自变量"}
        
        all_cols = numeric_x_cols + [y_col]
        valid_data = df[all_cols].dropna()
        
        if len(valid_data) < len(numeric_x_cols) + 2:
            return {"error": "数据不足"}
        
        X = valid_data[numeric_x_cols].values
        y = valid_data[y_col].values
        
        unique_y = np.unique(y)
        if len(unique_y) != 2:
            return {"error": "因变量必须是二分类变量"}
        
        model = LogisticRegression(max_iter=1000)
        model.fit(X, y)
        
        y_pred = model.predict(X)
        y_pred_proba = model.predict_proba(X)
        accuracy = np.mean(y_pred == y)
        
        from sklearn.metrics import confusion_matrix
        cm = confusion_matrix(y, y_pred)
        tn, fp, fn, tp = cm.ravel()
        
        return {
            "coefficients": {
                col: float(coef)
                for col, coef in zip(numeric_x_cols, model.coef_[0])
            },
            "intercept": float(model.intercept_[0]),
            "accuracy": float(accuracy),
            "confusion_matrix": {
                "true_negative": int(tn),
                "false_positive": int(fp),
                "false_negative": int(fn),
                "true_positive": int(tp)
            },
            "predictions": y_pred.tolist(),
            "predicted_probabilities": y_pred_proba.tolist(),
            "x_columns": numeric_x_cols,
            "y_column": y_col
        }

