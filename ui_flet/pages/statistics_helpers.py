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
            ft.DataColumn(ft.Text(header, size=FONT_SIZES['sm'], weight=ft.FontWeight.BOLD))
            for header in headers
        ],
        rows=rows,
        border=ft.border.all(1, FLUENT_COLORS['border']),
        border_radius=COMPONENT_SIZES['input_border_radius'],
    )
    controls.append(table)
    return controls


def create_stats_table(stats_data, title=None):
    """创建统计量表"""
    rows = [
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(key, size=FONT_SIZES['sm'])),
                ft.DataCell(ft.Text(f"{val:.4f}" if isinstance(val, (int, float)) else str(val), size=FONT_SIZES['sm'])),
            ]
        )
        for key, val in stats_data
    ]
    return create_data_table(["统计量", "值"], rows, title)


def execute_analysis_with_loading(
    result_area,
    page,
    analyzer_func,
    display_func,
    success_msg="分析完成",
    error_prefix="分析失败"
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
    
    Returns:
        bool: 是否执行成功
    """
    # 显示加载状态
    show_loading(result_area)
    
    try:
        # 执行分析
        result = analyzer_func()
        
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
    
    return ft.Column(
        controls=[
            ft.Checkbox(
                label=var,
                value=var in default_selected or var in variables[:max_display]
            )
            for var in variables[:max_display]
        ],
        spacing=SPACING['xs'],
    )

