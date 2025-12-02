"""
多变量分析模块
提供因子分析、判别分析、典型相关分析等功能
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
try:
    from sklearn.decomposition import FactorAnalysis, FastICA
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
    from scipy.stats import chi2
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class MultivariateAnalyzer:
    """多变量分析类"""
    
    @staticmethod
    def factor_analysis(
        df: pd.DataFrame,
        columns: List[str],
        n_factors: Optional[int] = None,
        rotation: str = 'varimax'
    ) -> Dict[str, Any]:
        """
        因子分析（探索性因子分析）
        
        参数:
            df: 数据框
            columns: 变量列
            n_factors: 因子数量（如果为None则自动选择）
            rotation: 旋转方法 ('varimax', 'promax', None)
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用因子分析")
        
        numeric_cols = [col for col in columns if col in df.select_dtypes(include=[np.number]).columns]
        if len(numeric_cols) < 2:
            return {'error': '至少需要2个数值变量'}
        
        data = df[numeric_cols].dropna()
        if len(data) < len(numeric_cols):
            return {'error': '数据点不足'}
        
        # 确定因子数量（使用特征值>1的规则）
        if n_factors is None:
            from sklearn.decomposition import PCA
            pca = PCA()
            pca.fit(data)
            eigenvalues = pca.explained_variance_
            n_factors = sum(eigenvalues > 1)
            if n_factors == 0:
                n_factors = min(3, len(numeric_cols))
        
        # 因子分析
        fa = FactorAnalysis(n_components=n_factors, rotation=rotation if rotation else None)
        fa.fit(data)
        
        # 因子载荷矩阵
        loadings = pd.DataFrame(
            fa.components_.T,
            columns=[f'因子{i+1}' for i in range(n_factors)],
            index=numeric_cols
        )
        
        # 因子得分
        factor_scores = fa.transform(data)
        factor_scores_df = pd.DataFrame(
            factor_scores,
            columns=[f'因子{i+1}得分' for i in range(n_factors)],
            index=data.index
        )
        
        # 解释的方差比例
        explained_variance = fa.noise_variance_
        
        return {
            'n_factors': n_factors,
            'loadings': loadings.to_dict(),
            'factor_scores': factor_scores_df.to_dict(),
            'explained_variance': float(explained_variance),
            'variables': numeric_cols
        }
    
    @staticmethod
    def linear_discriminant_analysis(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str]
    ) -> Dict[str, Any]:
        """
        线性判别分析（LDA）
        
        参数:
            df: 数据框
            target_column: 目标分类变量
            feature_columns: 特征变量列
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用判别分析")
        
        if target_column not in df.columns:
            return {'error': '目标列不存在'}
        
        numeric_cols = [col for col in feature_columns if col in df.select_dtypes(include=[np.number]).columns]
        if len(numeric_cols) < 1:
            return {'error': '至少需要1个数值特征变量'}
        
        # 准备数据
        data = df[numeric_cols + [target_column]].dropna()
        if len(data) == 0:
            return {'error': '数据点不足'}
        
        X = data[numeric_cols]
        y = data[target_column]
        
        # 检查类别数量
        unique_classes = y.unique()
        if len(unique_classes) < 2:
            return {'error': '目标变量至少需要2个类别'}
        
        # LDA
        lda = LinearDiscriminantAnalysis()
        lda.fit(X, y)
        
        # 预测
        y_pred = lda.predict(X)
        
        # 准确率
        accuracy = (y_pred == y).mean()
        
        # 判别函数系数
        coefficients = pd.DataFrame(
            lda.coef_,
            columns=numeric_cols,
            index=[f'类别_{cls}' for cls in unique_classes]
        )
        
        return {
            'model_type': 'Linear Discriminant Analysis',
            'accuracy': float(accuracy),
            'coefficients': coefficients.to_dict(),
            'classes': unique_classes.tolist(),
            'explained_variance_ratio': lda.explained_variance_ratio_.tolist() if hasattr(lda, 'explained_variance_ratio_') else []
        }
    
    @staticmethod
    def quadratic_discriminant_analysis(
        df: pd.DataFrame,
        target_column: str,
        feature_columns: List[str]
    ) -> Dict[str, Any]:
        """
        二次判别分析（QDA）
        
        参数:
            df: 数据框
            target_column: 目标分类变量
            feature_columns: 特征变量列
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用判别分析")
        
        if target_column not in df.columns:
            return {'error': '目标列不存在'}
        
        numeric_cols = [col for col in feature_columns if col in df.select_dtypes(include=[np.number]).columns]
        if len(numeric_cols) < 1:
            return {'error': '至少需要1个数值特征变量'}
        
        # 准备数据
        data = df[numeric_cols + [target_column]].dropna()
        if len(data) == 0:
            return {'error': '数据点不足'}
        
        X = data[numeric_cols]
        y = data[target_column]
        
        # 检查类别数量
        unique_classes = y.unique()
        if len(unique_classes) < 2:
            return {'error': '目标变量至少需要2个类别'}
        
        # QDA
        qda = QuadraticDiscriminantAnalysis()
        qda.fit(X, y)
        
        # 预测
        y_pred = qda.predict(X)
        
        # 准确率
        accuracy = (y_pred == y).mean()
        
        return {
            'model_type': 'Quadratic Discriminant Analysis',
            'accuracy': float(accuracy),
            'classes': unique_classes.tolist()
        }
    
    @staticmethod
    def canonical_correlation_analysis(
        df: pd.DataFrame,
        x_columns: List[str],
        y_columns: List[str]
    ) -> Dict[str, Any]:
        """
        典型相关分析
        
        参数:
            df: 数据框
            x_columns: 第一组变量
            y_columns: 第二组变量
        """
        x_numeric = [col for col in x_columns if col in df.select_dtypes(include=[np.number]).columns]
        y_numeric = [col for col in y_columns if col in df.select_dtypes(include=[np.number]).columns]
        
        if len(x_numeric) < 1 or len(y_numeric) < 1:
            return {'error': '每组至少需要1个数值变量'}
        
        # 准备数据
        data = df[x_numeric + y_numeric].dropna()
        if len(data) < max(len(x_numeric), len(y_numeric)) + 1:
            return {'error': '数据点不足'}
        
        X = data[x_numeric].values
        Y = data[y_numeric].values
        
        # 计算协方差矩阵
        cov_xx = np.cov(X.T)
        cov_yy = np.cov(Y.T)
        cov_xy = np.cov(X.T, Y.T)[:len(x_numeric), len(x_numeric):]
        cov_yx = cov_xy.T
        
        # 计算典型相关系数
        try:
            # 求解广义特征值问题
            inv_cov_xx = np.linalg.pinv(cov_xx)
            inv_cov_yy = np.linalg.pinv(cov_yy)
            
            matrix_a = inv_cov_xx @ cov_xy @ inv_cov_yy @ cov_yx
            eigenvalues, eigenvectors_x = np.linalg.eig(matrix_a)
            
            # 典型相关系数
            canonical_correlations = np.sqrt(np.real(eigenvalues))
            canonical_correlations = np.sort(canonical_correlations)[::-1]  # 降序排列
            
            # 典型变量系数
            canonical_vars_x = np.real(eigenvectors_x)
            canonical_vars_y = inv_cov_yy @ cov_yx @ canonical_vars_x
            
            return {
                'canonical_correlations': canonical_correlations.tolist(),
                'n_canonical_vars': len(canonical_correlations),
                'x_variables': x_numeric,
                'y_variables': y_numeric,
                'canonical_var_x_coefficients': canonical_vars_x.tolist(),
                'canonical_var_y_coefficients': canonical_vars_y.tolist()
            }
        except Exception as e:
            return {'error': f'典型相关分析失败: {str(e)}'}

