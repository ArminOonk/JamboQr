#!/usr/bin/python3.5
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import pyzbar.pyzbar as pyzbar


def decode(im):
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)

    # Print results
    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data, '\n')

    return decodedObjects


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)
font = cv2.FONT_HERSHEY_SIMPLEX

prev_time = time.time()
frame_counter = 0
frame_average = 10
osd_text = ''
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

    # On screen text
    frame_counter += 1
    if frame_counter % frame_average == 0:
        dt = time.time() - prev_time
        prev_time = time.time()
        osd_text = 'fps: ' + str(int(float(frame_average) / dt))

    cv2.putText(image, osd_text, (10, 50), font, 1.0, (255, 255, 255), 2, cv2.LINE_AA)

    decodedObjects = decode(image)

    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
