from objectDetection import objectDetection
from predict import textPredict
from PIL import Image
from torchvision import transforms
import requests
from io import BytesIO
import time

# https://pytorch.org/docs/stable/torchvision/transforms.html
# Interpolate?
# Transforms for prepping data to fit our model

def outputText(url, local=True):
    # bounding_list is a list of
    # [0: center x,
    #  1: center y,
    #  2: top left x,
    #  3: top left y,
    #  4: width,
    #  5: height,
    #  6: width + height,
    #  7: img]
    bounding_list = objectDetection(url)
    for obj in bounding_list[3]: # row 3
        img = obj[7]
        img.show()
        character_list = textPredict(img, is_path = False)
        print(character_list)


if __name__ == "__main__":
    outputText("examples/IMG_7311.jpg")

