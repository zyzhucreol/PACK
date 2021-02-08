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

def frame_handler(cam, frame):
    cam.queue_frame(frame)

with Vimba.get_instance() as vimba:
    cams = vimba.get_all_cameras()
    with cams[0] as cam:
        cam.start_streaming(frame_handler)
        time.sleep(5)
        cam.stop_streaming()