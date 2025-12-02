"""
文件操作工具
"""
import pandas as pd
import os
from typing import Optional
import io
import base64


def save_dataframe(df: pd.DataFrame, file_path: str, file_format: str = 'csv') -> bool:
    """
    保存DataFrame到文件
    
    Args:
        df: 要保存的DataFrame
        file_path: 文件路径
        file_format: 文件格式 ('csv', 'excel')
    
    Returns:
        bool: 是否成功
    """
    try:
        if file_format == 'csv':
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
        elif file_format == 'excel':
            df.to_excel(file_path, index=False)
        else:
            return False
        return True
    except Exception:
        return False


def export_chart_image(img_bytes: bytes, file_path: str) -> bool:
    """
    导出图表图片
    
    Args:
        img_bytes: 图片字节数据
        file_path: 保存路径
    
    Returns:
        bool: 是否成功
    """
    try:
        with open(file_path, 'wb') as f:
            f.write(img_bytes)
        return True
    except Exception:
        return False


def read_dataframe(file_path: str) -> Optional[pd.DataFrame]:
    """
    读取数据文件（支持多种编码）
    
    Args:
        file_path: 文件路径
    
    Returns:
        DataFrame或None
    """
    encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
    
    if file_path.endswith('.csv'):
        for encoding in encodings:
            try:
                return pd.read_csv(file_path, encoding=encoding)
            except (UnicodeDecodeError, pd.errors.ParserError):
                continue
            except Exception:
                break
    elif file_path.endswith(('.xlsx', '.xls')):
        try:
            return pd.read_excel(file_path)
        except Exception:
            pass
    
    return None

