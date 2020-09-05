import cv2
import numpy as np
from PIL import Image
from urllib.request import urlopen

def convert(image, debug = False):
    rgb_planes = cv2.split(image)

    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255,
                                 norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)

    result = cv2.merge(result_planes)
    result_norm = cv2.merge(result_norm_planes)

    result = 255 - result
    result_norm = 255 - result_norm
    result_norm = cv2.cvtColor(result_norm, cv2.COLOR_BGR2GRAY)
    ret, result_norm = cv2.threshold(result_norm, 100, 255, cv2.THRESH_BINARY)

    if debug:
        threshPIL = Image.fromarray(result_norm)  # thresh
        threshPIL.show(title="threshold_image")

    return result_norm


if __name__ == "__main__":

    urls = [
            "https://i.stack.imgur.com/VfmOK.png",
        ]

    for url in urls:
        img = Image.open(urlopen(url))
        img = np.array(img)
        img = cv2.resize(img, dsize=(1050, 1485), interpolation=cv2.INTER_AREA)
        img = convert(img, debug=True)
        print(img.shape)