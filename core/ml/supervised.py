"""
监督学习模块
提供分类和回归模型
重构后版本：使用分类和回归子模块
"""
from typing import Dict, Any, List, Optional
from core.ml.supervised_classification import SupervisedClassification
from core.ml.supervised_regression import SupervisedRegression


class SupervisedLearning(SupervisedClassification, SupervisedRegression):
    """监督学习类 - 组合分类和回归方法"""
    
    # 所有方法现在从SupervisedClassification和SupervisedRegression继承
    # 为了保持向后兼容，我们保留原有的方法名作为别名
    
    @staticmethod
    def svm_classification(*args, **kwargs):
        """支持向量机分类"""
        return SupervisedClassification.svm_classification(*args, **kwargs)
    
    @staticmethod
    def svm_regression(*args, **kwargs):
        """支持向量回归"""
        return SupervisedRegression.svm_regression(*args, **kwargs)
    
    @staticmethod
    def knn_classification(*args, **kwargs):
        """K近邻分类"""
        return SupervisedClassification.knn_classification(*args, **kwargs)
    
    @staticmethod
    def knn_regression(*args, **kwargs):
        """K近邻回归"""
        return SupervisedRegression.knn_regression(*args, **kwargs)
    
    @staticmethod
    def naive_bayes_classification(*args, **kwargs):
        """朴素贝叶斯分类"""
        return SupervisedClassification.naive_bayes_classification(*args, **kwargs)
    
    @staticmethod
    def mlp_classification(*args, **kwargs):
        """多层感知机分类"""
        return SupervisedClassification.mlp_classification(*args, **kwargs)
    
    @staticmethod
    def mlp_regression(*args, **kwargs):
        """多层感知机回归"""
        return SupervisedRegression.mlp_regression(*args, **kwargs)
    
    @staticmethod
    def ridge_regression(*args, **kwargs):
        """岭回归"""
        return SupervisedRegression.ridge_regression(*args, **kwargs)
    
    @staticmethod
    def lasso_regression(*args, **kwargs):
        """Lasso回归"""
        return SupervisedRegression.lasso_regression(*args, **kwargs)
    
    @staticmethod
    def elastic_net_regression(*args, **kwargs):
        """Elastic Net回归"""
        return SupervisedRegression.elastic_net_regression(*args, **kwargs)
    
    @staticmethod
    def adaboost_classification(*args, **kwargs):
        """AdaBoost分类"""
        return SupervisedClassification.adaboost_classification(*args, **kwargs)
    
    @staticmethod
    def gradient_boosting_classification(*args, **kwargs):
        """梯度提升分类"""
        return SupervisedClassification.gradient_boosting_classification(*args, **kwargs)
    
    @staticmethod
    def xgboost_classification(*args, **kwargs):
        """XGBoost分类"""
        return SupervisedClassification.xgboost_classification(*args, **kwargs)

