"""
监督学习模块 - 回归方法
将回归相关方法提取到此模块
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
try:
    from sklearn.svm import SVR
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.neural_network import MLPRegressor
    from sklearn.linear_model import Ridge, Lasso, ElasticNet
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class SupervisedRegression:
    """监督学习回归方法"""
    
    @staticmethod
    def svm_regression(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str],
        kernel: str = 'rbf',
        C: float = 1.0,
        gamma: Optional[str] = 'scale'
    ) -> Dict[str, Any]:
        """支持向量回归"""
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用SVR")
        
        if target_column not in df.columns:
            return {'error': '目标列不存在'}
        
        numeric_cols = [col for col in feature_columns if col in df.select_dtypes(include=[np.number]).columns]
        if len(numeric_cols) < 1:
            return {'error': '至少需要1个数值特征变量'}
        
        data = df[numeric_cols + [target_column]].dropna()
        if len(data) < 10:
            return {'error': '数据点不足'}
        
        X = data[numeric_cols].values
        y = data[target_column].values
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        y_scaled = scaler.fit_transform(y.reshape(-1, 1)).ravel()
        
        model = SVR(kernel=kernel, C=C, gamma=gamma)
        model.fit(X_scaled, y_scaled)
        
        y_pred = model.predict(X_scaled)
        y_pred_original = scaler.inverse_transform(y_pred.reshape(-1, 1)).ravel()
        
        r_squared = 1 - np.sum((y - y_pred_original) ** 2) / np.sum((y - np.mean(y)) ** 2)
        mse = np.mean((y - y_pred_original) ** 2)
        rmse = np.sqrt(mse)
        
        return {
            'model_type': 'SVM Regression',
            'kernel': kernel,
            'r_squared': float(r_squared),
            'mse': float(mse),
            'rmse': float(rmse),
            'n_support_vectors': int(model.n_support_)
        }
    
    @staticmethod
    def knn_regression(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str],
        n_neighbors: int = 5
    ) -> Dict[str, Any]:
        """K近邻回归"""
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用KNN")
        
        if target_column not in df.columns:
            return {'error': '目标列不存在'}
        
        numeric_cols = [col for col in feature_columns if col in df.select_dtypes(include=[np.number]).columns]
        if len(numeric_cols) < 1:
            return {'error': '至少需要1个数值特征变量'}
        
        data = df[numeric_cols + [target_column]].dropna()
        if len(data) < n_neighbors + 1:
            return {'error': '数据点不足'}
        
        X = data[numeric_cols].values
        y = data[target_column].values
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        model = KNeighborsRegressor(n_neighbors=n_neighbors)
        model.fit(X_scaled, y)
        
        y_pred = model.predict(X_scaled)
        r_squared = 1 - np.sum((y - y_pred) ** 2) / np.sum((y - np.mean(y)) ** 2)
        mse = np.mean((y - y_pred) ** 2)
        rmse = np.sqrt(mse)
        
        return {
            'model_type': 'KNN Regression',
            'n_neighbors': n_neighbors,
            'r_squared': float(r_squared),
            'mse': float(mse),
            'rmse': float(rmse)
        }
    
    @staticmethod
    def mlp_regression(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str],
        hidden_layers: tuple = (100,),
        max_iter: int = 500
    ) -> Dict[str, Any]:
        """多层感知机回归"""
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用MLP")
        
        if target_column not in df.columns:
            return {'error': '目标列不存在'}
        
        numeric_cols = [col for col in feature_columns if col in df.select_dtypes(include=[np.number]).columns]
        if len(numeric_cols) < 1:
            return {'error': '至少需要1个数值特征变量'}
        
        data = df[numeric_cols + [target_column]].dropna()
        if len(data) < 10:
            return {'error': '数据点不足'}
        
        X = data[numeric_cols].values
        y = data[target_column].values
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        y_scaled = scaler.fit_transform(y.reshape(-1, 1)).ravel()
        
        model = MLPRegressor(hidden_layer_sizes=hidden_layers, max_iter=max_iter, random_state=42)
        model.fit(X_scaled, y_scaled)
        
        y_pred = model.predict(X_scaled)
        y_pred_original = scaler.inverse_transform(y_pred.reshape(-1, 1)).ravel()
        
        r_squared = 1 - np.sum((y - y_pred_original) ** 2) / np.sum((y - np.mean(y)) ** 2)
        mse = np.mean((y - y_pred_original) ** 2)
        rmse = np.sqrt(mse)
        
        return {
            'model_type': 'MLP Regression',
            'hidden_layers': hidden_layers,
            'r_squared': float(r_squared),
            'mse': float(mse),
            'rmse': float(rmse)
        }
    
    @staticmethod
    def ridge_regression(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str],
        alpha: float = 1.0
    ) -> Dict[str, Any]:
        """岭回归"""
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用岭回归")
        
        if target_column not in df.columns:
            return {'error': '目标列不存在'}
        
        numeric_cols = [col for col in feature_columns if col in df.select_dtypes(include=[np.number]).columns]
        if len(numeric_cols) < 1:
            return {'error': '至少需要1个数值特征变量'}
        
        data = df[numeric_cols + [target_column]].dropna()
        if len(data) < len(numeric_cols) + 2:
            return {'error': '数据点不足'}
        
        X = data[numeric_cols].values
        y = data[target_column].values
        
        model = Ridge(alpha=alpha)
        model.fit(X, y)
        
        y_pred = model.predict(X)
        r_squared = model.score(X, y)
        mse = np.mean((y - y_pred) ** 2)
        rmse = np.sqrt(mse)
        
        return {
            'model_type': 'Ridge Regression',
            'alpha': alpha,
            'r_squared': float(r_squared),
            'mse': float(mse),
            'rmse': float(rmse),
            'coefficients': {col: float(coef) for col, coef in zip(numeric_cols, model.coef_)}
        }
    
    @staticmethod
    def lasso_regression(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str],
        alpha: float = 1.0
    ) -> Dict[str, Any]:
        """Lasso回归"""
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用Lasso回归")
        
        if target_column not in df.columns:
            return {'error': '目标列不存在'}
        
        numeric_cols = [col for col in feature_columns if col in df.select_dtypes(include=[np.number]).columns]
        if len(numeric_cols) < 1:
            return {'error': '至少需要1个数值特征变量'}
        
        data = df[numeric_cols + [target_column]].dropna()
        if len(data) < len(numeric_cols) + 2:
            return {'error': '数据点不足'}
        
        X = data[numeric_cols].values
        y = data[target_column].values
        
        model = Lasso(alpha=alpha)
        model.fit(X, y)
        
        y_pred = model.predict(X)
        r_squared = model.score(X, y)
        mse = np.mean((y - y_pred) ** 2)
        rmse = np.sqrt(mse)
        
        n_nonzero = np.sum(model.coef_ != 0)
        
        return {
            'model_type': 'Lasso Regression',
            'alpha': alpha,
            'r_squared': float(r_squared),
            'mse': float(mse),
            'rmse': float(rmse),
            'n_nonzero_coefs': int(n_nonzero),
            'coefficients': {col: float(coef) for col, coef in zip(numeric_cols, model.coef_) if coef != 0}
        }
    
    @staticmethod
    def elastic_net_regression(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str],
        alpha: float = 1.0,
        l1_ratio: float = 0.5
    ) -> Dict[str, Any]:
        """Elastic Net回归"""
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用Elastic Net")
        
        if target_column not in df.columns:
            return {'error': '目标列不存在'}
        
        numeric_cols = [col for col in feature_columns if col in df.select_dtypes(include=[np.number]).columns]
        if len(numeric_cols) < 1:
            return {'error': '至少需要1个数值特征变量'}
        
        data = df[numeric_cols + [target_column]].dropna()
        if len(data) < len(numeric_cols) + 2:
            return {'error': '数据点不足'}
        
        X = data[numeric_cols].values
        y = data[target_column].values
        
        model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio)
        model.fit(X, y)
        
        y_pred = model.predict(X)
        r_squared = model.score(X, y)
        mse = np.mean((y - y_pred) ** 2)
        rmse = np.sqrt(mse)
        
        return {
            'model_type': 'Elastic Net Regression',
            'alpha': alpha,
            'l1_ratio': l1_ratio,
            'r_squared': float(r_squared),
            'mse': float(mse),
            'rmse': float(rmse),
            'coefficients': {col: float(coef) for col, coef in zip(numeric_cols, model.coef_)}
        }

