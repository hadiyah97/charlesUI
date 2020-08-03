# USAGE
# python3 findTarget_4_withPyTess_Recog_CamTest.py

import cv2
from drivers.Camera import Camera

#Cap = Camera("PiCam", "csi", 2)
#Cap = Camera("PiCam", "CSI", 2)
Cap = Camera("WebCam", "0", 1)
#Cap = Camera("WebCam", "1", 2)

result = Cap.findTarget2(267)
print(result)
Cap.stopCapturing()
cv2.destroyAllWindows()









