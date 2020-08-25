import cv2
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, minimize
import numpy as np
import collections
from PIL import Image

def getAvgWhite(img_bw, debug=False):
    total_pixel = sorted(img_bw.flatten())
    total_pixel = list(filter(lambda num: num != 0 and num != 255,
                              total_pixel))
    pixel_dict = collections.Counter(total_pixel)
    pixel_x = []
    hist_y = []

    for grey_scale_value in sorted(pixel_dict.keys()):
        pixel_x.append(grey_scale_value)
        hist_y.append(pixel_dict[grey_scale_value])

    def gauss(x, mu, sigma, A):
        return A * np.exp(-(x - mu) ** 2 / 2 / sigma ** 2)

    def bimodal(x, mu1, sigma1, A1, mu2, sigma2, A2, mu3, sigma3, A3):
        return gauss(x, mu1, sigma1, A1) + gauss(x, mu2, sigma2, A2) + gauss(
            x, mu3, sigma3, A3)

    max_val1 = max(hist_y[:80])
    max_val2 = max(hist_y[100:200])
    try:
        max_val3 = max(hist_y[200:255])
    except ValueError:
        max_val3 = 1
    expected = (60, 17, max_val1, 170, 20, max_val2, 225, 17, max_val3)
    bounds = ([ 0.,   0.,       0., 100.,   0.,       0., 200.,   0.,       0.],
              [80., 255., max_val1, 200., 255., max_val2, 255., 255., max_val3])
    params, cov = curve_fit(bimodal, pixel_x, hist_y, expected,
                            bounds=bounds, maxfev=10800)
    func = lambda x: bimodal(x, *params)
    if debug:
        new_x = np.linspace(0, 255)
        new_y = func(new_x)
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(pixel_x, hist_y, "o")
        ax.plot(new_x, new_y, "-", lw=3)
        plt.show()

    #thresh = minimize(func, x0=100)["x"][0]
    params = list(params)
    max_hump = params.index(max(params))
    mean = params[max_hump-2]
    std  = params[max_hump-1]
    thresh_min = mean - 2*std
    thresh_max = mean + 2*std
    return thresh_min, thresh_max

def convert(image, debug=False):
    """
    Remove the background.
        1. Convert the image to a black and white mask.
        2. Get the average pixel color
        2. Group the white pixel together and find the largest contour
    """

    img_bw = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh_min, thresh_max = getAvgWhite(img_bw)
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

    """
    Remove any unwanted lines (red or blue)
        1. Check if there is any blue lines
        2. Remove any red lines.
    """
    img_copy = max_page_color.copy()
    hsv = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV_FULL)
    hist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])

    hist_list = hist.flatten().argsort()[-50:][::-1]
    blue_val = min(hist_list, key=lambda x:abs(x-38000))
    print(hist_list)
    elem = blue_val
    plt.imshow(hist, interpolation= 'nearest')
    plt.show()
    hue = elem // 256
    sat = elem % 256
    print(thresh_min, thresh_max, hue, sat, elem)
    thresh = (thresh_max + thresh_min)//2
    blue_min = np.array([hue - 20,  sat-40, 0]) #70])  # [89,10,0]
    blue_max = np.array([hue + 20, sat+40, 255]) #thresh]) # [140, 255, 255]
    blue_lines = cv2.inRange(hsv, blue_min, blue_max)

    if debug:
        max_page_color = cv2.cvtColor(max_page_color, cv2.COLOR_BGR2RGB)
        colorPIL = Image.fromarray(max_page_color)
        colorPIL.show(title="color")
        bluePIL = Image.fromarray(blue_lines)
        bluePIL.show(title="blue_lines")

    if (np.sum(blue_lines == 255) > 1000):
        """
        If there is a lot of blue in the image, 
        treat it like it is lined paper.
        """
        print("I THINK THIS IS A LINED PAPER")
        lined = True
    else:
        lined = False

    return
    print("return")
    if lined:
        # The way the hsv color system works red is 0-15 and 145-180
        # It basically loops around.

        red_min = np.array([140, 10, 70])
        red_max = np.array([180, 255, 255])
        frame_1 = cv2.inRange(hsv, red_min, red_max)

        red_min = np.array([0, 30, 0])
        red_max = np.array([15, 255, 255])
        frame_2 = cv2.inRange(hsv, red_min, red_max)
        red_lines = frame_1 + frame_2
        red_lines = cv2.morphologyEx(red_lines, cv2.MORPH_OPEN, (5, 5),
                                     iterations=10)
        red_lines = cv2.dilate(red_lines, (1, 1), iterations=5)
        if debug:
            redPIL = Image.fromarray(red_lines)
            redPIL.show(title="red_lines")

        img_t[:, :, :] = 255
        frame = red_lines + blue_lines
        mask = cv2.bitwise_and(img_t, img_t, mask=frame)
        mask = cv2.GaussianBlur(mask, (5, 5), 10)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, (5, 5), iterations=1)
        mask = cv2.dilate(mask, (1, 1), iterations=2)

        img_without_lines = cv2.bitwise_or(img, mask)

        if debug:
            maskPIL = Image.fromarray(img_without_lines)
            maskPIL.show(title="img")
    else:
        img_without_lines = img

    img_temp = img.copy()
    return


    ret, temp1 = cv2.threshold(temp, thresh, 255, cv2.THRESH_BINARY_INV)
    # temp = cv2.morphologyEx(temp, cv2.MORPH_OPEN, (5,5), iterations=1)
    temp = cv2.GaussianBlur(temp1, (5, 5), 0)
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 8))
    temp = cv2.morphologyEx(temp, cv2.MORPH_CLOSE, k,
                            iterations=1)  # iter=2
    thresh = temp

    if debug:
        threshPIL = Image.fromarray(temp1)  # thresh
        threshPIL.show(title="threshold_image")




    """
    Get the threshold
    """
    if lined:
        iteration_for_white = 4
    else:
        iteration_for_white = 3

    total_pixel = temp.flatten()
    white_list = list(filter(lambda x: x > 10, total_pixel))
    avg_white = sum(white_list) / len(white_list)
    for i in range(iteration_for_white):
        white_list = list(filter(lambda x: x < avg_white, white_list))
        avg_white = sum(white_list) / len(white_list)

    thresh = avg_white






    return

if __name__ == "__main__":
    urls = [
            "examples/IMG_7310.jpg",
        ]
    for url in urls:
        img = cv2.imread(url)  # local repository
        img = cv2.resize(img, dsize=(1050, 1485), interpolation=cv2.INTER_AREA)
        convert(img, debug=True)