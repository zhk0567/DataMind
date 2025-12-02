"""
数据表格组件
优化的数据表格显示
"""
import flet as ft
import pandas as pd
from ui_flet.styles import FLUENT_COLORS, FONT_SIZES, FONT_WEIGHT_BOLD, FONT_WEIGHT_NORMAL, get_text_style, get_text_kwargs


class FluentDataTable(ft.DataTable):
    """Fluent Design 风格数据表格"""
    
    def __init__(self, df: pd.DataFrame = None, max_rows: int = 100, max_cols: int = 10, **kwargs):
        super().__init__(**kwargs)
        
        if df is not None:
            self.load_dataframe(df, max_rows, max_cols)
    
    def load_dataframe(self, df: pd.DataFrame, max_rows: int = 100, max_cols: int = 10):
        """加载DataFrame数据"""
        columns = df.columns.tolist()
        max_cols = min(max_cols, len(columns))
        max_rows = min(max_rows, len(df))
        
        # 创建列
        self.columns = [
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
        
        # 创建行
        self.rows = []
        for idx, row in df.head(max_rows).iterrows():
            cells = [
                ft.DataCell(
                    ft.Text(
                        str(val)[:50] if pd.notna(val) else "",
                        **get_text_kwargs(
                            size=FONT_SIZES['xs'],
                            weight=FONT_WEIGHT_NORMAL,
                            color=FLUENT_COLORS['text_primary']
                        )
                    )
                )
                for val in row[:max_cols]
            ]
            self.rows.append(ft.DataRow(cells=cells))
        
        # 设置样式
        self.border = ft.border.all(1, FLUENT_COLORS['border'])
        self.border_radius = 4
        self.heading_row_color = FLUENT_COLORS['bg_tertiary']
        self.heading_text_style = get_text_style(
            size=FONT_SIZES['sm'],
            weight=FONT_WEIGHT_BOLD,
            color=FLUENT_COLORS['text_primary']
        )
        self.data_row_max_height = 40

