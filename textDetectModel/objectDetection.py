from os.path import exists
from os import mkdir
from os import listdir
from urllib.request import urlopen

import argparse
import cv2
from matplotlib import cm
import numpy as np
from PIL import Image
import time

global thresh
global erode
global dilate

import string


def objectDetection(url, file_char=None, debug=False):
    """
    REQUIRES: url is a valid address to a local or online repository
    ENSURES: list of PIL images ordered by x,y position
    returnlist[i] refers to the ith row, sorted by center x position of objs
    returnlist[i][j] the jth obj in the ith row
    """
    try:
        """
        Load the image.
        """
        if exists(url):
            img = cv2.imread(url)  # local repository
        else:
            imgPIL = Image.open(urlopen(url))  # online
            img = np.array(imgPIL)

        img = cv2.resize(img, dsize=(1050, 1485), interpolation=cv2.INTER_AREA)
        # (1049, 1485)
        # Respects the dimensions of A3 paper

        """
        Remove any unwanted lines in the image.
        """
        img_t = img.copy()
        hsv = cv2.cvtColor(img_t, cv2.COLOR_BGR2HSV)
        blue_min = np.array([90, 5, 0])  # [89,10,0]
        blue_max = np.array([134, 255, 255])
        blue_lines = cv2.inRange(hsv, blue_min, blue_max)

        if debug:
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

        if file_char is not None:
            """
            Create a repository for the letter
            """
            path = "final/" + file_char
            try:
                mkdir(path)
            except FileExistsError:
                pass

            file_start = len(listdir(path))

        """
        Convert the image to a black and white mask.
        """
        temp = cv2.cvtColor(img_without_lines, cv2.COLOR_BGR2GRAY)

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

        ret, temp1 = cv2.threshold(temp, thresh, 255, cv2.THRESH_BINARY_INV)
        # temp = cv2.morphologyEx(temp, cv2.MORPH_OPEN, (5,5), iterations=1)
        temp = cv2.GaussianBlur(temp1, (5, 5), 0)
        k = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 8))
        temp = cv2.morphologyEx(temp, cv2.MORPH_CLOSE, k,
                                iterations=1)  # iter=2
        thresh = temp

        if debug:
            threshPIL = Image.fromarray(thresh)
            threshPIL.show(title="threshold_image")

        """
        Find the Contours.
        """
        # contours, hierarchy = cv2.findContours(thresh, 2, 1)
        contours, hierarchy = cv2.findContours(
            thresh, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_NONE
        )
        print("THERE ARE %d POSSIBLE OBJECTS" % len(contours))
        num = 0
        bboxs = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            x, y, w, h = cv2.boundingRect(cnt)
            buffer = 10
            if area > 130 and y > buffer and x > buffer:
                im2 = temp1[y - buffer:y + h + buffer,
                      x - buffer:x + w + buffer]
                im2 = cv2.resize(im2, dsize=(32, 32),
                                 interpolation=cv2.INTER_LINEAR_EXACT)

                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
                bboxs.append([(x) + w / 2, (y) + h / 2, x, y, w, h, y + h,
                              Image.fromarray(im2)])
                if file_char is not None:
                    file_name = "final/" + file_char + "/" + file_char + "_fig_" + \
                                str(num + file_start) + ".jpg"
                    cv2.imwrite(file_name, im2)

                    num += 1
        if debug:
            bboxPIL = Image.fromarray(img)
            bboxPIL.show(title="Bounding Boxes")

        """
        Sort objects found by lines.
        Top Left is (0,0).
        """

        bboxs.sort(key=lambda x: x[3])

        returnList = []

        currentLow = 0
        currentList = []
        for obj in bboxs:

            if obj[3] > currentLow:
                # if the high is below the low, switch to a new line
                if currentList != []:
                    currentList.sort(key=lambda x: x[2], reverse=True)
                    returnList.append(currentList)
                currentList = []
                currentLow = obj[6]
                currentList.append(obj)
            else:
                if obj[6] > currentLow:
                    currentLow = obj[6]
                currentList.append(obj)
        if debug:
            colors = [
                (255, 0, 0),
                (0, 255, 0),
                (0, 0, 255),
                (255, 255, 0),
                (0, 255, 255),
                (255, 0, 255),
                (255, 255, 255),
            ]
            for i in range(len(returnList)):
                for box in returnList[i]:
                    x = box[2]
                    y = box[3]
                    w = box[4]
                    h = box[5]
                    cv2.rectangle(img, (x, y), (x + w, y + h), colors[i%7], 2)

            coloredPIL = Image.fromarray(img)
            coloredPIL.show(title="Colored Lines.png")

        return returnList
    except ValueError:
        print("ValueError")
        return []


def cut_up_macro(file_char):
    file_name_0 = "macro_images/" + file_char + ".jpg"
    file_name_1 = "macro_images/" + file_char + ".jpeg"
    objectDetection(file_name_0, file_char, debug=False)
    objectDetection(file_name_1, file_char, debug=False)

def get_files(exclude_list=[]):
    """
    exclude_list: a list containing just the string of
    the classes already processed
    """
    data_dir = "./macro_images/"
    classes = listdir(data_dir)
    f = lambda x: True in map(
        lambda y: x.replace(".JPG", "").replace(".jpeg", "") in y, exclude_list)
    main = [item for item in classes if not f(item)]

    for char in main:
        file_char = char.replace(".JPG", "").replace(".jpeg", "")
        print("Current Character: ", letter)
        cut_up_macro(letter)

if __name__ == "__main__":
    alphabet = list(string.ascii_lowercase)
    # numbers = [str(i) for i in range(10)]
    """
    Creating a data set from macro_image
    """
    # Option 1:
    # run through all the macro_files and exclude the ones you don't want.
    # get_files(exclude_list=alphabet)
    # Option 2:
    # Either make a for loop and iterate through your own list
    # or run one letter at a time.
    # cut_up_macro("a")
    """
    Running objectDetection
    """
    url = "data/IMG_7302.jpg"
    objectDetection(url=url, debug=True)