from os import listdir
import os
import cv2
import numpy as np
from PIL import Image
path = os.getcwd() + "\\final\\"
print(listdir(os.getcwd()+"\\final\\"))
files = (listdir(path))
for char in listdir(path):
    char_path = path + char + "\\"
    for file in listdir(char_path):
        img = cv2.imread(filename=char_path + file)
        if (1000 > np.sum(img == 255)):
            img = 255 - img
            pth = char_path + file
            img = Image.open(pth)
            img = np.array(img)
            print(img.shape, pth)
            #cv2.imwrite(filename=pth, img=img)
