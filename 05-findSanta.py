import pathlib
import cv2
import os
import numpy as np

import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

height, width = 2799, 2812
rowHeight = int(height / 15) - 1
colWidth = int(width / 15)
print(rowHeight, colWidth)

img_height = 184
img_width = 187
class_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
               'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


TF_MODEL_FILE_PATH = "imageClassificationModel.tflite"
interpreter = tf.lite.Interpreter(model_path=TF_MODEL_FILE_PATH)
print(interpreter.get_signature_list())

classify_lite = interpreter.get_signature_runner('serving_default')

# samplePath = pathlib.Path("dataTestProcessed/3_0_1.jpg")

# img = tf.keras.utils.load_img(samplePath, target_size=(img_height, img_width))
# img_array = tf.keras.utils.img_to_array(img)
# img_array = tf.expand_dims(img_array, 0)

# predictions_lite = classify_lite(rescaling_7_input=img_array)['dense_11']
# score_lite = tf.nn.softmax(predictions_lite)

# print("Score: {} | Position: {} | Letter: {}".format(np.max(score_lite),
#       np.argmax(score_lite), class_names[np.argmax(score_lite)]))


def getPage(pageName):
    page = cv2.imread(pageName)
    croppedPage = page[:-1, 2200:-1]
    return croppedPage


def crop(croppedPage):
    print("Cropping image and generating raw matrix")
    charImageMatrix = []
    x, y = 0, 0
    rowCounter = 0
    imageCounter = 1000
    while x < 15:
        row = croppedPage[rowCounter:rowCounter + rowHeight]
        colCounter = 0
        charCounter = 1
        charImageMatrixRow = []
        y = 0
        while y < 15:
            characterImage = row[:-1, colCounter:colCounter + colWidth]
            charImageMatrixRow.append(characterImage.tolist())
            colCounter = colCounter + colWidth
            charCounter += 1
            imageCounter += 1
            y += 1
        rowCounter = rowCounter + rowHeight
        charImageMatrix.append(charImageMatrixRow)
        x += 1
    return charImageMatrix


def generateCharacterMatrix(charImageMatrix):
    for row in charImageMatrix:
        print(len(row))


# totalNumberOfPages = 31
totalNumberOfPages = 3

for i in range(totalNumberOfPages):
    pageName = "pages/test_slide_new_" + str(i+1) + ".jpg"
    print("-------- [START] - {} --------".format(pageName))
    croppedPage = getPage(pageName)
    charImageMatrix = crop(croppedPage)
    generateCharacterMatrix(charImageMatrix)
    print("-------- [DONE] - {} --------\n".format(pageName))
    i += 1
