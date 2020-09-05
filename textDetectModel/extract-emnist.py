from emnist import extract_training_samples
import numpy as np
from PIL import Image
import string
import os
import cv2

os.chdir("C:\\Users\\zacan\\Downloads\\final_imgs\\")

images, labels = extract_training_samples('digits')

list_of_lists = []
ls = [i for i in range(10)]
print(ls)
for i in range(10):
    folder = os.getcwd() + "\\" + str(i)
    if not os.path.exists(folder):
        os.mkdir(folder)
    list_of_lists.append([])

img = np.array(images[i])
temp = Image.fromarray(img)
#temp.show()
#print(string.ascii_lowercase[labels[i]-1])

amt = 15000
for label, image in zip(labels[:amt], images[:amt]):
    img = np.array(image)
    img = cv2.resize(img, (32,32), cv2.INTER_AREA)

    char = str(label)
    num = len(os.listdir(os.getcwd() + "\\" + char))
    cv2.imwrite(os.getcwd() + "\\" + char +"\\" + char + str(num) + ".png", img)

    list_of_lists[label-1].append(0)


sums = list(map(lambda x: len(x), list_of_lists))
print(sums)