"""
统计图表生成模块
提供密度图、Q-Q图、残差图等统计图表
"""
import pandas as pd
import numpy as np
import matplotlib
# 设置非交互式后端，避免弹出新窗口
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from typing import List, Optional
from scipy import stats
from scipy.stats import probplot
import seaborn as sns

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


class StatisticalCharts:
    """统计图表生成类"""
    
    @staticmethod
    def create_density_plot(
        df: pd.DataFrame,
        cols: List[str],
        group_col: Optional[str] = None,
        kde: bool = True,
        ax=None
    ):
        """
        创建密度图
        
        参数:
            df: 数据框
            cols: 变量列表
            group_col: 分组变量
            kde: 是否显示KDE曲线
            ax: matplotlib轴对象
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        
        if group_col is None:
            # 单变量或多变量密度图
            for col in cols:
                data = df[col].dropna()
                ax.hist(data, bins=30, density=True, alpha=0.5, label=f'{col} 直方图')
                if kde:
                    from scipy.stats import gaussian_kde
                    kde_obj = gaussian_kde(data)
                    x_range = np.linspace(data.min(), data.max(), 200)
                    ax.plot(x_range, kde_obj(x_range), label=f'{col} KDE', linewidth=2)
        else:
            # 分组密度图
            groups = df[group_col].unique()
            colors = plt.cm.tab10(np.linspace(0, 1, len(groups)))
            for i, group in enumerate(groups):
                group_df = df[df[group_col] == group]
                for col in cols:
                    data = group_df[col].dropna()
                    if kde:
                        from scipy.stats import gaussian_kde
                        kde_obj = gaussian_kde(data)
                        x_range = np.linspace(data.min(), data.max(), 200)
                        ax.plot(x_range, kde_obj(x_range), 
                               label=f'{group} - {col}', 
                               color=colors[i], linewidth=2)
                    else:
                        ax.hist(data, bins=30, density=True, alpha=0.5, 
                               label=f'{group} - {col}', color=colors[i])
        
        ax.set_xlabel('数值')
        ax.set_ylabel('密度')
        if len(cols) == 1:
            ax.set_title(f'{cols[0]} 密度图')
        else:
            ax.set_title('密度对比图')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return ax
    
    @staticmethod
    def create_qq_plot(
        df: pd.DataFrame,
        col: str,
        dist: str = 'norm',
        ax=None
    ):
        """
        创建Q-Q图（正态性检验）
        
        参数:
            df: 数据框
            col: 变量名
            dist: 分布类型 ('norm', 'uniform', 'expon'等)
            ax: matplotlib轴对象
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 8))
        
        data = df[col].dropna()
        
        # 根据分布类型选择理论分布
        if dist == 'norm':
            dist_obj = stats.norm
        elif dist == 'uniform':
            dist_obj = stats.uniform
        elif dist == 'expon':
            dist_obj = stats.expon
        else:
            dist_obj = stats.norm
        
        # 创建Q-Q图
        probplot(data, dist=dist_obj, plot=ax)
        
        ax.set_title(f'{col} Q-Q图 (分布: {dist})')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return ax
    
    @staticmethod
    def create_pp_plot(
        df: pd.DataFrame,
        col: str,
        dist: str = 'norm',
        ax=None
    ):
        """
        创建P-P图
        
        参数:
            df: 数据框
            col: 变量名
            dist: 分布类型
            ax: matplotlib轴对象
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 8))
        
        data = df[col].dropna()
        sorted_data = np.sort(data)
        
        # 根据分布类型选择理论分布
        if dist == 'norm':
            dist_obj = stats.norm
            params = dist_obj.fit(data)
        elif dist == 'uniform':
            dist_obj = stats.uniform
            params = dist_obj.fit(data)
        elif dist == 'expon':
            dist_obj = stats.expon
            params = dist_obj.fit(data)
        else:
            dist_obj = stats.norm
            params = dist_obj.fit(data)
        
        # 计算理论累积概率
        theoretical_cdf = dist_obj.cdf(sorted_data, *params)
        # 计算经验累积概率
        empirical_cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
        
        ax.plot(theoretical_cdf, empirical_cdf, 'o', alpha=0.6)
        ax.plot([0, 1], [0, 1], 'r--', label='完美拟合线')
        ax.set_xlabel('理论累积概率')
        ax.set_ylabel('经验累积概率')
        ax.set_title(f'{col} P-P图 (分布: {dist})')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return ax
    
    @staticmethod
    def create_residual_plot(
        y_true: np.ndarray,
        y_pred: np.ndarray,
        residuals: Optional[np.ndarray] = None,
        plot_type: str = 'residual',
        ax=None
    ):
        """
        创建残差图
        
        参数:
            y_true: 真实值
            y_pred: 预测值
            residuals: 残差（如果为None则自动计算）
            plot_type: 图表类型 ('residual', 'qq_residual', 'leverage', 'cook')
            ax: matplotlib轴对象
        """
        if residuals is None:
            residuals = y_true - y_pred
        
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        
        if plot_type == 'residual':
            # 残差图
            ax.scatter(y_pred, residuals, alpha=0.6)
            ax.axhline(y=0, color='r', linestyle='--', linewidth=2)
            ax.set_xlabel('预测值')
            ax.set_ylabel('残差')
            ax.set_title('残差图')
            ax.grid(True, alpha=0.3)
        
        elif plot_type == 'qq_residual':
            # Q-Q残差图
            probplot(residuals, dist=stats.norm, plot=ax)
            ax.set_title('残差Q-Q图')
            ax.grid(True, alpha=0.3)
        
        elif plot_type == 'leverage':
            # 杠杆图（需要X矩阵，这里简化处理）
            ax.scatter(range(len(residuals)), residuals, alpha=0.6)
            ax.axhline(y=0, color='r', linestyle='--', linewidth=2)
            ax.set_xlabel('观测序号')
            ax.set_ylabel('残差')
            ax.set_title('杠杆图')
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return ax
    
    @staticmethod
    def create_violin_plot(
        df: pd.DataFrame,
        x_col: str,
        y_col: str,
        ax=None
    ):
        """
        创建小提琴图
        
        参数:
            df: 数据框
            x_col: 分类变量
            y_col: 数值变量
            ax: matplotlib轴对象
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        
        try:
            sns.violinplot(data=df, x=x_col, y=y_col, ax=ax)
        except ImportError:
            # 如果seaborn不可用，使用matplotlib实现简化版
            groups = df[x_col].unique()
            positions = range(len(groups))
            
            for i, group in enumerate(groups):
                group_data = df[df[x_col] == group][y_col].dropna()
                if len(group_data) > 0:
                    parts = ax.violinplot([group_data], positions=[i], widths=0.6)
                    for pc in parts['bodies']:
                        pc.set_facecolor('lightblue')
                        pc.set_alpha(0.7)
            
            ax.set_xticks(positions)
            ax.set_xticklabels(groups, rotation=45, ha='right')
        
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f'{y_col} 按 {x_col} 的小提琴图')
        plt.tight_layout()
        return ax

