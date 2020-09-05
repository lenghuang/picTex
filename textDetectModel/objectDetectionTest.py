from os.path import exists
from os import mkdir
from os import listdir
from urllib.request import urlopen
import string
import argparse

import cv2
import numpy as np
from PIL import Image

from cleanTest import convert

def iou(cnt1, cnt2):
    # if 1 just return 0
    x1, y1, w1, h1 = cnt1[2:6]
    x2, y2, w2, h2 = cnt2[2:6]
    A1 = cnt1[8]
    A2 = cnt2[8]
    xA = max(x1, x2)
    yA = max(y1, y2)
    xB = min(x1+w1, x2+w2)
    yB = min(y1+h1, y2+h2)

    A1 = w1*h1
    A2 = w2*h2
    interArea = max(0, xB - xA) * max(0, yB - yA)

    iou = interArea / float(A1 + A2 - interArea)
    if iou == 1:
        iou = 0
    if iou > 0:
        print(iou)
    return iou

def formatBboxs(bboxs, idxSeen):
    """
    Requires: Given a list of bounding boxes
    bbox id: Description
        0: Center_X
        1: Center_Y
        2: Upper_Left_X
        3: Upper_Left_Y
        4: Width
        5: Height
        6: Y + Height
        7: PIL image of Contour
        8: Area
        9: idx
    Ensures: Returns a list of objects sorted by hierarchy and lines
    """
    """
    Sort by Hierarchy
    """
    #  Sort by Area
    bboxs.sort(key=lambda x: x[8], reverse=True)
    sortedList = []

    for box in bboxs:
        i = box[9]


        if i not in idxSeen:
            idxSeen.append(i)
            currentBboxs = list(filter(lambda x: x[9] not in idxSeen, bboxs))
            childBboxs = list(filter(lambda x: iou(box, x) > 0.1, currentBboxs))
            childIdxSeen = list(map(lambda x: x[9], childBboxs))
            childBboxs = formatBboxs(childBboxs, idxSeen)
            idxSeen.extend(childIdxSeen)
            box.append(childBboxs)
            sortedList.append(box)

    """
    Sort by Lines
    """
    bboxs = sortedList
    bboxs.sort(key=lambda x: x[3])

    returnList = []
    currentLow = 0
    currentList = []
    for obj in bboxs:
        if obj[3] > currentLow:
            # if the high is below the low, switch to a new line
            if currentList != []:
                currentList.sort(key=lambda x: x[2], reverse=False)
                returnList.append(currentList)
            currentList = []
            currentLow = obj[6]
            currentList.append(obj)
        else:
            if obj[6] > currentLow:
                currentLow = obj[6]
            currentList.append(obj)

    if currentList != []:
        returnList.append(currentList)

    return returnList

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
        Remove the background, lines, and threshold the image
        """
        thresh = convert(img, debug=False)

        """
        Find the Contours.
        """
        contours, hierarchy = cv2.findContours(
            thresh, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_NONE
        )
        print("There are %d Contours" % len(contours))
        bboxs = []
        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > 0:
                x, y, w, h = cv2.boundingRect(contour)
                img_white = np.ones(img.shape)*255
                cv2.drawContours(img_white, contours, i, (0,0,0), 3)
                cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 1)

                buffery = 0
                bufferx = 5
                if y-buffery < 0 or x-bufferx < 0:
                    buffery = 0
                    bufferx = 0
                img_contour = img_white[y - buffery:y + h + buffery,
                          x - bufferx:x + w + bufferx]
                img_contour = cv2.resize(img_contour, dsize=(32, 32),
                                 interpolation=cv2.INTER_LINEAR_EXACT)
                img_contour = 255 - img_contour # INVERTED TEMPORARY

                img_contour = img_contour.astype(np.uint8)
                info_list = [x + (w/2), y + (h/2), x, y, w, h, y + h,
                             Image.fromarray(img_contour), w*h, i]
                bboxs.append(info_list)

        if debug:
            imgPIL = Image.fromarray(img)  # thresh
            imgPIL.show(title="threshold_image")

        returnList = formatBboxs(bboxs, [])

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
                for j, box in enumerate(returnList[i]):
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


if __name__ == "__main__":
    """
    Running objectDetection
    """
    url = "examples/IMG_5496.jpeg"
    objectDetection(url=url, debug=False)