from os.path import exists
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


def objectDetection(url):
    """
    REQUIRES: url is a valid address to a local or online repository
    ENSURES: list of PIL images ordered by x,y position
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
        imgPIL = Image.fromarray(img)
        img_temp = img.copy()
        # (1050, 1485)
        # Respects the dimensions of A4 paper

        """
        Convert the image to a black and white mask.
        """
        temp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        """
        Get the threshold
        """
        total_pixel = temp.flatten()
        white_list = list(filter(lambda x: x>10, total_pixel))
        avg_white = sum(white_list)/len(white_list)
        for i in range(2):
            white_list = list(filter(lambda x: x < avg_white, white_list))
            avg_white = sum(white_list)/len(white_list)

        thresh = avg_white
        dilate = 1
        erode = 0

        ret, temp = cv2.threshold(temp, thresh, 255, cv2.THRESH_BINARY_INV)
        temp = cv2.erode(temp, kernel=(5, 5), iterations=erode)
        temp = cv2.dilate(temp, kernel=(5, 5), iterations=dilate)
        thresh = temp

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
        bboxs = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            x, y, w, h = cv2.boundingRect(cnt)
            if area > 10:
                im2 = img_temp[y:y+h, x:x+w]
                im2 = cv2.resize(im2, dsize=(200, 200),
                                 interpolation=cv2.INTER_LINEAR_EXACT)

                #im3 = imgPIL.crop((x, y, x + w, y + h)).resize((200, 200))

                cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,0), 1)
                bboxs.append([(x) + w / 2, (y) + h / 2, x, y, w, h, y + h,
                              Image.fromarray(im2)])

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

        colors = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 0),
            (0, 255, 255),
            (255, 0, 255),
            (255, 255, 255),
        ]
        for i in range(7):
            for box in returnList[i]:
                x = box[2]
                y = box[3]
                w = box[4]
                h = box[5]
                cv2.rectangle(img, (x, y), (x + w, y + h), colors[i], 2)

        coloredPIL = Image.fromarray(img)
        coloredPIL.show(title="Colored Lines.png")
        return returnList
    except ValueError:
        print("ValueError")
        return []


if __name__ == "__main__":
    objectDetection("examples/IMG_7311.jpg")

