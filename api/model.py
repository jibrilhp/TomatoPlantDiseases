import tensorflow as tf
import numpy as np
import json
import requests

SIZE=256
MODEL_URI='http://localhost:8501/v1/models/plants:predict'


def get_prediction(image_path):
    image = tf.keras.preprocessing.image.load_img(image_path, target_size=(SIZE, SIZE))
    image = tf.keras.preprocessing.image.img_to_array(image)
    img = image.reshape(1, SIZE, SIZE, 3)
    img = img.astype('float32')
    img = img /255.0
    # image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
    # image = np.expand_dims(image, axis=0)

    data = json.dumps({
        'instances': img.tolist()
    })
    response = requests.post(MODEL_URI, data=data.encode('utf-8'))
    result = json.loads(response.text)
    print(result['predictions'][0])
    result = list(result['predictions'][0]).index(max(result['predictions'][0]))
    if result == 0:
        prediction = 'Bacterial Spot'
    elif result == 1:
        prediction = 'Early Blight'
    elif result == 2:
        prediction = 'Late Blight'
    elif result == 3:
        prediction = 'Leaf Mold'
    elif result == 4:
        prediction = 'Septoria Leaf Spot'
    elif result == 5:
        prediction = 'Spider Mites'
    elif result == 6:
        prediction = 'Target Spot'
    elif result == 7:
        prediction = 'Yellow Leaf Curl Virus'
    elif result == 8:
        prediction = 'Mosaic Virus'
    else:
        prediction = 'Healthy'
    # prediction = np.squeeze(result['predictions'][0])
    # class_name = CLASSES[int(prediction > 0.5)]
    return prediction
