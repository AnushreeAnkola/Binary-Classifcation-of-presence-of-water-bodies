# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 13:38:13 2018

@author: Rishabh Sharma
"""

# Convolutional Neural Network

# Part 1 - Building the CNN

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense, Dropout
import h5py
import keras
# Initialising the CNN
classifier = Sequential()

# Step 1 - Convolution
classifier.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'))

# Step 2 - Pooling
classifier.add(MaxPooling2D(pool_size = (2, 2)))

classifier.add(Dropout(0.2))

# Adding a second convolutional layer
classifier.add(Conv2D(32, (3, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))

classifier.add(Conv2D(32, (3, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Step 3 - Flattening
classifier.add(Flatten())

# Step 4 - Full connection
classifier.add(Dense(units = 128, activation = 'relu'))
classifier.add(Dropout(0.5))
classifier.add(Dense(units = 1, activation = 'sigmoid'))
# Compiling the CNN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Part 2 - Fitting the CNN to the images

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.5,
                                   rotation_range = 180,
                                   fill_mode = 'nearest',
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('dataset\Training_Data',
                                                 target_size = (64, 64),
                                                 batch_size = 32,
                                                 class_mode = 'binary',
                                                 shuffle = True)

test_set = test_datagen.flow_from_directory('dataset\Test_Data',
                                            target_size = (64, 64),
                                            batch_size = 32,
                                            shuffle = False,
                                            class_mode = 'binary')

classifier.fit_generator(training_set,
                         steps_per_epoch = 1000,
                         epochs = 5,
                         validation_data = test_set,
                         validation_steps = 250)


classifier.save("Rishabh_model_1.h5",overwrite=True)
classifier.summary()

import numpy as np
from keras.preprocessing import image

img = image.load_img('C:/CSUF/CPSC585Project/ANN Project/CPSC-585-Project-Artificial-Neural-Network/dataset/Training_Data/Without_Water/AA-39.PNG',target_size=(64,64,3))
img = np.expand_dims(img,axis = 0)
result = classifier.predict(img)
training_set.class_indices