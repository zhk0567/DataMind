"""
统计分析页面 - 相关分析执行方法
"""
from ui_flet.pages.statistics_helpers import execute_analysis_with_loading, validate_data_for_analysis
from ui_flet.pages.statistics_result_display_correlation import StatisticsResultDisplayCorrelationMixin
from ui_flet.utils.message_helper import show_snackbar


class StatisticsAnalyzersCorrelationMixin(StatisticsResultDisplayCorrelationMixin):
    """相关分析执行方法Mixin"""

    def _run_correlation_analysis(self, e):
        """执行相关分析"""
        if not hasattr(self, 'correlation_var_checkboxes'):
            return
        
        selected_vars = [
            row.label_text for row in self.correlation_var_checkboxes.controls
            if hasattr(row, 'checkbox') and row.checkbox.value
        ]
        
        if not selected_vars:
            show_snackbar(self.main_window.page, "请至少选择一个变量", "warning")
            return
        
        method = "pearson"
        if hasattr(self, 'correlation_method_dropdown') and self.correlation_method_dropdown.value:
            method = self.correlation_method_dropdown.value
        
        def validation_func():
            return validate_data_for_analysis(
                self.main_window.processed_data,
                "correlation",
                vars=selected_vars
            )
        
        def analyzer_func():
            return self.analyzer.correlation_analysis(
                self.main_window.processed_data,
                selected_vars,
                method
            )
        
        def display_func(result):
            self._display_correlation_result(result)
        
        execute_analysis_with_loading(
            self.result_area,
            self.main_window.page,
            analyzer_func,
            display_func,
            success_msg="相关分析完成",
            error_prefix="相关分析失败",
            validation_func=validation_func
        )

    def _run_partial_correlation(self, e):
        """执行偏相关分析"""
        if not hasattr(self, 'partial_x_dropdown') or not hasattr(self, 'partial_y_dropdown'):
            return
        if not self.partial_x_dropdown.value or not self.partial_y_dropdown.value:
            show_snackbar(self.main_window.page, "请选择X变量和Y变量", "warning")
            return
        
        x_var = self.partial_x_dropdown.value
        y_var = self.partial_y_dropdown.value
        
        control_vars = []
        if hasattr(self, 'partial_control_checkboxes'):
            control_vars = [
                row.label_text for row in self.partial_control_checkboxes.controls
                if hasattr(row, 'checkbox') and row.checkbox.value
            ]
        
        def validation_func():
            vars_list = [x_var, y_var] + control_vars
            return validate_data_for_analysis(
                self.main_window.processed_data,
                "correlation",
                vars=vars_list
            )
        
        def analyzer_func():
            return self.analyzer.partial_correlation(
                self.main_window.processed_data,
                x_var,
                y_var,
                control_vars
            )
        
        def display_func(result):
            self._display_partial_correlation_result(result)
        
        execute_analysis_with_loading(
            self.result_area,
            self.main_window.page,
            analyzer_func,
            display_func,
            success_msg="偏相关分析完成",
            error_prefix="偏相关分析失败",
            validation_func=validation_func
        )

    def _run_regression_analysis(self, e):
        """执行回归分析"""
        if not hasattr(self, 'regression_y_dropdown') or not hasattr(self, 'regression_x_checkboxes'):
            return
        if not self.regression_y_dropdown.value:
            show_snackbar(self.main_window.page, "请选择因变量", "warning")
            return
        
        y_var = self.regression_y_dropdown.value
        x_vars = [
            row.label_text for row in self.regression_x_checkboxes.controls
            if hasattr(row, 'checkbox') and row.checkbox.value
        ]
        
        if not x_vars:
            show_snackbar(self.main_window.page, "请至少选择一个自变量", "warning")
            return
        
        def validation_func():
            return validate_data_for_analysis(
                self.main_window.processed_data,
                "regression",
                y_col=y_var,
                x_cols=x_vars
            )
        
        def analyzer_func():
            return self.analyzer.regression_analysis(
                self.main_window.processed_data,
                [y_var] + x_vars,
                {}
            )
        
        def display_func(result):
            self._display_regression_result(result)
        
        execute_analysis_with_loading(
            self.result_area,
            self.main_window.page,
            analyzer_func,
            display_func,
            success_msg="回归分析完成",
            error_prefix="回归分析失败",
            validation_func=validation_func
        )

    def _run_stepwise_regression(self, e):
        """执行逐步回归分析"""
        if not hasattr(self, 'stepwise_y_dropdown') or not hasattr(self, 'stepwise_x_checkboxes'):
            return
        if not self.stepwise_y_dropdown.value:
            show_snackbar(self.main_window.page, "请选择因变量", "warning")
            return
        
        y_var = self.stepwise_y_dropdown.value
        x_vars = [
            row.label_text for row in self.stepwise_x_checkboxes.controls
            if hasattr(row, 'checkbox') and row.checkbox.value
        ]
        
        if not x_vars:
            show_snackbar(self.main_window.page, "请至少选择一个自变量", "warning")
            return
        
        direction = "forward"
        if hasattr(self, 'stepwise_direction_dropdown') and self.stepwise_direction_dropdown.value:
            direction = self.stepwise_direction_dropdown.value
        
        def validation_func():
            return validate_data_for_analysis(
                self.main_window.processed_data,
                "regression",
                y_col=y_var,
                x_cols=x_vars
            )
        
        def analyzer_func():
            return self.analyzer.stepwise_regression(
                self.main_window.processed_data,
                y_var,
                x_vars,
                direction
            )
        
        def display_func(result):
            self._display_regression_result(result)
        
        execute_analysis_with_loading(
            self.result_area,
            self.main_window.page,
            analyzer_func,
            display_func,
            success_msg="逐步回归分析完成",
            error_prefix="逐步回归分析失败",
            validation_func=validation_func
        )

    def _run_logistic_regression(self, e):
        """执行逻辑回归分析"""
        if not hasattr(self, 'logistic_y_dropdown') or not hasattr(self, 'logistic_x_checkboxes'):
            return
        if not self.logistic_y_dropdown.value:
            show_snackbar(self.main_window.page, "请选择因变量", "warning")
            return
        
        y_var = self.logistic_y_dropdown.value
        x_vars = [
            row.label_text for row in self.logistic_x_checkboxes.controls
            if hasattr(row, 'checkbox') and row.checkbox.value
        ]
        
        if not x_vars:
            show_snackbar(self.main_window.page, "请至少选择一个自变量", "warning")
            return
        
        def validation_func():
            return validate_data_for_analysis(
                self.main_window.processed_data,
                "regression",
                y_col=y_var,
                x_cols=x_vars
            )
        
        def analyzer_func():
            return self.analyzer.logistic_regression(
                self.main_window.processed_data,
                y_var,
                x_vars
            )
        
        def display_func(result):
            self._display_logistic_regression_result(result)
        
        execute_analysis_with_loading(
            self.result_area,
            self.main_window.page,
            analyzer_func,
            display_func,
            success_msg="逻辑回归分析完成",
            error_prefix="逻辑回归分析失败",
            validation_func=validation_func
        )

