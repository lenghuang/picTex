from os.path import exists
from os import mkdir
from os import listdir
from urllib.request import urlopen
import string
import argparse

import cv2
import numpy as np
from PIL import Image

from clean_final import convert


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
        Find the Contours.
        """

        contours, hierarchy = cv2.findContours(
            thresh, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_NONE
        )
        temp = thresh.copy()
        print("THERE ARE %d POSSIBLE OBJECTS" % len(contours))
        num = 0
        bboxs = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            x, y, w, h = cv2.boundingRect(cnt)
            buffer = 10
            if area > 10 and y > buffer and x > buffer:
                im2 = temp[y - buffer:y + h + buffer,
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
    # alphabet = list(string.ascii_lowercase)
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
    url = "examples/IMG_7300.jpg"
    objectDetection(url=url, debug=True)