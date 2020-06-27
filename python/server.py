import os
from datetime import datetime

import cv2

from flask import Flask, request
from flask_cors import CORS

from _misc import ensure_directory_exists
from _scan_for_dogs import scan_for_dogs

DATA_DIR = os.path.join('..', 'data')
TEMP_IMAGE_DIR = os.path.join(DATA_DIR, 'temp-images')

ensure_directory_exists(TEMP_IMAGE_DIR)

app = Flask(__name__)
CORS(app)

def create_filename():
    now = datetime.now()
    dt_string = now.strftime("%Y-%m--%d_%H:%M:%S")

    return '{}.jpg'.format(dt_string)


def save_temporary_image(temp_file):
    file_name = create_filename()
    filepath = os.path.join(TEMP_IMAGE_DIR, file_name)

    temp_file.save(filepath)

    # Remove file from memory
    temp_file.close()

    return filepath

def get_actual_image(temp_file):
    filepath = save_temporary_image(temp_file)

    img = cv2.imread(filepath)

    # Remove file from file system once we read it
    os.remove(filepath)
    return img


@app.route('/newImage', methods=['POST'])
def receiveNeweImage():
    default_name = 'bad_data'
    image_name = request.form.get('fname', default_name)
    image_data = request.files['image']

    image = get_actual_image(image_data)

    is_dog = scan_for_dogs(image)

    return image_name