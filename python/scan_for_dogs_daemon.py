import time
import os, json
import cv2
from _scan_for_dogs import scan_for_dogs

from _misc import ensure_directory_exists, go_to_script_directory, get_oldest_file, get_file_count

from _constants import TEMP_IMAGE_DIR

def get_image_and_delete(path):
    img = cv2.imread(path)

    os.remove(path)

    return img

# Takes a string like "../data/../2020-06-28_21:01:53.jpg" and turns it into "2020/06/28 21:04:01"
def get_date_from_file_name(filepath):
    filename = filepath.split(os.path.sep)[-1]
    date_time_string = filename.split('.')[0] \
        .replace('_', ' ') \
        .replace('-', '/')

    return date_time_string
    

dogs_found = 0
files_ran = 0
def scan_for_dogs_continuously():
    global dogs_found, files_ran
    go_to_script_directory()
    while True:
        file_count = get_file_count(TEMP_IMAGE_DIR)
        if file_count == 0:
            print('Found no images. Will try again in one second', end='\r')
            time.sleep(1)
            continue
        print('Previously found {} dog images out of {} total images. Found {} images waiting for processing. Processing oldest now...'.format(dogs_found, files_ran, file_count), end='\r')

        oldest_file_name = get_oldest_file(TEMP_IMAGE_DIR)

        date_string = get_date_from_file_name(oldest_file_name)

        img = get_image_and_delete(oldest_file_name)
        response = scan_for_dogs(img, date_string)
        if response is not None:
            dogs_found += 1
        files_ran += 1


scan_for_dogs_continuously()