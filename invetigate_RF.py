from os import listdir
from pickle import load
from keras.utils import to_categorical
import os
import datetime, json
import numpy as np
from joblib import load
import time
from flask import Flask
from extract_frames_from_video import load_data_valid, extract_frames_from_video_valid

app = Flask(__name__)

listInt = []
def getIndex(YList):
    index = 0
    #print("YList : ", YList)
    for data in YList[0]:
        #data = int(data)
        if data == 1:
            retour = index
        else:
            index += 1
    listInt.append(retour)
    return retour

def investigate_crash():
    startTime = time.time()
    # define categorical label
    label_dict = {
        0: 'Without Crash',
        1: 'Crash',
        2: 'Ambiguity Event',
        3: 'Unknwon Event',
        4: 'Unknown Event',
    }

    #load heterogenous data
    file3 = "epic.mp4"
    srcDir = "static/data/"
    for elt in os.listdir(srcDir):
        if elt.__eq__('crash_resultNew.json'):
            os.remove(srcDir + elt)
            print("Deletion crash_resultNew.json file with sucess!!!")

    extract_frames_from_video_valid(srcDir)
    Xtest = load_data_valid()
    print('input image shape : {}'.format(Xtest.shape))
    Xtest = np.reshape(Xtest, (-1, 150528))
    print('input image shape : {}'.format(Xtest.shape))

    # call model
    RFClassifier = load(open("model/RFClassifier_train3.pkl", "rb"))

    # evaluate
    predicted = RFClassifier.predict(Xtest)
    predict_cat = to_categorical(predicted, num_classes=5)
    predict_cat = predict_cat.astype('int')
    print("predicted : ", predict_cat)
    print("predict[0] : ", predict_cat[0])
    print("predict[4] : ", predict_cat[4])
    print('predict class shape : {}'.format(predict_cat.shape))
    i = 0
    cota = 0
    with open("static/data/crash_resultNew.json", "a") as fichier:
        now = datetime.datetime.now()
        daty = now.strftime("%d-%m-%Y")
        ora = now.strftime("%Hh:%Mm:%Ss")
        listJson = []
        i = 0
        fichier.write('{"VideoResults": [')

        for frame in listdir("static/generated_frames_valid/"):
            res = label_dict[getIndex(predict_cat[i])]
            frameK = frame
            print("frame : {}, crash found : {}".format(frame, res))
            frame = frame.split(".")[0]
            frameId = frame.split("d")[1]
            frameId = int(frameId)
            data = {'frame': frameK, 'resultat': res, 'zone': 1,'date': daty, 'heure': ora}
            listJson.append(data)
            try:
                if res.__eq__(label_dict[getIndex(predict_cat[1])]):
                    print("crash detected in frame n° :", frameId, "(" + frame + ".jpg)")
                    cota += 1
            except:
                print("il ya une erreur non prise en charge par le system")
            finally:
                i += 1
        i = 0
        while (i < len(listJson)):
            json.dump(listJson[i], fichier)
            if (i == len(listJson) - 1):
                pass
            else:
                fichier.write(",")
            i += 1
        fichier.write("]}")
        endTime = time.time()
        duree = endTime-startTime
        print('time consuming : ', duree, "s")
        return duree, listJson