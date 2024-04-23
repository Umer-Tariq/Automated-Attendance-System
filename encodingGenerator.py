import cv2
import face_recognition
import pickle
import os

def calculateEncodings(imgList):
    encodingList = []

    for img in imgList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        code = face_recognition.face_encodings(img)[0]
        encodingList.append(code)

    return encodingList


folderPath = 'Images'
pathList = os.listdir(folderPath)
imgList = []
studentIDs = []

for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIDs.append(os.path.splitext(path)[0])

encodingList = calculateEncodings(imgList)
encodingListwithIds = [encodingList, studentIDs]

file = open('Encodings.p', 'wb')
pickle.dump(encodingListwithIds, file)
file.close()
