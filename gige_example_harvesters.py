# -*- coding: utf-8 -*-
"""
Interface with GigE camera via GenICam support from Harvesters
Use Mono8 for alignment; BayerRG12 for capture

@author: Zheyuan Zhu
"""

import numpy as np
import matplotlib.pyplot as plt
from harvesters.core import Harvester
h = Harvester()
h.add_file('C:\Program Files\Allied Vision\Vimba_3.1\VimbaGigETL\Bin\Win64\VimbaGigETL.cti')
h.update()

#%% camera settings
exp_time=50000; # longest exposure time needed to reveal the details
framerate=5;
gain=0;
# color balance settings for lens
gain_r=1.87
gain_b=3.00

#%% image acquisition initialization and settings on device 0
ia = h.create_image_acquirer(0)
ia.remote_device.node_map.PixelFormat.value = 'Mono8'
ia.remote_device.node_map.BalanceWhiteAuto.value = 'Off'
ia.remote_device.node_map.ExposureAuto.value = 'Off'
ia.remote_device.node_map.GainAuto.value = 'Off'
ia.remote_device.node_map.BalanceRatioSelector.value = 'Red'
ia.remote_device.node_map.BalanceRatioAbs.value = gain_r
ia.remote_device.node_map.BalanceRatioSelector.value = 'Blue'
ia.remote_device.node_map.BalanceRatioAbs.value = gain_b
ia.remote_device.node_map.ExposureTimeAbs.value = exp_time
ia.remote_device.node_map.Gain.value = gain
ia.remote_device.node_map.AcquisitionFrameRateAbs.value = framerate

#%% start acqusition
ia.start_acquisition(run_in_background=True)
buffer=ia.fetch_buffer()
# do something with the buffer
component=buffer.payload.components[0]
width = component.width
height = component.height
data_format = component.data_format
img=np.reshape(component.data,(height,width),order='C')
# plot the image
plt.figure()
plt.imshow(img,cmap='jet')
buffer.queue()

#%% stop acquisition and free resources
ia.stop_acquisition()
ia.destroy()
h.reset()