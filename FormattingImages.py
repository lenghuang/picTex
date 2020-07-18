import cv2.cv2 as cv
from matplotlib import pyplot as plt
from PIL import Image
import os, glob
import numpy as np
import time
print("cwd: ", os.getcwd())
obj = "b"
type = ".jpg"
total_fig = 179
try:
    os.makedirs("venv\lib\\" +obj)
except FileExistsError:
    pass

for filename in glob.glob("venv\\lib\\roi*"):
    os.remove(filename)
filename = "venv\\lib\\macro_images\\" + obj + type

with Image.open(filename) as image:
    if type == ".jpg":
        height, width = image.size
    else:
        width, height = image.size#switched
img = cv.imread(filename,0)
print("dim: ", width, height, np.shape(img))

#make char easier to detect
edges = cv.Canny(img,100,200)
print("edges1: ", np.shape(img))
plt.subplot(121),plt.imshow(img,cmap = 'gray')
kernel = np.ones((5,5),np.uint8)
edges = cv.dilate(edges,kernel,iterations = 1)#iter was 1

plt.title('original image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('edge image'), plt.xticks([]), plt.yticks([])
plt.show()

#segment image into each char
edges = cv.bitwise_not(edges)
#lines = cv.houghlines(edges,1,np.pi/2,2400,min_theta=np.pi/2)
lines = cv.HoughLines(edges,1,np.pi/2,2300,min_theta=np.pi/2)

lines = []
last_line_0 = True
last_line_1 = False
print(len(edges), len(edges[0]))

for i in range(height):
    num_of_zeros = 0
    for j in range(width):
        if(edges[i,j] == 0): # OG (i,j)
            num_of_zeros += 1

    #last line was a 0
    #this line is > 1
    if(last_line_0 and num_of_zeros > 0):
        lines.append(i)
        last_line_0 = False
        last_line_1 = True

    #last line > 1
    #this is 0
    if(last_line_1 and num_of_zeros == 0): # == 0
        lines.append(i) #was i
        last_line_0 = True
        last_line_1 = False

for i in range(int(len(lines)/2)):
    top = lines[2*i]
    bottom = lines[2*i + 1]
    print("top %d" %top, ", bot %d" %bottom)
    roi = edges[top:bottom, 0:width]
    name = "venv/lib/roi" + str(i) + ".png"
    cv.imwrite(name, roi)
    cv.line(img,(0,top),(width,top),(0,255,255),3)


for file in (os.listdir("venv/lib")):
    if(file.startswith("roi")):
        print(file)
        name = "venv/lib/"
        file_of_interest = cv.imread(name+file)

        with Image.open(name+file) as image:
            width, height = image.size
        print(name+file, "width: ", width, ", height: ", height)
        lines = []
        temp = file_of_interest
        last_line_1 = True
        last_line_0 = False
        for j in range(width):
            num_of_zeros = 0
            for i in range(height):
                if(temp[i][j].all(0)):
                    num_of_zeros += 1
            if(num_of_zeros != height):
                #print(num_of_zeros, j)
                num_of_zeros = 0;
            #last line was a 0
            #this line is > 1
            if(last_line_0 and num_of_zeros > 0):
                lines.append(j)
                last_line_0 = False
                last_line_1 = True

            #last line > 1
            #this is 0
            if(last_line_1 and num_of_zeros == 0):
                lines.append(j)
                last_line_0 = True
                last_line_1 = False

        print(lines)
        """
        for x in lines:
            print(x)
            cv.line(file_of_interest, (x, 0), (x, height), (0,255,255), 3)
        """
        for i in range(int(len(lines)/2)):
            left = lines[2 * i]
            right = lines[2 * i + 1]

            roi = file_of_interest[0:height, left:right]
            names = "venv/lib/" + obj + "/fig" + str(total_fig) + ".png"
            total_fig += 1

            #fix sigma with more generalized approach
            width = 224
            height = 224
            dim = (width, height)

            # resize image
            rroi = cv.resize(roi, dim, interpolation = cv.INTER_CUBIC)#cv.INTER
            cv.imwrite(names, rroi)

            cv.line(file_of_interest, (left, 0), (left, height), (0, 255,
                                                                  255), 3)
            cv.line(file_of_interest, (right,0), (right, height), (0,0,255),3)
            #print("right: ", right, "left: ", left, "(x,y): ", (left, 0))

        cv.imwrite(name+file, file_of_interest)
cv.imwrite('venv\lib\edges.jpg', edges)
cv.imwrite('venv\lib\houghlines3.jpg',img)