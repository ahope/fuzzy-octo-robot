## From: https://automaticaddison.com/how-to-set-up-real-time-video-using-opencv-on-raspberry-pi-4/

# from picamera import PiCamera
# from time import sleep
# 
# camera = PiCamera()
# camera.start_preview()
# sleep(10)
# camera.stop_preview()

# Credit: Adrian Rosebrock
# https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
 
# import the necessary packages
from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
import time # Provides time-related functions
import cv2 # OpenCV library
import numpy as np

# Initialize the camera
camera = PiCamera()

backSub = cv2.createBackgroundSubtractorMOG2()
 
# Set the camera resolution
camera.resolution = (640, 480)
 
# Set the number of frames per second
camera.framerate = 32
 
# Generates a 3D RGB array and stores it in rawCapture
bg_capture = PiRGBArray(camera, size=(640, 480))
# Wait a certain number of seconds to allow the camera time to warmup
time.sleep(2)


# cap = cv2.VideoCapture(raw_capture)
# # take first frame of the video
# ret,frame = cap.read()

# camera.capture(bg_capture, format="bgr", use_video_port=True)
camera.capture("background.png", use_video_port=True)

# # setup initial location of window
# x, y, w, h = 300, 200, 100, 50 # simply hardcoded the values
# track_window = (x, y, w, h)
# # set up the ROI for tracking
# roi = raw_capture.array[y:y+h, x:x+w]
# hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
# mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
# roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
# cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
 


# cv2.imshow("bg", bg_capture.array)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
 
# aha: For some reason, after we do the original capture, I can't use the raw_capture array in the loop.
## Something about the wrong buffer length for a given width/height of the image
raw_capture = PiRGBArray(camera, size=(640, 480))

max_lowThreshold = 100
window_name = 'Edge Map'
title_trackbar = 'Min Threshold:'
ratio = 3
kernel_size = 3
low_threshold = 2

camera.start_recording("sample1.h264")
print("recording has started")
# time.sleep(10)
camera.wait_recording(15)
camera.stop_recording()

