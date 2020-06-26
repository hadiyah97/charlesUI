# USAGE
# python3 liveFeed_CamTest.py

import cv2
from drivers.Camera import Camera

#Cap = Camera("PiCam", "csi", 2)
#Cap = Camera("PiCam", "CSI", 2)
Cap = Camera("WebCam", "0", 2)
#Cap = Camera("WebCam", "1", 2)

Cap.liveFeed(0,0)
Cap.stopCapturing()
cv2.destroyAllWindows()
