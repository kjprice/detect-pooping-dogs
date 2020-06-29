import os, json
from datetime import datetime

import cv2

from flask import Flask, request
from flask_cors import CORS

from _misc import ensure_directory_exists, go_to_script_directory

from _constants import TEMP_IMAGE_DIR

go_to_script_directory()
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
def receiveNewImage():
    print('Received Message - creating prediction')
    default_name = 'bad_data'
    image_name = request.form.get('fname', default_name)
    image_data = request.files['image']

    save_temporary_image(image_data)

    return ''