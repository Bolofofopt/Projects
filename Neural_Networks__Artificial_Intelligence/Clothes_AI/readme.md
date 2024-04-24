# Same on the main branch
## clothes_AI
This AI model helps identify different types of clothes
### How it works
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
#### Results
![image](https://github.com/Bolofofopt/Public_Projects/assets/145719526/e8946fcf-d2cf-4a4a-9053-31fc3a199c27)
