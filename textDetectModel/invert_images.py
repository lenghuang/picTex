from os import listdir
import os
import cv2
import numpy as np
from PIL import Image
# os.chdir("C:\\Users\\zacan\\Downloads\\final_imgs")

path = os.getcwd() + "\\final_imgs\\" #+ "\\hasy\\"
# print(listdir(os.getcwd()))#+"\\hasy\\"))
files = (listdir(path))
# for char in listdir(path):
#     char_path = path + char + "\\"
#     print(char)
#     for file in listdir(char_path):
#         img = cv2.imread(filename=char_path + file)
#         # check = char[0] <= 'a'
#         #
#         check = False
#         if img is not None and (img == 255).sum() > 2000:
#             print((img==255).sum(), char)
#             check = True
#         if (check): #used to be np.sum
#             #img is not None
#             img = 255 - img
#             pth = char_path + file
#             cv2.imwrite(filename=pth, img=img)
for char in listdir(path):
    char_path = path + char + "\\"
    for file in listdir(char_path):
        img = cv2.imread(filename=char_path + file)

        if (char == '9'):
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(
                img, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_NONE
            )
            max_area = 0
            img_contour = None
            for i, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if area > max_area:
                    max_area = area
                    x, y, w, h = cv2.boundingRect(contour)
                    #img_white = np.ones(img.shape) * 255
                    #cv2.drawContours(img_white, contours, i, (0, 0, 0), 3)
                    #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)

                    buffery = 0
                    bufferx = 4
                    print(x)
                    if x - bufferx < 0:
                        buffery = 0
                        bufferx = x
                    img_contour = img[y - buffery:y + h + buffery,
                                  x - bufferx:x + w + bufferx]
                    img_contour = cv2.resize(img_contour, dsize=(32, 32),
                                             interpolation=cv2.INTER_LINEAR_EXACT)
                    #img_contour = 255 - img_contour  # INVERTED TEMPORARY

                    #img_contour = img_contour.astype(np.uint8)

            cv2.imshow("TEMP", img_contour)
            cv2.imshow("REAL", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


            pth = char_path + file
            #cv2.imwrite(filename=pth, img=img)