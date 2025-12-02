"""
Flet UI 样式定义
Fluent Design 风格 - 高标准视觉规范
"""
import flet as ft

# ==================== 颜色系统 ====================
# 现代化优雅配色方案 - 参考 Material Design 3 和 Fluent Design 2.0
FLUENT_COLORS = {
    # 主色调 - 现代蓝色（更柔和、优雅）
    'primary': '#2563EB',  # 现代蓝色，更柔和
    'primary_hover': '#1D4ED8',  # 悬停时稍深
    'primary_light': '#60A5FA',  # 浅蓝色
    'primary_dark': '#1E40AF',  # 深蓝色
    
    # 次要色 - 优雅的绿色和紫色
    'secondary': '#10B981',  # 现代绿色（更柔和）
    'secondary_hover': '#059669',
    'accent': '#8B5CF6',  # 优雅紫色（替代黄色，更现代）
    'accent_hover': '#7C3AED',
    
    # 状态颜色 - 现代化配色
    'success': '#10B981',  # 柔和的绿色
    'warning': '#F59E0B',  # 柔和的橙色
    'error': '#EF4444',  # 柔和的红色
    'info': '#3B82F6',  # 柔和的蓝色
    
    # 背景色 - 温和的灰色层次（更优雅）
    'bg_primary': '#FFFFFF',        # 纯白色背景
    'bg_secondary': '#F8FAFC',      # 极浅灰蓝背景（更温和）
    'bg_tertiary': '#F1F5F9',       # 浅灰蓝背景（更优雅）
    'bg_sidebar': '#1E293B',        # 深蓝灰侧边栏（更现代）
    'bg_card': '#FFFFFF',           # 卡片白色背景
    'bg_card_hover': '#F8FAFC',      # 卡片悬停背景（更温和）
    
    # 文字颜色 - 优化可读性和优雅度
    'text_primary': '#0F172A',      # 深蓝黑色（更优雅，对比度仍高）
    'text_secondary': '#475569',    # 中灰色（更柔和）
    'text_tertiary': '#64748B',     # 浅灰色（更温和）
    'text_disabled': '#94A3B8',     # 禁用状态（更柔和）
    'text_white': '#FFFFFF',        # 纯白色
    'text_light': '#CBD5E1',        # 浅灰色，用于侧边栏非激活项
    'text_on_primary': '#FFFFFF',   # 主色上的文字（白色）
    'text_on_dark': '#F1F5F9',      # 深色背景上的文字（浅灰蓝，更优雅）
    
    # 边框和分隔线 - 更柔和
    'border': '#E2E8F0',  # 更柔和的边框色
    'border_light': '#F1F5F9',  # 极浅边框
    'border_dark': '#CBD5E1',  # 深色边框
    'divider': '#E2E8F0',  # 分隔线
}

# ==================== 间距系统 ====================
SPACING = {
    'xs': 4,
    'sm': 8,
    'md': 12,
    'lg': 16,
    'xl': 20,
    'xxl': 24,
    'xxxl': 32,
    'huge': 40,
    'massive': 48,
}

# ==================== 字体系统 ====================
# 统一字体配置 - 确保所有文字显示一致，粗细均匀
FONT_FAMILY = "Microsoft YaHei, SimHei, sans-serif"  # 统一使用中文字体，确保中文正确显示
FONT_WEIGHT_NORMAL = ft.FontWeight.W_400  # 正常粗细
FONT_WEIGHT_MEDIUM = ft.FontWeight.W_500  # 中等粗细（用于按钮、导航等）
FONT_WEIGHT_BOLD = ft.FontWeight.W_700    # 粗体（用于标题、强调）

# 现代化字体大小 - 提升可读性和舒适度
FONT_SIZES = {
    'xs': 11,      # 从10增加到11，提升可读性
    'sm': 13,      # 从12增加到13，更舒适
    'md': 15,      # 从14增加到15，主要文字更易读
    'lg': 17,      # 从16增加到17，副标题更清晰
    'xl': 19,      # 从18增加到19，更突出
    'xxl': 22,     # 从20增加到22，更明显
    'title': 28,   # 从24增加到28，标题更醒目
    'title_large': 36,  # 从32增加到36，大标题更有冲击力
    'title_huge': 42,   # 从36增加到42，超大标题
}

# 统一文本样式辅助函数
def get_text_style(
    size: int = None,
    weight: ft.FontWeight = None,
    color: str = None,
    font_family: str = None
) -> ft.TextStyle:
    """
    创建统一的文本样式（用于 TextStyle 属性，如 label_style, text_style 等）
    
    Args:
        size: 字体大小（可选，使用 FONT_SIZES 中的值）
        weight: 字体粗细（可选，默认 W_400）
        color: 文字颜色（可选，默认 text_primary）
        font_family: 字体族（可选，默认使用 FONT_FAMILY）
    
    Returns:
        ft.TextStyle: 统一的文本样式对象
    """
    return ft.TextStyle(
        size=size or FONT_SIZES['md'],
        weight=weight or FONT_WEIGHT_NORMAL,
        color=color or FLUENT_COLORS['text_primary'],
        font_family=font_family or FONT_FAMILY,
    )


def get_text_kwargs(
    size: int = None,
    weight: ft.FontWeight = None,
    color: str = None,
    font_family: str = None
) -> dict:
    """
    获取 Text 组件的参数字典（只包含 Text 支持的参数）
    
    Args:
        size: 字体大小（可选，使用 FONT_SIZES 中的值）
        weight: 字体粗细（可选，默认 W_400）
        color: 文字颜色（可选，默认 text_primary）
        font_family: 字体族（可选，默认使用 FONT_FAMILY）
    
    Returns:
        dict: Text 组件支持的参数字典
    """
    kwargs = {}
    if size is not None:
        kwargs['size'] = size
    if weight is not None:
        kwargs['weight'] = weight
    if color is not None:
        kwargs['color'] = color
    if font_family is not None:
        kwargs['font_family'] = font_family
    else:
        kwargs['font_family'] = FONT_FAMILY
    
    # 设置默认值
    if 'size' not in kwargs:
        kwargs['size'] = FONT_SIZES['md']
    if 'weight' not in kwargs:
        kwargs['weight'] = FONT_WEIGHT_NORMAL
    if 'color' not in kwargs:
        kwargs['color'] = FLUENT_COLORS['text_primary']
    
    return kwargs

# ==================== 组件尺寸 ====================
# 现代化组件尺寸 - 更优雅的圆角和间距
COMPONENT_SIZES = {
    'button_height': 42,  # 从40增加到42，更舒适
    'button_height_large': 50,  # 从48增加到50
    'input_height': 42,  # 从40增加到42
    'card_padding': 28,  # 从24增加到28，更宽松
    'card_padding_small': 24,  # 从20增加到24
    'card_border_radius': 12,  # 从8增加到12，更现代
    'button_border_radius': 10,  # 从6增加到10，更优雅
    'input_border_radius': 8,  # 从4增加到8，更柔和
}

# ==================== 主题配置 ====================
FLUENT_THEME = ft.Theme(
    color_scheme_seed='#2563EB',  # 现代蓝色主色调
    use_material3=True,
    # 设置全局字体主题，确保所有文字使用统一字体
    text_theme=ft.TextTheme(
        body_large=ft.TextStyle(font_family=FONT_FAMILY, weight=FONT_WEIGHT_NORMAL),
        body_medium=ft.TextStyle(font_family=FONT_FAMILY, weight=FONT_WEIGHT_NORMAL),
        body_small=ft.TextStyle(font_family=FONT_FAMILY, weight=FONT_WEIGHT_NORMAL),
        title_large=ft.TextStyle(font_family=FONT_FAMILY, weight=FONT_WEIGHT_BOLD),
        title_medium=ft.TextStyle(font_family=FONT_FAMILY, weight=FONT_WEIGHT_BOLD),
        title_small=ft.TextStyle(font_family=FONT_FAMILY, weight=FONT_WEIGHT_MEDIUM),
        label_large=ft.TextStyle(font_family=FONT_FAMILY, weight=FONT_WEIGHT_NORMAL),
        label_medium=ft.TextStyle(font_family=FONT_FAMILY, weight=FONT_WEIGHT_NORMAL),
        label_small=ft.TextStyle(font_family=FONT_FAMILY, weight=FONT_WEIGHT_NORMAL),
    ),
)

# ==================== 按钮样式 ====================
BUTTON_STYLE = ft.ButtonStyle(
    color=FLUENT_COLORS['text_white'],
    bgcolor=FLUENT_COLORS['primary'],
    shape=ft.RoundedRectangleBorder(radius=COMPONENT_SIZES['button_border_radius']),
    padding=ft.padding.symmetric(
        horizontal=SPACING['xl'],
        vertical=SPACING['md']
    ),
)

BUTTON_STYLE_HOVER = ft.ButtonStyle(
    color=FLUENT_COLORS['text_white'],
    bgcolor=FLUENT_COLORS['primary_hover'],
    shape=ft.RoundedRectangleBorder(radius=COMPONENT_SIZES['button_border_radius']),
    padding=ft.padding.symmetric(
        horizontal=SPACING['xl'],
        vertical=SPACING['md']
    ),
)

# ==================== 卡片样式 ====================
# 现代化卡片样式 - 更优雅的阴影和边框
CARD_STYLE = {
    'elevation': 3,  # 从2增加到3，更有层次感
    'shadow_color': '#0000000D',  # 更柔和的阴影（5% 透明度）
    'border_radius': COMPONENT_SIZES['card_border_radius'],
    'bgcolor': FLUENT_COLORS['bg_card'],
    'border': ft.border.all(1, FLUENT_COLORS['border']),
    'padding': COMPONENT_SIZES['card_padding'],
}

# ==================== 输入框样式 ====================
INPUT_STYLE = {
    'border_radius': COMPONENT_SIZES['input_border_radius'],
    'border_color': FLUENT_COLORS['border'],
    'focused_border_color': FLUENT_COLORS['primary'],
    'bgcolor': FLUENT_COLORS['bg_primary'],
    'height': COMPONENT_SIZES['input_height'],
}

# ==================== 页面布局规范 ====================
PAGE_LAYOUT = {
    'header_spacing': SPACING['xxl'],  # 标题下方间距
    'section_spacing': SPACING['xl'],  # 区块间距
    'card_spacing': SPACING['lg'],  # 卡片间距
    'content_padding': SPACING['xxxl'],  # 内容区域padding
}

# ==================== WCAG AAA级无障碍标准 ====================
# 焦点指示器样式（符合WCAG AAA级标准）
FOCUS_INDICATOR = {
    'border_width': 3,  # 焦点边框宽度（至少2px，AAA级要求）
    'border_color': FLUENT_COLORS['primary'],  # 焦点边框颜色
    'border_radius': COMPONENT_SIZES['button_border_radius'],
    'outline_offset': 2,  # 焦点轮廓偏移
}

# 最小点击区域（WCAG AAA级要求至少44x44像素）
MIN_TOUCH_TARGET = {
    'width': 44,  # 最小宽度（像素）
    'height': 44,  # 最小高度（像素）
}

# 键盘导航支持
KEYBOARD_NAVIGATION = {
    'tab_order': 'sequential',  # Tab键顺序：sequential（顺序）或 custom（自定义）
    'skip_links': True,  # 是否支持跳过链接
}
