"""
统计分析页面辅助函数
提取公共方法和工具函数
"""
import flet as ft
import pandas as pd
from ui_flet.components.fluent_components import FluentButton, FluentDropdown, FluentTextField
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, COMPONENT_SIZES
from ui_flet.utils.message_helper import show_snackbar


def create_loading_indicator():
    """创建加载指示器"""
    return ft.Row(
        controls=[
            ft.ProgressRing(width=40, height=40),
            ft.Text("正在分析...", size=FONT_SIZES['md'], color=FLUENT_COLORS['text_secondary'])
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=SPACING['md'],
    )


def show_loading(result_area):
    """显示加载状态"""
    result_area.controls.clear()
    result_area.controls.append(create_loading_indicator())
    result_area.update()


def create_data_table(headers, rows, title=None):
    """创建数据表格"""
    controls = []
    if title:
        controls.append(
            ft.Text(
                title,
                size=FONT_SIZES['lg'],
                weight=ft.FontWeight.BOLD
            )
        )
        controls.append(ft.Container(height=SPACING['md']))
    
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text(header, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD, color=FLUENT_COLORS['text_primary']))
            for header in headers
        ],
        rows=rows,
        border=ft.border.all(1, FLUENT_COLORS['border']),
        border_radius=COMPONENT_SIZES['input_border_radius'],
        bgcolor=FLUENT_COLORS['bg_card'],
        heading_row_color=FLUENT_COLORS['bg_tertiary'],
        data_row_color={ft.ControlState.DEFAULT: FLUENT_COLORS['bg_card']},
    )
    controls.append(table)
    return controls


def create_stats_table(stats_data, title=None):
    """创建统计量表"""
    rows = [
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(key, size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
                ft.DataCell(ft.Text(f"{val:.4f}" if isinstance(val, (int, float)) else str(val), size=FONT_SIZES['sm'], color=FLUENT_COLORS['text_primary'])),
            ],
            color=FLUENT_COLORS['bg_card']
        )
        for key, val in stats_data
    ]
    return create_data_table(["统计量", "值"], rows, title)


def validate_data_for_analysis(df, analysis_type, **kwargs):
    """
    验证数据是否满足分析要求
    
    Args:
        df: 数据框
        analysis_type: 分析类型
        **kwargs: 其他参数（如变量列表、组别等）
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if df is None or df.empty:
        return False, "数据为空，无法进行分析"
    
    if analysis_type == "anova":
        # 方差分析：需要至少一个组有多个样本
        group_col = kwargs.get('group_col')
        value_col = kwargs.get('value_col')
        if group_col and value_col:
            groups = df[group_col].unique()
            for group in groups:
                group_data = df[df[group_col] == group][value_col].dropna()
                if len(group_data) <= 1:
                    return False, f"方差分析要求每个组至少有2个样本，但'{group}'组只有{len(group_data)}个样本"
    
    elif analysis_type == "discriminant":
        # 判别分析：样本数必须大于类别数
        target_col = kwargs.get('target_col')
        feature_cols = kwargs.get('feature_cols', [])
        if target_col:
            unique_classes = df[target_col].nunique()
            sample_count = len(df.dropna(subset=[target_col] + feature_cols))
            if sample_count <= unique_classes:
                return False, f"判别分析要求样本数({sample_count})必须大于类别数({unique_classes})"
    
    elif analysis_type == "regression":
        # 回归分析：需要足够的样本
        y_col = kwargs.get('y_col')
        x_cols = kwargs.get('x_cols', [])
        if y_col and x_cols:
            valid_data = df[[y_col] + x_cols].dropna()
            if len(valid_data) < len(x_cols) + 1:
                return False, f"回归分析需要至少{len(x_cols) + 1}个有效样本，但只有{len(valid_data)}个"
    
    elif analysis_type == "correlation":
        # 相关分析：需要至少2个变量，每个变量至少2个样本
        vars_list = kwargs.get('vars', [])
        if len(vars_list) < 2:
            return False, "相关分析需要至少选择2个变量"
        for var in vars_list:
            valid_count = df[var].dropna().count()
            if valid_count < 2:
                return False, f"变量'{var}'的有效样本数({valid_count})不足，至少需要2个"
    
    elif analysis_type == "pca":
        # 主成分分析：需要至少2个变量，每个变量至少2个样本
        vars_list = kwargs.get('vars', [])
        if len(vars_list) < 2:
            return False, "主成分分析需要至少选择2个变量"
        for var in vars_list:
            valid_count = df[var].dropna().count()
            if valid_count < 2:
                return False, f"变量'{var}'的有效样本数({valid_count})不足，至少需要2个"
    
    elif analysis_type == "clustering":
        # 聚类分析：需要足够的样本
        vars_list = kwargs.get('vars', [])
        n_clusters = kwargs.get('n_clusters', 3)
        if len(vars_list) < 1:
            return False, "聚类分析需要至少选择1个变量"
        valid_data = df[vars_list].dropna()
        if len(valid_data) < n_clusters:
            return False, f"聚类分析需要至少{n_clusters}个有效样本，但只有{len(valid_data)}个"
    
    elif analysis_type == "t_test_independent":
        # 独立样本t检验：每组至少2个样本
        group_col = kwargs.get('group_col')
        value_col = kwargs.get('value_col')
        if group_col and value_col:
            groups = df[group_col].unique()
            if len(groups) != 2:
                return False, f"独立样本t检验需要恰好2个组，但找到{len(groups)}个组"
            for group in groups:
                group_data = df[df[group_col] == group][value_col].dropna()
                if len(group_data) < 2:
                    return False, f"独立样本t检验要求每个组至少有2个样本，但'{group}'组只有{len(group_data)}个样本"
    
    elif analysis_type == "t_test_paired":
        # 配对样本t检验：需要至少2对数据
        col1 = kwargs.get('col1')
        col2 = kwargs.get('col2')
        if col1 and col2:
            valid_pairs = df[[col1, col2]].dropna()
            if len(valid_pairs) < 2:
                return False, f"配对样本t检验需要至少2对有效数据，但只有{len(valid_pairs)}对"
    
    elif analysis_type == "chi_square":
        # 卡方检验：需要足够的样本
        col1 = kwargs.get('col1')
        col2 = kwargs.get('col2')
        if col1 and col2:
            valid_data = df[[col1, col2]].dropna()
            if len(valid_data) < 2:
                return False, f"卡方检验需要至少2个有效样本，但只有{len(valid_data)}个"
    
    return True, None


def execute_analysis_with_loading(
    result_area,
    page,
    analyzer_func,
    display_func,
    success_msg="分析完成",
    error_prefix="分析失败",
    validation_func=None
):
    """
    执行分析的通用模板方法 - 统一处理加载、执行、显示和错误处理
    
    Args:
        result_area: 结果显示区域控件
        page: Flet Page对象
        analyzer_func: 分析函数，返回分析结果
        display_func: 显示结果的函数，接收result作为参数
        success_msg: 成功消息
        error_prefix: 错误消息前缀
        validation_func: 可选的验证函数，返回(is_valid, error_message)
    
    Returns:
        bool: 是否执行成功
    """
    # 数据验证
    if validation_func:
        is_valid, error_msg = validation_func()
        if not is_valid:
            result_area.controls.clear()
            result_area.controls.append(
                ft.Text(
                    f"⚠️ {error_msg}",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['warning']
                )
            )
            result_area.update()
            show_snackbar(page, error_msg, "warning", duration=5000)
            return False
    
    # 显示加载状态
    show_loading(result_area)
    
    try:
        # 执行分析
        result = analyzer_func()
        
        # 检查结果中是否有错误
        if isinstance(result, dict) and 'error' in result:
            error_msg = f"{error_prefix}: {result['error']}"
            result_area.controls.clear()
            result_area.controls.append(
                ft.Text(
                    f"❌ {error_msg}",
                    size=FONT_SIZES['md'],
                    color=FLUENT_COLORS['error']
                )
            )
            result_area.update()
            show_snackbar(page, error_msg, "error", duration=5000)
            return False
        
        # 显示结果
        display_func(result)
        
        # 显示成功消息
        show_snackbar(page, success_msg, "success")
        return True
        
    except Exception as ex:
        # 显示错误
        error_msg = f"{error_prefix}: {str(ex)}"
        result_area.controls.clear()
        result_area.controls.append(
            ft.Text(
                f"❌ {error_msg}",
                size=FONT_SIZES['md'],
                color=FLUENT_COLORS['error']
            )
        )
        result_area.update()
        show_snackbar(page, error_msg, "error", duration=5000)
        return False


def create_variable_dropdown(
    label: str,
    options: list,
    default_value=None,
    width: int = 380,
    on_change=None
) -> FluentDropdown:
    """
    创建变量选择下拉框 - 统一的UI控件创建方法
    
    Args:
        label: 标签文本
        options: 选项列表（字符串列表或ft.dropdown.Option列表）
        default_value: 默认值
        width: 宽度
        on_change: 值改变回调函数
    
    Returns:
        FluentDropdown: 配置好的下拉框组件
    """
    if options and isinstance(options[0], str):
        dropdown_options = [ft.dropdown.Option(opt) for opt in options]
    else:
        dropdown_options = options
    
    return FluentDropdown(
        label=label,
        options=dropdown_options,
        value=default_value or (options[0] if options else None),
        width=width,
        on_change=on_change
    )


def create_analyze_button(
    text: str = "开始分析",
    on_click=None,
    width: int = 380
) -> FluentButton:
    """
    创建分析按钮 - 统一的UI控件创建方法
    
    Args:
        text: 按钮文本
        on_click: 点击回调函数
        width: 宽度
    
    Returns:
        FluentButton: 配置好的按钮组件
    """
    return FluentButton(
        text=text,
        on_click=on_click,
        bg_color=FLUENT_COLORS['primary'],
        width=width
    )


def create_checkbox_with_label(label_text: str, value: bool = False) -> ft.Row:
    """
    创建带颜色标签的复选框 - 确保标签文字清晰可见
    
    Args:
        label_text: 标签文本
        value: 默认是否选中
    
    Returns:
        ft.Row: 包含复选框和标签的行组件
    """
    checkbox = ft.Checkbox(value=value)
    label = ft.Text(
        label_text,
        size=FONT_SIZES['sm'],
        color=FLUENT_COLORS['text_primary']
    )
    return ft.Row(
        controls=[checkbox, label],
        spacing=SPACING['xs'],
        tight=True,
    )


def create_variable_checkboxes(
    variables: list,
    default_selected: list = None,
    max_display: int = 10
) -> ft.Column:
    """
    创建变量多选框 - 统一的UI控件创建方法
    
    Args:
        variables: 变量列表
        default_selected: 默认选中的变量列表
        max_display: 最多显示的变量数量
    
    Returns:
        ft.Column: 包含复选框的列组件
    """
    if default_selected is None:
        default_selected = []
    
    checkboxes = []
    for var in variables[:max_display]:
        checkbox_row = create_checkbox_with_label(
            var,
            value=var in default_selected or var in variables[:max_display]
        )
        # 将checkbox保存到row的data属性，方便后续访问
        checkbox_row.data = checkbox_row.controls[0]  # 保存checkbox引用
        checkbox_row.label_text = var  # 保存标签文本
        checkboxes.append(checkbox_row)
    
    return ft.Column(
        controls=checkboxes,
        spacing=SPACING['xs'],
    )

