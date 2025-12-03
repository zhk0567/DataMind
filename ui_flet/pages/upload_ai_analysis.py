"""
数据上传页面 - AI分析功能模块
将AI分析相关方法提取到此模块
"""
import flet as ft
import threading
from ui_flet.styles import FLUENT_COLORS, SPACING, FONT_SIZES, FONT_WEIGHT_NORMAL, FONT_WEIGHT_MEDIUM, FONT_WEIGHT_BOLD
from ui_flet.styles import get_text_kwargs
from ui_flet.utils.message_helper import show_snackbar
from core.ai import AIAnalyzer


class UploadAIAnalysisMixin:
    """AI分析功能Mixin类"""
    
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
        
        # 显示加载状态
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
            scroll=ft.ScrollMode.ADAPTIVE,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        # 立即更新UI显示加载状态
        try:
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
            
            # AI分析结果（流式显示）
            if ai_response:
                controls.append(ft.Container(height=SPACING['lg']))
                controls.append(
                    ft.Text(
                        "🤖 AI分析结果（实时更新中...）",
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
                        ai_response,
                        **get_text_kwargs(
                            size=FONT_SIZES['md'],
                            weight=FONT_WEIGHT_NORMAL,
                            color=FLUENT_COLORS['text_primary']
                        )
                    )
                )
            
            # 更新UI
            self.ai_analysis_card.content = ft.Column(
                controls=controls,
                spacing=SPACING['md'],
                scroll=ft.ScrollMode.ADAPTIVE,
            )
            
            # 更新页面
            try:
                self.main_window.page.update()
            except Exception as e:
                print(f"更新流式UI失败: {e}")
                
        except Exception as e:
            print(f"更新流式UI时出错: {e}")
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
            
            # AI分析结果
            if ai_response:
                controls.append(ft.Container(height=SPACING['lg']))
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
            
            # 更新UI
            self.ai_analysis_card.content = ft.Column(
                controls=controls,
                spacing=SPACING['md'],
                scroll=ft.ScrollMode.ADAPTIVE,
            )
            self.is_analyzing = False
            
            # 强制更新UI
            try:
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
            scroll=ft.ScrollMode.ADAPTIVE,
        )
        
        # 强制更新UI
        try:
            self.main_window.page.update()
            print(f"错误UI已更新: {error_msg}")
        except Exception as e:
            print(f"更新错误UI时出错: {e}")
        
        # 显示snackbar
        try:
            show_snackbar(self.main_window.page, f"AI分析失败: {error_msg}", "error", duration=5000)
        except Exception as e:
            print(f"显示错误snackbar失败: {e}")

