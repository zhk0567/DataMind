"""
首页 - Flet版本
高标准视觉规范
"""
import flet as ft
from ui_flet.components.fluent_components import FluentCard, FluentButton, PageHeader
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, PAGE_LAYOUT, FONT_FAMILY, FONT_WEIGHT_NORMAL, FONT_WEIGHT_MEDIUM, FONT_WEIGHT_BOLD, get_text_style


class HomePage:
    """首页"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.content = None
    
    def get_content(self):
        """获取页面内容"""
        if self.content is None:
            self.content = self._create_content()
        return self.content
    
    def _create_content(self):
        """创建页面内容 - 严格网格布局"""
        # 标题区域 - 使用统一组件
        header = PageHeader(
            title="欢迎使用 DataMind",
            subtitle="现代化的数据分析平台，提供专业的数据处理和统计分析功能，支持数据上传、清洗、统计分析、可视化等完整的数据分析流程。"
        )
        
        # 功能卡片 - 使用严格的网格布局
        # 定义卡片固定尺寸
        CARD_WIDTH = 300
        CARD_HEIGHT = 200
        CARD_SPACING = SPACING['xl']  # 20px
        
        # 所有功能卡片
        all_cards = [
            self._create_feature_card(
                "📤 数据上传",
                "支持CSV、Excel格式数据上传",
                FLUENT_COLORS['primary'],
                CARD_WIDTH,
                CARD_HEIGHT
            ),
            self._create_feature_card(
                "🔧 数据处理",
                "数据清洗、转换、编码等预处理功能",
                FLUENT_COLORS['secondary'],
                CARD_WIDTH,
                CARD_HEIGHT
            ),
            self._create_feature_card(
                "📈 统计分析",
                "描述性统计、相关分析、方差分析、回归分析等",
                FLUENT_COLORS['accent'],
                CARD_WIDTH,
                CARD_HEIGHT
            ),
            self._create_feature_card(
                "📉 数据可视化",
                "多种图表类型，直观展示数据分析结果",
                FLUENT_COLORS['info'],
                CARD_WIDTH,
                CARD_HEIGHT
            ),
            self._create_feature_card(
                "🔒 数据安全",
                "所有数据处理在本地完成，保护数据隐私",
                FLUENT_COLORS['success'],
                CARD_WIDTH,
                CARD_HEIGHT
            ),
        ]
        
        # 第一行：3个卡片，严格对齐
        features_row1 = ft.Row(
            controls=all_cards[:3],
            spacing=CARD_SPACING,
            wrap=False,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
        
        # 第二行：2个卡片，使用精确计算居中
        # 计算需要的左侧间距：(第一行总宽度 - 第二行总宽度) / 2
        # 第一行：3个卡片 + 2个间距 = 3*300 + 2*20 = 940
        # 第二行：2个卡片 + 1个间距 = 2*300 + 1*20 = 620
        # 左侧间距：(940 - 620) / 2 = 160
        left_spacer_width = (CARD_WIDTH * 3 + CARD_SPACING * 2) - (CARD_WIDTH * 2 + CARD_SPACING * 1)
        left_spacer_width = left_spacer_width // 2
        
        features_row2 = ft.Row(
            controls=[
                ft.Container(width=left_spacer_width),  # 精确的左侧间距
                all_cards[3],
                all_cards[4],
            ],
            spacing=CARD_SPACING,
            wrap=False,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
        
        # 提示卡片 - 统一样式
        from ui_flet.styles import COMPONENT_SIZES
        tip_container = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.LIGHTBULB_OUTLINE,
                        color=FLUENT_COLORS['text_white'],
                        size=24,  # 增大图标
                    ),
                    ft.Text(
                        "提示：请先上传数据文件，然后进行数据处理和分析。",
                        size=FONT_SIZES['md'],
                        color=FLUENT_COLORS['text_white'],
                        weight=ft.FontWeight.W_500,  # 加粗提升可读性
                    ),
                ],
                spacing=SPACING['md'],
                alignment=ft.MainAxisAlignment.CENTER,  # 内容居中
            ),
            padding=ft.padding.symmetric(
                horizontal=SPACING['xxl'],
                vertical=SPACING['xl']  # 增大垂直内边距
            ),
            bgcolor=FLUENT_COLORS['primary'],
            border_radius=COMPONENT_SIZES['card_border_radius'],
            width=None,  # 自适应宽度
            alignment=ft.alignment.center,
        )
        
        # 主内容 - 统一间距，限制最大宽度确保居中
        content = ft.Column(
            controls=[
                header,
                ft.Container(height=PAGE_LAYOUT['header_spacing']),
                features_row1,
                ft.Container(height=SPACING['xl']),  # 行间距
                features_row2,
                ft.Container(height=PAGE_LAYOUT['section_spacing']),
                tip_container,
            ],
            spacing=0,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # 水平居中
        )
        
        return ft.Container(
            content=content,
            expand=True,
        )
    
    def _create_feature_card(self, title: str, description: str, accent_color: str, width: int = 300, height: int = 200):
        """创建功能卡片 - 严格统一标准，确保大小完全一致"""
        from ui_flet.styles import COMPONENT_SIZES
        
        # 创建卡片内容
        card_content = FluentCard(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            title,
                            size=FONT_SIZES['xxl'],
                            weight=ft.FontWeight.BOLD,
                            color=accent_color,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(height=SPACING['md']),  # 标题和描述之间的间距
                        ft.Text(
                            description,
                            size=FONT_SIZES['md'],
                            color=FLUENT_COLORS['text_secondary'],
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,  # 垂直居中
                    spacing=0,  # 使用Container控制间距
                ),
                padding=COMPONENT_SIZES['card_padding'],
                width=width - COMPONENT_SIZES['card_padding'] * 2,  # 减去padding
                height=height - COMPONENT_SIZES['card_padding'] * 2,
                alignment=ft.alignment.center,
            ),
            padding=0,  # 卡片本身不添加padding，由内部Container控制
        )
        
        # 严格固定尺寸的容器
        return ft.Container(
            content=card_content,
            width=width,
            height=height,
            alignment=ft.alignment.center,
        )
