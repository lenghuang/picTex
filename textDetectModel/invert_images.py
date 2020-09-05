from os import listdir
import os
import cv2
import numpy as np
from PIL import Image
os.chdir("C:\\Users\\zacan\\Downloads\\final_imgs")
path = os.getcwd() + "\\" #+ "\\hasy\\"
print(listdir(os.getcwd()))#+"\\hasy\\"))
files = (listdir(path))
for char in listdir(path):
    char_path = path + char + "\\"
    print(char)
    for file in listdir(char_path):
        img = cv2.imread(filename=char_path + file)
        # check = char[0] <= 'a'
        #
        check = False
        if img is not None and (img == 255).sum() > 2000:
            print((img==255).sum(), char)
            check = True
        if (check): #used to be np.sum
            #img is not None
            img = 255 - img
            pth = char_path + file
            cv2.imwrite(filename=pth, img=img)
