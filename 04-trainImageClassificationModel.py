from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
from tensorflow import keras
import os
import cv2
import numpy as np
import pathlib

import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


dataDir = pathlib.Path("dataPostProcessed")
imageCount = len(list(dataDir.glob('*/*.jpg')))
print(imageCount)

batch_size = 32
img_height = 184
img_width = 187


train_ds = tf.keras.utils.image_dataset_from_directory(
    dataDir,
    validation_split=0.2,
    subset="training",
    seed=76523,
    image_size=(img_height, img_width),
    batch_size=batch_size)

val_ds = tf.keras.utils.image_dataset_from_directory(
    dataDir,
    validation_split=0.2,
    subset="validation",
    seed=76523,
    image_size=(img_height, img_width),
    batch_size=batch_size)

class_names = train_ds.class_names
for id, c in enumerate(class_names):
    class_names[id] = c.split("_")[0]
print(class_names)

# TUNE
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

num_classes = len(class_names)

model = Sequential([
    layers.Rescaling(1./255, input_shape=(img_height,
                     img_width, 3), name="rescaleImage"),
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Dropout(0.2),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes, name="output")
], name='imageClassification')


model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(
    from_logits=True), metrics=['accuracy'])
model.summary()


epochs = 15
history = model.fit(train_ds, validation_data=val_ds, epochs=epochs)


samplePath = pathlib.Path("dataTestProcessed/3_0_1.jpg")

img = tf.keras.utils.load_img(samplePath, target_size=(img_height, img_width))
img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)
predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

print("Score: {} | Position: {} | Letter: {}".format(
    np.max(score), np.argmax(score), class_names[np.argmax(score)]))


converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open('imageClassificationModel.tflite', 'wb') as f:
    f.write(tflite_model)
