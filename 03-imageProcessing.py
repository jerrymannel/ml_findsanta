import pathlib as path
import os
import cv2
import numpy as np

dataProcessed = path.PurePath("dataProcessed")
dataPostProcessed = path.PurePath("dataPostProcessed")

outputFileList = []

max_mutations = 30


def translate(img, translationMatrix):
    return cv2.warpAffine(
        img,
        translationMatrix,
        img.shape[:2],
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(255, 255, 255)
    )


def generateTranslations(image):
    imageBaseName = image.split(".jpg")[0]
    img = cv2.imread(image).copy()
    counter = 1
    # HORIZONTAL
    print("\t {} - SHIFT-RIGHT".format(image))
    for i in range(max_mutations):
        translationMatrix = np.float32([[1, 0, i+1], [0, 1, 0]])
        imgTranslated = translate(img, translationMatrix)
        cv2.imwrite(imageBaseName + "_" + str(counter) + ".jpg", imgTranslated)
        counter += 1

    print("\t {} - SHIFT-LEFT".format(image))
    for i in range(max_mutations):
        translationMatrix = np.float32([[1, 0, -1-i], [0, 1, 0]])
        imgTranslated = translate(img, translationMatrix)
        cv2.imwrite(imageBaseName + "_" + str(counter) + ".jpg", imgTranslated)
        counter += 1

    # VERTICAL
    print("\t {} - SHIFT-DOWN".format(image))
    for i in range(max_mutations):
        translationMatrix = np.float32([[1, 0, 0], [0, 1, i+1]])
        imgTranslated = translate(img, translationMatrix)
        cv2.imwrite(imageBaseName + "_" + str(counter) + ".jpg", imgTranslated)
        counter += 1
    print("\t {} - SHIFT-UP".format(image))
    for i in range(max_mutations):
        translationMatrix = np.float32([[1, 0, 0], [0, 1, -1-i]])
        imgTranslated = translate(img, translationMatrix)
        cv2.imwrite(imageBaseName + "_" + str(counter) + ".jpg", imgTranslated)
        counter += 1

    # DIAGONALS
    print("\t {} - SHIFT-BOTTOM-RIGHT".format(image))
    for i in range(max_mutations):
        translationMatrix = np.float32([[1, 0, i+1], [0, 1, i+1]])
        imgTranslated = translate(img, translationMatrix)
        cv2.imwrite(imageBaseName + "_" + str(counter) + ".jpg", imgTranslated)
        counter += 1
    print("\t {} - SHIFT-TOP-RIGHT".format(image))
    for i in range(max_mutations):
        translationMatrix = np.float32([[1, 0, i+1], [0, 1, -i-1]])
        imgTranslated = translate(img, translationMatrix)
        cv2.imwrite(imageBaseName + "_" + str(counter) + ".jpg", imgTranslated)
        counter += 1
    print("\t {} - SHIFT-BOTTOM-LEFT".format(image))
    for i in range(max_mutations):
        translationMatrix = np.float32([[1, 0, -i-1], [0, 1, i+1]])
        imgTranslated = translate(img, translationMatrix)
        cv2.imwrite(imageBaseName + "_" + str(counter) + ".jpg", imgTranslated)
        counter += 1
    print("\t {} - SHIFT-TOP-LEFT".format(image))
    for i in range(max_mutations):
        translationMatrix = np.float32([[1, 0, -i-1], [0, 1, -i-1]])
        imgTranslated = translate(img, translationMatrix)
        cv2.imwrite(imageBaseName + "_" + str(counter) + ".jpg", imgTranslated)
        counter += 1


def convertToBW(imageName, outputImageName):
    print("{} -- to BW -> {}".format(imageName, outputImageName))
    image = cv2.imread(imageName)
    greaterThanGrayPixels = np.where((
        (image[:, :, 0] > 200) &
        (image[:, :, 1] > 200) &
        (image[:, :, 2] > 200)
    ))
    image[greaterThanGrayPixels] = [255, 255, 255]

    lessThanGrayPixels = np.where((
        (image[:, :, 0] < 200) &
        (image[:, :, 1] < 200) &
        (image[:, :, 2] < 200)
    ))
    image[lessThanGrayPixels] = [0, 0, 0]
    cv2.imwrite(outputImageName, image)


def main():
    for d in os.listdir(dataProcessed):
        if not os.path.exists(dataPostProcessed.joinpath(d)):
            os.mkdir(dataPostProcessed.joinpath(d))
    for d in os.listdir(dataProcessed):
        letter = d.split("_")[0]
        for image in os.listdir(dataProcessed.joinpath(d)):
            convertToBW(str(dataProcessed.joinpath(d).joinpath(image)),
                        str(dataPostProcessed.joinpath(d).joinpath(letter + ".jpg")))
            outputFileList.append(
                str(dataPostProcessed.joinpath(d).joinpath(letter + ".jpg")))

    for image in outputFileList:
        print("Generating{} - ".format(image))
        generateTranslations(image)


main()
