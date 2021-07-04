from tkinter import *
import cv2
from utils import *
from matplotlib import pyplot as plt
import os
import beepy

from PIL import ImageTk,Image
import subprocess
#from gtts import gTTS
from tkinter.filedialog import askopenfilename



videoCaptureObject = cv2.VideoCapture(0)

def scan1():
    message.configure(text="SCANNING IN PROGRESS........")

    max_val = 8
    max_pt = -1
    max_kp = 0

    orb = cv2.ORB_create()
    # orb is an alternative to SIFT

    #test_img = read_img('files/test_100_2.jpg')
    #test_img = read_img('files/test_50_2.jpg')
    path= askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
                           filetypes =(("Image File", "*.jpg"),("All Files","*.*")),
                           title = "Choose a file.")
    test_img = read_img(path)
    #test_img = read_img('files/test_20_4.jpg')

    # resizing must be dynamic
    original = resize_img(test_img, 0.4)
    #display('original', original)

    # keypoints and descriptors
    # (kp1, des1) = orb.detectAndCompute(test_img, None)
    (kp1, des1) = orb.detectAndCompute(test_img, None)

    training_set = ['files/20.jpg', 'files/50.jpg', 'files/100.jpg', 'files/500.jpg']

    for i in range(0, len(training_set)):
    	# train image
    	train_img = cv2.imread(training_set[i])

    	(kp2, des2) = orb.detectAndCompute(train_img, None)

    	# brute force matcher
    	bf = cv2.BFMatcher()
    	all_matches = bf.knnMatch(des1, des2, k=2)

    	good = []
    	# give an arbitrary number -> 0.789
    	# if good -> append to list of good matches
    	for (m, n) in all_matches:
    		if m.distance < 0.789 * n.distance:
    			good.append([m])

    	if len(good) > max_val:
    		max_val = len(good)
    		max_pt = i
    		max_kp = kp2

    	print(i, ' ', training_set[i], ' ', len(good))
    flag=1
    if max_val >20:
    	print(training_set[max_pt])
    	print('good matches ', max_val)

    	train_img = cv2.imread(training_set[max_pt])
    	img3 = cv2.drawMatchesKnn(test_img, kp1, train_img, max_kp, good, 4)

    	note = str(training_set[max_pt])[6:-4]
    	print('\nDetected denomination: Rs. ', note)


    	audio_file = 'audio/{}.mp3'.format(note)



    else:
    	flag=0

    message.configure(text="SCANNING COMPLETED!!!")
    if(flag==0):
        message3.configure(text="")
        message2.configure(text="ERROR!\n Fake Note Detected",fg="red",font=("Helvestica",40))


        s=beepy.beep(sound="ready")
    else:
        message2.configure(text="")
        message3.configure(text="Original note detected!\nDetected denomination: Rs."+" "+note,fg="green",font=("Helvestica",20))



def scan():
    message.configure(text="SCANNING IN PROGRESS........")
    cv2.imwrite("test_image.jpg",frame)
    max_val = 8
    max_pt = -1
    max_kp = 0

    orb = cv2.ORB_create()

    #test_img = read_img('files/test_100_2.jpg')
    #test_img = read_img('files/test_50_2.jpg')
    test_img = read_img('test_image.jpg')
    #test_img = read_img('files/test_100_3.jpg')
    #test_img = read_img('files/test_20_4.jpg')

    # resizing must be dynamic
    original = resize_img(test_img, 0.4)
    #display('original', original)

    # keypoints and descriptors
    # (kp1, des1) = orb.detectAndCompute(test_img, None)
    (kp1, des1) = orb.detectAndCompute(test_img, None)

    training_set = ['files/20.jpg', 'files/50.jpg', 'files/100.jpg', 'files/500.jpg']

    for i in range(0, len(training_set)):
    	# train image
    	train_img = cv2.imread(training_set[i])

    	(kp2, des2) = orb.detectAndCompute(train_img, None)

    	# brute force matcher
    	bf = cv2.BFMatcher()
    	all_matches = bf.knnMatch(des1, des2, k=2)

    	good = []
    	# give an arbitrary number -> 0.789
    	# if good -> append to list of good matches
    	for (m, n) in all_matches:
    		if m.distance < 0.789 * n.distance:
    			good.append([m])

    	if len(good) > max_val:
    		max_val = len(good)
    		max_pt = i
    		max_kp = kp2

    	print(i, ' ', training_set[i], ' ', len(good))
    flag=1
    if max_val >20:
    	print(training_set[max_pt])
    	print('good matches ', max_val)

    	train_img = cv2.imread(training_set[max_pt])
    	img3 = cv2.drawMatchesKnn(test_img, kp1, train_img, max_kp, good, 4)

    	note = str(training_set[max_pt])[6:-4]
    	print('\nDetected denomination: Rs. ', note)


    	audio_file = 'audio/{}.mp3'.format(note)



    else:
    	flag=0

    message.configure(text="SCANNING COMPLETED!!!")
    if(flag==0):
        message3.configure(text="")
        message2.configure(text="ERROR!\n Fake Note Detected",fg="red",font=("Helvestica",40))


        s=beepy.beep(sound="ready")
    else:
        message2.configure(text="")
        message3.configure(text="Original note detected!\nDetected denomination: Rs."+" "+note,fg="green",font=("Helvestica",20))


def scanning():
    global frame
    def yes():
        #cv2.waitKey(0) # wait for closing
        #cv2.destroyAllWindows() # Ok, destroy the window
        message.configure(text="Please click on Start Scanning")
        up['state']=NORMAL
        but['state']=DISABLED
        but_yes['state']=DISABLED
        but_no['state']=DISABLED

    message.configure(text=" Choose Below Option")
    ret,frame = videoCaptureObject.read()


    #--------------------------------------
    but_yes= Button(window,text="YES/NEXT" , font=("Helvestica",20),bg='black',fg='purple2', command=yes)
    but_yes.place(x=130,y=240, height=50,width=250)
    but_no= Button(window,text="NO/SCAN AGAIN" , font=("Helvestica",20),bg='black',fg='purple2', command=scanning)
    but_no.place(x=430,y=240, height=50,width=250)

    cv2.imshow('image',frame)
    #cv2.waitKey(0) # wait for closing
    #cv2.destroyAllWindows() # Ok, destroy the window
    but['state']=DISABLED
    #up['state']=NORMAL
    print("testing1")
    def des1():
        print("hello")
        cv2.destroyAllWindows() # Ok, destroy the window
    window.after(5000,des1)

def activate():
    but['state']=NORMAL
    m1.configure(text="")
    message.configure(text="Please click on Scan Currency to scan Image")
    upload['state']=NORMAL

window=Tk()
window.geometry('800x700')
window.title("COUNTERFEIT NOTES DETECTION")
window.configure(background='black')
window.resizable(0,0)


but= Button(window, command= scanning, font=("Helvestica",20),bg='black',fg='purple2')
but.place(x=300,y=40, height=50, width=250)
but['state']=DISABLED

message=Label(window,font=("Helvestica",15),bg='black',fg='white')
message.place(x=260,y=130)

up=Button(window,text="Start Scanning", command=scan, font=("Helvestica",20),bg='black',fg='purple2')
up.place(x=300,y=500, height=50, width=250)
but.configure(text="Scan Currency")
up['state']=DISABLED


upload=Button(window,text="Browse & Scan", font=("Helvestica",20),bg='black',fg='purple2', command=scan1)
upload.place(x=300,y=570, height=50, width=250)
upload['state']=DISABLED

message2=Label(window,font=("Helvestica",25),bg='black',fg='white')
message2.place(x=200,y=350)

message3=Label(window,font=("Helvestica",15),bg='black',fg='white')
message3.place(x=250,y=350)

m1=Label(window,font=("Helvestica",25),bg='black',fg='white')
m1.place(x=300,y=280)
m1.configure(text="LOADING DEPENDENCIES...")
window.after(20000,activate)
window.mainloop()
