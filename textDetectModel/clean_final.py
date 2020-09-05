import cv2
import numpy as np
import collections
from PIL import Image
from urllib.request import urlopen
import numpy as np

def getAvgWhite(img_bw, debug=True):
    total_pixel = sorted(img_bw.flatten())
    total_pixel = list(filter(lambda num: num > 125,
                              total_pixel))
    std = np.std(total_pixel)
    mean = np.mean(total_pixel)

    thresh_min = mean-std
    thresh_max = mean+std
    return thresh_min, thresh_max, mean, std

def convert(image, debug=False):
    """
    Remove the background.
        1. Convert the image to a black and white mask.
        2. Get the average pixel color
        2. Group the white pixel together and find the largest contour
    """
    img_bw = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh_min, thresh_max, mean, std = getAvgWhite(img_bw)
    thresh_min = 0 if thresh_min < 0 else int(thresh_min)
    thresh_max = 255 if thresh_max > 255 else int(thresh_max)
    ret, img_bw_threshold = cv2.threshold(img_bw, thresh_min, thresh_max,
                                                  cv2.THRESH_BINARY)
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 8))
    img_bw_threshold = cv2.morphologyEx(img_bw_threshold, cv2.MORPH_CLOSE, k,
                            iterations=1)  # iter=2

    contours, hierarchy = cv2.findContours(
        img_bw_threshold, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_NONE
    )

    max_area = 0
    max_page_bw = None
    max_page_color = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            x, y, w, h = cv2.boundingRect(cnt)
            max_page_bw = img_bw[y:y + h, x:x + w]
            max_page_color = image.copy()[y:y + h, x:x + w]
            max_page_bw = cv2.resize(max_page_bw, dsize=(1050, 1485),
                                     interpolation=cv2.INTER_LINEAR_EXACT)
            max_page_color = cv2.resize(max_page_color, dsize=(1050, 1485),
                                        interpolation=cv2.INTER_LINEAR_EXACT)


    thresh_min = mean - 2*std
    ret, img = cv2.threshold(max_page_bw, thresh_min, 255, cv2.THRESH_BINARY_INV)


    if debug:
        threshPIL = Image.fromarray(img)  # thresh
        threshPIL.show(title="threshold_image")

    return img



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