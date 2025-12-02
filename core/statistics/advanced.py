"""
高级分析模块
"""
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any, List, Optional


class AdvancedAnalysis:
    """高级分析类"""
    
    def principal_component_analysis(
        self, df: pd.DataFrame, columns: List[str],
        n_components: Optional[int] = None
    ) -> Dict[str, Any]:
        """主成分分析（PCA）"""
        numeric_cols = [
            col for col in columns
            if col in df.columns and df[col].dtype in ['int64', 'float64']
        ]
        
        if len(numeric_cols) < 2:
            return {"error": "至少需要2个数值型变量"}
        
        valid_data = df[numeric_cols].dropna()
        
        if len(valid_data) < len(numeric_cols):
            return {"error": "数据不足"}
        
        if n_components is None:
            n_components = min(len(numeric_cols), len(valid_data) - 1)
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(valid_data)
        
        pca = PCA(n_components=n_components)
        pca.fit(X_scaled)
        
        components = pca.components_
        explained_variance = pca.explained_variance_ratio_
        eigenvalues = pca.explained_variance_
        
        loadings = {}
        for i in range(n_components):
            loadings[f"PC{i+1}"] = {
                col: float(components[i, j])
                for j, col in enumerate(numeric_cols)
            }
        
        cumulative_variance = np.cumsum(explained_variance)
        
        return {
            "n_components": int(n_components),
            "eigenvalues": eigenvalues.tolist(),
            "explained_variance_ratio": explained_variance.tolist(),
            "cumulative_variance_ratio": cumulative_variance.tolist(),
            "loadings": loadings,
            "variables": numeric_cols
        }
    
    def kmeans_clustering(
        self, df: pd.DataFrame, columns: List[str], n_clusters: int = 3
    ) -> Dict[str, Any]:
        """K-means聚类"""
        numeric_cols = [
            col for col in columns
            if col in df.columns and df[col].dtype in ['int64', 'float64']
        ]
        
        if len(numeric_cols) < 2:
            return {"error": "至少需要2个数值型变量"}
        
        valid_data = df[numeric_cols].dropna()
        
        if len(valid_data) < n_clusters:
            return {"error": "数据点数量少于聚类数"}
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(valid_data)
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
        
        centers = scaler.inverse_transform(kmeans.cluster_centers_)
        
        cluster_stats = []
        for i in range(n_clusters):
            cluster_data = valid_data[labels == i]
            cluster_stats.append({
                "cluster": int(i),
                "n": int(len(cluster_data)),
                "means": {
                    col: float(cluster_data[col].mean())
                    for col in numeric_cols
                }
            })
        
        return {
            "n_clusters": int(n_clusters),
            "labels": labels.tolist(),
            "cluster_centers": {
                f"Cluster_{i}": {
                    col: float(centers[i, j])
                    for j, col in enumerate(numeric_cols)
                }
                for i in range(n_clusters)
            },
            "cluster_stats": cluster_stats,
            "inertia": float(kmeans.inertia_),
            "variables": numeric_cols
        }
    
    def hierarchical_clustering(
        self, df: pd.DataFrame, columns: List[str], n_clusters: int = 3,
        linkage: str = "ward"
    ) -> Dict[str, Any]:
        """层次聚类"""
        numeric_cols = [
            col for col in columns
            if col in df.columns and df[col].dtype in ['int64', 'float64']
        ]
        
        if len(numeric_cols) < 2:
            return {"error": "至少需要2个数值型变量"}
        
        valid_data = df[numeric_cols].dropna()
        
        if len(valid_data) < n_clusters:
            return {"error": "数据点数量少于聚类数"}
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(valid_data)
        
        clustering = AgglomerativeClustering(
            n_clusters=n_clusters, linkage=linkage
        )
        labels = clustering.fit_predict(X_scaled)
        
        cluster_stats = []
        for i in range(n_clusters):
            cluster_data = valid_data[labels == i]
            cluster_stats.append({
                "cluster": int(i),
                "n": int(len(cluster_data)),
                "means": {
                    col: float(cluster_data[col].mean())
                    for col in numeric_cols
                }
            })
        
        return {
            "n_clusters": int(n_clusters),
            "labels": labels.tolist(),
            "linkage": linkage,
            "cluster_stats": cluster_stats,
            "variables": numeric_cols
        }
    
    def decision_tree_classification(
        self, df: pd.DataFrame, y_col: str, x_cols: List[str],
        max_depth: Optional[int] = None
    ) -> Dict[str, Any]:
        """决策树分类"""
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
        
        if len(valid_data) < 10:
            return {"error": "数据不足"}
        
        X = valid_data[numeric_x_cols].values
        y = valid_data[y_col].values
        
        model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
        model.fit(X, y)
        
        y_pred = model.predict(X)
        accuracy = np.mean(y_pred == y)
        
        return {
            "accuracy": float(accuracy),
            "feature_importance": {
                col: float(imp)
                for col, imp in zip(numeric_x_cols, model.feature_importances_)
            },
            "predictions": y_pred.tolist(),
            "x_columns": numeric_x_cols,
            "y_column": y_col
        }
    
    def random_forest_classification(
        self, df: pd.DataFrame, y_col: str, x_cols: List[str],
        n_estimators: int = 100
    ) -> Dict[str, Any]:
        """随机森林分类"""
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
        
        if len(valid_data) < 10:
            return {"error": "数据不足"}
        
        X = valid_data[numeric_x_cols].values
        y = valid_data[y_col].values
        
        model = RandomForestClassifier(
            n_estimators=n_estimators, random_state=42
        )
        model.fit(X, y)
        
        y_pred = model.predict(X)
        accuracy = np.mean(y_pred == y)
        
        return {
            "accuracy": float(accuracy),
            "feature_importance": {
                col: float(imp)
                for col, imp in zip(numeric_x_cols, model.feature_importances_)
            },
            "predictions": y_pred.tolist(),
            "n_estimators": int(n_estimators),
            "x_columns": numeric_x_cols,
            "y_column": y_col
        }

