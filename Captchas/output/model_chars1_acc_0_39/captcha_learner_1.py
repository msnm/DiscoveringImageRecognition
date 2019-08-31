from keras import layers
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
import matplotlib.pylab as plt
from captcha_generator import get_data_set, get_all_possible_label_categories
from sklearn.preprocessing import LabelBinarizer
import tensorflow as tf
import numpy as np
from keras import optimizers, models
import os
import time
from shutil import copyfile


############### 0. Configuration settings
numberOfCaptchas = 2000
testPercentage = 0.8
testSize = int(numberOfCaptchas * testPercentage)
img_x, img_y = 96, 96
nr_of_chars = 1
numbers = False
color = False
depth = 1
if color:
    depth = 3  # RGB

output_dir = os.path.abspath('../output')

def main():
    train()
    #predict()


def train():
    ############### 1. Generating captchas

    images, labels = get_data_set(width=img_x, height=img_y, nr_of_chars=nr_of_chars, color=color,
                                  nr_of_captchas=numberOfCaptchas, numbers=numbers)

    ############### 2. Preprocessing the data
    #
    # Data needs to be reshaped into a 4D tensor - (sample_number, x_img_size, y_img_size, num_channels)
    # The number of channels = number of colors grescale = 1, color = 3
    images_train = images[:testSize]
    print('Before reshaping, 3D :', images_train.shape)
    images_train = images_train.reshape(images_train.shape[0], img_x, img_y, depth)
    images_train = images_train.astype('float32') / 255  # Scaling color dimension to 0-255 to 0-1
    print('After reshaping, 3D :', images_train[0].shape)

    images_test = images[testSize:]
    images_test = images_test.reshape(images_test.shape[0], img_x, img_y, depth)
    images_test = images_test.astype('float32') / 255

    labels_train = labels[:testSize]
    labels_test = labels[testSize:]

    # The categories are characters [aa, ab, ac, ... ]
    categories = get_all_possible_label_categories(nr_of_chars)
    lb = LabelBinarizer().fit(categories)
    labels_encoded_train = lb.transform(labels_train)
    labels_encoded_test = lb.transform(labels_test)

    ############### 3. Building the neural network
    # Sequential model
    model = Sequential()
    # First conv: 32 filters of 3x3
    model.add(Conv2D(32, (3, 3), padding='same', input_shape=(img_x, img_y, 1), activation="relu"))
    model.add(Dropout(0.25))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

    # Second conv
    model.add(layers.Conv2D(64, (3, 3), padding='same', activation='relu'))
    model.add(Dropout(0.3))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

    # Fully connected layer
    model.add(Flatten())
    model.add(Dense(512, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(len(categories), activation="softmax"))

    print(model.summary())
    model.compile(loss="categorical_crossentropy", optimizer=optimizers.Adam(), metrics=["accuracy"])

    ############### 4. Training the neural network
    history = model.fit(
        images_train,
        labels_encoded_train,
        batch_size=128,
        validation_data=(images_test, labels_encoded_test),
        epochs=30
    )

    ############### 5. Visualizing and saving the result
    # Retrieving the acc and loss
    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    # Creating the output dir for this model
    model_dir = os.path.join(output_dir, 'model_chars' + str(nr_of_chars) + '_acc_' + str(max(val_acc)).replace('.', '_')[:4])

    if os.path.exists(model_dir):
        model_dir = os.path.join(model_dir, '_' + str(time.time()))

    os.mkdir(model_dir)

    model.save(os.path.join(model_dir, 'model.h5'))
    model_json = model.to_json()
    copyfile('./captcha_learner_1.py', os.path.join(model_dir,'captcha_learner_1.py'))
    with open(os.path.join(model_dir, 'model.json'), "w") as json_file:
        json_file.write(model_json)

    epochs = range(1, len(acc) + 1)
    plt.figure()
    plt.subplot(211)
    plt.plot(epochs, acc, 'bo', label='Training acc')
    plt.plot(epochs, val_acc, 'b', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.legend()

    plt.subplot(212)

    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()
    plt.savefig(os.path.join(model_dir, 'metrics.png'))
    plt.show()

def predict():
    images, labels = get_data_set(width=img_x, height=img_y, nr_of_chars=nr_of_chars, color=color,
                                  nr_of_captchas=10, numbers=numbers)
    images_predict = images.reshape(images.shape[0], img_x, img_y, depth)
    images_predict = images_predict.astype('float32') / 255
    categories = get_all_possible_label_categories(nr_of_chars)

    loaded_model = models.load_model('/Users/mvrm/Documents/msnm/AI/DiscoveringImageRecognition/Captchas/output/model_chars1_acc_0_02/model.h5')
    new_predictions = loaded_model.predict_classes(images_predict)
    print(new_predictions)
    for i in range(len(images)):
        print('Actual: ' + labels[i] + ' Predicted: ' + str(categories[new_predictions[i]]))
        #plt.imshow(images[i])
        #plt.show()


if __name__ == '__main__':
    main()
