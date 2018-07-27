#!/usr/bin/python3.5
from picamera import PiCamera
import time
from picamera.array import PiYUVArray
import cv2
import pyzbar.pyzbar as pyzbar


camera = PiCamera()
camera.resolution = (640, 480)
rawCapture = PiYUVArray(camera, size=camera.resolution)

camera.start_preview()
time.sleep(2.0)

camera.capture(rawCapture, format="yuv")
camera.stop_preview()

image = rawCapture.array
image = image[:480, :640, 0]
cv2.imwrite('test_je.png', image)

decodedObjects = pyzbar.decode(image)

for obj in decodedObjects:
    print('Type : ' + str(obj.type))
    print('Data : ' + str(obj.data))
