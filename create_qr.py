#!/usr/bin/python3.5
import pyqrcode

qr_name = 'wrench'
qr = pyqrcode.create('jambo:' + qr_name, error='H')
qr.svg(qr_name + '.svg', scale=8)
print(qr.terminal(quiet_zone=1))
