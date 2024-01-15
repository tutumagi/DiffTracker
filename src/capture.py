import os
import tempfile
from PIL import ImageGrab


def capture():
    region = select_screen_region()
    temp_dir = tempfile.gettempdir()
    temp_filename = os.path.join(temp_dir, "temp_screenshot.png")
    capture_screen(region, temp_dir)


def capture_screen(region, save_path):
    screenshot = ImageGrab.grab(bbox=region)
    screenshot.save(save_path)


def select_screen_region():
    # TODO: 在这里添加代码以获取用户选择的屏幕区域
    # 你可以使用 Tkinter 的 Toplevel 窗口来实现一个简单的选择界面
    # 返回选取的区域坐标 (x, y, width, height)
    return (0, 0, 800, 600)  # 示例，整个屏幕
