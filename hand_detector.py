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
# from picamera.array import PiRGBArray  # Generates a 3D RGB array
# from picamera import PiCamera  # Provides a Python interface for the RPi Camera Module
import time  # Provides time-related functions
import cv2 as cv # OpenCV library
import numpy as np
import sys
from skimage.metrics import structural_similarity as compare_ssim
import imutils


img = cv.imread(cv.samples.findFile("resources/background.png"))
gray_background = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
if img is None:
    sys.exit("Could not read the image.")
cv.imshow("Display window", gray_background)
# k = cv.waitKey(0)

WIN_RF = "Reference"

framenum = -1 # Frame counter
cap = cv.VideoCapture("sample1.h264")

if not cap.isOpened():
    print("Could not open the reference " + sourceReference)
    sys.exit(-1)

ref_size = (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))
cv.namedWindow(WIN_RF, cv.WINDOW_AUTOSIZE)
cv.moveWindow(WIN_RF, 0, 0) #750,  2 (bernat =0)

# cv.namedWindow("diff", cv.WINDOW_AUTOSIZE)
# cv.moveWindow("diff", 640, 0) #750,  2 (bernat =0)

def skeletonize(image_in):
    '''Inputs and grayscale image and outputs a binary skeleton image'''
    size = np.size(image_in)
    skel = np.zeros(image_in.shape, np.uint8)

    ret, image_edit = cv2.threshold(image_in, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    done = False

    while not done:
        eroded = cv2.erode(image_edit, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(image_edit, temp)
        skel = cv2.bitwise_or(skel, temp)
        image_edit = eroded.copy()

        zeros = size - cv2.countNonZero(image_edit)
        if zeros == size:
            done = True

    return skel

delay = 3
# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    out = gray.copy()
    out[0:0, 300:400] = 0
    # diff = gray - gray_background
    cv.subtract(gray, gray_background, out)

    kernel = np.ones((5, 5), np.float32) / 25
    dst = cv.filter2D(out, -1, kernel)

    ret, thresh1 = cv.threshold(dst, 25, 255, cv.THRESH_BINARY)

    ## Using SSIM Instead of our more manual approach
    (score, diff) = compare_ssim(gray, gray_background, full=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))
    thresh = cv.threshold(diff, 0, 255,
                           cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
    cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL,
                            cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv.boundingRect(c)
        cv.rectangle(gray, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # cv.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Display the resulting frame
    cv.imshow('Frame', gray)
    cv.imshow("diff", thresh1)

    # Press Q on keyboard to  exit
    if cv.waitKey(250) & 0xFF == ord('q'):
      break

  # Break the loop
  else:
    break


# Press Q on keyboard to  exit
cv.waitKey(0)

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv.destroyAllWindows()

