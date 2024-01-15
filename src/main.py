import time
from capture import capture_area, select_area
from config import SLACK_TOKEN
from diff import compare, cp_image_path
from forward import SlackForward
from utils import ImagePathGenerator


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
