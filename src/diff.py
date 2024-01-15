import time
from typing import Tuple
import cv2
import numpy as np
from cv2.typing import MatLike

from capture import capture_screen
from utils import ImagePathGenerator


def load_image(image_path):
    # Load the image
    return cv2.imread(image_path)


def remove_similar_part(current_image: MatLike, similar_mask: MatLike):
    # Invert the mask (if necessary) so the similar part is black (0)
    inverted_mask = cv2.bitwise_not(similar_mask)

    # Remove the similar part from the current image
    remaining_part = cv2.bitwise_and(current_image, current_image, mask=inverted_mask)

    return remaining_part


def find_common_content(last_img, cur_img):
    # Initiate SIFT detector
    sift = cv2.SIFT_create()

    # Find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(last_img, None)
    kp2, des2 = sift.detectAndCompute(cur_img, None)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # Store all the good matches as per Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    if len(good) > 10:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        # Find homography
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        # Warp image to fit the first one
        h, w, d = last_img.shape
        warped_img2 = cv2.warpPerspective(cur_img, M, (w, h))

        # Create a mask from the warped image
        gray_warped_img2 = cv2.cvtColor(warped_img2, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray_warped_img2, 1, 255, cv2.THRESH_BINARY)

        # Use the mask to extract the common region
        # common_region = cv2.bitwise_and(img1, img1, mask=mask)
        common_region = cv2.bitwise_and(cur_img, cur_img, mask=mask)
        # return common_region and mask
        return common_region, mask

    else:
        print("Not enough matches are found - {}/{}".format(len(good), 10))
        return None


def begin_capture(screenshot_path: str):
    x = 1807
    y = 105
    width = 445
    height = 709
    region = (x, y, x + width, y + height)
    capture_screen(region=region, save_path=screenshot_path)


def find_bounding_box(image: MatLike) -> Tuple[int, int, int, int]:
    # Convert to grayscale and threshold
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Get the bounding box of the largest contour
        x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
        return x, y, w, h
    else:
        return 0, 0, 0, 0


def remove_common_area(src: MatLike) -> MatLike:
    # Find bounding box of the remaining part
    x, y, w, h = find_bounding_box(src)
    # 如果相同区域过小，则不进行处理
    if w <= 2 or h <= 2:
        return None
    # Crop the image to the bounding box
    cropped_result = src[y : y + h, x : x + w]

    return cropped_result


def compare(last_screenshot_path: str, cur_screenshot_path: str, final_diff_path: str):
    last_img = load_image(last_screenshot_path)
    cur_img = load_image(cur_screenshot_path)

    # Find common content
    common_content, common_mask = find_common_content(last_img, cur_img)

    if common_content is not None:
        # common_path = "./tmp/common.png"
        # diff_path = "./tmp/diff.png"
        # Display the common content
        # cv2.imshow("Common Content", rest_img2_content)
        # cv2.imshow("Common Content", common_content)
        # put the common_content into an image
        # cv2.imwrite(common_path, common_content)
        diff_content = remove_similar_part(cur_img, common_mask)
        # cv2.imwrite(diff_path, diff_content)

        final_diff = remove_common_area(diff_content)
        if final_diff is not None:
            cv2.imwrite(final_diff_path, final_diff)
            return True
        else:
            print("Failed to find final diff.")

        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    else:
        print("Failed to find common content.")
    return False


if __name__ == "__main__":
    today_id = time.strftime("%Y%m%d", time.localtime())
    # 替换为你的截图保存路径和差异图片保存路径

    image_path_generator = ImagePathGenerator(today_id)

    # 第一次截图
    cur_screenshot_path = image_path_generator.get_cur_screenshot_path()
    begin_capture(cur_screenshot_path)
    while True:
        time.sleep(1)
        tmp_image_path = image_path_generator.get_tmp_screenshot_path()
        begin_capture(tmp_image_path)

        final_diff_path = image_path_generator.get_final_diff_path()
        if compare(
            image_path_generator.get_last_screenshot_path(),
            tmp_image_path,
            final_diff_path,
        ):
            # 将当前图片内容保存为上一次的图片内容
            last_img = load_image(tmp_image_path)
            cv2.imwrite(image_path_generator.get_cur_screenshot_path(), last_img)

        # time.sleep(5)
        # 如果输入任何键，则退出
        # if cv2.waitKey(0) != -1:
        #     break
