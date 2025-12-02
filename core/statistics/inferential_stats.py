"""
推断统计分析模块
"""
import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Any, List


class InferentialStatistics:
    """推断统计分析类"""
    
    def t_test_one_sample(
        self, df: pd.DataFrame, column: str, test_value: float = 0.0
    ) -> Dict[str, Any]:
        """单样本t检验"""
        if column not in df.columns:
            return {"error": "指定的列不存在"}
        
        data = df[column].dropna()
        if len(data) < 2:
            return {"error": "数据不足"}
        
        t_stat, p_value = stats.ttest_1samp(data, test_value)
        
        return {
            "t_statistic": float(t_stat),
            "p_value": float(p_value),
            "df": int(len(data) - 1),
            "mean": float(data.mean()),
            "std": float(data.std()),
            "test_value": float(test_value),
            "significant": p_value < 0.05,
            "mean_difference": float(data.mean() - test_value),
            "ci_lower": float(data.mean() - 1.96 * data.std() / np.sqrt(len(data))),
            "ci_upper": float(data.mean() + 1.96 * data.std() / np.sqrt(len(data)))
        }
    
    def t_test_independent(
        self, df: pd.DataFrame, group_col: str, value_col: str
    ) -> Dict[str, Any]:
        """独立样本t检验"""
        if group_col not in df.columns or value_col not in df.columns:
            return {"error": "指定的列不存在"}
        
        groups = df.groupby(group_col)[value_col]
        group_names = list(groups.groups.keys())
        
        if len(group_names) != 2:
            return {"error": "分组变量必须恰好有2个水平"}
        
        group1_data = groups.get_group(group_names[0]).dropna()
        group2_data = groups.get_group(group_names[1]).dropna()
        
        if len(group1_data) < 2 or len(group2_data) < 2:
            return {"error": "数据不足"}
        
        levene_stat, levene_p = stats.levene(group1_data, group2_data)
        equal_var = levene_p > 0.05
        
        t_stat, p_value = stats.ttest_ind(group1_data, group2_data, equal_var=equal_var)
        
        return {
            "t_statistic": float(t_stat),
            "p_value": float(p_value),
            "df": int(len(group1_data) + len(group2_data) - 2),
            "group1_name": str(group_names[0]),
            "group1_mean": float(group1_data.mean()),
            "group1_std": float(group1_data.std()),
            "group1_n": int(len(group1_data)),
            "group2_name": str(group_names[1]),
            "group2_mean": float(group2_data.mean()),
            "group2_std": float(group2_data.std()),
            "group2_n": int(len(group2_data)),
            "mean_difference": float(group1_data.mean() - group2_data.mean()),
            "equal_var": bool(equal_var),
            "levene_statistic": float(levene_stat),
            "levene_p_value": float(levene_p),
            "significant": p_value < 0.05
        }
    
    def t_test_paired(
        self, df: pd.DataFrame, col1: str, col2: str
    ) -> Dict[str, Any]:
        """配对样本t检验"""
        if col1 not in df.columns or col2 not in df.columns:
            return {"error": "指定的列不存在"}
        
        valid_mask = df[[col1, col2]].notna().all(axis=1)
        paired_data1 = df.loc[valid_mask, col1]
        paired_data2 = df.loc[valid_mask, col2]
        
        if len(paired_data1) < 2:
            return {"error": "数据不足"}
        
        t_stat, p_value = stats.ttest_rel(paired_data1, paired_data2)
        differences = paired_data1 - paired_data2
        
        return {
            "t_statistic": float(t_stat),
            "p_value": float(p_value),
            "df": int(len(paired_data1) - 1),
            "col1_mean": float(paired_data1.mean()),
            "col1_std": float(paired_data1.std()),
            "col2_mean": float(paired_data2.mean()),
            "col2_std": float(paired_data2.std()),
            "mean_difference": float(differences.mean()),
            "std_difference": float(differences.std()),
            "significant": p_value < 0.05
        }
    
    def chi_square_test(
        self, df: pd.DataFrame, col1: str, col2: str
    ) -> Dict[str, Any]:
        """卡方检验"""
        if col1 not in df.columns or col2 not in df.columns:
            return {"error": "指定的列不存在"}
        
        contingency_table = pd.crosstab(df[col1], df[col2])
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        
        return {
            "chi2_statistic": float(chi2),
            "p_value": float(p_value),
            "degrees_of_freedom": int(dof),
            "contingency_table": contingency_table.to_dict(),
            "expected_frequencies": expected.tolist(),
            "significant": p_value < 0.05
        }
    
    def mann_whitney_test(
        self, df: pd.DataFrame, group_col: str, value_col: str
    ) -> Dict[str, Any]:
        """Mann-Whitney U检验"""
        if group_col not in df.columns or value_col not in df.columns:
            return {"error": "指定的列不存在"}
        
        groups = df.groupby(group_col)[value_col]
        group_names = list(groups.groups.keys())
        
        if len(group_names) != 2:
            return {"error": "分组变量必须恰好有2个水平"}
        
        group1_data = groups.get_group(group_names[0]).dropna()
        group2_data = groups.get_group(group_names[1]).dropna()
        
        if len(group1_data) < 2 or len(group2_data) < 2:
            return {"error": "数据不足"}
        
        u_stat, p_value = stats.mannwhitneyu(
            group1_data, group2_data, alternative='two-sided'
        )
        
        return {
            "u_statistic": float(u_stat),
            "p_value": float(p_value),
            "group1_name": str(group_names[0]),
            "group1_median": float(group1_data.median()),
            "group1_n": int(len(group1_data)),
            "group2_name": str(group_names[1]),
            "group2_median": float(group2_data.median()),
            "group2_n": int(len(group2_data)),
            "significant": p_value < 0.05
        }
    
    def kruskal_wallis_test(
        self, df: pd.DataFrame, group_col: str, value_col: str
    ) -> Dict[str, Any]:
        """Kruskal-Wallis检验"""
        if group_col not in df.columns or value_col not in df.columns:
            return {"error": "指定的列不存在"}
        
        groups = [
            group[value_col].dropna().values
            for name, group in df.groupby(group_col)
        ]
        group_names = list(df[group_col].unique())
        
        if len(groups) < 2:
            return {"error": "分组数量不足"}
        
        h_stat, p_value = stats.kruskal(*groups)
        
        group_stats = []
        for name, data in zip(group_names, groups):
            group_stats.append({
                "group": str(name),
                "median": float(np.median(data)),
                "n": int(len(data))
            })
        
        return {
            "h_statistic": float(h_stat),
            "p_value": float(p_value),
            "df": int(len(groups) - 1),
            "group_stats": group_stats,
            "significant": p_value < 0.05
        }
    
    def anova_analysis(
        self, df: pd.DataFrame, columns: List[str], options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """方差分析（ANOVA）"""
        if len(columns) < 2:
            return {"error": "方差分析需要至少2个变量"}
        
        group_col = columns[0]
        value_cols = columns[1:]
        
        results = {}
        for value_col in value_cols:
            if value_col not in df.columns:
                continue
            if df[value_col].dtype not in ['int64', 'float64']:
                continue
            
            groups = [
                group[value_col].dropna().values
                for name, group in df.groupby(group_col)
            ]
            
            if len(groups) < 2:
                results[value_col] = {"error": "分组数量不足"}
                continue
            
            f_stat, p_value = stats.f_oneway(*groups)
            
            all_data = df[[group_col, value_col]].dropna()
            grand_mean = all_data[value_col].mean()
            
            group_stats = []
            ss_between = 0
            ss_within = 0
            
            for name, group in df.groupby(group_col):
                group_data = group[value_col].dropna()
                if len(group_data) == 0:
                    continue
                
                group_mean = group_data.mean()
                n = len(group_data)
                ss_between += n * (group_mean - grand_mean) ** 2
                ss_within += ((group_data - group_mean) ** 2).sum()
                
                group_stats.append({
                    "group": str(name),
                    "mean": float(group_mean),
                    "std": float(group_data.std()),
                    "n": int(n)
                })
            
            df_between = len(groups) - 1
            df_within = len(all_data) - len(groups)
            ms_between = ss_between / df_between if df_between > 0 else 0
            ms_within = ss_within / df_within if df_within > 0 else 0
            
            results[value_col] = {
                "f_statistic": float(f_stat),
                "p_value": float(p_value),
                "significant": p_value < 0.05,
                "df_between": int(df_between),
                "df_within": int(df_within),
                "ss_between": float(ss_between),
                "ss_within": float(ss_within),
                "ms_between": float(ms_between),
                "ms_within": float(ms_within),
                "eta_squared": float(
                    ss_between / (ss_between + ss_within)
                ) if (ss_between + ss_within) > 0 else 0.0,
                "groups": group_stats
            }
        
        return results

