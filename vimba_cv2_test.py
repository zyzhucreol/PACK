# -*- coding: utf-8 -*-
"""
Interface with GigE camera via Allied Vision Vimba
Use Mono8 for alignment; BayerRG12 for capture

@author: Zheyuan Zhu
"""
import threading
import numpy as np
from vimba import Vimba
from vimba.camera import Camera, Frame
from vimba.frame import FrameStatus
import cv2
from scipy import fft

#%% copied from video_test_santized example
# from pyqtgraph.Qt import QtGui, QtCore
# import pyqtgraph as pg
# import pyqtgraph.ptime as ptime
# import VideoTemplate

# app = QtGui.QApplication([])

# win = QtGui.QMainWindow()
# win.setWindowTitle('Camera preview')
# ui = VideoTemplate.Ui_MainWindow()
# ui.setupUi(win)
# win.show()

# ui.maxSpin1.setOpts(value=255, step=1)
# ui.minSpin1.setOpts(value=0, step=1)

# vb = pg.ViewBox()
# ui.graphicsView.setCentralItem(vb)
# vb.setAspectLocked()
# img = pg.ImageItem()
# img.setCacheMode(1) #CacheMode of Qt, see https://doc.qt.io/qt-5/qgraphicsview.html#CacheModeFlag-enum
# # img.setRect(QtCore.QRectF(0, 0, 512, 512))
# vb.addItem(img)
# vb.setRange(QtCore.QRectF(0, 0, 512, 512))


# width = 1024
# height = 1024

# lastTime = ptime.time()
# fps = None
# def update(data_from_camera):
#     global ui, lastTime, fps, img
#     data_raw=np.abs(np.fft.fft2(data_from_camera))
#     data_raw=data_raw/np.max(data_raw)*255
#     data_on_the_fly=np.uint8(data_raw) # data must be uint8 if autoLevels=False
#     img.setImage(data_on_the_fly, autoLevels=False)
#     ui.stack.setCurrentIndex(0)

#     now = ptime.time()
#     dt = now - lastTime
#     lastTime = now
#     if fps is None:
#         fps = 1.0/dt
#     else:
#         s = np.clip(dt*3., 0, 1)
#         fps = fps * (1-s) + (1.0/dt) * s
#     ui.fpsLabel.setText('%0.2f fps' % fps)
#     app.processEvents()  ## force complete redraw for every plot
# # timer = QtCore.QTimer()
# # timer.timeout.connect(update)
# # timer.start(0)

#%% copied from Vimba example
do_nothing=lambda *args: None
crop_size=1024
frame_row=2056
frame_col=2464
start_ind_row=int((frame_row-crop_size)/2)
start_ind_col=int((frame_col-crop_size)/2)
end_ind_row=start_ind_row+crop_size
end_ind_col=start_ind_col+crop_size
x=np.arange(crop_size)
y=np.arange(crop_size)
x_c=(crop_size-1)/2
y_c=(crop_size-1)/2
X,Y=np.meshgrid(x,y,indexing='xy')
X_flat=np.reshape(X,(-1),order='F')
Y_flat=np.reshape(Y,(-1),order='F')
n_radius=int(crop_size/2)
R=np.sqrt((X-x_c)**2+(Y-y_c)**2)
fft_data=np.zeros((1024,1024))
f_avg=lambda r_temp:fft_data[(R>=r_temp-0.5) & (R<r_temp+0.5)].mean()
r=np.arange(1,n_radius)
background=np.zeros((1024,1024),'int8')

class Handler:
    def __init__(self):
        self.shutdown_event = threading.Event()

    def __call__(self, cam: Camera, frame: Frame):
        global fft_data
        ENTER_KEY_CODE = 13

        key = cv2.waitKey(1)
        if key == ENTER_KEY_CODE:
            self.shutdown_event.set()
            return

        elif frame.get_status() == FrameStatus.Complete:
            print('{} acquired {}'.format(cam, frame), flush=True)
            img_buffer=frame.as_numpy_ndarray()
            if np.shape(img_buffer)[2] == 1: # grayscale or Bayer image
                img=np.float64(np.squeeze(img_buffer))
            else: # rgb2gray
                img_float=np.float64(img_buffer)
                img=0.299*img_float[:,:,0]+0.5870*img_float[:,:,1]+0.1140*img_float[:,:,2]
            data=img[start_ind_row:end_ind_row,start_ind_col:end_ind_col]
            fft_data=np.log(np.abs(fft.fftshift(fft.fft2(data))))
            fft_data=fft_data/np.max(fft_data)
            fft_data_radial=np.vectorize(f_avg)(r)
            cv2.imshow('test-cam',fft_data)
            cv2.resizeWindow('test-cam',1024,768)
            # cv2.polylines(background,[np.column_stack((r,fft_data_radial))])
            # cv2.resizeWindow('MTF',1024,768)
        cam.queue_frame(frame)

def frame_handler(cam, frame):
    data_from_camera=frame2data(frame)
    cv2.imshow('test-cam',data_from_camera)
    cam.queue_frame(frame)

def frame2data(frame):
    img_buffer=frame.as_numpy_ndarray()
    if np.shape(img_buffer)[2] == 1: # grayscale or Bayer image
        img=np.float64(np.squeeze(img_buffer))
    else: # rgb2gray
        img_float=np.float64(img_buffer)
        img=0.299*img_float[:,:,0]+0.5870*img_float[:,:,1]+0.1140*img_float[:,:,2]
    data=img[start_ind_row:end_ind_row,start_ind_col:end_ind_col]
    return data

with Vimba.get_instance() as vimba:
    cams = vimba.get_all_cameras()
    with cams[0] as cam:
        handler = Handler()
        # asynchronous streaming
        try:
            cam.start_streaming(handler=handler, buffer_count=1)
            handler.shutdown_event.wait()
        finally:
            cam.stop_streaming()