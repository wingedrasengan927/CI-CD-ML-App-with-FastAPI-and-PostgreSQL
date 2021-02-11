import tensorflow as tf
import numpy as np

model_path = "./saved_model"
model = tf.keras.models.load_model(model_path)

def get_sentiment(review):
    if type(review) != str:
        return
    sentiment =  model.predict(np.array([review]))
    return round(float(sentiment[0][0]), 2)