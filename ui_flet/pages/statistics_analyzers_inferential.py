"""
统计分析页面 - 推断分析执行方法
"""
from ui_flet.pages.statistics_helpers import execute_analysis_with_loading, validate_data_for_analysis
from ui_flet.pages.statistics_result_display_inferential import StatisticsResultDisplayInferentialMixin


class StatisticsAnalyzersInferentialMixin(StatisticsResultDisplayInferentialMixin):
    """推断分析执行方法Mixin"""

    def _run_t_test_one(self, e):
        """执行单样本t检验"""
        if not hasattr(self, 'var_dropdown') or not self.var_dropdown.value:
            return
        if not hasattr(self, 'test_value_field'):
            return
        
        selected_var = self.var_dropdown.value
        try:
            test_value = float(self.test_value_field.value or 0)
        except ValueError:
            show_snackbar(self.main_window.page, "检验值必须是数字", "warning")
            return
        
        def validation_func():
            df = self.main_window.processed_data
            if df is None or df.empty:
                return False, "数据为空，无法进行分析"
            valid_data = df[selected_var].dropna()
            if len(valid_data) < 2:
                return False, f"单样本t检验需要至少2个有效样本，但只有{len(valid_data)}个"
            return True, None
        
        def analyzer_func():
            return self.analyzer.t_test_one_sample(
                self.main_window.processed_data,
                selected_var,
                test_value
            )
        
        def display_func(result):
            self._display_t_test_result(result, "单样本t检验")
        
        execute_analysis_with_loading(
            self.result_area,
            self.main_window.page,
            analyzer_func,
            display_func,
            success_msg="单样本t检验完成",
            error_prefix="单样本t检验失败",
            validation_func=validation_func
        )

    def _run_t_test_independent(self, e):
        """执行独立样本t检验"""
        if not hasattr(self, 'group_dropdown') or not hasattr(self, 'value_dropdown'):
            return
        if not self.group_dropdown.value or not self.value_dropdown.value:
            show_snackbar(self.main_window.page, "请选择分组变量和数值变量", "warning")
            return
        
        group_var = self.group_dropdown.value
        value_var = self.value_dropdown.value
        
        def validation_func():
            return validate_data_for_analysis(
                self.main_window.processed_data,
                "t_test_independent",
                group_col=group_var,
                value_col=value_var
            )
        
        def analyzer_func():
            return self.analyzer.t_test_independent(
                self.main_window.processed_data,
                group_var,
                value_var
            )
        
        def display_func(result):
            self._display_t_test_result(result, "独立样本t检验")
        
        execute_analysis_with_loading(
            self.result_area,
            self.main_window.page,
            analyzer_func,
            display_func,
            success_msg="独立样本t检验完成",
            error_prefix="独立样本t检验失败",
            validation_func=validation_func
        )

    def _run_t_test_paired(self, e):
        """执行配对样本t检验"""
        if not hasattr(self, 'paired_col1_dropdown') or not hasattr(self, 'paired_col2_dropdown'):
            return
        if not self.paired_col1_dropdown.value or not self.paired_col2_dropdown.value:
            show_snackbar(self.main_window.page, "请选择两个配对变量", "warning")
            return
        
        col1 = self.paired_col1_dropdown.value
        col2 = self.paired_col2_dropdown.value
        
        def validation_func():
            return validate_data_for_analysis(
                self.main_window.processed_data,
                "t_test_paired",
                col1=col1,
                col2=col2
            )
        
        def analyzer_func():
            return self.analyzer.t_test_paired(
                self.main_window.processed_data,
                col1,
                col2
            )
        
        def display_func(result):
            self._display_t_test_result(result, "配对样本t检验")
        
        execute_analysis_with_loading(
            self.result_area,
            self.main_window.page,
            analyzer_func,
            display_func,
            success_msg="配对样本t检验完成",
            error_prefix="配对样本t检验失败",
            validation_func=validation_func
        )

    def _run_chi_square(self, e):
        """执行卡方检验"""
        if not hasattr(self, 'chi_col1_dropdown') or not hasattr(self, 'chi_col2_dropdown'):
            return
        if not self.chi_col1_dropdown.value or not self.chi_col2_dropdown.value:
            show_snackbar(self.main_window.page, "请选择两个分类变量", "warning")
            return
        
        col1 = self.chi_col1_dropdown.value
        col2 = self.chi_col2_dropdown.value
        
        def validation_func():
            return validate_data_for_analysis(
                self.main_window.processed_data,
                "chi_square",
                col1=col1,
                col2=col2
            )
        
        def analyzer_func():
            return self.analyzer.chi_square_test(
                self.main_window.processed_data,
                col1,
                col2
            )
        
        def display_func(result):
            self._display_chi_square_result(result)
        
        execute_analysis_with_loading(
            self.result_area,
            self.main_window.page,
            analyzer_func,
            display_func,
            success_msg="卡方检验完成",
            error_prefix="卡方检验失败",
            validation_func=validation_func
        )

    def _run_anova(self, e):
        """执行方差分析"""
        if not hasattr(self, 'anova_group_dropdown') or not hasattr(self, 'anova_value_dropdown'):
            return
        if not self.anova_group_dropdown.value or not self.anova_value_dropdown.value:
            show_snackbar(self.main_window.page, "请选择分组变量和数值变量", "warning")
            return
        
        group_var = self.anova_group_dropdown.value
        value_var = self.anova_value_dropdown.value
        
        def validation_func():
            return validate_data_for_analysis(
                self.main_window.processed_data,
                "anova",
                group_col=group_var,
                value_col=value_var
            )
        
        def analyzer_func():
            return self.analyzer.anova_analysis(
                self.main_window.processed_data,
                [group_var, value_var],
                {}
            )
        
        def display_func(result):
            self._display_anova_result(result)
        
        execute_analysis_with_loading(
            self.result_area,
            self.main_window.page,
            analyzer_func,
            display_func,
            success_msg="方差分析完成",
            error_prefix="方差分析失败",
            validation_func=validation_func
        )

    def _run_mann_whitney(self, e):
        """执行Mann-Whitney检验"""
        if not hasattr(self, 'mw_group_dropdown') or not hasattr(self, 'mw_value_dropdown'):
            return
        if not self.mw_group_dropdown.value or not self.mw_value_dropdown.value:
            show_snackbar(self.main_window.page, "请选择分组变量和数值变量", "warning")
            return
        
        group_var = self.mw_group_dropdown.value
        value_var = self.mw_value_dropdown.value
        
        def validation_func():
            return validate_data_for_analysis(
                self.main_window.processed_data,
                "t_test_independent",
                group_col=group_var,
                value_col=value_var
            )
        
        def analyzer_func():
            return self.analyzer.mann_whitney_test(
                self.main_window.processed_data,
                group_var,
                value_var
            )
        
        def display_func(result):
            self._display_mann_whitney_result(result)
        
        execute_analysis_with_loading(
            self.result_area,
            self.main_window.page,
            analyzer_func,
            display_func,
            success_msg="Mann-Whitney检验完成",
            error_prefix="Mann-Whitney检验失败",
            validation_func=validation_func
        )

    def _run_kruskal_wallis(self, e):
        """执行Kruskal-Wallis检验"""
        if not hasattr(self, 'kw_group_dropdown') or not hasattr(self, 'kw_value_dropdown'):
            return
        if not self.kw_group_dropdown.value or not self.kw_value_dropdown.value:
            show_snackbar(self.main_window.page, "请选择分组变量和数值变量", "warning")
            return
        
        group_var = self.kw_group_dropdown.value
        value_var = self.kw_value_dropdown.value
        
        def validation_func():
            return validate_data_for_analysis(
                self.main_window.processed_data,
                "anova",
                group_col=group_var,
                value_col=value_var
            )
        
        def analyzer_func():
            return self.analyzer.kruskal_wallis_test(
                self.main_window.processed_data,
                group_var,
                value_var
            )
        
        def display_func(result):
            self._display_kruskal_wallis_result(result)
        
        execute_analysis_with_loading(
            self.result_area,
            self.main_window.page,
            analyzer_func,
            display_func,
            success_msg="Kruskal-Wallis检验完成",
            error_prefix="Kruskal-Wallis检验失败",
            validation_func=validation_func
        )

