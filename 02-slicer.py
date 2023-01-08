import os
import cv2
from random import randrange
from matplotlib import pyplot as plt


def show(data):
    plt.xticks([])
    plt.yticks([])
    plt.imshow(data)
    plt.show()


def printArrayInfo(arr):
    print("---------------------------")
    # print(arr)
    print("Size :: ", arr.size)
    print("Shape :: ", arr.shape)
    print("---------------------------")


def getPage(pageNum):
    # pageName = "pages/SLIDE-" + str(pageNum) + ".jpg"
    pageName = "pages/test_slide_new_" + str(pageNum) + ".jpg"
    print("Processing page - " + pageName)
    page = cv2.imread(pageName)
    # printArrayInfo(page)
    croppedPage = page[:-1, 2200:-1]
    return croppedPage


def crop(pageNum, croppedPage):
    x, y = 0, 0
    rowCounter = 0
    imageCounter = 1000
    while y < 15:
        # print(rowCounter, rowCounter + rowHeight)
        row = croppedPage[rowCounter:rowCounter + rowHeight]
        colCounter = 0
        charCounter = 1
        x = 0
        while x < 15:
            col_text = row[:-1, colCounter:colCounter + colWidth]
            # imageName = "data/{}_{}_{}.jpg".format(pageNum, x, y)
            imageName = "dataTest/{}_{}_{}.jpg".format(pageNum, x, y)
            cv2.imwrite(imageName, col_text)
            print("File {} saved.".format(imageName))
            colCounter = colCounter + colWidth
            charCounter += 1
            imageCounter += 1
            x += 1
        rowCounter = rowCounter + rowHeight
        y += 1


# totalNumberOfPages = 31
totalNumberOfPages = 4
height, width = 2799, 2812
rowHeight = int(height / 15) - 1
colWidth = int(width / 15)
print(rowHeight, colWidth)

i = 1
# for i in range(totalNumberOfPages):
croppedPage = getPage(4)
crop(4, croppedPage)
# i += 1
