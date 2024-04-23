import face_recognition 
import cv2
import dlib
import cmake
import os
import pickle 
import numpy as np
import cvzone


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

modeFolderPath = 'Resources/Modes'
modeFiles = os.listdir(modeFolderPath)
imgPathList = []

for path in modeFiles:
    imgPathList.append(cv2.imread(os.path.join(modeFolderPath, path)))


file = open('Encodings.p', 'rb')
encodingListwithIds = pickle.load(file)
file.close()
encodingList, studentIDs = encodingListwithIds
print(studentIDs)

imgBackgound = cv2.imread('Resources/background.png')

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFace = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackgound[162: 162 + 480, 55: 55 + 640] = img
    imgBackgound[44: 44 + 633, 808: 808 + 414] = imgPathList[0]

    for code, loc in zip(encodeCurFace, faceCurFrame):
        matches = face_recognition.compare_faces(encodingList, code)
        faceDist = face_recognition.face_distance(encodingList, code)
        print(matches)
        print(faceDist)

        y1, x2, y2, x1 = loc
        y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
        bbox = 55+x1, 162 + y1, x2 - x1, y2 - y1
        imgBackgound = cvzone.cornerRect(imgBackgound, bbox, rt=0)
        
        matchIndex = np.argmin(matches)
        if matches[matchIndex]:
            #print(studentIds[matchIndex])
            continue
        else:
            print("No match")

    cv2.imshow("Face Attendance", imgBackgound)
    cv2.waitKey(1)