"""
监督学习模块
提供分类和回归模型
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
try:
    from sklearn.svm import SVC, SVR
    from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
    from sklearn.naive_bayes import GaussianNB
    from sklearn.neural_network import MLPClassifier, MLPRegressor
    from sklearn.linear_model import Ridge, Lasso, ElasticNet
    from sklearn.ensemble import AdaBoostClassifier, AdaBoostRegressor, GradientBoostingClassifier, GradientBoostingRegressor
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False


class SupervisedLearning:
    """监督学习类"""
    
    @staticmethod
    def svm_classification(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str],
        kernel: str = 'rbf',
        C: float = 1.0,
        gamma: Optional[str] = 'scale'
    ) -> Dict[str, Any]:
        """
        支持向量机分类
        
        参数:
            df: 数据框
            target_column: 目标变量
            feature_columns: 特征变量
            kernel: 核函数 ('linear', 'poly', 'rbf', 'sigmoid')
            C: 正则化参数
            gamma: 核函数参数
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用SVM")
        
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
        
        # 如果是分类变量，进行编码
        if y.dtype == 'object':
            le = LabelEncoder()
            y = le.fit_transform(y)
        
        # 标准化特征
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # 训练模型
        model = SVC(kernel=kernel, C=C, gamma=gamma, random_state=42)
        model.fit(X_scaled, y)
        
        # 预测
        y_pred = model.predict(X_scaled)
        accuracy = np.mean(y_pred == y)
        
        return {
            'model_type': 'SVM Classification',
            'kernel': kernel,
            'accuracy': float(accuracy),
            'n_support_vectors': int(model.n_support_.sum()),
            'classes': model.classes_.tolist() if hasattr(model, 'classes_') else []
        }
    
    @staticmethod
    def svm_regression(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str],
        kernel: str = 'rbf',
        C: float = 1.0,
        gamma: Optional[str] = 'scale'
    ) -> Dict[str, Any]:
        """
        支持向量回归
        
        参数:
            df: 数据框
            target_column: 目标变量
            feature_columns: 特征变量
            kernel: 核函数
            C: 正则化参数
            gamma: 核函数参数
        """
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
        
        # 标准化
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        y_scaled = scaler.fit_transform(y.reshape(-1, 1)).ravel()
        
        # 训练模型
        model = SVR(kernel=kernel, C=C, gamma=gamma)
        model.fit(X_scaled, y_scaled)
        
        # 预测
        y_pred = model.predict(X_scaled)
        y_pred_original = scaler.inverse_transform(y_pred.reshape(-1, 1)).ravel()
        
        # 计算R²
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
    def knn_classification(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str],
        n_neighbors: int = 5
    ) -> Dict[str, Any]:
        """
        K近邻分类
        
        参数:
            df: 数据框
            target_column: 目标变量
            feature_columns: 特征变量
            n_neighbors: 邻居数量
        """
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
        
        if y.dtype == 'object':
            le = LabelEncoder()
            y = le.fit_transform(y)
        
        # 标准化
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # 训练模型
        model = KNeighborsClassifier(n_neighbors=n_neighbors)
        model.fit(X_scaled, y)
        
        # 预测
        y_pred = model.predict(X_scaled)
        accuracy = np.mean(y_pred == y)
        
        return {
            'model_type': 'KNN Classification',
            'n_neighbors': n_neighbors,
            'accuracy': float(accuracy)
        }
    
    @staticmethod
    def knn_regression(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str],
        n_neighbors: int = 5
    ) -> Dict[str, Any]:
        """
        K近邻回归
        
        参数:
            df: 数据框
            target_column: 目标变量
            feature_columns: 特征变量
            n_neighbors: 邻居数量
        """
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
        
        # 标准化
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # 训练模型
        model = KNeighborsRegressor(n_neighbors=n_neighbors)
        model.fit(X_scaled, y)
        
        # 预测
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
    def naive_bayes_classification(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str]
    ) -> Dict[str, Any]:
        """
        朴素贝叶斯分类
        
        参数:
            df: 数据框
            target_column: 目标变量
            feature_columns: 特征变量
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用朴素贝叶斯")
        
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
        
        if y.dtype == 'object':
            le = LabelEncoder()
            y = le.fit_transform(y)
        
        # 训练模型
        model = GaussianNB()
        model.fit(X, y)
        
        # 预测
        y_pred = model.predict(X)
        accuracy = np.mean(y_pred == y)
        
        return {
            'model_type': 'Naive Bayes Classification',
            'accuracy': float(accuracy),
            'classes': model.classes_.tolist()
        }
    
    @staticmethod
    def mlp_classification(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str],
        hidden_layers: tuple = (100,),
        activation: str = 'relu',
        max_iter: int = 500
    ) -> Dict[str, Any]:
        """
        多层感知器（神经网络）分类
        
        参数:
            df: 数据框
            target_column: 目标变量
            feature_columns: 特征变量
            hidden_layers: 隐藏层结构
            activation: 激活函数
            max_iter: 最大迭代次数
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用神经网络")
        
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
        
        if y.dtype == 'object':
            le = LabelEncoder()
            y = le.fit_transform(y)
        
        # 标准化
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # 训练模型
        model = MLPClassifier(
            hidden_layer_sizes=hidden_layers,
            activation=activation,
            max_iter=max_iter,
            random_state=42
        )
        model.fit(X_scaled, y)
        
        # 预测
        y_pred = model.predict(X_scaled)
        accuracy = np.mean(y_pred == y)
        
        return {
            'model_type': 'MLP Classification',
            'hidden_layers': hidden_layers,
            'activation': activation,
            'accuracy': float(accuracy),
            'n_iter': int(model.n_iter_),
            'loss': float(model.loss_)
        }
    
    @staticmethod
    def mlp_regression(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str],
        hidden_layers: tuple = (100,),
        activation: str = 'relu',
        max_iter: int = 500
    ) -> Dict[str, Any]:
        """
        多层感知器（神经网络）回归
        
        参数:
            df: 数据框
            target_column: 目标变量
            feature_columns: 特征变量
            hidden_layers: 隐藏层结构
            activation: 激活函数
            max_iter: 最大迭代次数
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用神经网络")
        
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
        
        # 标准化
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        y_scaled = scaler.fit_transform(y.reshape(-1, 1)).ravel()
        
        # 训练模型
        model = MLPRegressor(
            hidden_layer_sizes=hidden_layers,
            activation=activation,
            max_iter=max_iter,
            random_state=42
        )
        model.fit(X_scaled, y_scaled)
        
        # 预测
        y_pred = model.predict(X_scaled)
        y_pred_original = scaler.inverse_transform(y_pred.reshape(-1, 1)).ravel()
        
        r_squared = 1 - np.sum((y - y_pred_original) ** 2) / np.sum((y - np.mean(y)) ** 2)
        mse = np.mean((y - y_pred_original) ** 2)
        rmse = np.sqrt(mse)
        
        return {
            'model_type': 'MLP Regression',
            'hidden_layers': hidden_layers,
            'activation': activation,
            'r_squared': float(r_squared),
            'mse': float(mse),
            'rmse': float(rmse),
            'n_iter': int(model.n_iter_),
            'loss': float(model.loss_)
        }
    
    @staticmethod
    def ridge_regression(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str],
        alpha: float = 1.0
    ) -> Dict[str, Any]:
        """
        岭回归
        
        参数:
            df: 数据框
            target_column: 目标变量
            feature_columns: 特征变量
            alpha: 正则化参数
        """
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
        
        # 训练模型
        model = Ridge(alpha=alpha)
        model.fit(X, y)
        
        # 预测
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
        """
        Lasso回归
        
        参数:
            df: 数据框
            target_column: 目标变量
            feature_columns: 特征变量
            alpha: 正则化参数
        """
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
        
        # 训练模型
        model = Lasso(alpha=alpha)
        model.fit(X, y)
        
        # 预测
        y_pred = model.predict(X)
        r_squared = model.score(X, y)
        mse = np.mean((y - y_pred) ** 2)
        rmse = np.sqrt(mse)
        
        # 统计非零系数数量
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
        """
        Elastic Net回归
        
        参数:
            df: 数据框
            target_column: 目标变量
            feature_columns: 特征变量
            alpha: 正则化参数
            l1_ratio: L1和L2正则化的混合比例
        """
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
        
        # 训练模型
        model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio)
        model.fit(X, y)
        
        # 预测
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
    
    @staticmethod
    def adaboost_classification(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str],
        n_estimators: int = 50
    ) -> Dict[str, Any]:
        """
        AdaBoost分类
        
        参数:
            df: 数据框
            target_column: 目标变量
            feature_columns: 特征变量
            n_estimators: 弱学习器数量
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用AdaBoost")
        
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
        
        if y.dtype == 'object':
            le = LabelEncoder()
            y = le.fit_transform(y)
        
        # 训练模型
        model = AdaBoostClassifier(n_estimators=n_estimators, random_state=42)
        model.fit(X, y)
        
        # 预测
        y_pred = model.predict(X)
        accuracy = np.mean(y_pred == y)
        
        return {
            'model_type': 'AdaBoost Classification',
            'n_estimators': n_estimators,
            'accuracy': float(accuracy),
            'feature_importance': {col: float(imp) for col, imp in zip(numeric_cols, model.feature_importances_)}
        }
    
    @staticmethod
    def gradient_boosting_classification(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str],
        n_estimators: int = 100,
        learning_rate: float = 0.1
    ) -> Dict[str, Any]:
        """
        梯度提升分类
        
        参数:
            df: 数据框
            target_column: 目标变量
            feature_columns: 特征变量
            n_estimators: 树的数量
            learning_rate: 学习率
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用梯度提升")
        
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
        
        if y.dtype == 'object':
            le = LabelEncoder()
            y = le.fit_transform(y)
        
        # 训练模型
        model = GradientBoostingClassifier(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            random_state=42
        )
        model.fit(X, y)
        
        # 预测
        y_pred = model.predict(X)
        accuracy = np.mean(y_pred == y)
        
        return {
            'model_type': 'Gradient Boosting Classification',
            'n_estimators': n_estimators,
            'learning_rate': learning_rate,
            'accuracy': float(accuracy),
            'feature_importance': {col: float(imp) for col, imp in zip(numeric_cols, model.feature_importances_)}
        }
    
    @staticmethod
    def xgboost_classification(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str],
        n_estimators: int = 100,
        learning_rate: float = 0.1,
        max_depth: int = 3
    ) -> Dict[str, Any]:
        """
        XGBoost分类
        
        参数:
            df: 数据框
            target_column: 目标变量
            feature_columns: 特征变量
            n_estimators: 树的数量
            learning_rate: 学习率
            max_depth: 树的最大深度
        """
        if not XGBOOST_AVAILABLE:
            raise ImportError("需要安装xgboost库以使用XGBoost")
        
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
        
        if y.dtype == 'object':
            le = LabelEncoder()
            y = le.fit_transform(y)
        
        # 训练模型
        model = xgb.XGBClassifier(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            random_state=42
        )
        model.fit(X, y)
        
        # 预测
        y_pred = model.predict(X)
        accuracy = np.mean(y_pred == y)
        
        return {
            'model_type': 'XGBoost Classification',
            'n_estimators': n_estimators,
            'learning_rate': learning_rate,
            'max_depth': max_depth,
            'accuracy': float(accuracy),
            'feature_importance': {col: float(imp) for col, imp in zip(numeric_cols, model.feature_importances_)}
        }

