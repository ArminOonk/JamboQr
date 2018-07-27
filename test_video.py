#!/usr/bin/python3.5
# import the necessary packages
from picamera.array import PiYUVArray
from picamera import PiCamera
import time
import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np


def get_jambo_tags(decode_objects):
    jambo_tags = []
    for do in decode_objects:
        txt = do.data.decode("utf-8")
        if txt.startswith('jambo'):
            jambo_tags.append(txt)
    return jambo_tags


def main():
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (640, 480)
    raw_capture = PiYUVArray(camera, size=camera.resolution)

    # allow the camera to warmup
    time.sleep(0.1)
    font = cv2.FONT_HERSHEY_SIMPLEX

    prev_time = time.time()
    frame_counter = 0
    frame_average = 10
    osd_text = ''
    found_text = ''

    prev_nr_jambo = 0

    cv2.namedWindow('Frame', flags=cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    border = np.zeros((1080, 1920), np.uint8)

    # capture frames from the camera
    for frame in camera.capture_continuous(raw_capture, format="yuv", use_video_port=True):
        image = frame.array

        # On screen text
        frame_counter += 1
        if frame_counter % frame_average == 0:
            dt = time.time() - prev_time
            prev_time = time.time()
            osd_text = 'fps: ' + '{:.2f}'.format(float(frame_average) / dt)

        cv2.putText(image, osd_text, (10, 50), font, 1.0, (255, 255, 255), 2, cv2.LINE_AA)

        jambo_tags = get_jambo_tags(pyzbar.decode(image))

        if 'jambo:STOP' in jambo_tags:
            print('Stopping')
            return

        if len(jambo_tags) != prev_nr_jambo:
            found_text = 'Found:'
            print('Number of jambo tags: ' + str(len(jambo_tags)))
            prev_nr_jambo = len(jambo_tags)

            set_jambo = set(jambo_tags)
            for sj in set_jambo:
                tag_count = jambo_tags.count(sj)
                print(sj + ' occured: ' + str(tag_count))

                if tag_count == 4:
                    found_text += ' ' + sj

        cv2.putText(image, found_text, (10, 100), font, 1.0, (255, 255, 255), 2, cv2.LINE_AA)

        image = image[:camera.resolution[1], :camera.resolution[0], 0]
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
        raw_capture.truncate(0)

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            return


if __name__ == '__main__':
    main()
