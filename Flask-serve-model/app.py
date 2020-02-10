
from flask import Flask, jsonify, render_template, request
from model import *
import torch
from urllib.request import urlopen
import torchvision.transforms as transforms
from PIL import Image
import requests
from io import BytesIO

model = inpainting_D_AVA()
device = torch.device("cpu")
model = model.to(device)

model.load_state_dict(torch.load("inpainting_D_AVA.pkl", map_location=torch.device('cpu')))
model.eval()

test_transform = transforms.Compose([
    transforms.Scale(256), 
    transforms.RandomCrop(224), 
    transforms.ToTensor()
    ])

def url_to_image(url):
    response = requests.get(url)
    im = Image.open(BytesIO(response.content))
    imt = test_transform(im)
    imt = imt.unsqueeze(dim=0)
    imt = imt.to(device)
    # return the image
    return imt

# webapp
app = Flask(__name__)

@app.route('/prediction', methods=['POST', 'GET'])
def prediction():

    imt = url_to_image(request.json['url'])
    with torch.no_grad():
        out = model(imt)
    out = out.view(10, 1)
    mean = 0.0
    for j, e in enumerate(out, 1):
        mean += j * e

    score = round(float(mean[0]), 2)
    words = ""

    if score >= 9:
        words = "Truly a remarkable capture, aesthetics score: " + str(score) + "/10"
    elif score >= 8:
        words = "Wonderful! Aesthetics score: " + str(score) + "/10"
    elif score >= 7:
        words = "What a great image, aesthetics score: " + str(score) + "/10"
    elif score >= 6:
        words = "A pretty good picture, aesthetics score: " + str(score) + "/10"
    elif score >= 5:
        words = "A decent shot, aesthetics score: " + str(score) + "/10"
    elif score >= 4:
        words = "A reasonable attempt, aesthetics score: " + str(score) + "/10"
    elif score >= 3:
        words = "A poor effort, surely you can do better.. aesthetics score: " + str(score) + "/10"
    elif score >= 2:
        words = "This image is quite bad to be honest. Aesthetics score: " + str(score) + "/10"
    elif score >= 1:
        words = "Hmm.. Surely your skills need lots of improvement. Aesthetics score: " + str(score) + "/10"
    else:
        words = "This is so bad. Aesthetics score:" + str(score) + "/10"

    return jsonify(str(words))

if __name__ == '__main__':
    app.run(debug=True)
