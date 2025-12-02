"""
无监督学习模块
提供聚类和降维算法
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
try:
    from sklearn.cluster import DBSCAN, SpectralClustering
    from sklearn.mixture import GaussianMixture
    from sklearn.decomposition import FastICA
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

try:
    from sklearn.manifold import TSNE
    TSNE_AVAILABLE = True
except ImportError:
    TSNE_AVAILABLE = False

try:
    import umap
    UMAP_AVAILABLE = True
except ImportError:
    UMAP_AVAILABLE = False


class UnsupervisedLearning:
    """无监督学习类"""
    
    @staticmethod
    def dbscan_clustering(
        df: pd.DataFrame,
        columns: List[str],
        eps: float = 0.5,
        min_samples: int = 5
    ) -> Dict[str, Any]:
        """
        DBSCAN聚类
        
        参数:
            df: 数据框
            columns: 特征列
            eps: 邻域半径
            min_samples: 最小样本数
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用DBSCAN")
        
        numeric_cols = [col for col in columns if col in df.select_dtypes(include=[np.number]).columns]
        if len(numeric_cols) < 2:
            return {'error': '至少需要2个数值变量'}
        
        data = df[numeric_cols].dropna()
        if len(data) < min_samples:
            return {'error': '数据点不足'}
        
        X = data.values
        
        # 标准化
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # 聚类
        model = DBSCAN(eps=eps, min_samples=min_samples)
        labels = model.fit_predict(X_scaled)
        
        # 统计结果
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise = list(labels).count(-1)
        
        cluster_stats = {}
        for cluster_id in set(labels):
            if cluster_id == -1:
                continue
            cluster_mask = labels == cluster_id
            cluster_data = data[cluster_mask]
            cluster_stats[int(cluster_id)] = {
                'n_samples': int(cluster_mask.sum()),
                'means': {col: float(cluster_data[col].mean()) for col in numeric_cols}
            }
        
        return {
            'model_type': 'DBSCAN Clustering',
            'eps': eps,
            'min_samples': min_samples,
            'n_clusters': n_clusters,
            'n_noise': n_noise,
            'labels': labels.tolist(),
            'cluster_stats': cluster_stats
        }
    
    @staticmethod
    def spectral_clustering(
        df: pd.DataFrame,
        columns: List[str],
        n_clusters: int = 3,
        affinity: str = 'rbf'
    ) -> Dict[str, Any]:
        """
        谱聚类
        
        参数:
            df: 数据框
            columns: 特征列
            n_clusters: 聚类数
            affinity: 相似度矩阵类型
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用谱聚类")
        
        numeric_cols = [col for col in columns if col in df.select_dtypes(include=[np.number]).columns]
        if len(numeric_cols) < 2:
            return {'error': '至少需要2个数值变量'}
        
        data = df[numeric_cols].dropna()
        if len(data) < n_clusters:
            return {'error': '数据点不足'}
        
        X = data.values
        
        # 标准化
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # 聚类
        model = SpectralClustering(n_clusters=n_clusters, affinity=affinity, random_state=42)
        labels = model.fit_predict(X_scaled)
        
        # 统计结果
        cluster_stats = {}
        for cluster_id in range(n_clusters):
            cluster_mask = labels == cluster_id
            cluster_data = data[cluster_mask]
            cluster_stats[int(cluster_id)] = {
                'n_samples': int(cluster_mask.sum()),
                'means': {col: float(cluster_data[col].mean()) for col in numeric_cols}
            }
        
        return {
            'model_type': 'Spectral Clustering',
            'n_clusters': n_clusters,
            'affinity': affinity,
            'labels': labels.tolist(),
            'cluster_stats': cluster_stats
        }
    
    @staticmethod
    def gaussian_mixture(
        df: pd.DataFrame,
        columns: List[str],
        n_components: int = 3,
        covariance_type: str = 'full'
    ) -> Dict[str, Any]:
        """
        高斯混合模型（GMM）
        
        参数:
            df: 数据框
            columns: 特征列
            n_components: 混合成分数量
            covariance_type: 协方差类型
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用GMM")
        
        numeric_cols = [col for col in columns if col in df.select_dtypes(include=[np.number]).columns]
        if len(numeric_cols) < 2:
            return {'error': '至少需要2个数值变量'}
        
        data = df[numeric_cols].dropna()
        if len(data) < n_components:
            return {'error': '数据点不足'}
        
        X = data.values
        
        # 标准化
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # 训练模型
        model = GaussianMixture(
            n_components=n_components,
            covariance_type=covariance_type,
            random_state=42
        )
        model.fit(X_scaled)
        
        # 预测
        labels = model.predict(X_scaled)
        probabilities = model.predict_proba(X_scaled)
        
        # 统计结果
        cluster_stats = {}
        for cluster_id in range(n_components):
            cluster_mask = labels == cluster_id
            cluster_data = data[cluster_mask]
            cluster_stats[int(cluster_id)] = {
                'n_samples': int(cluster_mask.sum()),
                'weight': float(model.weights_[cluster_id]),
                'means': {col: float(cluster_data[col].mean()) for col in numeric_cols}
            }
        
        return {
            'model_type': 'Gaussian Mixture Model',
            'n_components': n_components,
            'covariance_type': covariance_type,
            'aic': float(model.aic(X_scaled)),
            'bic': float(model.bic(X_scaled)),
            'labels': labels.tolist(),
            'cluster_stats': cluster_stats
        }
    
    @staticmethod
    def ica_decomposition(
        df: pd.DataFrame,
        columns: List[str],
        n_components: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        独立成分分析（ICA）
        
        参数:
            df: 数据框
            columns: 特征列
            n_components: 成分数量
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用ICA")
        
        numeric_cols = [col for col in columns if col in df.select_dtypes(include=[np.number]).columns]
        if len(numeric_cols) < 2:
            return {'error': '至少需要2个数值变量'}
        
        data = df[numeric_cols].dropna()
        if len(data) < 2:
            return {'error': '数据点不足'}
        
        if n_components is None:
            n_components = min(len(numeric_cols), len(data))
        
        X = data.values
        
        # 标准化
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # ICA
        ica = FastICA(n_components=n_components, random_state=42, max_iter=1000)
        ica.fit(X_scaled)
        
        # 转换
        components = ica.components_
        transformed = ica.transform(X_scaled)
        
        # 混合矩阵
        mixing_matrix = ica.mixing_
        
        return {
            'model_type': 'Independent Component Analysis',
            'n_components': n_components,
            'components': components.tolist(),
            'mixing_matrix': mixing_matrix.tolist(),
            'transformed_data': transformed.tolist(),
            'variables': numeric_cols
        }
    
    @staticmethod
    def tsne_embedding(
        df: pd.DataFrame,
        columns: List[str],
        n_components: int = 2,
        perplexity: float = 30.0,
        learning_rate: float = 200.0
    ) -> Dict[str, Any]:
        """
        t-SNE降维
        
        参数:
            df: 数据框
            columns: 特征列
            n_components: 降维后的维度
            perplexity: 困惑度
            learning_rate: 学习率
        """
        if not TSNE_AVAILABLE:
            raise ImportError("需要安装scikit-learn库以使用t-SNE")
        
        numeric_cols = [col for col in columns if col in df.select_dtypes(include=[np.number]).columns]
        if len(numeric_cols) < 2:
            return {'error': '至少需要2个数值变量'}
        
        data = df[numeric_cols].dropna()
        if len(data) < 10:
            return {'error': '数据点不足'}
        
        X = data.values
        
        # 标准化
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # t-SNE
        tsne = TSNE(
            n_components=n_components,
            perplexity=perplexity,
            learning_rate=learning_rate,
            random_state=42
        )
        embedding = tsne.fit_transform(X_scaled)
        
        return {
            'model_type': 't-SNE Embedding',
            'n_components': n_components,
            'perplexity': perplexity,
            'learning_rate': learning_rate,
            'embedding': embedding.tolist(),
            'kl_divergence': float(tsne.kl_divergence_)
        }
    
    @staticmethod
    def umap_embedding(
        df: pd.DataFrame,
        columns: List[str],
        n_components: int = 2,
        n_neighbors: int = 15,
        min_dist: float = 0.1
    ) -> Dict[str, Any]:
        """
        UMAP降维
        
        参数:
            df: 数据框
            columns: 特征列
            n_components: 降维后的维度
            n_neighbors: 邻居数量
            min_dist: 最小距离
        """
        if not UMAP_AVAILABLE:
            raise ImportError("需要安装umap-learn库以使用UMAP")
        
        numeric_cols = [col for col in columns if col in df.select_dtypes(include=[np.number]).columns]
        if len(numeric_cols) < 2:
            return {'error': '至少需要2个数值变量'}
        
        data = df[numeric_cols].dropna()
        if len(data) < n_neighbors + 1:
            return {'error': '数据点不足'}
        
        X = data.values
        
        # 标准化
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # UMAP
        reducer = umap.UMAP(
            n_components=n_components,
            n_neighbors=n_neighbors,
            min_dist=min_dist,
            random_state=42
        )
        embedding = reducer.fit_transform(X_scaled)
        
        return {
            'model_type': 'UMAP Embedding',
            'n_components': n_components,
            'n_neighbors': n_neighbors,
            'min_dist': min_dist,
            'embedding': embedding.tolist()
        }

