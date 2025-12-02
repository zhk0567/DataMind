"""
AI自动分析器 - 使用Ollama进行数据分析
"""
import pandas as pd
from pandas.api.types import CategoricalDtype
import json
import requests
from typing import Dict, Optional, Any


class AIAnalyzer:
    """AI数据分析器"""
    
    def __init__(self, model_name: str = "qwen3-vl:235b-cloud", base_url: str = "http://localhost:11434"):
        """
        初始化AI分析器
        
        Args:
            model_name: Ollama模型名称
            base_url: Ollama服务地址
        """
        self.model_name = model_name
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
    
    def _call_ollama(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        调用Ollama API（非流式，用于兼容）
        
        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词
            
        Returns:
            AI返回的文本
        """
        try:
            # 构建请求数据
            data = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
            
            if system_prompt:
                data["system"] = system_prompt
            
            # 发送请求
            response = requests.post(
                self.api_url,
                json=data,
                timeout=20  # 20秒超时，平衡速度和稳定性
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                raise Exception(f"Ollama API错误: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            raise Exception("无法连接到Ollama服务，请确保Ollama已启动并运行在 http://localhost:11434")
        except requests.exceptions.Timeout:
            raise Exception("Ollama API请求超时，请检查模型是否已正确加载")
        except Exception as e:
            raise Exception(f"调用Ollama API失败: {str(e)}")
    
    def _call_ollama_stream(self, prompt: str, system_prompt: Optional[str] = None, callback=None):
        """
        调用Ollama API（流式响应）
        
        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词
            callback: 回调函数，接收每个chunk的文本片段 (chunk_text) -> None
            
        Returns:
            AI返回的完整文本
        """
        try:
            # 构建请求数据
            data = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": True  # 启用流式响应
            }
            
            if system_prompt:
                data["system"] = system_prompt
            
            # 发送请求
            response = requests.post(
                self.api_url,
                json=data,
                stream=True,  # 启用流式接收
                timeout=30  # 流式响应可能需要更长时间
            )
            
            if response.status_code != 200:
                raise Exception(f"Ollama API错误: {response.status_code} - {response.text}")
            
            # 逐行读取流式响应
            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        # 解析JSON
                        chunk_data = json.loads(line.decode('utf-8'))
                        chunk_text = chunk_data.get("response", "")
                        
                        if chunk_text:
                            full_response += chunk_text
                            # 调用回调函数实时更新UI
                            if callback:
                                callback(chunk_text)
                        
                        # 检查是否完成
                        if chunk_data.get("done", False):
                            break
                    except json.JSONDecodeError:
                        # 忽略无效的JSON行
                        continue
            
            return full_response
                
        except requests.exceptions.ConnectionError:
            raise Exception("无法连接到Ollama服务，请确保Ollama已启动并运行在 http://localhost:11434")
        except requests.exceptions.Timeout:
            raise Exception("Ollama API请求超时，请检查模型是否已正确加载")
        except Exception as e:
            raise Exception(f"调用Ollama API失败: {str(e)}")
    
    def analyze_dataframe(self, df: pd.DataFrame, callback=None) -> Dict[str, Any]:
        """
        分析数据框并返回AI分析结果（支持流式响应）
        
        Args:
            df: 要分析的数据框
            callback: 流式响应回调函数，接收每个chunk的文本片段 (chunk_text) -> None
            
        Returns:
            包含分析结果的字典
        """
        # 1. 自动进行基本统计分析
        basic_stats = self._get_basic_statistics(df)
        
        # 2. 构建AI提示词
        prompt = self._build_analysis_prompt(df, basic_stats)
        
        # 3. 系统提示词（极简化以加快响应速度，要求快速响应）
        system_prompt = """你是数据分析专家。根据统计信息，用中文快速给出简洁分析（150字以内）。

格式：使用标题和列表（•开头），总共不超过150字。

内容（必须包含）：
1. 数据质量评估（1句话）
2. 数据特征总结（2句话）
3. 主要问题和建议（3条）
4. 推荐的可视化方案（2个）
5. 推荐的统计分析方向（2个）

要求：快速响应，直接给出结论，不要展开说明。"""
        
        # 4. 调用AI（使用流式响应）
        if callback:
            ai_response = self._call_ollama_stream(prompt, system_prompt, callback)
        else:
            ai_response = self._call_ollama(prompt, system_prompt)
        
        # 5. 返回结果
        return {
            "basic_statistics": basic_stats,
            "ai_analysis": ai_response,
            "data_shape": df.shape,
            "columns": df.columns.tolist()
        }
    
    def _get_basic_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        获取数据框的基本统计信息
        
        Args:
            df: 数据框
            
        Returns:
            基本统计信息字典
        """
        stats = {
            "shape": {
                "rows": len(df),
                "columns": len(df.columns)
            },
            "columns": {},
            "missing_values": {},
            "data_types": {},
            "numeric_summary": {},
            "categorical_summary": {}
        }
        
        # 列信息
        for col in df.columns:
            stats["columns"][col] = {
                "dtype": str(df[col].dtype),
                "null_count": int(df[col].isnull().sum()),
                "null_percentage": float(df[col].isnull().sum() / len(df) * 100)
            }
            
            # 数值型列统计
            if pd.api.types.is_numeric_dtype(df[col]):
                stats["numeric_summary"][col] = {
                    "mean": float(df[col].mean()) if not df[col].isnull().all() else None,
                    "std": float(df[col].std()) if not df[col].isnull().all() else None,
                    "min": float(df[col].min()) if not df[col].isnull().all() else None,
                    "max": float(df[col].max()) if not df[col].isnull().all() else None,
                    "median": float(df[col].median()) if not df[col].isnull().all() else None
                }
            
            # 分类型列统计（只统计前5个最常见的值，减少计算量）
            col_dtype = df[col].dtype
            if pd.api.types.is_object_dtype(col_dtype) or isinstance(col_dtype, CategoricalDtype):
                value_counts = df[col].value_counts().head(5).to_dict()  # 从10减少到5
                stats["categorical_summary"][col] = {
                    "unique_count": int(df[col].nunique()),
                    "top_values": {str(k): int(v) for k, v in value_counts.items()}
                }
        
        # 缺失值统计
        missing_total = df.isnull().sum().sum()
        stats["missing_values"] = {
            "total": int(missing_total),
            "percentage": float(missing_total / (len(df) * len(df.columns)) * 100),
            "columns_with_missing": [col for col in df.columns if df[col].isnull().any()]
        }
        
        # 数据类型统计
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        stats["data_types"] = {
            "numeric_count": len(numeric_cols),
            "categorical_count": len(categorical_cols),
            "numeric_columns": numeric_cols,
            "categorical_columns": categorical_cols
        }
        
        return stats
    
    def _build_analysis_prompt(self, df: pd.DataFrame, basic_stats: Dict[str, Any]) -> str:
        """
        构建AI分析提示词（优化版本，减少数据量以加快速度）
        
        Args:
            df: 数据框
            basic_stats: 基本统计信息
            
        Returns:
            提示词字符串
        """
        # 只发送关键统计信息，不发送完整数据样本以加快速度
        # 极简prompt，大幅减少数据量以加快速度
        prompt = f"""数据: {basic_stats['shape']['rows']}行×{basic_stats['shape']['columns']}列, 数值列{basic_stats['data_types']['numeric_count']}个, 分类列{basic_stats['data_types']['categorical_count']}个, 缺失值{basic_stats['missing_values']['total']}个({basic_stats['missing_values']['percentage']:.1f}%)

数值列:"""
        
        # 只添加前3个数值型列的关键统计（进一步减少）
        numeric_cols = list(basic_stats['numeric_summary'].keys())[:3]
        for col in numeric_cols:
            num_info = basic_stats['numeric_summary'][col]
            if num_info['mean'] is not None:
                prompt += f" {col}(均值{num_info['mean']:.1f},范围{num_info['min']:.1f}-{num_info['max']:.1f})"
        
        prompt += "\n分类列:"
        
        # 只添加前2个分类型列的关键统计
        categorical_cols = list(basic_stats['categorical_summary'].keys())[:2]
        for col in categorical_cols:
            cat_info = basic_stats['categorical_summary'][col]
            prompt += f" {col}({cat_info['unique_count']}个唯一值)"
        
        prompt += f"""

请用150字以内快速给出分析，包括：1.数据质量评估 2.数据特征总结 3.主要问题和建议(3条) 4.推荐可视化方案(2个) 5.推荐统计分析方向(2个)。使用标题和列表，保持极简。"""
        
        return prompt

