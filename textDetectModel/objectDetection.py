from os.path import exists
from urllib.request import urlopen
import argparse
import cv2
from PIL import Image

global thresh
global erode
global dilate


def objectDetection(url):
    """
    REQUIRES: url is a valid address to a local or online repository
    ENSURES: list of images ordered by x,y position
    """
    global thresh
    global erode
    global dilate
    try:
        """
        Load the image.
        """
        if exists(url):
            img = cv2.imread(url)  # local repository
        else:
            img = Image.open(urlopen(url))  # online

        img = cv2.resize(img, dsize=(1050, 1485), interpolation=cv2.INTER_AREA)
        # img = cv2.resize(img, dsize=(200, 300), interpolation=cv2.INTER_AREA)
        # Respects the dimensions of A4 paper

        """
        Convert the image to a black and white mask.
        """
        named_window = "image"
        thresh = 140
        dilate = 1
        erode = 0

        # def change_thresh(val):
        #     global thresh
        #     thresh = val
        #     process()

        # def change_dilate(val):
        #     global dilate
        #     dilate = val
        #     process()

        # def change_erode(val):
        #     global erode
        #     erode = val
        #     process()

        # # function that processes the image
        # def process():
        #     global thresh
        #     global erode
        #     global dilate
        #     temp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #     ret, temp = cv2.threshold(temp, thresh, 255, cv2.THRESH_BINARY_INV)
        #     temp = cv2.erode(temp, kernel=(1, 5), iterations=erode)
        #     temp = cv2.dilate(temp, kernel=(1, 5), iterations=dilate)
        #     cv2.imshow(named_window, temp)

        # cv2.namedWindow(named_window)

        # cv2.createTrackbar("thresh: ", named_window, 0, 255, change_thresh)
        # cv2.createTrackbar("erode: ", named_window, 0, 255, change_erode)
        # cv2.createTrackbar("dilate: ", named_window, 0, 255, change_dilate)
        # process()
        # cv2.waitKey(0)

        temp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, temp = cv2.threshold(temp, thresh, 255, cv2.THRESH_BINARY_INV)
        temp = cv2.erode(temp, kernel=(5, 5), iterations=erode)
        temp = cv2.dilate(temp, kernel=(5, 5), iterations=dilate)
        thresh = temp

        """
        Find the Contours.
        """
        # contours, hierarchy = cv2.findContours(thresh, 2, 1)
        contours, hierarchy = cv2.findContours(
            thresh, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_NONE
        )
        print("THERE ARE %d OBJECTS" % len(contours))
        bboxs = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            x, y, w, h = cv2.boundingRect(cnt)
            if area > 10:
                im2 = img[y - 10 : y + h - 10, x : x + w]
                im2 = cv2.resize(im2, dsize=(200, 200), interpolation=cv2.INTER_LINEAR)

                # cv2.imshow("img", im2)
                # cv2.waitKey(0)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
                bboxs.append([(x) + w / 2, (y) + h / 2, x, y, w, h, y + h])

        # cv2.imshow("Bounding Boxes", img)
        # cv2.waitKey(0)

        """
        Sort objects found by lines.
        Top Left is (0,0).
        """
        heights = [i[5] for i in bboxs]
        avgHeight = sum(heights) / len(heights)
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

        # cv2.imshow("One Line", img)
        # cv2.waitKey(0)

        # print(returnList)
        return returnList
    except ValueError:
        print("valueError")
        return []


if __name__ == "__main__":
    objectDetection("examples/IMG_7311.jpg")

