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