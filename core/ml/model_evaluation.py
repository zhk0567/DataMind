"""
模型评估模块
提供交叉验证、超参数优化、模型对比等功能
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Callable
try:
    from sklearn.model_selection import (
        cross_val_score, KFold, LeaveOneOut, StratifiedKFold,
        GridSearchCV, RandomizedSearchCV
    )
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, f1_score,
        roc_auc_score, confusion_matrix, classification_report,
        mean_squared_error, mean_absolute_error, r2_score
    )
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class ModelEvaluator:
    """模型评估类"""
    
    @staticmethod
    def cross_validate(
        model: Any,
        X: np.ndarray,
        y: np.ndarray,
        cv: int = 5,
        scoring: str = 'accuracy',
        stratified: bool = False
    ) -> Dict[str, Any]:
        """
        交叉验证
        
        参数:
            model: 模型对象
            X: 特征数据
            y: 目标数据
            cv: 折数
            scoring: 评分指标
            stratified: 是否使用分层交叉验证
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用交叉验证")
        
        if stratified and scoring in ['accuracy', 'precision', 'recall', 'f1']:
            cv_splitter = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
        else:
            cv_splitter = KFold(n_splits=cv, shuffle=True, random_state=42)
        
        scores = cross_val_score(model, X, y, cv=cv_splitter, scoring=scoring)
        
        return {
            'cv': cv,
            'scoring': scoring,
            'scores': scores.tolist(),
            'mean': float(scores.mean()),
            'std': float(scores.std()),
            'min': float(scores.min()),
            'max': float(scores.max())
        }
    
    @staticmethod
    def leave_one_out_cv(
        model: Any,
        X: np.ndarray,
        y: np.ndarray,
        scoring: str = 'accuracy'
    ) -> Dict[str, Any]:
        """
        留一法交叉验证
        
        参数:
            model: 模型对象
            X: 特征数据
            y: 目标数据
            scoring: 评分指标
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用留一法交叉验证")
        
        loo = LeaveOneOut()
        scores = cross_val_score(model, X, y, cv=loo, scoring=scoring)
        
        return {
            'cv': 'Leave-One-Out',
            'scoring': scoring,
            'n_splits': len(scores),
            'scores': scores.tolist(),
            'mean': float(scores.mean()),
            'std': float(scores.std())
        }
    
    @staticmethod
    def evaluate_classification(
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_proba: Optional[np.ndarray] = None
    ) -> Dict[str, Any]:
        """
        评估分类模型
        
        参数:
            y_true: 真实标签
            y_pred: 预测标签
            y_proba: 预测概率（用于计算AUC）
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用分类评估")
        
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
        
        result = {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'confusion_matrix': confusion_matrix(y_true, y_pred).tolist()
        }
        
        # 如果有概率预测，计算AUC
        if y_proba is not None:
            try:
                # 二分类
                if y_proba.ndim == 1 or y_proba.shape[1] == 2:
                    if y_proba.ndim == 2:
                        y_proba_binary = y_proba[:, 1]
                    else:
                        y_proba_binary = y_proba
                    auc = roc_auc_score(y_true, y_proba_binary)
                    result['auc'] = float(auc)
            except:
                pass
        
        return result
    
    @staticmethod
    def evaluate_regression(
        y_true: np.ndarray,
        y_pred: np.ndarray
    ) -> Dict[str, Any]:
        """
        评估回归模型
        
        参数:
            y_true: 真实值
            y_pred: 预测值
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用回归评估")
        
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        
        return {
            'mse': float(mse),
            'rmse': float(rmse),
            'mae': float(mae),
            'r2_score': float(r2)
        }
    
    @staticmethod
    def grid_search(
        model: Any,
        X: np.ndarray,
        y: np.ndarray,
        param_grid: Dict[str, List],
        cv: int = 5,
        scoring: str = 'accuracy'
    ) -> Dict[str, Any]:
        """
        网格搜索超参数优化
        
        参数:
            model: 模型对象
            X: 特征数据
            y: 目标数据
            param_grid: 参数网格
            cv: 折数
            scoring: 评分指标
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用网格搜索")
        
        grid_search = GridSearchCV(
            model,
            param_grid,
            cv=cv,
            scoring=scoring,
            n_jobs=-1
        )
        grid_search.fit(X, y)
        
        return {
            'best_params': grid_search.best_params_,
            'best_score': float(grid_search.best_score_),
            'cv_results': {
                'mean_test_score': grid_search.cv_results_['mean_test_score'].tolist(),
                'std_test_score': grid_search.cv_results_['std_test_score'].tolist(),
                'params': grid_search.cv_results_['params']
            }
        }
    
    @staticmethod
    def random_search(
        model: Any,
        X: np.ndarray,
        y: np.ndarray,
        param_distributions: Dict[str, List],
        n_iter: int = 10,
        cv: int = 5,
        scoring: str = 'accuracy'
    ) -> Dict[str, Any]:
        """
        随机搜索超参数优化
        
        参数:
            model: 模型对象
            X: 特征数据
            y: 目标数据
            param_distributions: 参数分布
            n_iter: 迭代次数
            cv: 折数
            scoring: 评分指标
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用随机搜索")
        
        random_search = RandomizedSearchCV(
            model,
            param_distributions,
            n_iter=n_iter,
            cv=cv,
            scoring=scoring,
            n_jobs=-1,
            random_state=42
        )
        random_search.fit(X, y)
        
        return {
            'best_params': random_search.best_params_,
            'best_score': float(random_search.best_score_),
            'n_iter': n_iter
        }
    
    @staticmethod
    def compare_models(
        models: Dict[str, Any],
        X: np.ndarray,
        y: np.ndarray,
        cv: int = 5,
        scoring: str = 'accuracy'
    ) -> Dict[str, Any]:
        """
        对比多个模型
        
        参数:
            models: 模型字典 {名称: 模型对象}
            X: 特征数据
            y: 目标数据
            cv: 折数
            scoring: 评分指标
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用模型对比")
        
        results = {}
        for name, model in models.items():
            cv_result = ModelEvaluator.cross_validate(model, X, y, cv=cv, scoring=scoring)
            results[name] = {
                'mean_score': cv_result['mean'],
                'std_score': cv_result['std'],
                'scores': cv_result['scores']
            }
        
        # 找出最佳模型
        best_model = max(results.items(), key=lambda x: x[1]['mean_score'])
        
        return {
            'results': results,
            'best_model': best_model[0],
            'best_score': best_model[1]['mean_score']
        }

