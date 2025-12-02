"""
基础图表生成模块
提供柱状图、折线图、散点图等基础图表的增强功能
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Optional, Dict, Any
from scipy import stats
from sklearn.linear_model import LinearRegression

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


class BasicCharts:
    """基础图表生成类"""
    
    @staticmethod
    def create_bar_chart(
        df: pd.DataFrame,
        x_col: str,
        y_col: Optional[str] = None,
        group_col: Optional[str] = None,
        chart_type: str = 'grouped',
        orientation: str = 'vertical',
        error_bars: bool = False,
        ax=None
    ):
        """
        创建柱状图
        
        参数:
            df: 数据框
            x_col: X轴变量（分类变量）
            y_col: Y轴变量（数值变量，如果为None则使用频数）
            group_col: 分组变量（用于分组或堆叠）
            chart_type: 图表类型 ('grouped', 'stacked', 'percent_stacked')
            orientation: 方向 ('vertical', 'horizontal')
            error_bars: 是否显示误差棒
            ax: matplotlib轴对象
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        
        if y_col is None:
            # 频数柱状图
            value_counts = df[x_col].value_counts()
            x_data = value_counts.index
            y_data = value_counts.values
            
            if orientation == 'vertical':
                bars = ax.bar(x_data, y_data)
                ax.set_xlabel(x_col)
                ax.set_ylabel('频数')
            else:
                bars = ax.barh(x_data, y_data)
                ax.set_ylabel(x_col)
                ax.set_xlabel('频数')
        else:
            # 有Y变量的柱状图
            if group_col is None:
                # 简单柱状图
                grouped = df.groupby(x_col)[y_col].agg(['mean', 'std'] if error_bars else 'mean')
                x_data = grouped.index
                y_data = grouped['mean'] if error_bars else grouped
                
                if error_bars:
                    yerr = grouped['std']
                    if orientation == 'vertical':
                        bars = ax.bar(x_data, y_data, yerr=yerr, capsize=5)
                        ax.set_xlabel(x_col)
                        ax.set_ylabel(y_col)
                    else:
                        bars = ax.barh(x_data, y_data, xerr=yerr, capsize=5)
                        ax.set_ylabel(x_col)
                        ax.set_xlabel(y_col)
                else:
                    if orientation == 'vertical':
                        bars = ax.bar(x_data, y_data)
                        ax.set_xlabel(x_col)
                        ax.set_ylabel(y_col)
                    else:
                        bars = ax.barh(x_data, y_data)
                        ax.set_ylabel(x_col)
                        ax.set_xlabel(y_col)
            else:
                # 分组或堆叠柱状图
                pivot_data = df.pivot_table(
                    values=y_col,
                    index=x_col,
                    columns=group_col,
                    aggfunc='mean'
                )
                
                x_data = pivot_data.index
                groups = pivot_data.columns
                
                if chart_type == 'grouped':
                    x_pos = np.arange(len(x_data))
                    width = 0.8 / len(groups)
                    
                    for i, group in enumerate(groups):
                        offset = (i - len(groups) / 2 + 0.5) * width
                        if orientation == 'vertical':
                            ax.bar(x_pos + offset, pivot_data[group], width, label=group)
                        else:
                            ax.barh(x_pos + offset, pivot_data[group], width, label=group)
                    
                    if orientation == 'vertical':
                        ax.set_xticks(x_pos)
                        ax.set_xticklabels(x_data, rotation=45, ha='right')
                        ax.set_xlabel(x_col)
                        ax.set_ylabel(y_col)
                    else:
                        ax.set_yticks(x_pos)
                        ax.set_yticklabels(x_data)
                        ax.set_ylabel(x_col)
                        ax.set_xlabel(y_col)
                    ax.legend()
                
                elif chart_type == 'stacked':
                    if orientation == 'vertical':
                        ax = pivot_data.plot(kind='bar', stacked=True, ax=ax)
                        ax.set_xlabel(x_col)
                        ax.set_ylabel(y_col)
                        ax.legend(title=group_col)
                    else:
                        ax = pivot_data.plot(kind='barh', stacked=True, ax=ax)
                        ax.set_ylabel(x_col)
                        ax.set_xlabel(y_col)
                        ax.legend(title=group_col)
                
                elif chart_type == 'percent_stacked':
                    pivot_pct = pivot_data.div(pivot_data.sum(axis=1), axis=0) * 100
                    if orientation == 'vertical':
                        ax = pivot_pct.plot(kind='bar', stacked=True, ax=ax)
                        ax.set_xlabel(x_col)
                        ax.set_ylabel(f'{y_col} (%)')
                        ax.legend(title=group_col)
                    else:
                        ax = pivot_pct.plot(kind='barh', stacked=True, ax=ax)
                        ax.set_ylabel(x_col)
                        ax.set_xlabel(f'{y_col} (%)')
                        ax.legend(title=group_col)
        
        ax.set_title(f'{x_col} 柱状图')
        plt.tight_layout()
        return ax
    
    @staticmethod
    def create_line_chart(
        df: pd.DataFrame,
        x_col: str,
        y_cols: List[str],
        group_col: Optional[str] = None,
        chart_type: str = 'line',
        smooth: bool = False,
        markers: bool = False,
        ax=None
    ):
        """
        创建折线图
        
        参数:
            df: 数据框
            x_col: X轴变量
            y_cols: Y轴变量列表（多系列）
            group_col: 分组变量
            chart_type: 图表类型 ('line', 'area', 'stacked_area')
            smooth: 是否平滑曲线
            markers: 是否显示标记点
            ax: matplotlib轴对象
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        
        if group_col is None:
            # 多系列折线图
            for y_col in y_cols:
                y_data = df[y_col].values
                x_data = df[x_col].values
                
                if smooth:
                    # 使用样条插值平滑
                    from scipy.interpolate import interp1d
                    sorted_idx = np.argsort(x_data)
                    x_sorted = x_data[sorted_idx]
                    y_sorted = y_data[sorted_idx]
                    f = interp1d(x_sorted, y_sorted, kind='cubic')
                    x_smooth = np.linspace(x_sorted.min(), x_sorted.max(), 300)
                    y_smooth = f(x_smooth)
                    ax.plot(x_smooth, y_smooth, label=y_col, marker='o' if markers else None)
                else:
                    ax.plot(x_data, y_data, label=y_col, marker='o' if markers else None)
        else:
            # 分组折线图
            for group in df[group_col].unique():
                group_df = df[df[group_col] == group]
                for y_col in y_cols:
                    label = f'{group} - {y_col}' if len(y_cols) > 1 else group
                    ax.plot(
                        group_df[x_col],
                        group_df[y_col],
                        label=label,
                        marker='o' if markers else None
                    )
        
        if chart_type == 'area':
            ax.fill_between(df[x_col], df[y_cols[0]], alpha=0.3)
        elif chart_type == 'stacked_area':
            ax.stackplot(df[x_col], *[df[y_col] for y_col in y_cols], labels=y_cols, alpha=0.7)
            ax.legend()
        
        ax.set_xlabel(x_col)
        if len(y_cols) == 1:
            ax.set_ylabel(y_cols[0])
        else:
            ax.set_ylabel('数值')
            ax.legend()
        
        ax.set_title(f'{x_col} 折线图')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return ax
    
    @staticmethod
    def create_scatter_chart(
        df: pd.DataFrame,
        x_col: str,
        y_col: str,
        group_col: Optional[str] = None,
        size_col: Optional[str] = None,
        regression: bool = False,
        confidence: bool = False,
        ax=None
    ):
        """
        创建散点图
        
        参数:
            df: 数据框
            x_col: X轴变量
            y_col: Y轴变量
            group_col: 分组变量
            size_col: 气泡图大小变量
            regression: 是否显示回归线
            confidence: 是否显示置信区间
            ax: matplotlib轴对象
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        
        x_data = df[x_col].values
        y_data = df[y_col].values
        
        if group_col is None:
            if size_col is None:
                # 普通散点图
                ax.scatter(x_data, y_data, alpha=0.6)
            else:
                # 气泡图
                sizes = df[size_col].values
                ax.scatter(x_data, y_data, s=sizes*100, alpha=0.6)
        else:
            # 分组散点图
            groups = df[group_col].unique()
            colors = plt.cm.tab10(np.linspace(0, 1, len(groups)))
            for i, group in enumerate(groups):
                group_df = df[df[group_col] == group]
                ax.scatter(
                    group_df[x_col],
                    group_df[y_col],
                    label=group,
                    color=colors[i],
                    alpha=0.6
                )
            ax.legend()
        
        if regression:
            # 添加回归线
            mask = ~(np.isnan(x_data) | np.isnan(y_data))
            x_clean = x_data[mask]
            y_clean = y_data[mask]
            
            if len(x_clean) > 1:
                model = LinearRegression()
                model.fit(x_clean.reshape(-1, 1), y_clean)
                x_line = np.linspace(x_clean.min(), x_clean.max(), 100)
                y_line = model.predict(x_line.reshape(-1, 1))
                ax.plot(x_line, y_line, 'r--', label='回归线', linewidth=2)
                
                if confidence:
                    # 计算置信区间
                    y_pred = model.predict(x_clean.reshape(-1, 1))
                    residuals = y_clean - y_pred
                    mse = np.mean(residuals**2)
                    se = np.sqrt(mse)
                    t_val = stats.t.ppf(0.975, len(x_clean) - 2)
                    ci = t_val * se * np.sqrt(1 + 1/len(x_clean) + 
                                              (x_line - x_clean.mean())**2 / 
                                              np.sum((x_clean - x_clean.mean())**2))
                    ax.fill_between(x_line, y_line - ci, y_line + ci, 
                                   alpha=0.2, color='red', label='95%置信区间')
                ax.legend()
        
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f'{x_col} vs {y_col} 散点图')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return ax

