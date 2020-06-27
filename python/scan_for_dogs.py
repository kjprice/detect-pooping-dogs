#!/usr/bin/env python
import time
import cv2
import os
from datetime import datetime
import glob

import pandas as pd

from _classifier import get_image_predictions, is_dog_in_image_predictions

DATA_DIR = os.path.join('data')
IMAGE_PATH = os.path.join(DATA_DIR, 'screen-captures')
DOG_IMAGE_PATH = os.path.join(DATA_DIR, 'dog-images')
PREDICTIONS_CSV_PATH = os.path.join(DATA_DIR, 'predictions.csv')

cap = cv2.VideoCapture(0)

df = None


def ensure_directory_exists(directory):
    try:
        return os.makedirs(directory)
    except:
        return None
    
def get_dataframe():
    global df

    try:
        df = pd.read_csv(PREDICTIONS_CSV_PATH)
    except:
        df = pd.DataFrame()
    
    return df

def save_dataframe(df):
    df.to_csv(PREDICTIONS_CSV_PATH, index=False)


def get_normal_image_path(image_name):
    return os.path.join(IMAGE_PATH, image_name)

def get_dog_image_path(image_name):
    return os.path.join(DOG_IMAGE_PATH, image_name)

def save_image(filename, image):
    filepath = get_normal_image_path(filename)
    img = cv2.resize(image, (224, 224))

    out = cv2.imwrite(filepath, img)

def save_dog_image(filename, image):
    filepath = get_dog_image_path(filename)
    out = cv2.imwrite(filepath, image)

def get_image_from_cam():
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    return [frame, rgb]

def get_numbers_from_string(text):
    numbers = [s for s in text if s.isdigit()]
    if len(numbers) == 0:
        return None
    
    numbers_joined = ''.join(numbers)

    return int(numbers_joined)


def get_most_recent_file_count():
    try:
        glob_filepath = os.path.join(IMAGE_PATH, '*')
        list_of_files = glob.glob(glob_filepath)
    except Exception as e:
        print(e)
        return 0
    
    if len(list_of_files) == 0:
        return 0
    
    latest_file = max(list_of_files, key=os.path.getctime)

    print('latest_file', latest_file)

    file_number_count = get_numbers_from_string(latest_file)
    print('file_number_count', file_number_count)

    return file_number_count + 1



def create_dataframe_row(image_filename, predictions, is_dog):
    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")

    df_dict = {
        'filename': [image_filename],
        'is_dog': [is_dog],
        'date_ran': [dt_string]
    }

    for i, prediction in enumerate(predictions):
        df_dict['prediction_{}'.format(i)] = [prediction[1]]
        df_dict['confidence_{}'.format(i)] = [prediction[2]]
        
    df_record = pd.DataFrame(df_dict)

    return df_record

def save_predictions(image_filename, predictions, is_dog):
    global df
    new_df = create_dataframe_row(image_filename, predictions, is_dog)

    df = pd.concat([df, new_df], sort=False)
    

    save_dataframe(df)

found_dogs_count = 0
def main():
    global found_dogs_count

    ensure_directory_exists(IMAGE_PATH)
    ensure_directory_exists(DOG_IMAGE_PATH)

    get_dataframe()

    count = get_most_recent_file_count()
    print('Starting with file count {}'.format(count))
    while(True):
        print('count {}...found {} possible dogs'.format(count, found_dogs_count), end='\r')
        frame, rgb = get_image_from_cam()

        # cv2.imshow('frame', rgb)
        filename = 'image_{}.jpg'.format(count)
        save_image(filename, frame)

        predictions = get_image_predictions(frame)

        is_dog = is_dog_in_image_predictions(predictions)
        if is_dog:
            found_dogs_count += 1
            save_dog_image(filename, frame)

        save_predictions(filename, predictions, is_dog)


        count += 1
        time.sleep(3)

    cap.release()
    cv2.destroyAllWindows()

main()