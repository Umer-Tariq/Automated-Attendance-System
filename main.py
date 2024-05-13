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
from customtkinter import *

#function for login page

def login_window():
    def check_password():
        password = entry.get()
        if password == "password123":  
            print("Login successful!")
            app.destroy()  
            return True
        else:
            label.configure(text="Incorrect password. Try again.")
            entry.delete(0, END)  
            return False

    def login():
        if check_password():
            return True

    app = CTk()
    app.geometry("600x480")
    app.resizable(0,0)

    side_img_data = Image.open("side-img.png")
    password_icon_data = Image.open("password-icon.png")
    side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
    password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17,17))
    CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")


    frame = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
    frame.pack_propagate(0)
    frame.pack(expand=True, side="right")

    CTkLabel(master=frame, text="Welcome!", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
    label = CTkLabel(master=frame, text="Sign in to Attendance Register", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12))
    label.pack(anchor="w", padx=(25, 0))

    CTkLabel(master=frame, text="  Password:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
    entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*")
    entry.pack(anchor="w", padx=(25, 0))

    CTkButton(master=frame, text="Login", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225,command =login).pack(anchor="w", pady=(40, 0), padx=(25, 0))


    app.mainloop()

#Function to Display Message
def display_message(message):
    message_label.configure(text=message)

Lis = []

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

#login page Call
login_window()

attendance = {}
root = CTk()
root.geometry("1000x480")
root.minsize(1000,480)
root.maxsize(1000,480)
root2 = CTk()


root.title("Attendance In Progress")

cap = cv2.VideoCapture(0)

#Master Frame 
frame_frame= CTkFrame(master=root, width=1000, height=480, fg_color="#FFFFFF",bg_color="#FFFFFF")
frame_frame.pack_propagate(0)
frame_frame.pack(expand=True, side="right")

#left Side Message Frame
message_frame = CTkFrame(frame_frame,width=300,bg_color="#FFFFFF",fg_color="#FFFFFF")
message_frame.pack(expand=True, side="left")

message_label = CTkLabel(message_frame, text="Waiting for face detection...", font=("Arial Bold", 16),text_color="#601E88")
message_label.pack(pady=20)

#Stop Button
stopatt = CTkButton(master=message_frame, text="Stop Attendance", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225,height=40,command =root.destroy)
stopatt.pack(anchor="w", pady=(350, 0), padx=(20, 2))

#Video Frame
frame_label = CTkLabel(frame_frame,text="")
frame_label.pack()

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

    #new Rectangle Logic
    frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    #ends here

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

        #Old Face Rect Logic
        # y1, x2, y2, x1 = loc
        # y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
        # bbox = x1, y1, x2 - x1, y2 - y1
        # img = cvzone.cornerRect(img, bbox, rt=0)

        matchIndex = np.argmin(faceDist)
        if matches[matchIndex]:
            count_mismatch = 0
            face_id_detected.append(studentIDs[matchIndex])
            if count == 5:
                #FACE IS RECOGNIZED AND THE ATTENDANCE IS MARKED STATUS: YOUR ATTENDACE HAS BEEN MARKED
                id_detected = get_id(face_id_detected)
                display_message("Welcome! Attendance Marked")
                ##the prson has been detected. So nark their attendance
                if id_detected in Lis:
                    display_message("Attendance already marked!")
                else:
                    Lis.append(id_detected)
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
                display_message("No Match! Kindly Mark Your Attendance using OTP")
                ##OTP Function called here target=functionName 
                '''if otp_thread is None or not otp_thread.is_alive():
                    otp_thread = threading.Thread(target=otp_msg)
                    otp_thread.start()
                '''
                reply = messagebox.askyesno("OTP", "Do you want to mark attendance using OTP?")

                root2.withdraw()
                #OTP MSG IS THE OTP FUNCTION
                if reply:
                    otp_returned = otp_msg(Lis)
                    if otp_returned != False and otp_returned != 101:
                        display_message("Attendance Marked using OTP")
                        mark(otp_returned, file_name, col_num)
                        save_file(file_name)
                        Lis.append(otp_returned)
                        count = 0
                        face_id_detected.clear()
                    elif otp_returned != 101:
                        display_message("Attendance alread marked!")
                else:
                    continue

                count_mismatch = 0
            else:
                count_mismatch += 1
                display_message("Unable to Recognize")
            count = 0
            face_id_detected.clear()

    #Updating Image Frames
    photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
    frame_label.configure(image=photo)
    frame_label.image = photo
    root.update()
##close excel sheet
root.mainloop()
save_file(file_name)
##send email
send_copy(file_name, section, subject)

# except Exception as e:
#     print("Keyboard interrupt detected. Sending email copy...")