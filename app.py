""" Starts a Flash Web Application """
import os
from flask import Flask, request, render_template, jsonify
from daltonize import daltonize
import numpy as np
from PIL import Image
import cv2
from flask_cors import CORS
import base64


def apply_inhancment(src):
    orig_img = np.asarray(Image.open(src).convert("RGB"), dtype=np.float16)
    dl = daltonize
    orig_img = dl.gamma_correction(orig_img, 2.4)
    dalton_rgb = dl.daltonize(orig_img, 'd')
    dalton_img = dl.array_to_img(dalton_rgb, 2.4) 
    return (dalton_img)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads' 


@app.route('/upload', methods=['POST'])
def upload_image():
    """ sends image to func and returns edited image"""
    image = request.files['image']
    filename = "imagebfore.jpg"
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    processed_image = apply_inhancment(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    processed_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return {"image": encoded_string.decode('utf-8')}

cors = CORS(app, resources={r"/upload": {"origins": "*"}})
if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5001)