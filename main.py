"""
DataMind - 数据分析平台
启动入口

使用方法：
    python main.py
"""
import sys
import os


def check_dependencies():
    """
    检查必要的依赖是否已安装
    
    Returns:
        bool: 依赖是否完整
    """
    required = ['pandas', 'numpy', 'matplotlib', 'flet']
    
    missing = []
    for module in required:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print(f"错误：缺少必要的依赖包: {', '.join(missing)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    return True


def main():
    """主函数：启动Flet应用"""
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    import flet as ft
    from ui_flet.main_window import MainWindow
    
    def app_main(page: ft.Page):
        """Flet主函数"""
        app = MainWindow(page)
    
    print("=" * 60)
    print(" " * 15 + "DataMind - 数据分析平台")
    print("=" * 60)
    print("正在启动应用...")
    print("=" * 60)
    print()
    
    try:
        ft.app(target=app_main, view=ft.AppView.FLET_APP)
    except Exception as e:
        print(f"\n启动失败: {e}")
        print("请确保已安装所有依赖: pip install -r requirements.txt")
        sys.exit(1)


if __name__ == "__main__":
    main()

