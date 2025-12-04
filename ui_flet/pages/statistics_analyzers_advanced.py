"""
统计分析页面 - 高级分析执行方法
"""
from ui_flet.pages.statistics_helpers import execute_analysis_with_loading, validate_data_for_analysis
from ui_flet.pages.statistics_result_display_advanced import StatisticsResultDisplayAdvancedMixin
from ui_flet.utils.message_helper import show_snackbar


class StatisticsAnalyzersAdvancedMixin(StatisticsResultDisplayAdvancedMixin):
    """高级分析执行方法Mixin"""

    def _run_pca(self, e):
        """执行主成分分析"""
        if not hasattr(self, 'pca_var_checkboxes'):
            return
        
        selected_vars = [
            row.label_text for row in self.pca_var_checkboxes.controls
            if hasattr(row, 'checkbox') and row.checkbox.value
        ]
        
        if not selected_vars:
            show_snackbar(self.main_window.page, "请至少选择一个变量", "warning")
            return
        
        n_components = None
        if hasattr(self, 'pca_n_components_field') and self.pca_n_components_field.value:
            try:
                n_components = int(self.pca_n_components_field.value)
            except ValueError:
                pass
        
        def validation_func():
            return validate_data_for_analysis(
                self.main_window.processed_data,
                "pca",
                vars=selected_vars
            )
        
        def analyzer_func():
            return self.analyzer.principal_component_analysis(
                self.main_window.processed_data,
                selected_vars,
                n_components
            )
        
        def display_func(result):
            self._display_pca_result(result)
        
        execute_analysis_with_loading(
            self.result_area,
            self.main_window.page,
            analyzer_func,
            display_func,
            success_msg="主成分分析完成",
            error_prefix="主成分分析失败",
            validation_func=validation_func
        )

    def _run_kmeans(self, e):
        """执行K-means聚类"""
        if not hasattr(self, 'kmeans_var_checkboxes'):
            return
        
        selected_vars = [
            row.label_text for row in self.kmeans_var_checkboxes.controls
            if hasattr(row, 'checkbox') and row.checkbox.value
        ]
        
        if not selected_vars:
            show_snackbar(self.main_window.page, "请至少选择一个变量", "warning")
            return
        
        n_clusters = 3
        if hasattr(self, 'kmeans_n_clusters_field') and self.kmeans_n_clusters_field.value:
            try:
                n_clusters = int(self.kmeans_n_clusters_field.value)
            except ValueError:
                pass
        
        def validation_func():
            return validate_data_for_analysis(
                self.main_window.processed_data,
                "clustering",
                vars=selected_vars,
                n_clusters=n_clusters
            )
        
        def analyzer_func():
            return self.analyzer.kmeans_clustering(
                self.main_window.processed_data,
                selected_vars,
                n_clusters
            )
        
        def display_func(result):
            self._display_kmeans_result(result)
        
        execute_analysis_with_loading(
            self.result_area,
            self.main_window.page,
            analyzer_func,
            display_func,
            success_msg="K-means聚类完成",
            error_prefix="K-means聚类失败",
            validation_func=validation_func
        )

    def _run_hierarchical_clustering(self, e):
        """执行层次聚类"""
        if not hasattr(self, 'hierarchical_var_checkboxes'):
            return
        
        selected_vars = [
            row.label_text for row in self.hierarchical_var_checkboxes.controls
            if hasattr(row, 'checkbox') and row.checkbox.value
        ]
        
        if not selected_vars:
            show_snackbar(self.main_window.page, "请至少选择一个变量", "warning")
            return
        
        n_clusters = 3
        if hasattr(self, 'hierarchical_n_clusters_field') and self.hierarchical_n_clusters_field.value:
            try:
                n_clusters = int(self.hierarchical_n_clusters_field.value)
            except ValueError:
                pass
        
        linkage = "ward"
        if hasattr(self, 'hierarchical_linkage_dropdown') and self.hierarchical_linkage_dropdown.value:
            linkage = self.hierarchical_linkage_dropdown.value
        
        def validation_func():
            return validate_data_for_analysis(
                self.main_window.processed_data,
                "clustering",
                vars=selected_vars,
                n_clusters=n_clusters
            )
        
        def analyzer_func():
            return self.analyzer.hierarchical_clustering(
                self.main_window.processed_data,
                selected_vars,
                n_clusters,
                linkage
            )
        
        def display_func(result):
            self._display_hierarchical_clustering_result(result)
        
        execute_analysis_with_loading(
            self.result_area,
            self.main_window.page,
            analyzer_func,
            display_func,
            success_msg="层次聚类完成",
            error_prefix="层次聚类失败",
            validation_func=validation_func
        )

    def _run_decision_tree(self, e):
        """执行决策树分类"""
        if not hasattr(self, 'decision_tree_y_dropdown') or not hasattr(self, 'decision_tree_x_checkboxes'):
            return
        if not self.decision_tree_y_dropdown.value:
            show_snackbar(self.main_window.page, "请选择目标变量", "warning")
            return
        
        y_var = self.decision_tree_y_dropdown.value
        x_vars = [
            row.label_text for row in self.decision_tree_x_checkboxes.controls
            if hasattr(row, 'checkbox') and row.checkbox.value
        ]
        
        if not x_vars:
            show_snackbar(self.main_window.page, "请至少选择一个特征变量", "warning")
            return
        
        max_depth = None
        if hasattr(self, 'decision_tree_max_depth_field') and self.decision_tree_max_depth_field.value:
            try:
                max_depth = int(self.decision_tree_max_depth_field.value)
            except ValueError:
                pass
        
        def validation_func():
            return validate_data_for_analysis(
                self.main_window.processed_data,
                "regression",
                y_col=y_var,
                x_cols=x_vars
            )
        
        def analyzer_func():
            return self.analyzer.decision_tree_classification(
                self.main_window.processed_data,
                y_var,
                x_vars,
                max_depth
            )
        
        def display_func(result):
            self._display_decision_tree_result(result)
        
        execute_analysis_with_loading(
            self.result_area,
            self.main_window.page,
            analyzer_func,
            display_func,
            success_msg="决策树分类完成",
            error_prefix="决策树分类失败",
            validation_func=validation_func
        )

    def _run_factor_analysis(self, e):
        """执行因子分析"""
        if not hasattr(self, 'factor_var_checkboxes'):
            return
        
        selected_vars = [
            row.label_text for row in self.factor_var_checkboxes.controls
            if hasattr(row, 'checkbox') and row.checkbox.value
        ]
        
        if not selected_vars:
            show_snackbar(self.main_window.page, "请至少选择一个变量", "warning")
            return
        
        n_factors = None
        if hasattr(self, 'factor_n_factors_field') and self.factor_n_factors_field.value:
            try:
                n_factors = int(self.factor_n_factors_field.value)
            except ValueError:
                pass
        
        def validation_func():
            return validate_data_for_analysis(
                self.main_window.processed_data,
                "pca",
                vars=selected_vars
            )
        
        def analyzer_func():
            return self.analyzer.factor_analysis(
                self.main_window.processed_data,
                selected_vars,
                n_factors
            )
        
        def display_func(result):
            self._display_factor_analysis_result(result)
        
        execute_analysis_with_loading(
            self.result_area,
            self.main_window.page,
            analyzer_func,
            display_func,
            success_msg="因子分析完成",
            error_prefix="因子分析失败",
            validation_func=validation_func
        )

    def _run_discriminant_analysis(self, e):
        """执行判别分析"""
        if not hasattr(self, 'discriminant_y_dropdown') or not hasattr(self, 'discriminant_x_checkboxes'):
            return
        if not self.discriminant_y_dropdown.value:
            show_snackbar(self.main_window.page, "请选择目标变量", "warning")
            return
        
        y_var = self.discriminant_y_dropdown.value
        x_vars = [
            row.label_text for row in self.discriminant_x_checkboxes.controls
            if hasattr(row, 'checkbox') and row.checkbox.value
        ]
        
        if not x_vars:
            show_snackbar(self.main_window.page, "请至少选择一个特征变量", "warning")
            return
        
        def validation_func():
            return validate_data_for_analysis(
                self.main_window.processed_data,
                "discriminant",
                target_col=y_var,
                feature_cols=x_vars
            )
        
        def analyzer_func():
            # 使用线性判别分析
            return self.analyzer.linear_discriminant_analysis(
                self.main_window.processed_data,
                y_var,
                x_vars
            )
        
        def display_func(result):
            self._display_discriminant_analysis_result(result)
        
        execute_analysis_with_loading(
            self.result_area,
            self.main_window.page,
            analyzer_func,
            display_func,
            success_msg="判别分析完成",
            error_prefix="判别分析失败",
            validation_func=validation_func
        )

