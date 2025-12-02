"""
数据质量评估模块
提供完整性、一致性、准确性检查
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


class DataQualityAssessor:
    """数据质量评估类"""
    
    @staticmethod
    def assess_completeness(df: pd.DataFrame) -> Dict[str, Any]:
        """
        评估数据完整性
        
        返回:
            完整性评估结果
        """
        total_cells = len(df) * len(df.columns)
        missing_cells = df.isnull().sum().sum()
        complete_cells = total_cells - missing_cells
        
        completeness_by_column = {}
        for col in df.columns:
            missing = df[col].isnull().sum()
            complete = len(df) - missing
            completeness_by_column[col] = {
                'missing_count': int(missing),
                'missing_percentage': (missing / len(df)) * 100,
                'complete_count': int(complete),
                'complete_percentage': (complete / len(df)) * 100
            }
        
        return {
            'overall_completeness': (complete_cells / total_cells) * 100 if total_cells > 0 else 0,
            'total_cells': int(total_cells),
            'missing_cells': int(missing_cells),
            'complete_cells': int(complete_cells),
            'by_column': completeness_by_column,
            'completely_missing_columns': [
                col for col, info in completeness_by_column.items()
                if info['complete_count'] == 0
            ],
            'fully_complete_columns': [
                col for col, info in completeness_by_column.items()
                if info['missing_count'] == 0
            ]
        }
    
    @staticmethod
    def assess_consistency(df: pd.DataFrame) -> Dict[str, Any]:
        """
        评估数据一致性
        
        返回:
            一致性评估结果
        """
        consistency_issues = []
        
        # 检查数据类型一致性
        type_consistency = {}
        for col in df.columns:
            dtype = str(df[col].dtype)
            type_consistency[col] = dtype
        
        # 检查数值范围一致性
        range_issues = {}
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            data = df[col].dropna()
            if len(data) > 0:
                min_val = data.min()
                max_val = data.max()
                mean_val = data.mean()
                std_val = data.std()
                
                # 检查是否有异常大的值
                if std_val > 0:
                    z_scores = np.abs((data - mean_val) / std_val)
                    extreme_values = (z_scores > 5).sum()
                    if extreme_values > 0:
                        range_issues[col] = {
                            'extreme_count': int(extreme_values),
                            'min': float(min_val),
                            'max': float(max_val),
                            'mean': float(mean_val)
                        }
        
        # 检查分类变量一致性
        categorical_issues = {}
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            unique_values = df[col].dropna().unique()
            # 检查是否有相似的值（可能是输入错误）
            # 这里简化处理，实际可以更复杂
            if len(unique_values) > 100:
                categorical_issues[col] = {
                    'unique_count': len(unique_values),
                    'warning': '分类变量值过多，可能存在不一致'
                }
        
        return {
            'type_consistency': type_consistency,
            'range_issues': range_issues,
            'categorical_issues': categorical_issues,
            'overall_consistency_score': 100 - len(range_issues) * 10 - len(categorical_issues) * 5
        }
    
    @staticmethod
    def assess_accuracy(df: pd.DataFrame, rules: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        评估数据准确性
        
        参数:
            df: 数据框
            rules: 自定义验证规则
        
        返回:
            准确性评估结果
        """
        accuracy_issues = []
        
        # 检查重复值
        duplicate_count = df.duplicated().sum()
        if duplicate_count > 0:
            accuracy_issues.append({
                'type': 'duplicates',
                'count': int(duplicate_count),
                'percentage': (duplicate_count / len(df)) * 100
            })
        
        # 检查数值列的合理性
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            data = df[col].dropna()
            if len(data) > 0:
                # 检查负值（如果应该为正）
                negative_count = (data < 0).sum()
                if negative_count > 0 and col.lower() not in ['difference', 'change', 'delta']:
                    accuracy_issues.append({
                        'type': 'negative_values',
                        'column': col,
                        'count': int(negative_count)
                    })
                
                # 检查零值（如果不应该为零）
                zero_count = (data == 0).sum()
                if zero_count == len(data):
                    accuracy_issues.append({
                        'type': 'all_zeros',
                        'column': col,
                        'warning': '列中所有值都为零'
                    })
        
        # 应用自定义规则
        if rules:
            for rule_name, rule_func in rules.items():
                try:
                    result = rule_func(df)
                    if result:
                        accuracy_issues.append({
                            'type': 'custom_rule',
                            'rule': rule_name,
                            'issues': result
                        })
                except Exception as e:
                    accuracy_issues.append({
                        'type': 'rule_error',
                        'rule': rule_name,
                        'error': str(e)
                    })
        
        return {
            'issues': accuracy_issues,
            'total_issues': len(accuracy_issues),
            'accuracy_score': max(0, 100 - len(accuracy_issues) * 10)
        }
    
    @staticmethod
    def generate_quality_report(df: pd.DataFrame) -> Dict[str, Any]:
        """
        生成完整的数据质量报告
        
        返回:
            包含所有质量评估结果的字典
        """
        completeness = DataQualityAssessor.assess_completeness(df)
        consistency = DataQualityAssessor.assess_consistency(df)
        accuracy = DataQualityAssessor.assess_accuracy(df)
        
        # 计算总体质量分数
        overall_score = (
            completeness['overall_completeness'] * 0.4 +
            consistency['overall_consistency_score'] * 0.3 +
            accuracy['accuracy_score'] * 0.3
        )
        
        return {
            'overall_quality_score': overall_score,
            'completeness': completeness,
            'consistency': consistency,
            'accuracy': accuracy,
            'summary': {
                'total_rows': len(df),
                'total_columns': len(df.columns),
                'missing_cells': completeness['missing_cells'],
                'duplicate_rows': accuracy['issues'][0]['count'] if accuracy['issues'] and accuracy['issues'][0]['type'] == 'duplicates' else 0,
                'quality_level': (
                    '优秀' if overall_score >= 90 else
                    '良好' if overall_score >= 70 else
                    '中等' if overall_score >= 50 else
                    '较差'
                )
            }
        }

