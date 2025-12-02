"""
数据上传页面 - Flet版本
高标准视觉规范
"""
import flet as ft
import pandas as pd
import os
import threading
import asyncio
from ui_flet.components.fluent_components import FluentCard, FluentButton, PageHeader, FluentDropdown
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, PAGE_LAYOUT, COMPONENT_SIZES, FONT_FAMILY, FONT_WEIGHT_NORMAL, FONT_WEIGHT_MEDIUM, FONT_WEIGHT_BOLD, get_text_style, get_text_kwargs
from ui_flet.utils.message_helper import show_snackbar
from ui_flet.utils.file_helper import read_dataframe
from core.ai import AIAnalyzer


class UploadPage:
    """数据上传页面"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.content = None
        self.file_picker = None
        self.file_label = None
        self.info_label = None
        self.data_table = None
        self.ai_analyzer = None  # 延迟初始化，避免导入错误
        self.ai_analysis_card = None
        self.is_analyzing = False
        self.streaming_text = ""  # 流式响应文本
        self.basic_stats = None  # 基本统计信息（用于流式显示）
    
    def get_content(self):
        """获取页面内容"""
        if self.content is None:
            self.content = self._create_content()
        return self.content
    
    def _create_content(self):
        """创建页面内容"""
        # 标题区域 - 使用统一组件
        header = PageHeader(
            title="📤 数据上传",
            subtitle="上传CSV或Excel格式的数据文件"
        )
        
        # 文件选择器
        self.file_picker = ft.FilePicker(
            on_result=self._handle_file_selected
        )
        
        # 上传卡片 - 统一间距和样式
        self.file_label = ft.Text(
            "未选择文件",
            **get_text_kwargs(
                size=FONT_SIZES['md'],
                weight=FONT_WEIGHT_MEDIUM,
                color=FLUENT_COLORS['text_primary']
            )
        )
        
        self.info_label = ft.Text(
            "",
            **get_text_kwargs(
                size=FONT_SIZES['md'],
                weight=FONT_WEIGHT_NORMAL,
                color=FLUENT_COLORS['text_secondary']
            )
        )
        
        upload_card = FluentCard(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            FluentButton(
                                text="📁 选择文件上传",
                                on_click=self._handle_file_picker_click,
                                bg_color=FLUENT_COLORS['primary'],
                            ),
                            ft.Container(expand=True),
                            self.file_label,
                        ],
                        spacing=SPACING['lg'],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Container(height=SPACING['sm']),
                    self.info_label,
                ],
                spacing=0,
            ),
            padding=COMPONENT_SIZES['card_padding'],
        )
        
        # 数据预览卡片 - 统一样式
        preview_card = FluentCard(
            title="📋 数据预览",
            content=ft.Container(
                content=ft.Text(
                    "请先上传数据文件",
                    **get_text_kwargs(
                        size=FONT_SIZES['md'],
                        weight=FONT_WEIGHT_NORMAL,
                        color=FLUENT_COLORS['text_secondary']
                    ),
                    text_align=ft.TextAlign.CENTER,
                ),
                padding=SPACING['xl'],
                alignment=ft.alignment.center,
            ),
            padding=COMPONENT_SIZES['card_padding'],
        )
        
        self.preview_card = preview_card
        
        # AI分析卡片 - 右侧显示
        self.ai_analysis_card = FluentCard(
            title="🤖 AI自动分析",
            content=ft.Column(
                controls=[
                    ft.Text(
                        "上传数据后将自动进行AI分析",
                        **get_text_kwargs(
                            size=FONT_SIZES['md'],
                            weight=FONT_WEIGHT_NORMAL,
                            color=FLUENT_COLORS['text_secondary']
                        )
                    )
                ],
                spacing=SPACING['md'],
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=COMPONENT_SIZES['card_padding'],
        )
        
        # 左侧内容区域
        left_content = ft.Column(
            controls=[
                upload_card,
                ft.Container(height=PAGE_LAYOUT['card_spacing']),
                preview_card,
            ],
            spacing=0,
            expand=True,
        )
        
        # 右侧AI分析区域
        right_content = ft.Column(
            controls=[
                self.ai_analysis_card,
            ],
            spacing=0,
            expand=True,
        )
        
        # 主内容区域 - 左右分栏
        main_row = ft.Row(
            controls=[
                ft.Container(
                    content=left_content,
                    expand=2,
                    padding=ft.padding.only(right=SPACING['md']),
                ),
                ft.Container(
                    content=right_content,
                    expand=1,
                    padding=ft.padding.only(left=SPACING['md']),
                ),
            ],
            spacing=0,
            expand=True,
        )
        
        # 主内容 - 统一间距
        content = ft.Column(
            controls=[
                header,
                ft.Container(height=PAGE_LAYOUT['header_spacing']),
                main_row,
            ],
            spacing=0,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )
        
        return ft.Container(
            content=content,
            expand=True,
            padding=ft.padding.only(right=SPACING['md']),  # 为滚动条留出空间
        )
    
    def _handle_file_picker_click(self, e):
        """处理文件选择器按钮点击"""
        # 确保 FilePicker 已添加到页面 overlay
        if self.file_picker and self.file_picker not in self.main_window.page.overlay:
            self.main_window.page.overlay.append(self.file_picker)
            self.main_window.page.update()
        
        # 打开文件选择对话框
        if self.file_picker:
            self.file_picker.pick_files(
                allowed_extensions=["csv", "xlsx", "xls"],
                dialog_title="选择数据文件"
            )
    
    def _handle_file_selected(self, e: ft.FilePickerResultEvent):
        """处理文件选择"""
        if e.files and len(e.files) > 0:
            file_path = e.files[0].path
            
            # 显示加载状态
            self.file_label.value = "正在读取文件..."
            self.file_label.update()
            
            try:
                # 使用工具函数读取文件（支持多种编码）
                df = read_dataframe(file_path)
                
                if df is None:
                    raise Exception("无法读取文件，请检查文件格式和编码")
                
                # 保存数据
                self.main_window.data = df
                self.main_window.processed_data = df.copy()
                
                # 更新界面
                self.file_label.value = f"✅ 已选择: {os.path.basename(file_path)}"
                self.file_label.color = FLUENT_COLORS['success']
                
                missing_count = df.isnull().sum().sum()
                self.info_label.value = (
                    f"📊 数据维度: {df.shape[0]:,} 行 × {df.shape[1]:,} 列 | "
                    f"⚠️ 缺失值: {missing_count:,} 个"
                )
                
                # 显示数据预览
                self._display_data_preview(df)
                
                # 通知其他页面数据已更新
                if hasattr(self.main_window, 'pages'):
                    for page_key, page in self.main_window.pages.items():
                        if hasattr(page, 'on_data_changed'):
                            page.on_data_changed()
                
                # 显示成功消息
                show_snackbar(
                    self.main_window.page,
                    f"数据加载成功！共 {df.shape[0]:,} 行数据，正在启动AI分析...",
                    "success"
                )
                
                # 更新页面 - 统一使用页面更新，避免控件未添加错误
                self.main_window.page.update()
                
                # 自动启动AI分析（延迟一点确保UI已更新）
                import time
                def start_analysis():
                    time.sleep(0.3)  # 短暂延迟，确保页面已更新
                    print(f"准备启动AI分析，数据形状: {df.shape}")
                    self._start_ai_analysis(df)
                
                # 在新线程中延迟启动，避免阻塞
                import threading
                thread = threading.Thread(target=start_analysis, daemon=True)
                thread.start()
                
            except Exception as ex:
                # 显示错误
                self.file_label.value = f"❌ 文件读取失败: {str(ex)}"
                self.file_label.color = FLUENT_COLORS['error']
                self.file_label.update()
                
                show_snackbar(
                    self.main_window.page,
                    f"文件读取失败: {str(ex)}",
                    "error",
                    duration=5000
                )
    
    def _display_data_preview(self, df):
        """显示数据预览"""
        try:
            # 创建数据表格
            columns = df.columns.tolist()
            
            if len(columns) == 0:
                # 如果没有列，显示提示
                self.preview_card.content.content = ft.Container(
                    content=ft.Text(
                        "数据为空",
                        size=FONT_SIZES['md'],
                        color=FLUENT_COLORS['text_secondary'],
                        text_align=ft.TextAlign.CENTER,
                    ),
                    padding=SPACING['xl'],
                    alignment=ft.alignment.center,
                )
                # 更新整个页面而不是单个控件
                self.main_window.page.update()
                return
            
            max_cols = min(10, len(columns))  # 最多显示10列
            max_rows = min(100, len(df))  # 最多显示100行
            
            # 创建表格列 - 使用字符串而不是Text控件，避免控件未添加错误
            data_columns = [
                ft.DataColumn(
                    ft.Text(
                        col,
                        **get_text_kwargs(
                            size=FONT_SIZES['sm'],
                            weight=FONT_WEIGHT_BOLD,
                            color=FLUENT_COLORS['text_primary']
                        )
                    ),
                    numeric=False
                )
                for col in columns[:max_cols]
            ]
            
            # 创建数据行
            data_rows = []
            for idx, row in df.head(max_rows).iterrows():
                cells = [
                    ft.DataCell(
                        ft.Text(
                            str(val)[:50] if pd.notna(val) else "",  # 限制显示长度
                            size=FONT_SIZES['sm'],
                            color=FLUENT_COLORS['text_primary']
                        )
                    )
                    for val in row[:max_cols]
                ]
                data_rows.append(ft.DataRow(cells=cells))
            
            data_table = ft.DataTable(
                columns=data_columns,
                rows=data_rows,
                border=ft.border.all(1, FLUENT_COLORS['border']),
                border_radius=COMPONENT_SIZES['input_border_radius'],
                heading_row_color=FLUENT_COLORS['bg_tertiary'],
                heading_text_style=ft.TextStyle(
                    size=FONT_SIZES['sm'],
                    weight=ft.FontWeight.BOLD,
                    color=FLUENT_COLORS['text_primary']
                ),
                data_row_max_height=40,
            )
            
            # 更新预览卡片 - 统一间距
            scroll_view = ft.Container(
                content=data_table,
                padding=SPACING['xl'],
            )
            
            scroll_column = ft.Column(
                controls=[scroll_view],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            )
            
            self.preview_card.content.content = scroll_column
            # 更新整个页面而不是单个控件，确保所有控件都已添加到页面树中
            self.main_window.page.update()
            
        except Exception as ex:
            # 如果更新失败，显示错误但不中断流程
            show_snackbar(
                self.main_window.page,
                f"预览更新失败: {str(ex)}",
                "error",
                duration=3000
            )
    
    def _start_ai_analysis(self, df):
        """启动AI分析"""
        print(f"_start_ai_analysis 被调用，is_analyzing={self.is_analyzing}")
        
        if self.is_analyzing:
            print("AI分析正在进行中，跳过")
            return
        
        # 确保AI分析器已初始化
        if self.ai_analyzer is None:
            try:
                print("初始化AI分析器...")
                self.ai_analyzer = AIAnalyzer()
                print("AI分析器初始化成功")
            except Exception as e:
                print(f"AI分析器初始化失败: {e}")
                import traceback
                traceback.print_exc()
                self._show_ai_analysis_error(f"AI分析器初始化失败: {str(e)}")
                return
        
        # 确保AI分析卡片已初始化
        if self.ai_analysis_card is None:
            print("错误：AI分析卡片未初始化")
            return
        
        print("开始显示加载状态...")
        
        self.is_analyzing = True
        
        # 显示加载状态 - 重新创建Column以确保UI刷新
        self.ai_analysis_card.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.ProgressRing(
                                width=50, 
                                height=50, 
                                stroke_width=4,
                                color=FLUENT_COLORS['primary']
                            ),
                            ft.Container(height=SPACING['md']),
                            ft.Text(
                                "AI正在分析数据，请稍候...",
                                **get_text_kwargs(
                                    size=FONT_SIZES['md'],
                                    weight=FONT_WEIGHT_MEDIUM,
                                    color=FLUENT_COLORS['text_primary']
                                )
                            ),
                            ft.Text(
                                "预计10秒内完成",
                                **get_text_kwargs(
                                    size=FONT_SIZES['sm'],
                                    weight=FONT_WEIGHT_NORMAL,
                                    color=FLUENT_COLORS['text_secondary']
                                )
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0,
                    ),
                    padding=SPACING['xl'],
                    alignment=ft.alignment.center,
                )
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        # 立即更新UI显示加载状态
        try:
            # 先更新卡片
            self.ai_analysis_card.update()
            # 然后更新整个页面
            self.main_window.page.update()
            print("加载状态已显示")
        except Exception as e:
            print(f"更新UI失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 在新线程中执行分析（避免阻塞UI）
        thread = threading.Thread(target=self._perform_ai_analysis, args=(df,), daemon=True)
        thread.start()
    
    def _perform_ai_analysis(self, df):
        """执行AI分析（在后台线程中，使用流式响应）"""
        try:
            print("开始AI分析（流式响应）...")
            
            # 初始化流式响应状态
            self.streaming_text = ""
            self.basic_stats = None
            
            # 定义流式响应回调函数
            def on_chunk_received(chunk_text):
                """接收到每个chunk时的回调"""
                self.streaming_text += chunk_text
                
                # 实时更新UI显示部分结果
                try:
                    async def async_update_chunk():
                        self._update_ai_analysis_ui_streaming(self.streaming_text)
                    
                    # 使用run_task确保在主线程中执行
                    self.main_window.page.run_task(async_update_chunk)
                except Exception as e:
                    print(f"更新流式UI失败: {e}")
            
            # 调用AI分析器（使用流式响应）
            result = self.ai_analyzer.analyze_dataframe(df, callback=on_chunk_received)
            self.basic_stats = result['basic_statistics']
            
            print("AI分析完成，开始更新最终UI...")
            
            # 使用page.run_task确保在主线程中更新最终UI
            try:
                async def async_update():
                    self._update_ai_analysis_ui(result)
                
                # 使用run_task确保在主线程中执行
                self.main_window.page.run_task(async_update)
                print("UI更新任务已提交")
            except Exception as e:
                # 如果run_task失败，直接调用（Flet的update应该是线程安全的）
                print(f"使用run_task失败，直接更新: {e}")
                self._update_ai_analysis_ui(result)
                print("UI更新完成（直接调用）")
            
        except Exception as ex:
            error_msg = str(ex)
            print(f"AI分析失败: {error_msg}")
            import traceback
            traceback.print_exc()
            # 使用相同的方式更新错误UI
            try:
                async def async_error():
                    self._show_ai_analysis_error(error_msg)
                self.main_window.page.run_task(async_error)
            except Exception as e:
                # 如果run_task失败，直接调用
                print(f"使用run_task失败，直接更新错误: {e}")
                self._show_ai_analysis_error(error_msg)
    
    def _update_ai_analysis_ui_streaming(self, partial_text):
        """更新AI分析结果UI（流式响应，实时显示部分结果）"""
        try:
            if self.basic_stats is None:
                # 如果基本统计信息还没有，只显示加载状态
                return
            
            stats = self.basic_stats
            ai_response = partial_text
            
            # 构建显示内容
            controls = []
            
            # 基本统计信息
            shape = stats['shape']
            missing = stats['missing_values']
            data_types = stats['data_types']
            
            controls.append(
                ft.Text(
                    "📊 数据基本信息",
                    **get_text_kwargs(
                        size=FONT_SIZES['lg'],
                        weight=FONT_WEIGHT_BOLD,
                        color=FLUENT_COLORS['primary']
                    )
                )
            )
            controls.append(ft.Container(height=SPACING['sm']))
            controls.append(
                ft.Text(
                    f"数据维度: {shape['rows']:,} 行 × {shape['columns']:,} 列",
                    **get_text_kwargs(
                        size=FONT_SIZES['md'],
                        weight=FONT_WEIGHT_NORMAL,
                        color=FLUENT_COLORS['text_primary']
                    )
                )
            )
            controls.append(
                ft.Text(
                    f"缺失值: {missing['total']:,} 个 ({missing['percentage']:.2f}%)",
                    **get_text_kwargs(
                        size=FONT_SIZES['md'],
                        weight=FONT_WEIGHT_NORMAL,
                        color=FLUENT_COLORS['text_primary']
                    )
                )
            )
            controls.append(
                ft.Text(
                    f"数值型列: {data_types['numeric_count']} 个 | 分类型列: {data_types['categorical_count']} 个",
                    **get_text_kwargs(
                        size=FONT_SIZES['md'],
                        weight=FONT_WEIGHT_NORMAL,
                        color=FLUENT_COLORS['text_primary']
                    )
                )
            )
            
            controls.append(ft.Divider(height=1))
            controls.append(ft.Container(height=SPACING['md']))
            
            # AI分析结果（流式显示）
            controls.append(
                ft.Text(
                    "🤖 AI分析结果（正在生成...）",
                    **get_text_kwargs(
                        size=FONT_SIZES['lg'],
                        weight=FONT_WEIGHT_BOLD,
                        color=FLUENT_COLORS['primary']
                    )
                )
            )
            controls.append(ft.Container(height=SPACING['sm']))
            
            # 显示部分文本（简单格式，不进行复杂格式化以加快更新速度）
            if ai_response:
                # 简单显示文本，添加一个闪烁的光标效果
                controls.append(
                    ft.Text(
                        ai_response + "▊",  # 添加光标效果
                        **get_text_kwargs(
                            size=FONT_SIZES['md'],
                            weight=FONT_WEIGHT_NORMAL,
                            color=FLUENT_COLORS['text_primary']
                        )
                    )
                )
            else:
                controls.append(
                    ft.Text(
                        "正在生成分析结果...",
                        **get_text_kwargs(
                            size=FONT_SIZES['md'],
                            weight=FONT_WEIGHT_NORMAL,
                            color=FLUENT_COLORS['text_secondary']
                        )
                    )
                )
            
            # 更新卡片内容
            self.ai_analysis_card.content = ft.Column(
                controls=controls,
                spacing=SPACING['md'],
                scroll=ft.ScrollMode.AUTO,
            )
            
            # 更新UI
            try:
                self.ai_analysis_card.update()
                self.main_window.page.update()
            except Exception as e:
                print(f"更新流式UI时出错: {e}")
                
        except Exception as e:
            print(f"流式更新UI失败: {e}")
            import traceback
            traceback.print_exc()
    
    def _update_ai_analysis_ui(self, result):
        """更新AI分析结果UI（最终完整结果）"""
        try:
            stats = result['basic_statistics']
            ai_response = result['ai_analysis']
            
            # 构建显示内容
            controls = []
            
            # 基本统计信息
            shape = stats['shape']
            missing = stats['missing_values']
            data_types = stats['data_types']
            
            controls.append(
                ft.Text(
                    "📊 数据基本信息",
                    **get_text_kwargs(
                        size=FONT_SIZES['lg'],
                        weight=FONT_WEIGHT_BOLD,
                        color=FLUENT_COLORS['primary']
                    )
                )
            )
            controls.append(ft.Container(height=SPACING['sm']))
            controls.append(
                ft.Text(
                    f"数据维度: {shape['rows']:,} 行 × {shape['columns']:,} 列",
                    **get_text_kwargs(
                        size=FONT_SIZES['md'],
                        weight=FONT_WEIGHT_NORMAL,
                        color=FLUENT_COLORS['text_primary']
                    )
                )
            )
            controls.append(
                ft.Text(
                    f"缺失值: {missing['total']:,} 个 ({missing['percentage']:.2f}%)",
                    **get_text_kwargs(
                        size=FONT_SIZES['md'],
                        weight=FONT_WEIGHT_NORMAL,
                        color=FLUENT_COLORS['text_primary']
                    )
                )
            )
            controls.append(
                ft.Text(
                    f"数值型列: {data_types['numeric_count']} 个 | 分类型列: {data_types['categorical_count']} 个",
                    **get_text_kwargs(
                        size=FONT_SIZES['md'],
                        weight=FONT_WEIGHT_NORMAL,
                        color=FLUENT_COLORS['text_primary']
                    )
                )
            )
            
            controls.append(ft.Divider(height=1))
            controls.append(ft.Container(height=SPACING['md']))
            
            # AI分析结果
            controls.append(
                ft.Text(
                    "🤖 AI分析结果",
                    **get_text_kwargs(
                        size=FONT_SIZES['lg'],
                        weight=FONT_WEIGHT_BOLD,
                        color=FLUENT_COLORS['primary']
                    )
                )
            )
            controls.append(ft.Container(height=SPACING['sm']))
            
            # 格式化AI响应 - 改进排版和去除markdown标记
            # 先清理文本，去除所有markdown标记和*号
            import re
            cleaned_response = ai_response
            
            # 去除markdown标题标记
            cleaned_response = re.sub(r'^#+\s*', '', cleaned_response, flags=re.MULTILINE)
            # 去除列表标记（- 或 * 开头，包括多个*）
            cleaned_response = re.sub(r'^[-*]+\s+', '', cleaned_response, flags=re.MULTILINE)
            # 去除行内的所有*号（用于强调，但保留文本内容）
            cleaned_response = re.sub(r'\*+([^*]*)\*+', r'\1', cleaned_response)
            # 去除行首的数字列表标记（1. 2. 等）
            cleaned_response = re.sub(r'^\d+\.\s+', '', cleaned_response, flags=re.MULTILINE)
            # 去除行尾的*号
            cleaned_response = re.sub(r'\*+\s*$', '', cleaned_response, flags=re.MULTILINE)
            # 去除多余的*号（连续多个*）
            cleaned_response = re.sub(r'\*{2,}', '', cleaned_response)
            
            lines = cleaned_response.split('\n')
            current_section = []
            in_list = False
            
            for line in lines:
                line = line.strip()
                
                # 空行处理
                if not line:
                    if current_section:
                        # 输出当前段落
                        paragraph_text = ' '.join(current_section).strip()
                        if paragraph_text:
                            controls.append(
                                ft.Text(
                                    paragraph_text,
                                    **get_text_kwargs(
                                        size=FONT_SIZES['md'],
                                        weight=FONT_WEIGHT_NORMAL,
                                        color=FLUENT_COLORS['text_primary']
                                    )
                                )
                            )
                        current_section = []
                        controls.append(ft.Container(height=SPACING['sm']))
                    in_list = False
                    continue
                
                # 检测是否是标题（通过格式判断：短行、可能包含冒号等）
                is_title = (
                    len(line) < 30 and 
                    (line.endswith('：') or line.endswith(':') or 
                     '评估' in line or '总结' in line or '建议' in line or 
                     '方案' in line or '方向' in line or '问题' in line)
                )
                
                if is_title:
                    # 输出之前的段落
                    if current_section:
                        paragraph_text = ' '.join(current_section).strip()
                        if paragraph_text:
                            controls.append(
                                ft.Text(
                                    paragraph_text,
                                    **get_text_kwargs(
                                        size=FONT_SIZES['md'],
                                        weight=FONT_WEIGHT_NORMAL,
                                        color=FLUENT_COLORS['text_primary']
                                    )
                                )
                            )
                        current_section = []
                    
                    # 添加标题
                    title_text = line.rstrip('：:').strip()
                    controls.append(ft.Container(height=SPACING['md']))
                    controls.append(
                        ft.Text(
                            title_text,
                            **get_text_kwargs(
                                size=FONT_SIZES['lg'],
                                weight=FONT_WEIGHT_BOLD,
                                color=FLUENT_COLORS['primary']
                            )
                        )
                    )
                    controls.append(ft.Container(height=SPACING['xs']))
                    in_list = False
                else:
                    # 普通文本或列表项
                    # 检测是否是列表项（短行、可能包含句号或分号结尾）
                    is_list_item = (
                        len(line) < 100 and 
                        (line.endswith('。') or line.endswith('；') or 
                         line.endswith('.') or line.endswith(';'))
                    )
                    
                    if is_list_item:
                        # 处理列表项
                        if current_section and not in_list:
                            # 输出之前的段落
                            paragraph_text = ' '.join(current_section).strip()
                            if paragraph_text:
                                controls.append(
                                    ft.Text(
                                        paragraph_text,
                                        **get_text_kwargs(
                                            size=FONT_SIZES['md'],
                                            weight=FONT_WEIGHT_NORMAL,
                                            color=FLUENT_COLORS['text_primary']
                                        )
                                    )
                                )
                            current_section = []
                            controls.append(ft.Container(height=SPACING['xs']))
                        
                        # 添加列表项，使用更好的排版
                        list_text = line.strip()
                        controls.append(
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Container(
                                            content=ft.Text(
                                                "•",
                                                **get_text_kwargs(
                                                    size=FONT_SIZES['md'],
                                                    weight=FONT_WEIGHT_NORMAL,
                                                    color=FLUENT_COLORS['primary']
                                                )
                                            ),
                                            width=24,
                                            alignment=ft.alignment.top_left,
                                            padding=ft.padding.only(top=2),
                                        ),
                                        ft.Text(
                                            list_text,
                                            **get_text_kwargs(
                                                size=FONT_SIZES['md'],
                                                weight=FONT_WEIGHT_NORMAL,
                                                color=FLUENT_COLORS['text_primary']
                                            ),
                                            expand=True,
                                        )
                                    ],
                                    spacing=0,
                                    vertical_alignment=ft.CrossAxisAlignment.START,
                                ),
                                padding=ft.padding.only(left=0, right=0, top=SPACING['xs'], bottom=SPACING['xs']),
                            )
                        )
                        in_list = True
                    else:
                        # 普通段落文本
                        if in_list:
                            # 列表结束，输出之前的列表项
                            controls.append(ft.Container(height=SPACING['xs']))
                            in_list = False
                        
                        current_section.append(line)
            
            # 输出最后一段
            if current_section:
                paragraph_text = ' '.join(current_section).strip()
                if paragraph_text:
                    controls.append(
                        ft.Text(
                            paragraph_text,
                            **get_text_kwargs(
                                size=FONT_SIZES['md'],
                                weight=FONT_WEIGHT_NORMAL,
                                color=FLUENT_COLORS['text_primary']
                            )
                        )
                    )
            
            if not controls:
                controls.append(
                    ft.Text(
                        ai_response,
                        **get_text_kwargs(
                            size=FONT_SIZES['md'],
                            weight=FONT_WEIGHT_NORMAL,
                            color=FLUENT_COLORS['text_primary']
                        )
                    )
                )
            
            # 更新卡片内容 - 重新创建Column以确保UI刷新
            self.ai_analysis_card.content = ft.Column(
                controls=controls,
                spacing=SPACING['md'],
                scroll=ft.ScrollMode.AUTO,
            )
            self.is_analyzing = False
            
            # 强制更新UI - 确保在主线程中更新
            try:
                # 先更新卡片
                self.ai_analysis_card.update()
                # 然后更新整个页面
                self.main_window.page.update()
                print("UI已更新")
            except Exception as e:
                print(f"更新UI时出错: {e}")
                import traceback
                traceback.print_exc()
            
            # 显示snackbar
            try:
                show_snackbar(self.main_window.page, "AI分析完成！", "success")
            except Exception as e:
                print(f"显示snackbar失败: {e}")
            
        except Exception as e:
            self._show_ai_analysis_error(str(e))
    
    def _show_ai_analysis_error(self, error_msg):
        """显示AI分析错误"""
        self.is_analyzing = False
        
        # 重新创建Column以确保UI刷新
        self.ai_analysis_card.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.ERROR, color=FLUENT_COLORS['error'], size=24),
                        ft.Text(
                            f"分析失败: {error_msg}",
                            size=FONT_SIZES['md'],
                            color=FLUENT_COLORS['error']
                        )
                    ],
                    spacing=SPACING['sm']
                )
            ],
            spacing=SPACING['md'],
            scroll=ft.ScrollMode.AUTO,
        )
        
        # 强制更新UI
        try:
            # 先更新卡片
            self.ai_analysis_card.update()
            # 然后更新整个页面
            self.main_window.page.update()
            print(f"错误UI已更新: {error_msg}")
        except Exception as e:
            print(f"更新错误UI时出错: {e}")
        
        # 显示snackbar
        try:
            show_snackbar(self.main_window.page, f"AI分析失败: {error_msg}", "error", duration=5000)
        except Exception as e:
            print(f"显示错误snackbar失败: {e}")
