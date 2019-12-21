import cv2
import matplotlib.pyplot as plt
import numpy as np
import math
from skimage.transform import resize
from os import listdir
import os, glob

n_classes = 5
listVideo = []

def extract_frames_from_video_valid(srcDir):
    if glob.glob("static/generated_frames_valid/valid0.jpg"):
        for elt in os.listdir("static/generated_frames_valid/"):
            os.remove("static/generated_frames_valid/" + elt)
        print("Deletion files with sucess!!!")
        for video in os.listdir(srcDir):
            dir = srcDir
        file3 = dir + video
        count = 0
        cap = cv2.VideoCapture(file3)
        frameRate = cap.get(5)
        while(cap.isOpened()):
            frameId = cap.get(1)
            ret, frame = cap.read()
            if(ret!=True):
                break
            if(frameId%math.floor(frameRate)==0):
                filename = "valid%d.jpg"%count
                count+=1
                print(filename)
                cv2.imwrite("static/generated_frames_valid/" + filename, frame)
        cap.release()
    else:
        count = 0
        for video in os.listdir(srcDir):
            dir = srcDir
        file3 = dir + video
        cap = cv2.VideoCapture(file3)
        frameRate = cap.get(5)
        while(cap.isOpened()):
            frameId = cap.get(1)
            ret, frame = cap.read()
            if(ret!=True):
                break
            if(frameId%math.floor(frameRate)==0):
                filename = "valid%d.jpg"%count
                count+=1
                print(filename)
                cv2.imwrite("static/generated_frames_valid/" + filename, frame)
        cap.release()
    print("Done!!!")

def load_data_valid():
    X_valid = []
    X_valid_im = []
    for img_name in listdir("static/generated_frames_valid/"):
        img = plt.imread("static/generated_frames_valid/" + img_name)
        X_valid.append(img)
    X_valid = np.array(X_valid)
    for i in range(0, X_valid.shape[0]):
        img = resize(X_valid[i], preserve_range=True, output_shape=(224, 224)).astype(int)
        X_valid_im.append(img)
    X_valid_im = np.array(X_valid_im)
    return X_valid_im