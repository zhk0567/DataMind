"""
Fluent Design 风格组件
基于Flet实现 - 高标准视觉规范
"""
import flet as ft
from ui_flet.styles import (
    FLUENT_COLORS, BUTTON_STYLE, CARD_STYLE, INPUT_STYLE,
    SPACING, FONT_SIZES, COMPONENT_SIZES,
    FOCUS_INDICATOR, MIN_TOUCH_TARGET,
    FONT_FAMILY, FONT_WEIGHT_NORMAL, FONT_WEIGHT_MEDIUM, FONT_WEIGHT_BOLD,
    get_text_style, get_text_kwargs
)


class FluentButton(ft.ElevatedButton):
    """Fluent Design 风格按钮 - 统一标准，符合WCAG AAA级标准"""
    
    def __init__(
        self,
        text: str,
        on_click=None,
        icon=None,
        bg_color=None,
        width=None,
        height=None,
        size='md',  # 'sm', 'md', 'lg'
        tooltip=None,  # 工具提示（用于屏幕阅读器）
        aria_label=None,  # ARIA标签（用于屏幕阅读器）
        **kwargs
    ):
        # 根据尺寸设置高度和padding
        if size == 'sm':
            btn_height = max(COMPONENT_SIZES['button_height'], MIN_TOUCH_TARGET['height'])
            padding = ft.padding.symmetric(horizontal=SPACING['lg'], vertical=SPACING['sm'])
        elif size == 'lg':
            btn_height = max(COMPONENT_SIZES['button_height_large'], MIN_TOUCH_TARGET['height'])
            padding = ft.padding.symmetric(horizontal=SPACING['xxl'], vertical=SPACING['lg'])
        else:  # md
            btn_height = max(COMPONENT_SIZES['button_height'], MIN_TOUCH_TARGET['height'])
            padding = ft.padding.symmetric(horizontal=SPACING['xl'], vertical=SPACING['md'])
        
        # 确保宽度符合最小点击区域要求
        if width is not None:
            width = max(width, MIN_TOUCH_TARGET['width'])
        
        # 创建按钮样式，包含焦点指示器和统一字体
        button_style = BUTTON_STYLE if not bg_color else ft.ButtonStyle(
            color=FLUENT_COLORS['text_white'],
            bgcolor=bg_color,
            shape=ft.RoundedRectangleBorder(radius=COMPONENT_SIZES['button_border_radius']),
            padding=padding,
            text_style=get_text_style(
                size=FONT_SIZES['md'],
                weight=FONT_WEIGHT_MEDIUM,
                color=FLUENT_COLORS['text_white']
            ),
        )
        
        # 如果没有指定样式，使用默认样式并添加字体配置
        if not bg_color:
            button_style.text_style = get_text_style(
                size=FONT_SIZES['md'],
                weight=FONT_WEIGHT_MEDIUM,
                color=FLUENT_COLORS['text_white']
            )
        
        super().__init__(
            text=text,
            on_click=on_click,
            icon=icon,
            style=button_style,
            width=width,
            height=height or btn_height,
            tooltip=tooltip or text,  # 默认使用文本作为工具提示
            **kwargs
        )
        
        # 设置ARIA属性（如果Flet支持）
        if aria_label:
            # Flet可能通过tooltip或其他属性支持
            self.tooltip = aria_label


class FluentCard(ft.Card):
    """Fluent Design 风格卡片 - 统一标准"""
    
    def __init__(
        self,
        content=None,
        title=None,
        padding=None,
        elevation=2,
        **kwargs
    ):
        # 使用标准padding
        if padding is None:
            padding = CARD_STYLE['padding']
        
        # 构建内容
        card_content = []
        if title:
            card_content.append(
                ft.Container(
                    content=ft.Text(
                        title,
                        **get_text_kwargs(
                            size=FONT_SIZES['xxl'],
                            weight=FONT_WEIGHT_BOLD,
                            color=FLUENT_COLORS['text_primary']
                        )
                    ),
                    padding=ft.padding.only(bottom=SPACING['md']),
                )
            )
            card_content.append(
                ft.Divider(
                    height=1,
                    color=FLUENT_COLORS['divider'],
                )
            )
            card_content.append(
                ft.Container(height=SPACING['lg'])
            )
        
        if content:
            if isinstance(content, list):
                card_content.extend(content)
            else:
                card_content.append(content)
        
        container = ft.Container(
            content=ft.Column(
                controls=card_content,
                spacing=SPACING['lg'],
                tight=True,
            ),
            padding=padding,
            bgcolor=CARD_STYLE['bgcolor'],
            border=ft.border.all(1, FLUENT_COLORS['border']),
            border_radius=CARD_STYLE['border_radius'],
        )
        
        super().__init__(
            content=container,
            elevation=elevation,
            shadow_color=CARD_STYLE['shadow_color'],
            **kwargs
        )


class FluentTextField(ft.TextField):
    """Fluent Design 风格文本输入框 - 统一标准，符合WCAG AAA级标准"""
    
    def __init__(
        self,
        label=None,
        hint_text=None,
        value=None,
        width=None,
        aria_label=None,  # ARIA标签（用于屏幕阅读器）
        **kwargs
    ):
        # 确保高度符合最小点击区域要求
        input_height = max(INPUT_STYLE['height'], MIN_TOUCH_TARGET['height'])
        
        super().__init__(
            label=label,
            hint_text=hint_text,
            value=value,
            width=width,
            border_radius=INPUT_STYLE['border_radius'],
            border_color=INPUT_STYLE['border_color'],
            focused_border_color=FLUENT_COLORS['primary'],  # 焦点边框颜色（高对比度）
            focused_border_width=FOCUS_INDICATOR['border_width'],  # 焦点边框宽度
            bgcolor=INPUT_STYLE['bgcolor'],
            height=input_height,
            label_style=get_text_style(
                size=FONT_SIZES['sm'],
                weight=FONT_WEIGHT_NORMAL,
                color=FLUENT_COLORS['text_primary']
            ),
            text_style=get_text_style(
                size=FONT_SIZES['md'],
                weight=FONT_WEIGHT_NORMAL,
                color=FLUENT_COLORS['text_primary']
            ),
            tooltip=aria_label or label or hint_text,  # 工具提示
            **kwargs
        )


class FluentDropdown(ft.Dropdown):
    """Fluent Design 风格下拉框 - 统一标准，符合WCAG AAA级标准"""
    
    def __init__(
        self,
        label=None,
        options=None,
        value=None,
        width=None,
        aria_label=None,  # ARIA标签（用于屏幕阅读器）
        **kwargs
    ):
        # 确保高度符合最小点击区域要求
        dropdown_height = max(INPUT_STYLE['height'], MIN_TOUCH_TARGET['height'])
        
        super().__init__(
            label=label,
            options=options or [],
            value=value,
            width=width,
            border_radius=INPUT_STYLE['border_radius'],
            border_color=INPUT_STYLE['border_color'],
            focused_border_color=FLUENT_COLORS['primary'],  # 焦点边框颜色（高对比度）
            focused_border_width=FOCUS_INDICATOR['border_width'],  # 焦点边框宽度
            bgcolor=INPUT_STYLE['bgcolor'],
            label_style=get_text_style(
                size=FONT_SIZES['sm'],
                weight=FONT_WEIGHT_NORMAL,
                color=FLUENT_COLORS['text_primary']
            ),
            text_style=get_text_style(
                size=FONT_SIZES['md'],
                weight=FONT_WEIGHT_NORMAL,
                color=FLUENT_COLORS['text_primary']
            ),
            tooltip=aria_label or label,  # 工具提示
            **kwargs
        )


class FluentSidebar(ft.Container):
    """Fluent Design 风格侧边栏 - 统一标准"""
    
    def __init__(self, on_nav_click=None, **kwargs):
        self.on_nav_click = on_nav_click
        self.selected_index = 0
        
        # 导航项（确保使用简体中文，使用正确的"处"字 U+5904）
        # 注意：使用纯文字，避免emoji可能导致的字体渲染问题
        nav_items = [
            ("首页", "home"),
            ("数据上传", "upload"),
            ("数据处理", "process"),  # "处"字：U+5904 (简体)，确保正确显示
            ("统计分析", "statistics"),
            ("数据可视化", "visualization"),
        ]
        
        # 创建导航按钮列表
        nav_buttons = []
        for i, (text, key) in enumerate(nav_items):
            # WCAG AAA级标准：选中项使用深色文字在浅色背景上，确保高对比度
            is_selected = i == 0
            btn = ft.ElevatedButton(
                text=text,
                data=key,
                on_click=self._handle_nav_click,
                style=ft.ButtonStyle(
                    # 选中项：深色文字在浅色背景上（高对比度）
                    # 未选中项：浅色文字在深色背景上（高对比度）
                    color=FLUENT_COLORS['text_primary'] if is_selected else FLUENT_COLORS['text_on_dark'],
                    bgcolor=FLUENT_COLORS['bg_primary'] if is_selected else '#00000000',  # 选中用白色，未选中透明
                    shape=ft.RoundedRectangleBorder(radius=4),
                    padding=ft.padding.symmetric(horizontal=SPACING['xl'], vertical=SPACING['md']),
                    # 统一字体粗细：所有导航项使用相同的字体粗细和大小
                    text_style=get_text_style(
                        size=FONT_SIZES['md'],
                        weight=FONT_WEIGHT_MEDIUM,
                    ),
                ),
                width=280,
                height=COMPONENT_SIZES['button_height'],
            )
            nav_buttons.append(btn)
        
        self.nav_buttons = nav_buttons
        
        # 侧边栏内容
        sidebar_content = ft.Column(
            controls=[
                # Logo和标题
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "DataMind",
                                **get_text_kwargs(
                                    size=FONT_SIZES['title'],
                                    weight=FONT_WEIGHT_BOLD,
                                    color=FLUENT_COLORS['text_white']
                                )
                            ),
                            ft.Text(
                                "数据分析平台",
                                **get_text_kwargs(
                                    size=FONT_SIZES['sm'],
                                    weight=FONT_WEIGHT_NORMAL,
                                    color=FLUENT_COLORS['text_on_dark']
                                )
                            ),
                        ],
                        spacing=SPACING['sm'],
                    ),
                    padding=ft.padding.only(
                        left=SPACING['xxl'],
                        top=SPACING['xxxl'],
                        bottom=SPACING['xl']
                    ),
                ),
                ft.Divider(
                    height=1,
                    color=FLUENT_COLORS['divider']
                ),
                # 导航按钮
                ft.Container(
                    content=ft.Column(
                        controls=nav_buttons,
                        spacing=SPACING['xs'],
                    ),
                    padding=ft.padding.symmetric(
                        horizontal=SPACING['md'],
                        vertical=SPACING['md']
                    ),
                ),
                # 版本信息
                ft.Container(
                    content=ft.Text(
                        "v1.0.0",
                        **get_text_kwargs(
                            size=FONT_SIZES['xs'],
                            weight=FONT_WEIGHT_NORMAL,
                            color=FLUENT_COLORS['text_on_dark']
                        )
                    ),
                    alignment=ft.alignment.bottom_center,
                    padding=ft.padding.only(bottom=SPACING['lg']),
                ),
            ],
            spacing=0,
            expand=True,
        )
        
        super().__init__(
            content=sidebar_content,
            width=280,
            bgcolor=FLUENT_COLORS['bg_sidebar'],
            padding=0,
            **kwargs
        )
    
    def _handle_nav_click(self, e):
        """处理导航点击"""
        key = e.control.data
        
        # 更新按钮样式
        # WCAG AAA级标准：选中项使用深色文字在白色背景上，确保高对比度（21:1）
        for i, btn in enumerate(self.nav_buttons):
            if btn.data == key:
                self.selected_index = i
                # 选中状态：白色背景 + 深色文字（高对比度）
                btn.style.bgcolor = FLUENT_COLORS['bg_primary']  # 白色背景
                btn.style.color = FLUENT_COLORS['text_primary']  # 深色文字（#1A1A1A）
            else:
                # 未选中状态：透明背景 + 浅色文字
                btn.style.bgcolor = '#00000000'  # 透明
                btn.style.color = FLUENT_COLORS['text_on_dark']  # 浅色文字
            
            # 确保字体样式统一（防止样式被覆盖）
            btn.style.text_style = get_text_style(
                size=FONT_SIZES['md'],
                weight=FONT_WEIGHT_MEDIUM,
            )
            
            btn.update()
        
        # 调用回调
        if self.on_nav_click:
            self.on_nav_click(key)


class PageHeader(ft.Container):
    """页面标题组件 - 统一标准"""
    
    def __init__(
        self,
        title: str,
        subtitle: str = None,
        action: ft.Control = None,
    ):
        controls = [
            ft.Text(
                title,
                **get_text_kwargs(
                    size=FONT_SIZES['title_large'],
                    weight=FONT_WEIGHT_BOLD,
                    color=FLUENT_COLORS['text_primary']
                )
            ),
        ]
        
        if subtitle:
            controls.append(
                ft.Text(
                    subtitle,
                    **get_text_kwargs(
                        size=FONT_SIZES['md'],
                        weight=FONT_WEIGHT_NORMAL,
                        color=FLUENT_COLORS['text_secondary']
                    )
                )
            )
        
        header_content = ft.Column(
            controls=controls,
            spacing=SPACING['sm'],
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )
        
        if action:
            header_row = ft.Row(
                controls=[
                    header_content,
                    ft.Container(expand=True),
                    action,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,  # 垂直居中对齐
            )
            super().__init__(
                content=header_row,
                padding=ft.padding.only(
                    right=SPACING['md'],  # 右侧padding，为滚动条留出空间
                ),
            )
        else:
            super().__init__(
                content=header_content,
                padding=0,
            )
