import os
import tempfile
import time
import tkinter as tk
from PIL import ImageGrab
from capture import capture_area, select_area

from config import SLACK_TOKEN
from diff import compare, cp_image_path, load_image
from forward import SlackForward
from utils import ImagePathGenerator


class ScreenCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DiffTracker")

        # Slack 相关配置
        self.slack_token = SLACK_TOKEN  # 替换为你的 Slack API Token
        self.slack_channel = "全体"  # 替换为你的 Slack 频道

        # 创建按钮
        self.start_button = tk.Button(root, text="开始监控", command=self.start_monitoring)
        self.start_button.pack(pady=10)

    def start_monitoring(self):
        # 获取屏幕上用户选取的区域
        region = self.select_screen_region()

        # 在这里添加开始监控的代码
        while True:
            screenshot = ImageGrab.grab(bbox=region)
            # 处理截图...
            # 将截图保存在临时目录
            temp_dir = tempfile.gettempdir()
            temp_filename = os.path.join(temp_dir, "temp_screenshot.png")
            screenshot.save(temp_filename)

            # 将截图发送到 Slack 频道
            self.send_image_to_slack(temp_filename)

            # 处理截图...
            break

    def select_screen_region(self):
        # TODO: 在这里添加代码以获取用户选择的屏幕区域
        # 你可以使用 Tkinter 的 Toplevel 窗口来实现一个简单的选择界面
        # 返回选取的区域坐标 (x, y, width, height)
        return (0, 0, 800, 600)  # 示例，整个屏幕


def mainloop():
    # init service
    today_id = time.strftime("%Y%m%d", time.localtime())
    image_path_generator = ImagePathGenerator(today_id)
    slack_forward = SlackForward(SLACK_TOKEN, "C03ED3E18FL")

    # 第一次截图
    cur_screenshot_path = image_path_generator.get_cur_screenshot_path()
    select_area_region = select_area()
    capture_area(select_area_region, cur_screenshot_path)
    while True:
        time.sleep(1)
        tmp_image_path = image_path_generator.get_tmp_screenshot_path()
        capture_area(select_area_region, tmp_image_path)

        final_diff_path = image_path_generator.get_final_diff_path()
        if compare(
            image_path_generator.get_last_screenshot_path(),
            tmp_image_path,
            final_diff_path,
        ):
            # 将当前图片内容保存为上一次的图片内容
            cp_image_path(
                tmp_image_path, image_path_generator.get_cur_screenshot_path()
            )
            # 将 diff 图片发送到 Slack 频道
            slack_forward.send_image(final_diff_path)


if __name__ == "__main__":
    mainloop()
    # root = tk.Tk()
    # app = ScreenCaptureApp(root)
    # root.mainloop()
