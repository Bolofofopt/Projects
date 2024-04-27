### What I Learned:
    - Neural Networks
    - Computer Vision
    - Keras Framework
    - TensorFlow Backend

### Skills Improved:
    - Python

### Softwares/Tools/Code Languages Used:
    - Python
    - TensorFlow
    - Keras

# Neural Networks Projects
These projects were built when working for Thales- Ground Transportation Systems Portugal, they were built for training purpurses because I developed an Artificial Intelligence for CCTVs in the context of RailRoad security and needed some grounds first before finishing the main project

### Framework used
The framework used was Keras with TensorFlow as backend



# flores_AI
This AI model helps identify different types of flowers.
## How it works
## How the code works
First I needed to import dependecies and download the dataset I wanted:
```python
import os
os.environ["KERAS_BACKEND"] = "tensorflow"
import matplotlib.pyplot as plt
import numpy as np
import PIL
import tensorflow as tf
import keras
from keras import layers
from keras.models import Sequential

import pathlib

dataset_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz"
data_dir = tf.keras.utils.get_file('flower_photos.tar', origin=dataset_url, extract=True)
data_dir = pathlib.Path(data_dir).with_suffix('')
checkpoint_path = "training_1/cp.weights.h5"
checkpoint_dir = os.path.dirname( checkpoint_path )
```
I used for this context a dataset that tensorflow has for this model.

Then after getting the dataset I defined some very imported variables like image height and width, how many images are in the dataset, the batch size and the number of epochs for training and standardization purposes.
```python
image_count = len(list(data_dir.glob('*/*.jpg')))
print(image_count)

BATCH_SIZE = 32
IMG_HEIGHT = 180
IMG_WIDTH = 180
EPOCHS=10
```

After that I split the data in 2 datasets, a training dataset and a validation one
```python
train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE)

val_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE)

class_names = train_ds.class_names
print(class_names)
```
Then I standarlize the training data and assigned a label to it
```python

plt.figure(figsize=(10, 10))
for images, labels in train_ds.take(1):
    for i in range(9):
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(images[i].numpy().astype("uint8"))
        plt.title(class_names[labels[i]])
        plt.axis("off") 

for image_batch, labels_batch in train_ds:
    print(image_batch.shape)
    print(labels_batch.shape)
    break

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

normalization_layer = layers.Rescaling(1./255)
normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
image_batch, labels_batch = next(iter(normalized_ds))
first_image = image_batch[0]
print(np.min(first_image), np.max(first_image))
```
The only thing that's left is the define the model, compile it, load weights (previous epochs) and fit the model
```python
num_classes = len(class_names)

model = Sequential([
    layers.Rescaling(1./255, input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes)
])

model.compile(optimizer='adam',
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=['accuracy'])
model.load_weights( checkpoint_path )
model.summary()

# test_loss, test_acc = model.evaluate( train_ds, val_ds, verbose=2 )
import math
n_batches = len(image_batch) / BATCH_SIZE
n_batches = math.ceil(n_batches)
cp_callback = keras.callbacks.ModelCheckpoint( filepath=checkpoint_path,
                                                save_weights_only=True,
                                                verbose=1,
                                                save_freq=5*n_batches)


history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    callbacks=[ cp_callback ])
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

print( '\nRestored Model, Test accuracy:', val_acc )


epochs_range = range(EPOCHS)
```
To optimise the model I saved via checkpoint it's weights after each 5 epochs via math, then before I fitted the model, this is trainin g the model I loaded weights from the last checkpoint.

To finish I tested the model and saved it:
```python
epochs_range = range(EPOCHS)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

model.save('roses.keras')
```
### To use the model in another environment:
Just load the model that was saved, copy some functions that are needed because they complement the model (they are not apart of it so they don't get saved) 
```python
import os
os.environ["KERAS_BACKEND"] = "tensorflow"

import tensorflow as tf
import keras
import numpy as np
import matplotlib.pyplot as plt


load_model = keras.models.load_model('roses.keras')
load_model.summary()
```
## Model efficiency
On these 2 graphs we can see the model efficiency based on a few EPOCHs, these graphs are from the flores_AI model but the architecture and the model training is the same for both models (flores_AI & clothes_AI)

For the first 10 Epochs:

![Figure1](https://github.com/Bolofofopt/Public_Projects/assets/145719526/6a4008d2-d820-4bce-8ead-59df74d2c6d3)

For the 10 to 20 Epochs:

![Figure2](https://github.com/Bolofofopt/Public_Projects/assets/145719526/c52c3071-419f-4a6b-aa29-f27fc0761d22)



## Results
![image](https://github.com/Bolofofopt/Public_Projects/assets/145719526/f15dff3a-3597-4023-8272-7709327eb092)

# clothes_AI
This AI model helps identify different types of clothes
## How it works
## How the code works
First the libraries & download the dataset:
```python
import os
os.environ["KERAS_BACKEND"] = "tensorflow"

import tensorflow as tf
import keras
import numpy as np
import matplotlib.pyplot as plt

# tf.keras.datasets.fashion_mnist.load_data()

fashion_mnist = tf.keras.datasets.fashion_mnist
( train_images, train_labels ), ( test_images, test_labels ) = fashion_mnist.load_data()
```
Then define class names, split train data and validation data & create the model:
```python
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

train_images = train_images / 255.0
test_images = test_images / 255.0


def create_model():
    model = tf.keras.Sequential([
    tf.keras.layers.Flatten( input_shape=( 28, 28 ) ),
    tf.keras.layers.Dense( 128, activation="relu" ),
    tf.keras.layers.Dense( 10 )])

    model.compile( optimizer='adam',
                    loss=tf.keras.losses.SparseCategoricalCrossentropy( from_logits=True ),
                    metrics=[ 'accuracy' ])
    return model
model = create_model()

model.summary()
```
Model optimization via checkpoints:
```python
checkpoint_path = "training_1/cp.weights.h5"
checkpoint_dir = os.path.dirname( checkpoint_path )

model.load_weights( checkpoint_path )
test_loss, test_acc = model.evaluate( test_images, test_labels, verbose=2 )
print( '\nRestored Model, Test accuracy:', test_acc )
```
Probability model, checkpoints configuration & model training&saving
```python
probability_model = tf.keras.Sequential( [model,
                                            tf.keras.layers.Softmax()] )
predictions = probability_model.predict( test_images )

predictions[ 0 ]
np.argmax( predictions[ 0 ] )

test_labels[ 0 ]



import math
batch_size = 32
n_batches = len(train_images) / batch_size
n_batches = math.ceil(n_batches)
cp_callback = keras.callbacks.ModelCheckpoint( filepath=checkpoint_path,
                                                save_weights_only=True,
                                                verbose=1,
                                                save_freq=20*n_batches)

model.fit( train_images,
            train_labels,
            epochs=40,
            batch_size=batch_size,
            validation_data=(test_images, test_labels ),
            callbacks=[ cp_callback ],
            verbose=0)

os.listdir( checkpoint_dir )
model.save('model.keras')
```
Then all that is left is testing the model
```python
def plot_image( i, predictions_array, true_label, img ):
    true_label, img = true_label[ i ], img[ i ]
    plt.grid( False )
    plt.xticks([])
    plt.yticks([])

    plt.imshow( img, cmap=plt.cm.binary )

    predicted_label = np.argmax( predictions_array )
    if predicted_label == true_label:
        color = 'blue'
    else: color = 'red'
    
    plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                100*np.max(predictions_array),
                                class_names[true_label]),
                                color=color)

def plot_value_array(i, predictions_array, true_label):
    true_label = true_label[i]
    plt.grid(False)
    plt.xticks(range(10))
    plt.yticks([])
    thisplot = plt.bar(range(10), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')

i = 0
plt.figure(figsize=(6,3))
plt.subplot(1,2,1)
plot_image(i, predictions[i], test_labels, test_images)
plt.subplot(1,2,2)
plot_value_array(i, predictions[i],  test_labels)
plt.show()

i = 12
plt.figure(figsize=(6,3))
plt.subplot(1,2,1)
plot_image(i, predictions[i], test_labels, test_images)
plt.subplot(1,2,2)
plot_value_array(i, predictions[i],  test_labels)
plt.show()

num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
    plt.subplot(num_rows, 2*num_cols, 2*i+1)
    plot_image(i, predictions[i], test_labels, test_images)
    plt.subplot(num_rows, 2*num_cols, 2*i+2)
    plot_value_array(i, predictions[i], test_labels)
plt.tight_layout()
plt.show()

img = test_images[1]

print(img.shape)

img = (np.expand_dims(img,0))

print(img.shape)

predictions_single = probability_model.predict(img)

print(predictions_single)

plot_value_array(1, predictions_single[0], test_labels)
_ = plt.xticks(range(10), class_names, rotation=45)
plt.show()
```
### Loading the model for model optimization
```python
import os
os.environ["KERAS_BACKEND"] = "tensorflow"

import tensorflow as tf
import keras
import numpy as np
import matplotlib.pyplot as plt
"""
loading_path = "training_1/cp.weights.h5"
loading_dir = os.path.dirname( loading_path )

def create_model():
    model = tf.keras.Sequential([
    tf.keras.layers.Flatten( input_shape=( 28, 28 ) ),
    tf.keras.layers.Dense( 128, activation="relu" ),
    tf.keras.layers.Dense( 10 )])

    model.compile( optimizer='adam',
                    loss=tf.keras.losses.SparseCategoricalCrossentropy( from_logits=True ),
                    metrics=[ 'accuracy' ])
    return model
model = create_model()

model.load_weights( loading_path )
"""
fashion_mnist = tf.keras.datasets.fashion_mnist
( train_images, train_labels ), ( test_images, test_labels ) = fashion_mnist.load_data()

new_model = keras.models.load_model('model.keras')
new_model.summary()
loss, acc = new_model.evaluate(test_images, test_labels, verbose=2)
print('Restored model, accuracy: {:5.2f}%'.format(100 * acc))

print(new_model.predict(test_images).shape)

probability_model = tf.keras.Sequential( [new_model,
                                            tf.keras.layers.Softmax()] )
predictions = probability_model.predict( test_images )
predictions = probability_model.predict( test_images )
predictions[ 0 ]
np.argmax( predictions[ 0 ] )

test_labels[ 0 ]
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

def plot_image( i, predictions_array, true_label, img ):
    true_label, img = true_label[ i ], img[ i ]
    plt.grid( False )
    plt.xticks([])
    plt.yticks([])

    plt.imshow( img, cmap=plt.cm.binary )

    predicted_label = np.argmax( predictions_array )
    if predicted_label == true_label:
        color = 'blue'
    else: color = 'red'
    
    plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                100*np.max(predictions_array),
                                class_names[true_label]),
                                color=color)

def plot_value_array(i, predictions_array, true_label):
    true_label = true_label[i]
    plt.grid(False)
    plt.xticks(range(10))
    plt.yticks([])
    thisplot = plt.bar(range(10), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')

num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
    plt.subplot(num_rows, 2*num_cols, 2*i+1)
    plot_image(i, predictions[i], test_labels, test_images)
    plt.subplot(num_rows, 2*num_cols, 2*i+2)
    plot_value_array(i, predictions[i], test_labels)
plt.tight_layout()
plt.show()
```
## Results
![image](https://github.com/Bolofofopt/Public_Projects/assets/145719526/e8946fcf-d2cf-4a4a-9053-31fc3a199c27)


## Diagram
### For the  model trainer
![image](https://github.com/Bolofofopt/Public_Projects/assets/145719526/59e0227c-59d8-438a-b195-7e80e0666a0d)
![image](https://github.com/Bolofofopt/Public_Projects/assets/145719526/6e983494-948a-4956-9142-fed89c60c341)
### For the model user/loader
![image](https://github.com/Bolofofopt/Public_Projects/assets/145719526/15d4ddeb-cbe6-465e-81e9-98e6acc6893b)
![image](https://github.com/Bolofofopt/Public_Projects/assets/145719526/2e7a6d1e-c72b-4065-be52-8d9efc2fdfd6)
