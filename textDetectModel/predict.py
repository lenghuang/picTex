import numpy as np
from PIL import Image
import requests
from io import BytesIO
import cv2
import onnxruntime as nxrun
from classes import classes



model_path = "./models/pictex_100.pt"


def transform(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray_size = cv2.resize(img_gray, dsize=(32,32), interpolation=cv2.INTER_AREA)
    img_gray_size = np.array(img_gray_size)
    floatImage = np.float64(img_gray_size)
    #Scale image to be [0-1]
    floatImage /= 255
    floatImage += -0.5
    floatImage *= 2
    img = np.float32(floatImage)
    return img


def textPredict(image_path, local=False, is_path = True):
    sess = nxrun.InferenceSession("testing3.onnx")
    input_name = (sess.get_inputs()[0].name)

    if is_path:
        # Make new CNN object and load model
        # Load image from local
        # image = Image.open(image_path)
        # Load image from url
        # response = requests.get(image_path)
        image = image_path if local else BytesIO(requests.get(image_path).content)
        image = cv2.imread(image)
        image = np.expand_dims(transform(image), axis=0) # batch size of 1
        image = np.expand_dims(image, axis=0)
        print(image.shape, image.dtype)
        outputs = sess.run(None, {input_name: image})
        print(np.argmax(outputs))

        # print("Top predictions are:")
        # for i, index in enumerate(indices[0]):
        #     print(f"{classes[int(index)]} with value: {values[0][i]:>20}")
        return classes[np.argmax(outputs)]
    else:
        img = image_path.convert('RGB')
        img.show()
        image = np.array(img)
        image = np.expand_dims(transform(image), axis=0)  # batch size of 1
        image = np.expand_dims(image, axis=0)
        outputs = sess.run(None, {input_name: image})
        print(classes[np.argmax(outputs)])
        return classes[np.argmax(outputs)]



if __name__ == "__main__":
    # local image
    tempchar = 'a'
    image_path = "./final/" + tempchar + '/' + tempchar + "_fig_7.jpg"
    textPredict(image_path, True)
    # number 1
    # textPredict(
    #     "https://printables.space/files/uploads/download-and-print/large-printable-numbers/1-a4-1200x1697.jpg"
    # )
    # # number 5
    # textPredict(
    #     "https://gamedata.britishcouncil.org/sites/default/files/attachment/number-5_2.jpg",
    # )

