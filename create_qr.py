#!/usr/bin/python3.5
import pyqrcode

qr = pyqrcode.create('jambo:gearhead', error='H')
qr.svg('jambo.svg', scale=8)
print(qr.terminal(quiet_zone=1))
