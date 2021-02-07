# Software for Portiable Astronomical Computation-and-imaging Kit (PACK)
Portiable Astronomical Computation-and-imaging Kit (PACK) is a take-home project for ameture astronomical imaging. The hardware overview of the PACK imaging system can be found at https://www.facebook.com/zyzhu0/posts/2763787760599751. This repository provides the hardware control, image acquisition and processing modules.

To modify the package for a different camera:
* Make sure the camera supports GenICam protocol. Obtain the transport layer *.cti file from the camera SDK directory.
* Check and prepare the list of attribute names for camera control. For example, to change the exposure time, some camera uses the attribute name "ExposureTime", some uses "ExposureTimeAbs". These names can be found in NI-MAX if NI-imaq is installed.
