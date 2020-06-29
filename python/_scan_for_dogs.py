#!/usr/bin/env python
import math, os
from datetime import datetime
import time

import cv2

import pandas as pd

from _classifier import get_image_predictions, is_dog_in_image_predictions
from _misc import ensure_directory_exists, go_to_script_directory, get_most_recent_file

go_to_script_directory()

DATA_DIR = os.path.join('..', 'data')
IMAGE_PATH = os.path.join(DATA_DIR, 'screen-captures')
IMAGES_PIECES_PATH = os.path.join(DATA_DIR, 'image-pieces')
DOG_IMAGE_PATH = os.path.join(DATA_DIR, 'dog-images')
PREDICTIONS_CSV_PATH = os.path.join(DATA_DIR, 'predictions.csv')

RUN_TESTS = (__name__ == "__main__")

SAVE_IMAGE_PIECES = RUN_TESTS

df = None

REQUIRED_CONFIDENCE_FOR_DOG = 0.25 # 25% confidence
HIGH_CONFIDENCE_FOR_DOG = 0.75

def get_dataframe():
    global df

    if df is not None:
        return

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

    cv2.imwrite(filepath, img)

def save_dog_image(filename, image):
    filepath = get_dog_image_path(filename)
    cv2.imwrite(filepath, image)

def get_numbers_from_string(text):
    numbers = [s for s in text if s.isdigit()]
    if len(numbers) == 0:
        return None
    
    numbers_joined = ''.join(numbers)

    return int(numbers_joined)

def get_most_recent_file_count(filepath):
    latest_file = get_most_recent_file(filepath)
    if latest_file is None:
        return 0

    file_number_count = get_numbers_from_string(latest_file)
    return file_number_count + 1

def get_starting_file_count():
    dog_file_count = get_most_recent_file_count(DOG_IMAGE_PATH)
    non_dog_file_count = get_most_recent_file_count(IMAGE_PATH)

    return max(dog_file_count, non_dog_file_count)



def create_dataframe_row(image_filename, max_dog_prediction_score, max_dog_prediction_name, predicted_items, date_string):
    df_dict = {
        'filename': [image_filename],
        'dog_score': [max_dog_prediction_score],
        'dog_name': [max_dog_prediction_name],
        'date': date_string
    }

    for i, prediction in enumerate(predicted_items):
        df_dict['prediction_{}'.format(i)] = [prediction['name']]
        df_dict['confidence_{}'.format(i)] = [prediction['score']]
        
    df_record = pd.DataFrame(df_dict)

    return df_record

def save_predictions(filename, max_dog_prediction_score, max_dog_prediction_name, predicted_items, date_string):
    global df
    new_df = create_dataframe_row(filename, max_dog_prediction_score, max_dog_prediction_name, predicted_items, date_string)

    df = pd.concat([df, new_df], sort=False)
    

    save_dataframe(df)

def crop_image(image_raw, pixels_to_remove_width, pixels_to_remove_height):
    height, width, colors = image_raw.shape
    
    x = [0, width]
    y = [0, height]

    if pixels_to_remove_width is not None and pixels_to_remove_width != 0:
        half_diff = math.ceil(pixels_to_remove_width / 2)
        start_x = half_diff
        end_x = width - half_diff
        x = [start_x, end_x]
    if pixels_to_remove_height is not None and pixels_to_remove_height != 0:
        half_diff = math.ceil(pixels_to_remove_height / 2)
        start_y = half_diff
        end_y = height - half_diff
        y = [start_y, end_y]

    return image_raw[y[0]:y[1], x[0]:x[1]]

# This turns an image into a perfect square
def crop_image_to_square(image_raw):
    height, width, colors = image_raw.shape
    
    pixels_to_remove_width = 0
    pixels_to_remove_height = 0
    
    if width > height:
        pixels_to_remove_width = width - height
    elif height > width:
        pixels_to_remove_height = height - width

    
    return crop_image(image_raw, pixels_to_remove_width, pixels_to_remove_height)

# This crops into the size that the neural network requires
def format_image(image_raw):
    cropped_image = crop_image_to_square(image_raw)
    return cv2.resize(cropped_image, (224, 224))

# Splits the images into squares over the rows and columns
def get_image_pieces(image, use_buffer_x=False, use_buffer_y = False):
    OPTIMAL_SQUARE_DIMENSION = 224
    height, width, channels = image.shape

    x_buffer = 0 if not use_buffer_x else OPTIMAL_SQUARE_DIMENSION
    y_buffer = 0 if not use_buffer_y else OPTIMAL_SQUARE_DIMENSION

    height_without_buffer = height - y_buffer
    width_without_buffer = width - x_buffer

    max_columns = int(height_without_buffer / OPTIMAL_SQUARE_DIMENSION) # Round down

    max_rows = int(width_without_buffer / OPTIMAL_SQUARE_DIMENSION) 

    pixels_lost_width = (width_without_buffer % OPTIMAL_SQUARE_DIMENSION) + x_buffer
    pixels_lost_height = (height_without_buffer % OPTIMAL_SQUARE_DIMENSION) + y_buffer

    cropped_image = crop_image(image, pixels_lost_width, pixels_lost_height)

    image_pieces = []
    for n in range(max_columns):
        y_start = n * OPTIMAL_SQUARE_DIMENSION
        y_end = (n + 1) * OPTIMAL_SQUARE_DIMENSION
        y = [y_start, y_end]
        for i in range(max_rows):
            x_start = i * OPTIMAL_SQUARE_DIMENSION
            x_end = (i + 1) * OPTIMAL_SQUARE_DIMENSION
            x = [x_start, x_end]

            image_piece = image[y[0]:y[1], x[0]:x[1]]
            image_pieces.append(image_piece)

    return image_pieces


def save_image_pieces(directory_index, image_pieces):
    if not SAVE_IMAGE_PIECES:
        return
    directory_path = os.path.join(IMAGES_PIECES_PATH, str(directory_index))
    ensure_directory_exists(directory_path)

    for i, image in enumerate(image_pieces):
        file_name = '{}.jpg'.format(i)
        filepath = os.path.join(directory_path, file_name)

        cv2.imwrite(filepath, image)

def create_all_image_pieces(image_raw):
    image_pieces = []
    
    normal_image_pieces = get_image_pieces(image_raw)
    save_image_pieces(0, normal_image_pieces)
    image_pieces += normal_image_pieces

    left_buffer_image_pieces = get_image_pieces(image_raw, True)
    image_pieces += left_buffer_image_pieces
    save_image_pieces(1, left_buffer_image_pieces)

    top_buffer_image_pieces = get_image_pieces(image_raw, False, True)
    image_pieces += top_buffer_image_pieces
    save_image_pieces(2, top_buffer_image_pieces)

    top_and_left_buffer_image_pieces = get_image_pieces(image_raw, True, True)
    image_pieces += top_and_left_buffer_image_pieces
    save_image_pieces(3, top_and_left_buffer_image_pieces)

    return image_pieces

def add_high_probability_items_to_cache(predictions, items_dict):
    for prediction in predictions:
        name = prediction[1]
        score = prediction[2]
        if score > .30:
            if name not in items_dict.keys():
                items_dict[name] = score
                continue

            original_score = items_dict[name]
            if score > original_score:
                items_dict[name] = score

def get_dog_prediction(image_raw):
    image_pieces = create_all_image_pieces(image_raw)

    max_dog_prediction_score = 0
    max_dog_prediction_name = ''
    predicted_items_dict = {}

    for image in image_pieces:
        predictions = get_image_predictions(image)
        add_high_probability_items_to_cache(predictions, predicted_items_dict)
        [is_dog, prediction] = is_dog_in_image_predictions(predictions)
        if is_dog:
            prediction_score = prediction[2]
            prediction_name = prediction[1]
            if prediction_score > max_dog_prediction_score:
                max_dog_prediction_score = float(prediction_score)
                max_dog_prediction_name = prediction_name
    
    # Minimum threshold for a doggie
    if max_dog_prediction_score < REQUIRED_CONFIDENCE_FOR_DOG:
        return None

    predicted_items = []
    for predicted_name in predicted_items_dict.keys():
        score = predicted_items_dict[predicted_name]
        predicted_items.append({
            'score': score,
            'name': predicted_name
        })

    return [max_dog_prediction_score, max_dog_prediction_name, predicted_items]

def get_date():
    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")

    return dt_string

def scan_for_dogs(image_raw, date_string = None):
    ensure_directory_exists(IMAGE_PATH)
    ensure_directory_exists(DOG_IMAGE_PATH)
    ensure_directory_exists(IMAGES_PIECES_PATH)

    
    dog_prediction = get_dog_prediction(image_raw)

    start_count = get_starting_file_count()
    filename = 'image_{}.jpg'.format(start_count)
    if dog_prediction is None:
        small_image = format_image(image_raw)
        save_image(filename, small_image)
        return None
    
    max_dog_prediction_score, max_dog_prediction_name, predicted_items = dog_prediction

    get_dataframe()

    save_dog_image(filename, image_raw)

    if date_string is None:
        date_string = get_date()

    save_predictions(filename, max_dog_prediction_score, max_dog_prediction_name, predicted_items, date_string)
    end = time.time()

    return [max_dog_prediction_name, max_dog_prediction_score]


def run_test():
    print('This appears to not be ran as a dependency file...running tests')
    TEMP_IMAGE_DIR = os.path.join(DATA_DIR, 'test-images')

    TEST_IMAGE_FILEPATH = os.path.join(TEMP_IMAGE_DIR, 'dog-park.jpeg')

    ensure_directory_exists(TEMP_IMAGE_DIR)

    image = cv2.imread(TEST_IMAGE_FILEPATH)

    is_dog_response = scan_for_dogs(image)

    if is_dog_response is None:
        raise AssertionError('The image is aparently not a dog, but we expect it to be')

    [dog_name, dog_score] = is_dog_response

    if dog_name != 'English_setter':
        raise AssertionError('Expected the prediction to be a ')

    print('Test completed and the image was found to be a "{}" correctly with a {} score'.format(dog_name, dog_score))

if RUN_TESTS:
    run_test()

    
