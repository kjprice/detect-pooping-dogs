from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
import cv2

from nltk.corpus import wordnet

import os

model = ResNet50(weights='imagenet')

def name_exists_in_hypernym(name, syn):
    hypernyms = syn.hypernyms()
    
    if hypernyms is None or len(hypernyms) == 0:
        return False
    
    for hypernym in hypernyms:
        hypernym_name = syn.name()
        if name in hypernym_name:
            return True
        if name_exists_in_hypernym(name, hypernym):
            return True
    
    return False

def is_dog_in_image_prediction(prediction):
    prediction_name = prediction[1]
    
    if 'dog' in prediction_name:
        return True
    
    synsets = wordnet.synsets(prediction_name)
    if synsets is None or len(synsets) == 0:
        return False
    
    for syn in synsets:
        if name_exists_in_hypernym('dog', syn):
            return True
    return False

def is_dog_in_image_predictions(image_predictions):
    for prediction in image_predictions:
        if is_dog_in_image_prediction(prediction):
            return True
    return False
    

    
def get_image_predictions(img_raw):
    # image_filepath = get_test_image_path(image_name)
        
    # img = image.load_img(image_filepath, target_size=(224, 224))

    # x = image.img_to_array(img)

    img = cv2.resize(img_raw, (224, 224))

    x = img
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)
    
    return  decode_predictions(preds, top=3)[0]

# def predict_images():
#     for image_name in dog_images:
#         predictions = get_image_predictions(image_name)
        
#         return predictions

