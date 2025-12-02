"""
结果解释器
为统计分析结果生成中文解释文本
"""
from typing import Dict, Any


class ResultInterpreter:
    """结果解释器"""
    
    @staticmethod
    def interpret_descriptive_stats(result: Dict[str, Any], var_name: str) -> str:
        """解释描述性统计结果"""
        interpretation = f"变量 '{var_name}' 的描述性统计结果：\n\n"
        
        if 'mean' in result and 'std' in result:
            mean = result['mean']
            std = result['std']
            interpretation += f"• 均值：{mean:.4f}，表示数据的平均水平。\n"
            interpretation += f"• 标准差：{std:.4f}，表示数据的离散程度。\n"
            
            if mean != 0:
                cv = std / abs(mean)
                if cv < 0.1:
                    interpretation += "• 变异系数较小，数据相对集中。\n"
                elif cv > 0.5:
                    interpretation += "• 变异系数较大，数据离散程度较高。\n"
        
        if 'skewness' in result:
            skew = result['skewness']
            if abs(skew) < 0.5:
                interpretation += "• 偏度接近0，数据分布基本对称。\n"
            elif skew > 0:
                interpretation += "• 偏度为正，数据右偏（尾部在右侧）。\n"
            else:
                interpretation += "• 偏度为负，数据左偏（尾部在左侧）。\n"
        
        if 'kurtosis' in result:
            kurt = result['kurtosis']
            if abs(kurt) < 0.5:
                interpretation += "• 峰度接近0，数据分布接近正态分布。\n"
            elif kurt > 0:
                interpretation += "• 峰度为正，数据分布较尖（尾部较厚）。\n"
            else:
                interpretation += "• 峰度为负，数据分布较平（尾部较薄）。\n"
        
        return interpretation
    
    @staticmethod
    def interpret_t_test(result: Dict[str, Any], test_type: str) -> str:
        """解释t检验结果"""
        interpretation = f"{test_type}检验结果：\n\n"
        
        if 'p_value' in result:
            p_val = result['p_value']
            alpha = result.get('alpha', 0.05)
            
            if p_val < alpha:
                interpretation += f"• 在显著性水平 α={alpha} 下，P值 = {p_val:.6f} < {alpha}，拒绝原假设。\n"
                interpretation += "• 结论：存在统计学上的显著差异。\n"
            else:
                interpretation += f"• 在显著性水平 α={alpha} 下，P值 = {p_val:.6f} ≥ {alpha}，不能拒绝原假设。\n"
                interpretation += "• 结论：没有足够的证据表明存在显著差异。\n"
        
        if 'effect_size' in result:
            effect = result['effect_size']
            interpretation += f"• 效应量：{effect:.4f}，"
            if abs(effect) < 0.2:
                interpretation += "属于小效应。\n"
            elif abs(effect) < 0.5:
                interpretation += "属于中等效应。\n"
            elif abs(effect) < 0.8:
                interpretation += "属于大效应。\n"
            else:
                interpretation += "属于很大效应。\n"
        
        return interpretation
    
    @staticmethod
    def interpret_correlation(result: Dict[str, Any]) -> str:
        """解释相关分析结果"""
        interpretation = "相关分析结果：\n\n"
        
        if 'correlation_matrix' in result:
            corr_matrix = result['correlation_matrix']
            if isinstance(corr_matrix, dict):
                for pair, corr_val in corr_matrix.items():
                    if isinstance(pair, tuple):
                        var1, var2 = pair
                    else:
                        var1, var2 = pair.split(' vs ')
                    
                    interpretation += f"• {var1} 与 {var2} 的相关系数：{corr_val:.4f}，"
                    
                    abs_corr = abs(corr_val)
                    if abs_corr < 0.1:
                        interpretation += "几乎无相关。\n"
                    elif abs_corr < 0.3:
                        interpretation += "弱相关。\n"
                    elif abs_corr < 0.5:
                        interpretation += "中等相关。\n"
                    elif abs_corr < 0.7:
                        interpretation += "强相关。\n"
                    else:
                        interpretation += "很强相关。\n"
                    
                    if corr_val > 0:
                        interpretation += "  方向：正相关（同向变化）。\n"
                    else:
                        interpretation += "  方向：负相关（反向变化）。\n"
        
        return interpretation
    
    @staticmethod
    def interpret_regression(result: Dict[str, Any]) -> str:
        """解释回归分析结果"""
        interpretation = "回归分析结果：\n\n"
        
        if 'r_squared' in result:
            r2 = result['r_squared']
            interpretation += f"• 决定系数 R² = {r2:.4f}，表示模型解释了 {r2*100:.2f}% 的数据变异。\n"
            
            if r2 > 0.7:
                interpretation += "  模型拟合优度：优秀。\n"
            elif r2 > 0.5:
                interpretation += "  模型拟合优度：良好。\n"
            elif r2 > 0.3:
                interpretation += "  模型拟合优度：中等。\n"
            else:
                interpretation += "  模型拟合优度：较差。\n"
        
        if 'coefficients' in result:
            interpretation += "\n• 回归系数：\n"
            coefs = result['coefficients']
            if isinstance(coefs, dict):
                for var, coef_info in coefs.items():
                    if isinstance(coef_info, dict):
                        coef = coef_info.get('coefficient', coef_info.get('coef', 0))
                        p_val = coef_info.get('p_value', coef_info.get('p', 1))
                        sig = "显著" if p_val < 0.05 else "不显著"
                        interpretation += f"  - {var}: 系数 = {coef:.4f} ({sig}, P = {p_val:.6f})\n"
                    else:
                        interpretation += f"  - {var}: 系数 = {coef_info:.4f}\n"
        
        if 'f_p_value' in result:
            f_p = result['f_p_value']
            if f_p < 0.05:
                interpretation += "\n• 模型整体显著性检验：显著（F检验P < 0.05），模型有效。\n"
            else:
                interpretation += "\n• 模型整体显著性检验：不显著（F检验P ≥ 0.05），模型可能无效。\n"
        
        return interpretation
    
    @staticmethod
    def interpret_anova(result: Dict[str, Any]) -> str:
        """解释方差分析结果"""
        interpretation = "方差分析（ANOVA）结果：\n\n"
        
        if 'f_statistic' in result and 'p_value' in result:
            f_stat = result['f_statistic']
            p_val = result['p_value']
            
            interpretation += f"• F统计量：{f_stat:.4f}\n"
            interpretation += f"• P值：{p_val:.6f}\n"
            
            if p_val < 0.05:
                interpretation += "• 结论：在显著性水平 α=0.05 下，各组均值存在显著差异。\n"
                interpretation += "  至少有一组的均值与其他组不同。\n"
            else:
                interpretation += "• 结论：在显著性水平 α=0.05 下，各组均值无显著差异。\n"
                interpretation += "  没有足够的证据表明组间存在差异。\n"
        
        if 'effect_size' in result:
            eta_sq = result['effect_size']
            interpretation += f"• 效应量（η²）：{eta_sq:.4f}，"
            if eta_sq < 0.01:
                interpretation += "小效应。\n"
            elif eta_sq < 0.06:
                interpretation += "中等效应。\n"
            else:
                interpretation += "大效应。\n"
        
        return interpretation

