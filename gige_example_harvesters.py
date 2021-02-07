# -*- coding: utf-8 -*-
"""
Interface with GigE camera via GenICam support from Harvesters

@author: Zheyuan Zhu
"""

import numpy as np
from harvesters.core import Harvester
h = Harvester()
h.add_file('C:\Program Files\Allied Vision\Vimba_3.1\VimbaGigETL\Bin\Win64\VimbaGigETL.cti')
h.update()

#%% image acquisition initialization and settings on device 0
ia = h.create_image_acquirer(0)
ia.remote_device.node_map.BalanceWhiteAuto.value = 'Off'
ia.remote_device.node_map.ExposureAuto.value = 'Off'
ia.remote_device.node_map.ExposureTimeAbs.value = 50000
ia.remote_device.node_map.AcquisitionFrameRateAbs.value = 5

#%% start acqusition
ia.start_acquisition(run_in_background = True)
buffer = ia.fetch_buffer()

# do something with the buffer
img_from_buffer=buffer.payload.components[0].data
img=np.reshape(img_from_buffer,(2056,2464),order='C')
buffer.queue()

#%% procedures to stop acquisition and free resources
ia.stop_acquisition()
ia.destroy()
h.reset()