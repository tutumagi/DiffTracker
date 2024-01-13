import os
import tempfile
import tkinter as tk
from PIL import ImageGrab
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from config import SLACK_TOKEN


class ScreenCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DiffTracker")

        # Slack 相关配置
        self.slack_token = SLACK_TOKEN  # 替换为你的 Slack API Token
        self.slack_channel = "#全体"  # 替换为你的 Slack 频道

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

    def send_image_to_slack(self, image_path):
        """
        将截图发送到 Slack 频道。

        Parameters:
            - image_path: str, 截图文件的路径。
        """
        # 将截图发送到 Slack 频道
        client = WebClient(token=self.slack_token)

        try:
            response = client.files_upload_v2(
                channel=self.slack_channel,
                file=image_path,
                initial_comment="Difference detected!",
            )
            print("File uploaded successfully:", response["file"]["name"])
        except SlackApiError as e:
            print(f"Error uploading file to Slack: {e.response['error']}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenCaptureApp(root)
    root.mainloop()
