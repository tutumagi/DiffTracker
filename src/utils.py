class ImagePathGenerator:
    def __init__(self, today_id):
        self.today_id = today_id
        self.index = 0

    def get_cur_screenshot_path(self):
        cur_img_id = f"{self.today_id}_{self.index}"
        cur_screenshot_path = f"./tmp/screenshot_{cur_img_id}.png"
        self.index += 1
        return cur_screenshot_path

    def get_last_screenshot_path(self):
        last_img_id = f"{self.today_id}_{self.index-1}"
        last_screenshot_path = f"./tmp/screenshot_{last_img_id}.png"
        return last_screenshot_path

    def get_final_diff_path(self):
        final_img_id = f"{self.today_id}_{self.index-1}_{self.index}"
        final_diff_path = f"./tmp/diff/{final_img_id}.png"
        return final_diff_path

    def get_tmp_screenshot_path(self):
        tmp_screenshot_path = f"./tmp/tmp_screenshot.png"
        return tmp_screenshot_path
