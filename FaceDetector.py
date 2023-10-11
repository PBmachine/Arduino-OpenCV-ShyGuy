# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
OpenCV detector code adapted from 
         @authors:
Yash Chandak    Ankit Dhall
OpenCV Human face tracker combined with arduino powered bot to
follow humans.
-------------------------------------------------------------------------------
"""
import numpy as np
import time
import serial
import cv2
import ShyGuy
import utils
"""
Arduino connected at port No. COM28,
Confirm and change this value accordingly from control panel
Baud Rate = 9600
"""


arduino_port = 'COM3'
arduino = serial.Serial(arduino_port, 9600)
time.sleep(2) # waiting the initialization...
# print("initialised")




def send(state,motion):

    new = False
    message = ""
    prev_state = shyguy.prev_state
    prev_motion = shyguy.prev_motion
    if (state !=prev_state):
        new = True
        prev_state = new
    if (round(prev_motion,2) != round(prev_motion,2)):
        new = True
        prev_motion = motion
    if new:
        string = state[0]+','+str(round(motion*100))
        message = bytes(string, 'utf-8')
        arduino.write(b'<')
        arduino.write(message)
        arduino.write(b'>')
    


def processImage(img,resize=False):
    blur = 13 #must be odd!
    #returns a greyscale and blurred image from input
    if(resize):
        img = cv2.resize(img,(500,400))
    img= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img,(blur,blur),0)
    return img

def markFace(faces,frame):
    if(len(faces)==0):
        return
    max_area=-1
    i=0
    for (x,y,w,h) in faces:
        if w*h > max_area:
            max_area=w*h
            pos=i
        i=i+1
    RECT=faces[pos]
    #Mark the face being tracked on the image display
    cv2.rectangle(frame, (RECT[0], RECT[1]), (RECT[0]+RECT[2], RECT[1]+RECT[3]), (0, 255, 0), 2)

def findFace(img):
    #detect faces
    faces = face_cascade.detectMultiScale(img,
    scaleFactor = 1.05,
    minNeighbors = 5,
    minSize=(30, 30),
    maxSize=(500,500)
    )
    return faces

def compareFrames(first_frame, current_frame):
    #takes two frames (first frame and current) and returns rectangles (x,y,w,h) for moving objects
    delta_frame = cv2.absdiff(first_frame, current_frame)
    threshold_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    threshold_frame = cv2.dilate(threshold_frame, None, iterations=2)
    #Contours
    cnts, hierarchy = cv2.findContours(threshold_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #Draw rectangle for moving objects
    rectangles = []
    for contour in cnts:
        if cv2.contourArea(contour) < 500:
            continue
        elif (cv2.contourArea(contour)>3000):
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangles.append((x,y,w,h))
        # cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)
    return rectangles



chill_timer = utils.timer(60*5,1)
debug_timer = utils.timer(5,1000)
update_scene = utils.timer(6,1)
frame_timer = utils.timer(0.1,1000) #check against previous frames
send_timer = utils.timer(0.5,1000) #check against previous frames

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
first_frame = None

cap = cv2.VideoCapture(0)
# cap.grab()
ret, frame = cap.retrieve()
cv2.namedWindow('frame')


motion_detected = False
shyguy = ShyGuy.shyguy()
faces = []
motion = []
check_faces = []
check_motion = []
avg_motion = 0
numcheck = 10
newFrame = True
showScreen = True
shyguy_state = ()

#Run the tracker in infinite loop
while True:
    #grab the frames from web camera
    ret, frame = cap.read()
    if ret ==0:
        print("frame not loaded")
        continue

    # if frame_timer.elapsed():
    #     newFrame = True 
    if (ret==True and newFrame==True):
        #set first frame if not already set
        frame = processImage(frame)
        if first_frame is None:
            first_frame=frame

        if update_scene.elapsed():
            #update the "base" motion frame periodically
            first_frame=frame
        
        #look for moving objects
        motion = compareFrames(first_frame,frame)
        faces = findFace(frame)
        num_faces = utils.checkAvgLen(faces,check_faces)
        num_motion = utils.checkAvgLen(motion,check_motion)

        cur_state,cur_motion = shyguy.update(num_faces,num_motion)
        if send_timer.elapsed():
            send(cur_state,cur_motion)


        if (showScreen):
            markFace(faces,frame)
            cv2.imshow('input',frame)
            if (debug_timer.elapsed()):
                print(f'num motion objects: {num_motion}')
                print(f'num faces: {num_faces}')
                print(f'elapsed{debug_timer.time_since_init()}')
                print(f'{cur_state,cur_motion}')
  

    #press q or ESC to exit program
    key = cv2.waitKey(1)
    if (key==ord('q') or key==27):
        break
    

#end loop
    
#Free up memory on exit    
cap.release()
cv2.destroyAllWindows()
# arduino.close()


