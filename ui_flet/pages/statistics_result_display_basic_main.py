"""
基本统计分析结果展示 - 主方法
"""
import flet as ft
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES


class StatisticsResultDisplayBasicMainMixin:
    """基本统计分析结果展示 - 主方法"""

    def _display_result(self, result: dict, analysis_type: str):
        """显示分析结果"""
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
            # 格式化显示结果
            if analysis_type == 'descriptive':
                self._display_descriptive_result(result)
            elif analysis_type == 'correlation':
                self._display_correlation_result(result)
            elif analysis_type == 'regression':
                self._display_regression_result(result)
        
        self.btn_export.visible = True
        self.result_area.update()
        self.btn_export.update()
        
        # 确保页面更新以显示结果
        try:
            if hasattr(self.main_window, 'page'):
                self.main_window.page.update()
        except Exception:
            pass

