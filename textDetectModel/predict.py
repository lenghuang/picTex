from torchvision import datasets, transforms, models
from torch.utils.data.sampler import SubsetRandomSampler
import numpy as np
import torch
from net import Net
from classes import classes
from PIL import Image
import requests
from io import BytesIO

model_path = "./models/pictex_text_detect.pt"
image_path = "./datasets/our_images_final/a/fig0.png"

# Transforms for prepping data to fit our model
transform = transforms.Compose(
    [
        transforms.Grayscale(1),
        transforms.Resize((32, 32)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,)),
    ]
)


def predict(image_path, local=False):
    # Make new CNN object and load model
    model = Net()
    model.load_state_dict(torch.load(model_path))
    # Load image from local
    # image = Image.open(image_path)
    # Load image from url
    # response = requests.get(image_path)
    image = image_path if local else BytesIO(requests.get(image_path).content)
    image = transform(Image.open(image)).unsqueeze(0)
    outputs = model(image)
    print(outputs)
    values, indices = outputs.topk(5)
    print("Top predictions are:")
    for i, index in enumerate(indices[0]):
        print(f"{classes[index]} with value: {values[0][i]:>20}")


# local image
predict(image_path, True)
# number 1
predict(
    "https://printables.space/files/uploads/download-and-print/large-printable-numbers/1-a4-1200x1697.jpg"
)
# number 5
predict(
    "https://gamedata.britishcouncil.org/sites/default/files/attachment/number-5_2.jpg",
)

