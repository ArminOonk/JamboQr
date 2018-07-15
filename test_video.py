#!/usr/bin/python3.5
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np


def decode(im):
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)

    # # Print results
    # for obj in decodedObjects:
    #     print('Type : ', obj.type)
    #     print('Data : ', obj.data, '\n')

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

m_sepia = np.asarray([[0.393, 0.769, 0.189],
                      [0.349, 0.686, 0.168],
                      [0.272, 0.534, 0.131]])

prev_nr_jambo = 0
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
    jambo_tags = []
    for do in decodedObjects:
        txt = do.data.decode("utf-8")
        if txt.startswith('jambo'):
            jambo_tags.append(txt)

    if len(jambo_tags) != prev_nr_jambo:
        print('Number of jambo tags: ' + str(len(jambo_tags)))
        prev_nr_jambo = len(jambo_tags)

        set_jambo = set(jambo_tags)
        for sj in set_jambo:
            print(sj + ' occured: ' + str(jambo_tags.count(sj)))


    # Sephia
    sepia = cv2.transform(image, m_sepia)

    # show the frame
    cv2.imshow("Frame", sepia)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
