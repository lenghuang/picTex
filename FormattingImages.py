import cv2 as cv
from matplotlib import pyplot as plt
from pil import image
import os, glob
import numpy as np
import time

print("cwd: ", os.getcwd())
obj = "times"
try:
    os.makedirs("venv\lib\\" + obj)
except fileexistserror:
    pass

for filename in glob.glob("venv\\lib\\roi*"):
    os.remove(filename)
filename = "venv\\lib\\macro_images\\" + obj + ".jpg"
with image.open(filename) as image:
    width, height = image.size
img = cv.imread(filename, 0)
print("dim: ", width, height)

# make char easier to detect
edges = cv.canny(img, 100, 200)
plt.subplot(121), plt.imshow(img, cmap='gray')
kernel = np.ones((5, 5), np.uint8)
edges = cv.dilate(edges, kernel, iterations=1)
plt.title('original image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(edges, cmap='gray')
plt.title('edge image'), plt.xticks([]), plt.yticks([])
plt.show()

# segment image into each char
edges = cv.bitwise_not(edges)
# lines = cv.houghlines(edges,1,np.pi/2,2400,min_theta=np.pi/2)
lines = cv.houghlines(edges, 1, np.pi / 2, 2300, min_theta=np.pi / 2)

lines = []
last_line_0 = true
last_line_1 = false

for i in range(width):
    num_of_zeros = 0
    for j in range(height):
        if (edges[i, j] == 0):
            num_of_zeros += 1

    # last line was a 0
    # this line is > 1
    if (last_line_0 and num_of_zeros > 0):
        lines.append(i)
        last_line_0 = false
        last_line_1 = true

    # last line > 1
    # this is 0
    if (last_line_1 and num_of_zeros == 0):
        lines.append(i)
        last_line_0 = true
        last_line_1 = false

for i in range(int(len(lines) / 2)):
    top = lines[2 * i]
    bottom = lines[2 * i + 1]
    roi = edges[top:bottom, 0:width]
    name = "venv\lib\roi" + str(i) + ".png"
    cv.imwrite(name, roi)
    cv.line(img, (0, top), (width, top), (0, 255, 255), 3)

total_fig = 0
for file in (os.listdir("venv\lib")):
    if (file.startswith("roi")):
        print(file)
        name = "venv\lib\\"
        file_of_interest = cv.imread(name + file)

        with image.open(name + file) as image:
            width, height = image.size
        print(name + file, "width: ", width, ", height: ", height)
        lines = []
        temp = file_of_interest
        last_line_1 = true
        last_line_0 = false
        for j in range(width):
            num_of_zeros = 0
            for i in range(height):
                if (temp[i][j].all(0)):
                    num_of_zeros += 1
            if (num_of_zeros != height):
                # print(num_of_zeros, j)
                num_of_zeros = 0;
            # last line was a 0
            # this line is > 1
            if (last_line_0 and num_of_zeros > 0):
                lines.append(j)
                last_line_0 = false
                last_line_1 = true

            # last line > 1
            # this is 0
            if (last_line_1 and num_of_zeros == 0):
                lines.append(j)
                last_line_0 = true
                last_line_1 = false

        print(lines)
        """
        for x in lines:
            print(x)
            cv.line(file_of_interest, (x, 0), (x, height), (0,255,255), 3)
        """
        for i in range(int(len(lines) / 2)):
            left = lines[2 * i]
            right = lines[2 * i + 1]

            roi = file_of_interest[0:height, left:right]
            names = "venv\lib\\" + obj + "\fig" + str(total_fig) + ".png"
            total_fig += 1

            # fix sigma with more generalized approach
            width = 200
            height = 200
            dim = (width, height)

            # resize image
            rroi = cv.resize(roi, dim, interpolation=cv.inter_area)
            cv.imwrite(names, rroi)

            cv.line(file_of_interest, (left, 0), (left, height), (0, 255,
                                                                  255), 3)
            cv.line(file_of_interest, (right, 0), (right, height), (0, 0, 255),
                    3)
            # print("right: ", right, "left: ", left, "(x,y): ", (left, 0))

        cv.imwrite(name + file, file_of_interest)
cv.imwrite('venv\lib\edges.jpg', edges)
cv.imwrite('venv\lib\houghlines3.jpg', img)