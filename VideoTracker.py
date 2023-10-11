#image load and track
#https://github.com/Dhrumilcse/Face-and-Motion-detector-OpenCV/tree/master

import cv2
from datetime import datetime


first_frame = None
our_video = cv2.VideoCapture(0)
def detectFacesFrame(check,frame):

    check, newframe = our_video.read()
    #Conver to Gray
    frame = cv2.cvtColor(newframe, cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(frame,(21,21),0)

    #Set first frame
    if first_frame is None:
        first_frame=frame

    rectangles = compareFrames(first_frame,frame)
    drawFrame(frame,rectangles, first_frame)


def drawFrame(frame, rectangles, first_frame):
    for x, y, w, h in rectangles:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)
    cv2.imshow("First Frame", first_frame)
    cv2.imshow("Detecting objects", frame)



def imgFromPath(imgpath):
    img = cv2.imread(imgpath,0)
    return img

def processImage(img,resize=False):
    #returns a greyscale and blurred image from input
    if(resize):
        img = cv2.resize(img,(500,400))
    img= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img,(21,21),0)
    return img



# cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3) - applied to the current frame


def findFace(img):
    #Load Cascade
    face_cascade = cv2.CascadeClassifier("haarcascade_frontface_default.xml")
    #detect faces
    faces = face_cascade.detectMultiScale(img,
    scaleFactor = 1.05,
    minNeighbors = 5
    )
    return faces

def showFaces(img,faces):
    for x, y, w, h in faces:
        img_rect = cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 3)
    #Show Image with rectangles around faces
    cv2.imshow("Face Detection", img_rect)
    cv2.waitKey(0)
    cv2.destroyAllWindows



    






