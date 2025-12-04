"""
相关分析结果展示 - 偏相关分析
"""
import flet as ft
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES


class StatisticsResultDisplayCorrelationPartialMixin:
    """相关分析结果展示 - 偏相关分析"""

    def _display_partial_correlation_result(self, result):
        """显示偏相关分析结果"""
        self.result_area.controls.clear()
        
        if 'error' in result:
            self.result_area.controls.append(
                ft.Text(
                    f"错误: {result['error']}",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['error']
                )
            )
        else:
            corr_value = result.get('partial_correlation', 0)
            p_value = result.get('p_value', 0)
            
            self.result_area.controls.append(
                ft.Text(
                    f"偏相关系数: {corr_value:.4f}",
                    size=FONT_SIZES['md'],
                    weight=ft.FontWeight.BOLD
                )
            )
            self.result_area.controls.append(
                ft.Text(
                    f"p值 {p_value:.4f}",
                    size=FONT_SIZES['md']
                )
            )
        
        self.btn_export.visible = True
        self.result_area.update()
        self.btn_export.update()
        
        # 确保页面更新以显示结果
        try:
            if hasattr(self.main_window, 'page'):
                self.main_window.page.update()
        except Exception:
            pass

