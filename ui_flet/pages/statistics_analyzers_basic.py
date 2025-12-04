"""
统计分析页面 - 基本分析执行方法
"""
from ui_flet.pages.statistics_helpers import execute_analysis_with_loading
from ui_flet.pages.statistics_result_display_basic import StatisticsResultDisplayBasicMixin


class StatisticsAnalyzersBasicMixin(StatisticsResultDisplayBasicMixin):
    """基本分析执行方法Mixin"""

    def _run_descriptive_analysis(self, e):
        """执行描述性统计分析"""
        if not hasattr(self, 'var_dropdown') or not self.var_dropdown.value:
            return
        
        selected_var = self.var_dropdown.value
        
        def analyzer_func():
            return self.analyzer.descriptive_statistics(
                self.main_window.processed_data,
                [selected_var]
            )
        
        def display_func(result):
            self._display_descriptive_result(result)
        
        execute_analysis_with_loading(
            self.result_area,
            self.main_window.page,
            analyzer_func,
            display_func,
            success_msg="描述性统计分析完成",
            error_prefix="描述性统计分析失败"
        )

    def _run_frequency_analysis(self, e):
        """执行频数分析"""
        if not hasattr(self, 'var_dropdown') or not self.var_dropdown.value:
            return
        
        selected_var = self.var_dropdown.value
        
        def analyzer_func():
            return self.analyzer.frequency_analysis(
                self.main_window.processed_data,
                [selected_var]
            )
        
        def display_func(result):
            self._display_frequency_result(result)
        
        execute_analysis_with_loading(
            self.result_area,
            self.main_window.page,
            analyzer_func,
            display_func,
            success_msg="频数分析完成",
            error_prefix="频数分析失败"
        )

    def _run_crosstab_analysis(self, e):
        """执行交叉表分析"""
        if not hasattr(self, 'row_dropdown') or not hasattr(self, 'col_dropdown'):
            return
        if not self.row_dropdown.value or not self.col_dropdown.value:
            return
        
        row_var = self.row_dropdown.value
        col_var = self.col_dropdown.value
        
        def analyzer_func():
            import pandas as pd
            result = self.analyzer.crosstab_analysis(
                self.main_window.processed_data,
                row_var,
                col_var
            )
            # 将结果转换为DataFrame格式
            if 'crosstab' in result and isinstance(result['crosstab'], dict):
                result['crosstab'] = pd.DataFrame(result['crosstab'])
            return result
        
        def display_func(result):
            self._display_crosstab_result(result)
        
        execute_analysis_with_loading(
            self.result_area,
            self.main_window.page,
            analyzer_func,
            display_func,
            success_msg="交叉表分析完成",
            error_prefix="交叉表分析失败"
        )

