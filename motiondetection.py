#import all necessary libraries
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
from twilio.rest import Client
import pyimgur

import time
import os
from dotenv import load_dotenv, find_dotenv


#initalize raspberry pi camera to certain resolution and framerate
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 30

capture = PiRGBArray(camera, size = (640,480))

#sleep to give camera time to power on
time.sleep(2)

#reference image, what future frames will be compared to
reference = None


#necessary client ids to fill from apis
TWILIO_ACCOUNT_SID = 'YOUR TWILIO ACCOUNT SID'
TWILIO_AUTH_TOKEN = 'YOUR TWILIO AUTHENTICATION TOKEN'
TWILIO_PHONE_NUMBER ='YOUR TWILIO PHONE NUMBER'
CELL_PHONE_NUMBER = 'YOUR MOBILE PHONE NUMBER'

IMGUR_API_ID = 'YOUR IMGUR API CLIENT ID'


#set path to your imgur account to upload detected images
im = pyimgur.Imgur(IMGUR_API_ID)


#environment constants
os.environ['TWILIO_ACCOUNT_SID'] = TWILIO_ACCOUNT_SID
os.environ['TWILIO_AUTH_TOKEN'] = TWILIO_AUTH_TOKEN
os.environ['TWILIO_PHONE_NUMBER'] = TWILIO_PHONE_NUMBER
os.environ['CELL_PHONE_NUMBER'] = CELL_PHONE_NUMBER



#while video in capture is playing.
for image in camera.capture_continuous(capture, format = 'bgr', use_video_port = True):

    #store current frame being viewed
    frame = image.array

    # convert current frame to gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # blur the image to for differentiating purposes
    gray = cv2.GaussianBlur(gray, (9, 9), 0)

    #if reference frame is none, initalize
    if reference is None:
        reference = gray.copy().astype("float")

    #accumulate the reference image as a weighted average, so
    #for small variables in image to not be tracked as much
    cv2.accumulateWeighted(gray, reference, 0.5)

    #difference between average and current frame
    change = cv2.absdiff(gray, cv2.convertScaleAbs(reference))


    # threshold for a difference to be recognized in motion
    thresh = cv2.threshold(change, 20, 255, cv2.THRESH_BINARY)[1]

    #iterations is noise level, change to higher for less noise
    dilate = cv2.dilate(thresh, None, iterations=3)

    #contours
    contours = cv2.findContours(dilate.copy(), cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)[0]

    # highlight motion
    for c in contours:
        #if detected object is >=500 pixels in size, detect it as motion
        if cv2.contourArea(c) >= 500:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        #send image to local folder to upload to imgur
	    cv2.imwrite('detected.jpg', frame)
	    upload = im.upload_image('detected.jpg', title="detected and uploaded with pyimgur")

        #send image to whatsapp and sleep so messages don't get spammed
	    client = Client(os.environ.get('TWILIO_ACCOUNT_SID'),os.environ.get('TWILIO_AUTH_TOKEN'))
	    client.messages.create(from_=os.environ.get('TWILIO_PHONE_NUMBER'),to=os.environ.get('CELL_PHONE_NUMBER'), media_url = upload.link,body = 'Object detected!')
	    time.sleep(1)

    # Display frame
    cv2.imshow('Motion Detector', frame)

    capture.truncate(0)
    
    # Press 'esc' for quit
    if cv2.waitKey(40) == 27:
        break

#close calls if escape is clicked or camera closes
cv2.destroyAllWindows()

