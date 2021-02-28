# -*- coding: utf-8 -*-
"""
Sanitized version of the "video speed test" example from pyqtgraph
data displayed in the video is generated on-the-fly, reaching ~20fps
"""

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
import VideoTemplate

app = QtGui.QApplication([])

win = QtGui.QMainWindow()
win.setWindowTitle('Camera preview')
ui = VideoTemplate.Ui_MainWindow()
ui.setupUi(win)
win.show()

ui.maxSpin1.setOpts(value=255, step=1)
ui.minSpin1.setOpts(value=0, step=1)

vb = pg.ViewBox()
ui.graphicsView.setCentralItem(vb)
vb.setAspectLocked()
img = pg.ImageItem()
img.setCacheMode(1) #CacheMode of Qt, see https://doc.qt.io/qt-5/qgraphicsview.html#CacheModeFlag-enum
# img.setRect(QtCore.QRectF(0, 0, 512, 512))
vb.addItem(img)
vb.setRange(QtCore.QRectF(0, 0, 512, 512))


width = 1024
height = 1024

lastTime = ptime.time()
fps = None
def update():
    global ui, lastTime, fps, img
    data_raw=np.abs(np.fft.fft2(np.random.normal(size=(width,height),loc=128,scale=64)))
    data_on_the_fly=np.uint8(data_raw) # data must be uint8 if autoLevels=False
    img.setImage(data_on_the_fly, autoLevels=False)
    ui.stack.setCurrentIndex(0)

    now = ptime.time()
    dt = now - lastTime
    lastTime = now
    if fps is None:
        fps = 1.0/dt
    else:
        s = np.clip(dt*3., 0, 1)
        fps = fps * (1-s) + (1.0/dt) * s
    ui.fpsLabel.setText('%0.2f fps' % fps)
    app.processEvents()  ## force complete redraw for every plot
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)