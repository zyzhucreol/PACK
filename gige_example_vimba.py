# -*- coding: utf-8 -*-
"""
Interface with GigE camera via Allied Vision Vimba
Use Mono8 for alignment; BayerRG12 for capture

@author: Zheyuan Zhu
"""

import numpy as np
import matplotlib.pyplot as plt
from vimba import Vimba
import time

do_nothing=lambda *args: None

def frame_handler(cam, frame):
    cam.queue_frame(frame)
    _=process_frame(frame)

def process_frame(frame):
    img_buffer=frame.as_numpy_ndarray()
    if np.shape(img_buffer)[2] == 1: # grayscale or Bayer image
        img=np.float64(np.squeeze(img_buffer))
    else: # rgb2gray
        img_float=np.float64(img_buffer)
        img=0.299*img_float[:,:,0]+0.5870*img_float[:,:,1]+0.1140*img_float[:,:,2]
    fft_img=np.abs(np.fft.fftshift(np.fft.fft2(img)))
    return fft_img

with Vimba.get_instance() as vimba:
    cams = vimba.get_all_cameras()
    with cams[0] as cam:
        # synchronous acquisition
        for frame in cam.get_frame_generator(limit=10):
            fft_img = process_frame(frame)
        # asynchronous streaming
        cam.start_streaming(frame_handler)
        time.sleep(5)
        cam.stop_streaming()
        
plt.figure()
plt.imshow(np.log10(fft_img),cmap='jet')