"""
监督学习模块 - 分类方法
将分类相关方法提取到此模块
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
try:
    from sklearn.svm import SVC
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.naive_bayes import GaussianNB
    from sklearn.neural_network import MLPClassifier
    from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False


class SupervisedClassification:
    """监督学习分类方法"""
    
    @staticmethod
    def svm_classification(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str],
        kernel: str = 'rbf',
        C: float = 1.0,
        gamma: Optional[str] = 'scale'
    ) -> Dict[str, Any]:
        """支持向量机分类"""
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
        
        if y.dtype == 'object':
            le = LabelEncoder()
            y = le.fit_transform(y)
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        model = SVC(kernel=kernel, C=C, gamma=gamma, random_state=42)
        model.fit(X_scaled, y)
        
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
    def knn_classification(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str],
        n_neighbors: int = 5
    ) -> Dict[str, Any]:
        """K近邻分类"""
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
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        model = KNeighborsClassifier(n_neighbors=n_neighbors)
        model.fit(X_scaled, y)
        
        y_pred = model.predict(X_scaled)
        accuracy = np.mean(y_pred == y)
        
        return {
            'model_type': 'KNN Classification',
            'n_neighbors': n_neighbors,
            'accuracy': float(accuracy)
        }
    
    @staticmethod
    def naive_bayes_classification(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str]
    ) -> Dict[str, Any]:
        """朴素贝叶斯分类"""
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
        
        model = GaussianNB()
        model.fit(X, y)
        
        y_pred = model.predict(X)
        accuracy = np.mean(y_pred == y)
        
        return {
            'model_type': 'Naive Bayes Classification',
            'accuracy': float(accuracy)
        }
    
    @staticmethod
    def mlp_classification(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str],
        hidden_layers: tuple = (100,),
        max_iter: int = 500
    ) -> Dict[str, Any]:
        """多层感知机分类"""
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
        
        if y.dtype == 'object':
            le = LabelEncoder()
            y = le.fit_transform(y)
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        model = MLPClassifier(hidden_layer_sizes=hidden_layers, max_iter=max_iter, random_state=42)
        model.fit(X_scaled, y)
        
        y_pred = model.predict(X_scaled)
        accuracy = np.mean(y_pred == y)
        
        return {
            'model_type': 'MLP Classification',
            'hidden_layers': hidden_layers,
            'accuracy': float(accuracy)
        }
    
    @staticmethod
    def adaboost_classification(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str],
        n_estimators: int = 50
    ) -> Dict[str, Any]:
        """AdaBoost分类"""
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
        
        model = AdaBoostClassifier(n_estimators=n_estimators, random_state=42)
        model.fit(X, y)
        
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
        """梯度提升分类"""
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
        
        model = GradientBoostingClassifier(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            random_state=42
        )
        model.fit(X, y)
        
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
        """XGBoost分类"""
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
        
        model = xgb.XGBClassifier(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            random_state=42
        )
        model.fit(X, y)
        
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

