"""
Flet 主窗口
"""
import flet as ft
from ui_flet.components.fluent_components import FluentSidebar
from ui_flet.pages import (
    HomePage,
    UploadPage,
    ProcessPage,
    StatisticsPage,
    VisualizationPage
)


class MainWindow:
    """主窗口类"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "DataMind - 数据分析平台"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        
        # 应用现代化主题配置
        from ui_flet.styles import FLUENT_THEME
        self.page.theme = FLUENT_THEME
        
        self.page.window.width = 1400
        self.page.window.height = 900
        self.page.window.min_width = 1200
        self.page.window.min_height = 700
        
        # 数据存储
        self.data = None
        self.processed_data = None
        
        # WCAG AAA级标准：启用键盘导航支持
        self._setup_keyboard_navigation()
        
        # 创建UI
        self._create_ui()
    
    def _setup_keyboard_navigation(self):
        """设置键盘导航支持（WCAG AAA级标准）"""
        # Flet自动支持Tab键导航，这里可以添加自定义键盘快捷键
        # 例如：Ctrl+S保存，Esc关闭对话框等
        pass
    
    def _create_ui(self):
        """创建UI"""
        # 主布局
        main_row = ft.Row(
            controls=[],
            spacing=0,
            expand=True,
        )
        
        # 侧边栏
        self.sidebar = FluentSidebar(
            on_nav_click=self._handle_navigation
        )
        
        # 内容区域
        from ui_flet.styles import SPACING, FLUENT_COLORS
        self.content_area = ft.Container(
            content=ft.Column(
                controls=[],
                spacing=0,
                expand=True,
            ),
            expand=True,
            padding=SPACING['xxxl'],
            bgcolor=FLUENT_COLORS['bg_secondary'],
        )
        
        # 页面容器
        self.page_stack = ft.Stack(
            controls=[],
            expand=True,
        )
        
        self.content_area.content.controls.append(self.page_stack)
        
        main_row.controls = [self.sidebar, self.content_area]
        
        # 先设置页面内容（必须在创建页面之前）
        self.page.add(main_row)
        
        # 创建页面
        self.pages = {
            'home': HomePage(self),
            'upload': UploadPage(self),
            'process': ProcessPage(self),
            'statistics': StatisticsPage(self),
            'visualization': VisualizationPage(self),
        }
        
        # 添加文件选择器到页面overlay（必须在页面创建后）
        if 'upload' in self.pages:
            upload_page = self.pages['upload']
            if hasattr(upload_page, 'file_picker') and upload_page.file_picker:
                self.page.overlay.append(upload_page.file_picker)
        
        # 添加可视化页面的保存文件选择器
        if 'visualization' in self.pages:
            viz_page = self.pages['visualization']
            if hasattr(viz_page, 'save_file_picker') and viz_page.save_file_picker:
                self.page.overlay.append(viz_page.save_file_picker)
        
        # 默认显示首页（必须在页面添加到page之后）
        self._show_page('home')
    
    def _handle_navigation(self, page_key: str):
        """处理导航"""
        self._show_page(page_key)
    
    def _show_page(self, page_key: str):
        """显示指定页面"""
        # 清空页面栈
        self.page_stack.controls.clear()
        
        # 显示新页面
        if page_key in self.pages:
            page_content = self.pages[page_key].get_content()
            self.page_stack.controls.append(page_content)
            
            # 先更新页面，确保控件已添加到页面树中
            self.page.update()
            
            # 如果页面有数据变化回调，调用它（此时控件已在页面中）
            if hasattr(self.pages[page_key], 'on_data_changed'):
                try:
                    self.pages[page_key].on_data_changed()
                    # 如果数据更新成功，再次更新页面
                    self.page.update()
                except Exception as e:
                    # 如果更新失败，记录错误但不影响页面显示
                    print(f"Warning: Failed to update page data: {e}")

