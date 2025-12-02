"""
文本组件辅助工具
统一创建 Text 组件，确保字体一致
"""
import flet as ft
from ui_flet.styles import FONT_SIZES, FLUENT_COLORS, get_text_kwargs, FONT_WEIGHT_NORMAL, FONT_WEIGHT_BOLD, FONT_WEIGHT_MEDIUM


def create_text(
    value: str,
    size: str = 'md',
    weight: str = 'normal',  # 'normal', 'medium', 'bold'
    color: str = None,
    **kwargs
) -> ft.Text:
    """
    创建统一的 Text 组件
    
    Args:
        value: 文本内容
        size: 字体大小（'xs', 'sm', 'md', 'lg', 'xl', 'xxl', 'title', 'title_large', 'title_huge'）
        weight: 字体粗细（'normal', 'medium', 'bold'）
        color: 文字颜色（可选，默认 text_primary）
        **kwargs: 其他 ft.Text 参数
    
    Returns:
        ft.Text: 统一配置的 Text 组件
    """
    # 映射字体粗细
    weight_map = {
        'normal': FONT_WEIGHT_NORMAL,
        'medium': FONT_WEIGHT_MEDIUM,
        'bold': FONT_WEIGHT_BOLD,
    }
    
    # 获取字体大小
    font_size = FONT_SIZES.get(size, FONT_SIZES['md'])
    
    # 获取文字颜色
    text_color = color or FLUENT_COLORS['text_primary']
    
    # 获取文本参数
    text_kwargs = get_text_kwargs(
        size=font_size,
        weight=weight_map.get(weight, FONT_WEIGHT_NORMAL),
        color=text_color
    )
    
    # 创建 Text 组件
    return ft.Text(
        value,
        **text_kwargs,
        **kwargs
    )

