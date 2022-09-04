import cv2
import numpy as np

HORIZONTAL_EDGE_LENGTH = 1080
VERTICAL_EDGE_LENGTH = 1920
TOP_BORDER_SIZE = 50
BOTTOM_BORDER_SIZE = 250
LEFT_BORDER_SIZE = 50
RIGHT_BORDER_SIZE = 50


def create(bg_img, logo_img):
    logo_img = cv2.imread(logo_img, cv2.IMREAD_UNCHANGED)
    logo_img = cv2.resize(logo_img, (0, 0), fx=0.5, fy=0.5)
    new_img = scale_img(bg_img)
    new_img_with_border = cv2.copyMakeBorder(new_img,
                                             TOP_BORDER_SIZE, BOTTOM_BORDER_SIZE, LEFT_BORDER_SIZE, RIGHT_BORDER_SIZE,
                                             cv2.BORDER_CONSTANT, value=(255, 255, 255))
    top_left_x, top_left_y, bottom_right_x, bottom_right_y = calc_logo_area(new_img_with_border, logo_img)
    # destination = new_img_with_border[int(top_left_y):int(bottom_right_y), int(top_left_x):int(bottom_right_x)]
    # result = cv2.addWeighted(destination, 0, logo_img, 1, 0)
    # new_img_with_border[int(top_left_y):int(bottom_right_y), int(top_left_x):int(bottom_right_x)] = result
    add_transparent_image(new_img_with_border, logo_img, int(top_left_x), int(top_left_y))

    # cv2.imshow("", new_img_with_border)
    # key = cv2.waitKey()
    cv2.imwrite("result.jpg", new_img_with_border)


def add_transparent_image(background, foreground, x_offset=None, y_offset=None):
    # https://stackoverflow.com/questions/40895785/using-opencv-to-overlay-transparent-image-onto-another-image
    bg_h, bg_w, bg_channels = background.shape
    fg_h, fg_w, fg_channels = foreground.shape

    assert bg_channels == 3, f'background image should have exactly 3 channels (RGB). found:{bg_channels}'
    assert fg_channels == 4, f'foreground image should have exactly 4 channels (RGBA). found:{fg_channels}'

    # center by default
    if x_offset is None:
        x_offset = (bg_w - fg_w) // 2
    if y_offset is None:
        y_offset = (bg_h - fg_h) // 2

    w = min(fg_w, bg_w, fg_w + x_offset, bg_w - x_offset)
    h = min(fg_h, bg_h, fg_h + y_offset, bg_h - y_offset)

    if w < 1 or h < 1:
        return

    # clip foreground and background images to the overlapping regions
    bg_x = max(0, x_offset)
    bg_y = max(0, y_offset)
    fg_x = max(0, x_offset * -1)
    fg_y = max(0, y_offset * -1)
    foreground = foreground[fg_y:fg_y + h, fg_x:fg_x + w]
    background_subsection = background[bg_y:bg_y + h, bg_x:bg_x + w]

    # separate alpha and color channels from the foreground image
    foreground_colors = foreground[:, :, :3]
    alpha_channel = foreground[:, :, 3] / 255  # 0-255 => 0.0-1.0

    # construct an alpha_mask that matches the image shape
    alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))

    # combine the background with the overlay image weighted by alpha
    composite = background_subsection * (1 - alpha_mask) + foreground_colors * alpha_mask

    # overwrite the section of the background image that has been updated
    background[bg_y:bg_y + h, bg_x:bg_x + w] = composite


def calc_logo_area(bg_img, to_add_img):
    bg_img_height, bg_img_width = bg_img.shape[0:2]
    to_add_img_height, to_add_img_width = to_add_img.shape[0:2]
    center_x = bg_img_width / 2
    center_y = bg_img_height - BOTTOM_BORDER_SIZE / 2
    half_to_add_img_width = to_add_img_width / 2
    half_to_add_img_height = to_add_img_height / 2
    top_left_x = center_x - half_to_add_img_width
    top_left_y = center_y - half_to_add_img_height
    bottom_right_x = center_x + half_to_add_img_width
    bottom_right_y = center_y + half_to_add_img_height
    return top_left_x, top_left_y, bottom_right_x, bottom_right_y


def scale_img(bg_img):
    origin_img = cv2.imread(bg_img)
    origin_height, origin_width = origin_img.shape[0:2]  # cv2.IMREAD_COLOR 返回值不止两个，取前面两个，注意是[高:宽]
    zoom_ratio = get_scale_ratio(origin_width, origin_height)
    return cv2.resize(origin_img, (0, 0), fx=zoom_ratio, fy=zoom_ratio)


def get_scale_ratio(origin_width, origin_height):
    if is_horizontal_pic(origin_width, origin_height):
        if origin_width > HORIZONTAL_EDGE_LENGTH:
            return (HORIZONTAL_EDGE_LENGTH - LEFT_BORDER_SIZE - RIGHT_BORDER_SIZE) / origin_width
    else:
        if origin_height > VERTICAL_EDGE_LENGTH:
            return (VERTICAL_EDGE_LENGTH - TOP_BORDER_SIZE - BOTTOM_BORDER_SIZE) / origin_height
    return 1


def is_horizontal_pic(width, height):
    if width > height:
        return True
    else:
        return False


if __name__ == '__main__':
    """
    功能说明：
    给图片添加白边框和 logo。后续可基于该代码进行批处理
    
    本代码思路：
    1. 将原图缩小到 1080p
    2. 给原图增加白边
    3. 添加 logo
    另外的思路：
    1. 缩放原图到 1080p
    2. 将给 logo 图片增加边框，使 logo 图片的宽和缩放后的原图等宽，注意：处理过后的 logo 图片高度为 250
    3. 拼接 logo 图片和原图
    4. 给拼接后的图片增加 50 边框
    """
    create(r"C:\xxx\DSC_4326.jpg", r"C:\xxx\logo.png")
