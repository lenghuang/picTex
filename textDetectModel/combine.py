from objectDetection import objectDetection
from predict import textPredict
from PIL import Image
from torchvision import transforms
import requests
from io import BytesIO

# Transforms for prepping data to fit our model
transform = transforms.Compose([transforms.Grayscale(1)])

# Get's the top left x, top left y, width, and height of
# a Zach box or bbarray (bounding box array)
def getCut(bbarray):
    return (bbarray[2], bbarray[3], bbarray[4], bbarray[5])


def outputText(url, local=True):
    # bounding_list is a list of
    # [center x, center y, top left x, top left y, width, height, width + height]
    bounding_list = objectDetection(url)
    image = url if local else BytesIO(requests.get(url).content)
    image = transform(Image.open(image))
    first = bounding_list[4][10]
    x, y, w, h = getCut(first)
    cut_image = image.crop((x, y, x + w, y + h)).resize((200, 200))
    cut_image.show()

    # character_list = list(map(lambda img: textPredict(img, local=True), image_list))
    # print(character_list)


if __name__ == "__main__":
    outputText("examples/IMG_7311.jpg")

