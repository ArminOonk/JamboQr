#!/usr/bin/python3.5
# import the necessary packages
from picamera.array import PiYUVArray
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


def main():
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiYUVArray(camera, size=camera.resolution)

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

    cv2.namedWindow('Frame', flags=cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    border = cv2.imread('border.png')
    # print('imread border shape: ' + str(border.shape))
    border = np.zeros((1080, 1920), np.uint8)

    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="yuv", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array
        image = image[:camera.resolution[1], :camera.resolution[0], 0]

        # On screen text
        frame_counter += 1
        if frame_counter % frame_average == 0:
            dt = time.time() - prev_time
            prev_time = time.time()
            osd_text = 'fps: ' + '{:.2f}'.format(float(frame_average) / dt)

        # cv2.putText(image, osd_text, (10, 50), font, 1.0, (255, 255, 255), 2, cv2.LINE_AA)

        decodedObjects = decode(image)
        jambo_tags = []
        for do in decodedObjects:
            txt = do.data.decode("utf-8")
            if txt.startswith('jambo'):
                jambo_tags.append(txt)

            if txt == 'jambo:STOP':
                print('Stopping')
                return

        if len(jambo_tags) != prev_nr_jambo:
            print('Number of jambo tags: ' + str(len(jambo_tags)))
            prev_nr_jambo = len(jambo_tags)

            set_jambo = set(jambo_tags)
            for sj in set_jambo:
                print(sj + ' occured: ' + str(jambo_tags.count(sj)))

        # Sephia
        # image = cv2.transform(image, m_sepia)
        image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        y_offset = int(0.5 * (border.shape[0] - image.shape[0]))
        x_offset = int(0.5 * (border.shape[1] - image.shape[1]))

        y1, y2 = y_offset, y_offset + image.shape[0]
        x1, x2 = x_offset, x_offset + image.shape[1]

        border[y1:y2, x1:x2] = image

        # show the frame
        cv2.imshow("Frame", border)
        key = cv2.waitKey(1) & 0xFF

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            return


if __name__ == '__main__':
    main()
