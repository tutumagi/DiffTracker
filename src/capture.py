import os
import tempfile
from PIL import ImageGrab


def capture_area(region, save_path):
    screenshot = ImageGrab.grab(bbox=region)
    screenshot.save(save_path)


def select_area():
    # TODO: 在这里添加代码以获取用户选择的屏幕区域
    # 你可以使用 Tkinter 的 Toplevel 窗口来实现一个简单的选择界面
    # 返回选取的区域坐标 (x, y, width, height)
    x = 1807
    y = 105
    width = 445
    height = 709
    region = (x, y, x + width, y + height)
    return region
