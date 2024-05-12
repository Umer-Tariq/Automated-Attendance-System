import cv2
import dlib
import cmake
import os
import pickle 
import numpy as np
import cvzone
import face_recognition 
import time
import threading
import datetime
import tkinter as tk
from tkinter import simpledialog
import signal
from maili import send_copy
from otp import otp_msg
from attendance_marking import read_file, prepare_file, mark, find_colreference2, save_file
from PIL import Image, ImageTk
from tkinter import messagebox, simpledialog

def get_id(list_of_ids):
    d = dict()
    for id in list_of_ids:
        if id in d:
            d[id] += 1
        else:
            d[id] = 0
    
    max = -1
    id = -9999
    for key in d.keys():
        if d[key] > max:
            max = d[key]
            id = key
    
    return id

def display_message(message):
    message_label.config(text=message)


attendance = {}
root = tk.Tk()
#video by hamza's workshop
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


count = 0
count_mismatch = 0
face_id_detected = []
#thread used to call the OTP function
otp_thread = None

##open excel file here
current_time_12hr = datetime.datetime.now().strftime('%I:%M %p')
current_min = current_time_12hr.split(':')[1] 
current_min = int(current_min.split(' ')[0])

section, subject, ccode =  read_file('R11')
file_name = prepare_file(section, ccode)
col_num = find_colreference2(file_name)

# try:
while current_min < 59:
    current_time_12hr = datetime.datetime.now().strftime('%I:%M %p')
    current_min = current_time_12hr.split(':')[1] 
    current_min = int(current_min.split(' ')[0])
    success, img = cap.read()
    frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFace = face_recognition.face_encodings(imgS, faceCurFrame)


    if len(faceCurFrame) == 0:  
        count = 0
        face_id_detected.clear()
        count_mismatch = 0
    for code, loc in zip(encodeCurFace, faceCurFrame):
        matches = face_recognition.compare_faces(encodingList, code, tolerance=0.50)
        faceDist = face_recognition.face_distance(encodingList, code)

        y1, x2, y2, x1 = loc
        y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
        bbox = x1, y1, x2 - x1, y2 - y1
        img = cvzone.cornerRect(img, bbox, rt=0)
        matchIndex = np.argmin(faceDist)
        if matches[matchIndex]:
            count_mismatch = 0
            face_id_detected.append(studentIDs[matchIndex])
            if count == 5:
                #FACE IS RECOGNIZED AND THE ATTENDANCE IS MARKED STATUS: YOUR ATTENDACE HAS BEEN MARKED
                id_detected = get_id(face_id_detected)
                display_message("Welcome! Attendance Marked")
                ##the prson has been detected. So nark their attendance
                mark(id_detected, file_name, col_num)
                save_file(file_name)
                count = 0
                face_id_detected.clear()
            else:
                count += 1
                display_message("Identifying! Please Wait")


            else:
                if count_mismatch == 3:
                    #THE PERSON IS NOT RECOGNIZED STATUS: NO MATCH! PLEASE USE OTP TO MARK YOUR ATTENDANCE
                    cv2.putText(imgBackgound, 'No Match! Kindly Mark your attendance using OTP', (x1 + 1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2)
                    ##OTP Function called here target=functionName 
                    '''if otp_thread is None or not otp_thread.is_alive():
                        otp_thread = threading.Thread(target=otp_msg)
                        otp_thread.start()
                    '''
                    
                    root.withdraw()
                    #OTP MSG IS THE OTP FUNCTION
                    otp_returned = otp_msg()
                    if otp_returned != False:
                    #else:
                        cv2.putText(imgBackgound, 'Attendance marked using OTP', (x1 + 1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 255), 2)
                        mark(otp_returned, file_name, col_num)
                        save_file(file_name)
                        count = 0
                        face_id_detected.clear()

                    count_mismatch = 0
                else:
                    count_mismatch += 1
                    cv2.putText(imgBackgound, 'Unable to recognize, ' + str(count_mismatch), (x1 , y1), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2)
                count = 0
                face_id_detected.clear()

        cv2.imshow("Face Attendance", imgBackgound)
        cv2.waitKey(1)
    ##close excel sheet
    save_file(file_name)
    ##send email
    send_copy(file_name, section, subject)
except Exception as e:
    print("Keyboard interrupt detected. Sending email copy...")
