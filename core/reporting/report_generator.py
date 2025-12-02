"""
统计报告生成器
生成Word、PDF等格式的统计报告
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from datetime import datetime
import os


class ReportGenerator:
    """统计报告生成器"""
    
    def __init__(self):
        self.report_sections = []
    
    def generate_descriptive_report(
        self,
        result: Dict[str, Any],
        variable_name: str
    ) -> str:
        """
        生成描述性统计报告
        
        参数:
            result: 描述性统计结果字典
            variable_name: 变量名
        """
        report = f"## {variable_name} 描述性统计报告\n\n"
        report += f"**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # 基本统计量
        report += "### 基本统计量\n\n"
        report += "| 统计量 | 数值 |\n"
        report += "|--------|------|\n"
        
        if 'count' in result:
            report += f"| 样本量 | {result['count']:.0f} |\n"
        if 'mean' in result:
            report += f"| 均值 | {result['mean']:.4f} |\n"
        if 'std' in result:
            report += f"| 标准差 | {result['std']:.4f} |\n"
        if 'min' in result:
            report += f"| 最小值 | {result['min']:.4f} |\n"
        # 支持两种键名格式
        q25 = result.get('q25') or result.get('25%')
        if q25 is not None:
            report += f"| 第一四分位数 (Q1) | {q25:.4f} |\n"
        median = result.get('median') or result.get('50%')
        if median is not None:
            report += f"| 中位数 | {median:.4f} |\n"
        q75 = result.get('q75') or result.get('75%')
        if q75 is not None:
            report += f"| 第三四分位数 (Q3) | {q75:.4f} |\n"
        if 'max' in result:
            report += f"| 最大值 | {result['max']:.4f} |\n"
        
        # 高级统计量
        if 'skewness' in result or 'kurtosis' in result:
            report += "\n### 分布特征\n\n"
            report += "| 统计量 | 数值 |\n"
            report += "|--------|------|\n"
            if 'skewness' in result:
                skew = result['skewness']
                skew_desc = "右偏" if skew > 0 else "左偏" if skew < 0 else "对称"
                report += f"| 偏度 | {skew:.4f} ({skew_desc}) |\n"
            if 'kurtosis' in result:
                kurt = result['kurtosis']
                kurt_desc = "尖峰" if kurt > 0 else "平峰" if kurt < 0 else "正态"
                report += f"| 峰度 | {kurt:.4f} ({kurt_desc}) |\n"
        
        # 缺失值信息
        if 'missing_count' in result:
            report += "\n### 数据质量\n\n"
            report += f"- 缺失值数量：{result['missing_count']:.0f}\n"
            if 'missing_pct' in result:
                report += f"- 缺失值比例：{result['missing_pct']:.2f}%\n"
        
        # 解释说明
        report += "\n### 结果解释\n\n"
        if 'mean' in result and 'std' in result:
            cv = result['std'] / result['mean'] if result['mean'] != 0 else 0
            report += f"- 均值 {result['mean']:.4f} 表示数据的中心趋势。\n"
            report += f"- 标准差 {result['std']:.4f} 表示数据的离散程度。\n"
            if cv > 0:
                cv_desc = "高" if cv > 0.5 else "中等" if cv > 0.2 else "低"
                report += f"- 变异系数 {cv:.4f} ({cv_desc}变异) 表示相对离散程度。\n"
        
        return report
    
    def generate_hypothesis_test_report(
        self,
        result: Dict[str, Any],
        test_name: str,
        hypothesis: str
    ) -> str:
        """
        生成假设检验报告
        
        参数:
            result: 检验结果字典
            test_name: 检验名称
            hypothesis: 假设说明
        """
        report = f"## {test_name} 检验报告\n\n"
        report += f"**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # 假设说明
        report += "### 检验假设\n\n"
        report += f"{hypothesis}\n\n"
        
        # 检验结果
        report += "### 检验结果\n\n"
        report += "| 项目 | 数值 |\n"
        report += "|------|------|\n"
        
        if 'statistic' in result:
            report += f"| 检验统计量 | {result['statistic']:.4f} |\n"
        if 'p_value' in result:
            report += f"| P值 | {result['p_value']:.6f} |\n"
        if 'df' in result:
            report += f"| 自由度 | {result['df']:.0f} |\n"
        if 'confidence_interval' in result:
            ci = result['confidence_interval']
            report += f"| 95%置信区间 | [{ci[0]:.4f}, {ci[1]:.4f}] |\n"
        
        # 效应量
        if 'effect_size' in result:
            report += "\n### 效应量\n\n"
            effect = result['effect_size']
            effect_type = result.get('effect_type', 'Cohen\'s d')
            effect_desc = self._interpret_effect_size(effect, effect_type)
            report += f"- {effect_type}: {effect:.4f} ({effect_desc})\n"
        
        # 结论
        report += "\n### 结论\n\n"
        if 'p_value' in result:
            alpha = result.get('alpha', 0.05)
            if result['p_value'] < alpha:
                report += f"- 在显著性水平 α={alpha} 下，拒绝原假设（P < {alpha}）。\n"
                report += "- 有统计学证据表明存在显著差异。\n"
            else:
                report += f"- 在显著性水平 α={alpha} 下，不能拒绝原假设（P ≥ {alpha}）。\n"
                report += "- 没有足够的统计学证据表明存在显著差异。\n"
        
        # 注意事项
        report += "\n### 注意事项\n\n"
        report += "- 本检验基于样本数据，结果仅适用于当前样本。\n"
        report += "- 请结合实际情况和专业判断解释结果。\n"
        if 'assumptions' in result:
            report += f"- 检验假设：{result['assumptions']}\n"
        
        return report
    
    def generate_regression_report(
        self,
        result: Dict[str, Any],
        model_type: str = "线性回归"
    ) -> str:
        """
        生成回归分析报告
        
        参数:
            result: 回归结果字典
            model_type: 模型类型
        """
        report = f"## {model_type} 分析报告\n\n"
        report += f"**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # 模型摘要
        report += "### 模型摘要\n\n"
        report += "| 指标 | 数值 |\n"
        report += "|------|------|\n"
        
        if 'r_squared' in result:
            report += f"| R² | {result['r_squared']:.4f} |\n"
        if 'adjusted_r_squared' in result:
            report += f"| 调整R² | {result['adjusted_r_squared']:.4f} |\n"
        if 'f_statistic' in result:
            report += f"| F统计量 | {result['f_statistic']:.4f} |\n"
        if 'f_p_value' in result:
            report += f"| F检验P值 | {result['f_p_value']:.6f} |\n"
        
        # 系数表
        if 'coefficients' in result:
            report += "\n### 回归系数\n\n"
            report += "| 变量 | 系数 | 标准误 | t值 | P值 | 95%置信区间 |\n"
            report += "|------|------|--------|-----|-----|-------------|\n"
            
            coefs = result['coefficients']
            if isinstance(coefs, dict):
                for var, coef_info in coefs.items():
                    if isinstance(coef_info, dict):
                        coef = coef_info.get('coefficient', coef_info.get('coef', 0))
                        se = coef_info.get('std_err', coef_info.get('se', 0))
                        t_val = coef_info.get('t_value', coef_info.get('t', 0))
                        p_val = coef_info.get('p_value', coef_info.get('p', 1))
                        ci_lower = coef_info.get('ci_lower', 0)
                        ci_upper = coef_info.get('ci_upper', 0)
                        
                        report += f"| {var} | {coef:.4f} | {se:.4f} | {t_val:.4f} | {p_val:.6f} | [{ci_lower:.4f}, {ci_upper:.4f}] |\n"
                    else:
                        report += f"| {var} | {coef_info:.4f} | - | - | - | - |\n"
            
            if 'intercept' in result:
                intercept = result['intercept']
                report += f"| 截距 | {intercept:.4f} | - | - | - | - |\n"
        
        # 模型诊断
        if 'diagnostics' in result:
            report += "\n### 模型诊断\n\n"
            diag = result['diagnostics']
            if 'durbin_watson' in diag:
                dw = diag['durbin_watson']
                dw_desc = "无自相关" if 1.5 < dw < 2.5 else "可能存在自相关"
                report += f"- Durbin-Watson统计量: {dw:.4f} ({dw_desc})\n"
            if 'vif' in diag:
                report += "- 方差膨胀因子 (VIF):\n"
                for var, vif_val in diag['vif'].items():
                    vif_desc = "无多重共线性" if vif_val < 5 else "可能存在多重共线性"
                    report += f"  - {var}: {vif_val:.4f} ({vif_desc})\n"
        
        # 结论
        report += "\n### 结论\n\n"
        if 'r_squared' in result:
            r2 = result['r_squared']
            r2_desc = "强" if r2 > 0.7 else "中等" if r2 > 0.3 else "弱"
            report += f"- 模型拟合优度R² = {r2:.4f}，表示模型解释了{r2*100:.2f}%的变异（{r2_desc}拟合）。\n"
        
        if 'f_p_value' in result:
            if result['f_p_value'] < 0.05:
                report += "- 模型整体显著（F检验P < 0.05）。\n"
            else:
                report += "- 模型整体不显著（F检验P ≥ 0.05）。\n"
        
        return report
    
    def _interpret_effect_size(self, effect: float, effect_type: str) -> str:
        """解释效应量"""
        if effect_type in ['Cohen\'s d', 'Cohen d', 'd']:
            if abs(effect) < 0.2:
                return "小效应"
            elif abs(effect) < 0.5:
                return "中等效应"
            elif abs(effect) < 0.8:
                return "大效应"
            else:
                return "很大效应"
        elif effect_type in ['r', 'Pearson r']:
            if abs(effect) < 0.1:
                return "小效应"
            elif abs(effect) < 0.3:
                return "中等效应"
            elif abs(effect) < 0.5:
                return "大效应"
            else:
                return "很大效应"
        else:
            return "需要进一步解释"
    
    def save_markdown_report(self, report: str, file_path: str):
        """保存Markdown格式报告"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(report)
    
    def save_text_report(self, report: str, file_path: str):
        """保存纯文本格式报告"""
        # 简单的Markdown到文本转换
        text = report
        # 移除Markdown标记
        text = text.replace('## ', '').replace('### ', '').replace('**', '')
        text = text.replace('|', ' ').replace('- ', '  ')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
    
    def generate_complete_report(
        self,
        result: Dict[str, Any],
        analysis_key: str,
        analysis_name: str,
        table_data: Optional[str] = None,
        interpretation: Optional[str] = None
    ) -> str:
        """
        生成完整分析报告（参考SPSS Pro格式）
        整合表格数据、统计报告和结果解释
        
        参数:
            result: 分析结果字典
            analysis_key: 分析类型键
            analysis_name: 分析名称
            table_data: 表格数据（文本格式，可选）
            interpretation: 结果解释（可选）
        """
        report = f"# {analysis_name} 分析报告\n\n"
        report += f"**报告生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        report += "---\n\n"
        
        # 1. 分析概述
        report += "## 一、分析概述\n\n"
        report += f"本报告展示了 **{analysis_name}** 的完整分析结果，包括数据摘要、统计结果、详细解释和结论。\n\n"
        report += "---\n\n"
        
        # 2. 数据摘要（表格数据）
        if table_data:
            report += "## 二、数据摘要\n\n"
            report += table_data
            report += "\n---\n\n"
        
        # 3. 统计结果
        report += "## 三、统计结果\n\n"
        
        # 根据分析类型生成相应的统计报告
        if analysis_key == "descriptive":
            var_name = list(result.keys())[0] if result else "变量"
            stat_report = self.generate_descriptive_report(result[var_name], var_name)
            # 移除标题，只保留内容
            stat_report = stat_report.split('\n', 2)[2] if '\n' in stat_report else stat_report
            report += stat_report
        elif analysis_key in ["t_test_one", "t_test_independent", "t_test_paired"]:
            test_names = {
                "t_test_one": "单样本t检验",
                "t_test_independent": "独立样本t检验",
                "t_test_paired": "配对样本t检验"
            }
            hypothesis = "检验样本均值是否与理论值/其他组存在显著差异"
            stat_report = self.generate_hypothesis_test_report(
                result, test_names[analysis_key], hypothesis
            )
            stat_report = stat_report.split('\n', 2)[2] if '\n' in stat_report else stat_report
            report += stat_report
        elif analysis_key == "regression":
            stat_report = self.generate_regression_report(result, "线性回归")
            stat_report = stat_report.split('\n', 2)[2] if '\n' in stat_report else stat_report
            report += stat_report
        elif analysis_key == "stepwise_regression":
            stat_report = self.generate_regression_report(result, "逐步回归")
            stat_report = stat_report.split('\n', 2)[2] if '\n' in stat_report else stat_report
            report += stat_report
        elif analysis_key == "logistic_regression":
            stat_report = self.generate_regression_report(result, "逻辑回归")
            stat_report = stat_report.split('\n', 2)[2] if '\n' in stat_report else stat_report
            report += stat_report
        elif analysis_key == "anova":
            hypothesis = "检验多组均值是否存在显著差异"
            stat_report = self.generate_hypothesis_test_report(
                result, "方差分析", hypothesis
            )
            stat_report = stat_report.split('\n', 2)[2] if '\n' in stat_report else stat_report
            report += stat_report
        elif analysis_key == "correlation":
            report += self._generate_correlation_report(result)
        else:
            # 通用报告格式
            report += self._generate_generic_stat_report(result, analysis_name)
        
        report += "\n---\n\n"
        
        # 4. 结果解释
        if interpretation:
            report += "## 四、结果解释\n\n"
            report += interpretation
            report += "\n---\n\n"
        
        # 5. 结论与建议
        report += "## 五、结论与建议\n\n"
        report += self._generate_conclusion(result, analysis_key)
        report += "\n\n"
        
        # 6. 注意事项
        report += "## 六、注意事项\n\n"
        report += "- 本分析基于当前样本数据，结果仅适用于当前数据集。\n"
        report += "- 请结合实际情况和专业判断解释结果。\n"
        report += "- 如需进一步分析，建议咨询统计学专家。\n"
        
        return report
    
    def _generate_correlation_report(self, result: Dict[str, Any]) -> str:
        """生成相关分析报告"""
        report = ""
        if 'correlation_matrix' in result:
            corr_matrix = result['correlation_matrix']
            if isinstance(corr_matrix, dict):
                report += "### 相关系数矩阵\n\n"
                report += "| 变量1 | 变量2 | 相关系数 | 显著性 |\n"
                report += "|-------|-------|----------|--------|\n"
                for pair, corr_val in corr_matrix.items():
                    if isinstance(pair, tuple):
                        var1, var2 = pair
                    else:
                        var1, var2 = pair.split(' vs ')
                    p_val = result.get('p_values', {}).get(pair, 1.0)
                    sig = "显著" if p_val < 0.05 else "不显著"
                    report += f"| {var1} | {var2} | {corr_val:.4f} | {sig} (P={p_val:.4f}) |\n"
        return report
    
    def _generate_generic_stat_report(self, result: Dict[str, Any], analysis_name: str) -> str:
        """生成通用统计报告"""
        report = f"### {analysis_name} 统计结果\n\n"
        report += "| 项目 | 数值 |\n"
        report += "|------|------|\n"
        
        for key, value in result.items():
            if key != "error":
                if isinstance(value, bool):
                    value_str = "是" if value else "否"
                elif isinstance(value, (int, float)):
                    value_str = f"{value:.4f}" if isinstance(value, float) else str(value)
                elif isinstance(value, (list, dict)):
                    value_str = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                else:
                    value_str = str(value)
                report += f"| {key} | {value_str} |\n"
        
        return report
    
    def _generate_conclusion(self, result: Dict[str, Any], analysis_key: str) -> str:
        """生成结论与建议"""
        conclusion = ""
        
        if analysis_key == "descriptive":
            var_name = list(result.keys())[0] if result else "变量"
            var_result = result[var_name]
            if 'mean' in var_result and 'std' in var_result:
                conclusion += f"- 变量 '{var_name}' 的均值为 {var_result['mean']:.4f}，标准差为 {var_result['std']:.4f}。\n"
                if 'skewness' in var_result:
                    skew = var_result['skewness']
                    if abs(skew) < 0.5:
                        conclusion += "- 数据分布基本对称，接近正态分布。\n"
                    else:
                        conclusion += f"- 数据分布存在偏斜（偏度={skew:.4f}），建议进行数据转换或使用非参数方法。\n"
        
        elif analysis_key in ["t_test_one", "t_test_independent", "t_test_paired"]:
            if 'p_value' in result:
                p_val = result['p_value']
                alpha = result.get('alpha', 0.05)
                if p_val < alpha:
                    conclusion += f"- 在显著性水平 α={alpha} 下，检验结果显著（P={p_val:.6f}），拒绝原假设。\n"
                    conclusion += "- 建议：存在统计学上的显著差异，需要进一步分析差异的实际意义。\n"
                else:
                    conclusion += f"- 在显著性水平 α={alpha} 下，检验结果不显著（P={p_val:.6f}），不能拒绝原假设。\n"
                    conclusion += "- 建议：没有足够的证据表明存在显著差异，但也不能完全排除差异的可能性。\n"
        
        elif analysis_key in ["regression", "stepwise_regression", "logistic_regression"]:
            if 'r_squared' in result:
                r2 = result['r_squared']
                conclusion += f"- 模型拟合优度 R² = {r2:.4f}，解释了 {r2*100:.2f}% 的数据变异。\n"
                if r2 > 0.7:
                    conclusion += "- 模型拟合效果优秀，可以用于预测。\n"
                elif r2 > 0.3:
                    conclusion += "- 模型拟合效果中等，建议考虑添加更多变量或使用其他模型。\n"
                else:
                    conclusion += "- 模型拟合效果较差，建议重新审视模型设定或数据质量。\n"
            
            if 'f_p_value' in result:
                if result['f_p_value'] < 0.05:
                    conclusion += "- 模型整体显著，具有统计学意义。\n"
                else:
                    conclusion += "- 模型整体不显著，需要重新考虑模型设定。\n"
        
        elif analysis_key == "anova":
            if 'p_value' in result:
                p_val = result['p_value']
                if p_val < 0.05:
                    conclusion += f"- 方差分析结果显著（P={p_val:.6f}），各组均值存在显著差异。\n"
                    conclusion += "- 建议：进行事后检验（如Tukey HSD）以确定具体哪些组之间存在差异。\n"
                else:
                    conclusion += f"- 方差分析结果不显著（P={p_val:.6f}），各组均值无显著差异。\n"
        
        elif analysis_key == "correlation":
            conclusion += "- 相关分析揭示了变量之间的关系强度和方向。\n"
            conclusion += "- 建议：结合散点图等可视化方法进一步理解变量关系。\n"
        
        else:
            conclusion += "- 分析已完成，请根据具体结果进行专业判断。\n"
        
        return conclusion

