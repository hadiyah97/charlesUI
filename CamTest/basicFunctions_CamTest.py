# USAGE
# python3 basicFunctions_CamTest.py

import cv2
from drivers.Camera import Camera

# Setting up the camera
# cam_val:   can be a str or an int (0/1/csi/CSI)
# cam_name:  must be a str
# dispRatio: set display window resolution
#            dispW = screenW/dispRatio)
#            dispH = screenH/dispRatio)

# Cap = Camera(cam_name, cam_val, dispRatio)

#Cap = Camera("PiCam", "csi", 2)
#Cap = Camera("PiCam", "CSI", 2)
Cap = Camera("WebCam", "0", 2)
#Cap = Camera("WebCam", "1", 2)

print("[INFO]\tPress q to quit OR p to take a screenshot")
while True:
    key = cv2.waitKey(1) & 0xFF

    Cap.captureFrame()
    Cap.displayFrame(0, 0)

    if key == ord('q'):
        break
    elif key == ord('p'):
        Cap.saveFrame()

Cap.stopCapturing()
cv2.destroyAllWindows()
