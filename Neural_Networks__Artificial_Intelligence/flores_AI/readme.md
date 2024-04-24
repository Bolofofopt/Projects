# Same on the main branch
## flores_AI
This AI model helps identify different types of flowers.
### How it works
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
#### To use the model in another environment:
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
### Model efficiency
On these 2 graphs we can see the model efficiency based on a few EPOCHs, these graphs are from the flores_AI model but the architecture and the model training is the same for both models (flores_AI & clothes_AI)
![Figure1](https://github.com/Bolofofopt/Public_Projects/assets/145719526/6a4008d2-d820-4bce-8ead-59df74d2c6d3)

![Figure2](https://github.com/Bolofofopt/Public_Projects/assets/145719526/c52c3071-419f-4a6b-aa29-f27fc0761d22)
