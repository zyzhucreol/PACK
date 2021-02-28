## has to be in the pyqtgraph example folder to work
import sys

import picamera
import picamera.array
from fractions import Fraction
camera=picamera.PiCamera()
camera.iso = 80
camera.framerate = 5
camera.shutter_speed = 700000
camera.exposure_mode = 'off'
camera.awb_mode = 'off'
camera.awb_gains = (Fraction(313, 128), Fraction(289, 128))
camera.resolution = (1664,1232)
stream = picamera.array.PiRGBArray(camera)
# -*- coding: utf-8 -*-
"""
Demonstrates very basic use of ImageItem to display image data inside a ViewBox.
"""

from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
import pyqtgraph.ptime as ptime

app = QtGui.QApplication([])

## Create window with GraphicsView widget
win = pg.GraphicsLayoutWidget()
win.show()  ## show widget alone in its own window
win.setWindowTitle('picamera preview')
view = win.addViewBox()

## lock the aspect ratio so pixels are always square
view.setAspectLocked(True)

## Create image item
img = pg.ImageItem(border='w')
view.addItem(img)

## Set initial view bounds
view.setRange(QtCore.QRectF(0, 0, 600, 600))

updateTime = ptime.time()
fps = 0

def updateData():
    global img, data, i, updateTime, fps
    # Display the data from camera stream
    # camera.capture(stream, 'rgb')
    # img_rgb_array=np.float32(stream.array)
    # img_int_array=img_rgb_array[:,:,0]*0.299+img_rgb_array[:,:,1]*0.587+img_rgb_array[:,:,2]*0.114
    # data=np.transpose(img_int_array)
    # Display data from random number generator for debug purpose
    data=np.random.random((2056,2464))
    img.setImage(data)#,autoLevels=False, levels=[0,255])
    stream.seek(0)
    stream.truncate()
    QtCore.QTimer.singleShot(1, updateData)
    now = ptime.time()
    fps2 = 1.0 / (now-updateTime)
    updateTime = now
    fps = fps * 0.9 + fps2 * 0.1
    
    print("fps=",fps,end='\r')
    

updateData()

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()