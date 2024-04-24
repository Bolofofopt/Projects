import os
os.environ["KERAS_BACKEND"] = "tensorflow"

import tensorflow as tf
import keras
import numpy as np
import matplotlib.pyplot as plt


load_model = keras.models.load_model('roses.keras')
load_model.summary()