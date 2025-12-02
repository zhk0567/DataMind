"""
消息提示工具
"""
import flet as ft
from ui_flet.styles import FLUENT_COLORS


def show_snackbar(page: ft.Page, message: str, msg_type: str = "info", duration: int = 3000):
    """
    显示SnackBar消息
    符合WCAG AAA级标准：提供清晰的视觉和文本反馈。
    
    Args:
        page: Flet Page对象
        message: 消息内容
        msg_type: 消息类型 ('info', 'success', 'warning', 'error')
        duration: 显示时长（毫秒）
    """
    from ui_flet.styles import FONT_SIZES, SPACING
    
    icon_map = {
        'info': ft.Icons.INFO,
        'success': ft.Icons.CHECK_CIRCLE,
        'warning': ft.Icons.WARNING,
        'error': ft.Icons.ERROR,
    }
    
    color_map = {
        'info': FLUENT_COLORS['info'],
        'success': FLUENT_COLORS['success'],
        'warning': FLUENT_COLORS['warning'],
        'error': FLUENT_COLORS['error'],
    }
    
    bg_color = color_map.get(msg_type, FLUENT_COLORS['info'])
    icon_data = icon_map.get(msg_type, ft.Icons.INFO)
    
    # WCAG AAA级标准：确保消息文本与背景有足够对比度
    # 使用白色文字在彩色背景上，对比度通常超过7:1
    page.snack_bar = ft.SnackBar(
        content=ft.Row(
            [
                ft.Icon(icon_data, color=FLUENT_COLORS['text_white'], size=20),
                ft.Text(
                    message, 
                    color=FLUENT_COLORS['text_white'], 
                    size=FONT_SIZES['md'],
                    weight=ft.FontWeight.W_500,  # 加粗提升可读性
                ),
            ],
            spacing=SPACING['md'],
            tight=True,
        ),
        bgcolor=bg_color,
        duration=duration,
        # WCAG AAA级标准：确保SnackBar可以被屏幕阅读器识别
        action="确定",  # 提供操作按钮
        action_color=FLUENT_COLORS['text_white'],
    )
    page.snack_bar.open = True
    page.update()


def show_banner(page: ft.Page, message: str, msg_type: str = "info", actions: list = None):
    """
    显示Banner消息
    
    Args:
        page: Flet Page对象
        message: 消息内容
        msg_type: 消息类型 ('info', 'success', 'warning', 'error')
        actions: 操作按钮列表
    """
    color_map = {
        'info': FLUENT_COLORS['info'],
        'success': FLUENT_COLORS['success'],
        'warning': FLUENT_COLORS['warning'],
        'error': FLUENT_COLORS['error'],
    }
    
    bg_color = color_map.get(msg_type, FLUENT_COLORS['info'])
    
    if actions is None:
        actions = [
            ft.TextButton("关闭", on_click=lambda _: setattr(page.banner, 'open', False) or page.update())
        ]
    
    page.banner = ft.Banner(
        bgcolor=bg_color,
        leading=ft.Icon(
            ft.Icons.INFO if msg_type == 'info' else
            ft.Icons.CHECK_CIRCLE if msg_type == 'success' else
            ft.Icons.WARNING if msg_type == 'warning' else
            ft.Icons.ERROR,
            color='#FFFFFF',
            size=40
        ),
        content=ft.Text(message, color='#FFFFFF', size=14),
        actions=actions,
    )
    page.banner.open = True
    page.update()

