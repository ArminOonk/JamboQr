#!/usr/bin/python3.5
import cv2
import numpy as np

filename = 'zonnebloem.png'
frame = cv2.imread(filename)

m_sepia = np.asarray([[0.393, 0.769, 0.189],
                             [0.349, 0.686, 0.168],
                             [0.272, 0.534, 0.131]])
sepia = cv2.transform(frame, m_sepia)
# sepia = cv2.cvtColor(sepia, cv2.cv.CV_RGB2BGR)

cv2.imwrite(filename + '-output.png', sepia)
