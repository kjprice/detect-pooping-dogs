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

        oldest_file = get_oldest_file(TEMP_IMAGE_DIR)

        img = get_image_and_delete(oldest_file)
        response = scan_for_dogs(img)
        if response is not None:
            dogs_found += 1
        files_ran += 1


scan_for_dogs_continuously()