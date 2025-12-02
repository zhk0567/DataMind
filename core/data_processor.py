"""
数据处理核心模块 - 扩展版（参考SPSSPRO功能）
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
try:
    from sklearn.preprocessing import LabelEncoder, StandardScaler
except ImportError:
    LabelEncoder = None
    StandardScaler = None


class DataProcessor:
    """数据处理类 - 扩展版"""
    
    def get_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        获取数据摘要信息
        """
        return {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "missing_values": df.isnull().sum().to_dict(),
            "numeric_columns": df.select_dtypes(include=[np.number]).columns.tolist(),
            "categorical_columns": df.select_dtypes(include=['object']).columns.tolist(),
            "memory_usage": df.memory_usage(deep=True).sum()
        }
    
    def clean_data(self, df: pd.DataFrame, options: Dict[str, Any]) -> pd.DataFrame:
        """
        清洗数据
        """
        cleaned_df = df.copy()
        
        # 处理缺失值
        if options.get("handle_missing") == "drop":
            cleaned_df = cleaned_df.dropna()
        elif options.get("handle_missing") == "fill_mean":
            numeric_cols = cleaned_df.select_dtypes(include=[np.number]).columns
            cleaned_df[numeric_cols] = cleaned_df[numeric_cols].fillna(
                cleaned_df[numeric_cols].mean()
            )
        elif options.get("handle_missing") == "fill_median":
            numeric_cols = cleaned_df.select_dtypes(include=[np.number]).columns
            cleaned_df[numeric_cols] = cleaned_df[numeric_cols].fillna(
                cleaned_df[numeric_cols].median()
            )
        elif options.get("handle_missing") == "fill_mode":
            for col in cleaned_df.columns:
                if cleaned_df[col].isnull().any():
                    mode_value = cleaned_df[col].mode()
                    if len(mode_value) > 0:
                        cleaned_df[col] = cleaned_df[col].fillna(mode_value[0])
        elif options.get("handle_missing") == "fill_custom":
            fill_value = options.get("fill_value", "")
            if fill_value:
                try:
                    fill_value = float(fill_value)
                except ValueError:
                    pass
                cleaned_df = cleaned_df.fillna(fill_value)
        
        # 处理异常值
        if options.get("handle_outliers"):
            numeric_cols = cleaned_df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                Q1 = cleaned_df[col].quantile(0.25)
                Q3 = cleaned_df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                cleaned_df = cleaned_df[
                    (cleaned_df[col] >= lower_bound) & (cleaned_df[col] <= upper_bound)
                ]
        
        # 处理重复值
        if options.get("handle_duplicates") == "drop":
            cleaned_df = cleaned_df.drop_duplicates()
        elif options.get("handle_duplicates") == "keep_first":
            cleaned_df = cleaned_df.drop_duplicates(keep='first')
        elif options.get("handle_duplicates") == "keep_last":
            cleaned_df = cleaned_df.drop_duplicates(keep='last')
        
        return cleaned_df
    
    def encode_categorical(
        self, df: pd.DataFrame, columns: List[str], method: str = "one-hot"
    ) -> pd.DataFrame:
        """
        编码分类变量
        """
        encoded_df = df.copy()
        
        if method == "one-hot":
            encoded_df = pd.get_dummies(encoded_df, columns=columns)
        elif method == "label":
            if LabelEncoder is None:
                raise ImportError("需要安装scikit-learn库以使用标签编码")
            le = LabelEncoder()
            for col in columns:
                encoded_df[col] = le.fit_transform(encoded_df[col].astype(str))
        
        return encoded_df
    
    def filter_data(
        self, df: pd.DataFrame, conditions: List[Dict[str, Any]]
    ) -> pd.DataFrame:
        """
        数据筛选
        conditions: [{"column": "col1", "operator": ">", "value": 10}, ...]
        """
        filtered_df = df.copy()
        
        for condition in conditions:
            col = condition.get("column")
            operator = condition.get("operator")
            value = condition.get("value")
            
            if col not in filtered_df.columns:
                continue
            
            if operator == "==":
                filtered_df = filtered_df[filtered_df[col] == value]
            elif operator == "!=":
                filtered_df = filtered_df[filtered_df[col] != value]
            elif operator == ">":
                filtered_df = filtered_df[filtered_df[col] > value]
            elif operator == ">=":
                filtered_df = filtered_df[filtered_df[col] >= value]
            elif operator == "<":
                filtered_df = filtered_df[filtered_df[col] < value]
            elif operator == "<=":
                filtered_df = filtered_df[filtered_df[col] <= value]
            elif operator == "in":
                filtered_df = filtered_df[filtered_df[col].isin(value)]
            elif operator == "not in":
                filtered_df = filtered_df[~filtered_df[col].isin(value)]
            elif operator == "contains":
                filtered_df = filtered_df[
                    filtered_df[col].astype(str).str.contains(str(value), na=False)
                ]
        
        return filtered_df
    
    def sort_data(
        self, df: pd.DataFrame, columns: List[str], ascending: List[bool]
    ) -> pd.DataFrame:
        """
        数据排序
        """
        if len(columns) != len(ascending):
            ascending = [True] * len(columns)
        
        return df.sort_values(by=columns, ascending=ascending)
    
    def merge_data(
        self, df1: pd.DataFrame, df2: pd.DataFrame,
        how: str = "inner", on: Optional[List[str]] = None,
        left_on: Optional[List[str]] = None, right_on: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        数据合并
        """
        if on:
            return pd.merge(df1, df2, on=on, how=how)
        elif left_on and right_on:
            return pd.merge(df1, df2, left_on=left_on, right_on=right_on, how=how)
        else:
            return pd.merge(df1, df2, how=how)
    
    def split_data(
        self, df: pd.DataFrame, group_col: str
    ) -> Dict[str, pd.DataFrame]:
        """
        数据拆分
        """
        result = {}
        for name, group in df.groupby(group_col):
            result[str(name)] = group.copy()
        return result
    
    def recode_variable(
        self, df: pd.DataFrame, column: str, mapping: Dict[Any, Any]
    ) -> pd.DataFrame:
        """
        变量重编码
        """
        recoded_df = df.copy()
        recoded_df[column] = recoded_df[column].map(mapping)
        return recoded_df
    
    def compute_variable(
        self, df: pd.DataFrame, new_col: str, expression: str
    ) -> pd.DataFrame:
        """
        计算新变量
        expression: 表达式，如 "col1 + col2", "col1 * 2", "col1 / col2"
        """
        computed_df = df.copy()
        
        # 简单的表达式计算（支持基本运算）
        try:
            # 替换列名为实际值
            for col in df.columns:
                expression = expression.replace(col, f"computed_df['{col}']")
            
            computed_df[new_col] = eval(expression)
        except Exception as e:
            raise ValueError(f"表达式计算失败: {str(e)}")
        
        return computed_df
    
    def standardize_variables(
        self, df: pd.DataFrame, columns: List[str]
    ) -> pd.DataFrame:
        """
        标准化变量（Z-score标准化）
        """
        if StandardScaler is None:
            raise ImportError("需要安装scikit-learn库以使用标准化")
        
        standardized_df = df.copy()
        scaler = StandardScaler()
        
        for col in columns:
            if col in standardized_df.columns:
                standardized_df[col] = scaler.fit_transform(
                    standardized_df[[col]]
                ).flatten()
        
        return standardized_df
    
    def normalize_variables(
        self, df: pd.DataFrame, columns: List[str], method: str = "min-max"
    ) -> pd.DataFrame:
        """
        归一化变量
        method: 'min-max' 或 'z-score'
        """
        normalized_df = df.copy()
        
        for col in columns:
            if col not in normalized_df.columns:
                continue
            
            if method == "min-max":
                min_val = normalized_df[col].min()
                max_val = normalized_df[col].max()
                if max_val != min_val:
                    normalized_df[col] = (
                        (normalized_df[col] - min_val) / (max_val - min_val)
                    )
            elif method == "z-score":
                mean_val = normalized_df[col].mean()
                std_val = normalized_df[col].std()
                if std_val != 0:
                    normalized_df[col] = (normalized_df[col] - mean_val) / std_val
        
        return normalized_df
    
    def discretize_variable(
        self, df: pd.DataFrame, column: str, method: str = "equal_width",
        n_bins: int = 5, labels: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        变量离散化
        method: 'equal_width'（等宽）或 'equal_freq'（等频）
        """
        discretized_df = df.copy()
        
        if method == "equal_width":
            discretized_df[column + "_binned"] = pd.cut(
                discretized_df[column], bins=n_bins, labels=labels
            )
        elif method == "equal_freq":
            discretized_df[column + "_binned"] = pd.qcut(
                discretized_df[column], q=n_bins, labels=labels
            )
        
        return discretized_df
    
    def aggregate_data(
        self, df: pd.DataFrame, group_cols: List[str],
        agg_cols: List[str], agg_functions: List[str]
    ) -> pd.DataFrame:
        """
        数据聚合
        agg_functions: ['mean', 'sum', 'count', 'std', 'min', 'max', ...]
        """
        agg_dict = {}
        for col, func in zip(agg_cols, agg_functions):
            if col not in agg_dict:
                agg_dict[col] = []
            agg_dict[col].append(func)
        
        return df.groupby(group_cols).agg(agg_dict).reset_index()
