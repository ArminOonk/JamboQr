#!/usr/bin/python3.5
from picamera import PiCamera
import time
from picamera.array import PiYUVArray
import cv2

camera = PiCamera()
camera.resolution = (640, 480)
rawCapture = PiYUVArray(camera, size=camera.resolution)

time.sleep(0.1)

camera.capture(rawCapture, format="yuv")
image = rawCapture.array
print(str(image.shape))
cv2.imwrite('test_je.png', image[:480, :640, 0])

