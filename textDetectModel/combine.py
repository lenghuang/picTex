from objectDetection import objectDetection
from predict import textPredict


def outputText(url):
    image_list = objectDetection(url)
    character_list = list(map(lambda img: textPredict(img), image_list))
    print(character_list)
