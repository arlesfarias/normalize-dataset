#this script will get all files in a dir to rotate and crop images to create
#a dataset

import numpy as np
import cv2 as cv
import glob
import math
import os.path

currentImg = None
p1 = None
p2 = None
p3 = None
p4 = None
click = 0
count = 0
imgs =  glob.glob('*.jpg')
cv.namedWindow('Imagem')
directory = './imgs/'

def cropRotateCenter(event, x, y, flags, param):
    global p1, p2, p3, click, currentImg
    color = (255, 0, 0)
    if event == cv.EVENT_MOUSEMOVE:
        img = currentImg.copy()
        if click == 1:
            cv.line(img, p1, (x, y), color)
        if click > 1:
            cv.line(img, (x,0), (x, currentImg.shape[0]), color)
            cv.line(img, (0, y), (currentImg.shape[1], y), color)
        cv.imshow("Imagem", img)
    if event == cv.EVENT_LBUTTONDOWN:
        click += 1
        if click == 1:
            p1 = (x, y)
        if click == 2:
            p2 = (x, y)
            height, width, channels = currentImg.shape
            angulo = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
            deg = math.degrees(angulo)
            M = cv.getRotationMatrix2D((width/2, height/2), deg, 1)
            currentImg = cv.warpAffine(currentImg, M, (width, height))
        if click == 3:
            p3 = (x, y)
            cv.line(currentImg, (p3[0],0), (p3[0], currentImg.shape[0]), color)
            cv.line(currentImg, (0, p3[1]), (currentImg.shape[1], p3[1]), color)
        if click == 4:
            p4 = (x, y)
            cv.line(currentImg, (p4[0],0), (p4[0], currentImg.shape[0]), color)
            cv.line(currentImg, (0, p4[1]), (currentImg.shape[1], p4[1]), color)
            h = p4[1] - p3[1]
            w = p4[0] - p3[0]
            currentImg = currentImg[p3[1]:p4[1],p3[0]:p4[0]]
        cv.imshow('Imagem', currentImg)

cv.setMouseCallback('Imagem', cropRotateCenter)

for imgName in imgs:
    img = cv.imread(imgName)
    currentImg = img.copy()
    cv.imshow('Imagem', img)
    if cv.waitKey(0) == 32:
        if not os.path.exists(directory):
            os.makedirs(directory)
        cv.imwrite(directory + 'img' + str(count) + '.jpg', currentImg)
        count += 1
    click = 0
