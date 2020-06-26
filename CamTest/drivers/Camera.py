import cv2
import enum
import tkinter
import imutils
import pytesseract
import numpy as np
from datetime import datetime
from imutils.object_detection import non_max_suppression

class Camera:
    # cam_val:   can be a str or an int (0/1/csi/CSI)
    # cam_name:  must be a str
    # dispRatio: set display window resolution
    #            dispW = screenW/dispRatio)
    #            dispH = screenH/dispRatio)
    def __init__(self, cam_name, cam_val, dispRatio=1):
        print("[INFO]\tInitializing "+cam_name)
        self.flip = 0
        self.rec = False
        self.cam_name = cam_name
        self.dispRatio = dispRatio
        self.setDispRes()
        self.validateCamVal(cam_val)
        self.startCapturing()
        self.setResolution()
        print("[INFO]\tStreaming "+self.cam_name)

    # Validate camera input value,
    # and store validated value to Camera instance
    def validateCamVal(self, cam_val): # __init__
        if type(cam_val) == int:
            if (cam_val == 1) or (cam_val == 0):
                self.cam_val = cam_val
            else:
                print("[ERROR]\tInvalid camera input value\n[ERROR]\tProgram terminated")
                cv2.destroyAllWindows()
                quit()
        elif type(cam_val) == str:
            if (cam_val == "0") or (cam_val == "1"):
                self.cam_val = int(cam_val)
            elif (cam_val == "csi") or (cam_val == "CSI"):
                self.cam_val = self.getCSIvalue()
            else:
                print("[ERROR]\tInvalid camera input value\n[ERROR]\tProgram terminated")
                cv2.destroyAllWindows()
                quit()
        else:
            print("[ERROR\tInvalid camera input value\n[ERROR]\tProgram terminated")
            cv2.destroyAllWindows()
            quit()

    # Start capturing frame
    def startCapturing(self): # __init__
        self.Cap = cv2.VideoCapture(self.cam_val)
        if self.Cap is None:
            print("[ERROR]\tCould not initialize camera.\n[ERROR]\tProgram terminated")
            cv2.destroyAllWindows()
            quit()
        if not self.Cap.isOpened():
            self.Cap.open(self.cam_val, cv2.CAP_GSTREAMER)

        ret, self.frame = self.Cap.read() # ret=True/False
        if not ret:
            print("[ERROR]\tCould not read image from camera. Check input camera value\n[ERROR]\tProgram terminated")
            quit()
        else:
            print("[INFO]\t"+self.cam_name+" connected")

        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.Writer = None
        self.rec = False
        self.recording_frame = np.zeros((self.frame.shape[:2]), dtype="uint8")

    # Set Display resolution
    def setDispRes(self): # __init__
        # get screen resolution
        screen = tkinter.Tk()
        screenW = screen.winfo_screenwidth()
        screenH = screen.winfo_screenheight()
        # set display resolution
        self.dispW = int(screenW/self.dispRatio)
        self.dispH = int(screenH/self.dispRatio)

    # Set Captured/Recording resolution
    def setResolution(self): # __init__
        # get screen resolution
        screen = tkinter.Tk()
        screenW = screen.winfo_screenwidth()
        screenH = screen.winfo_screenheight()

        # get camera resolution
        capture_width  = self.Cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
        capture_height = self.Cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float

        #print("capture_width " + str(capture_width))
        #print("capture_height " + str(capture_height))        

        self.capture_width = int(capture_width)
        self.capture_height = int(capture_height)
        # set recording resolution
        self.recW = self.capture_width
        self.recH = self.capture_height

        print("[INFO]\tCamera Resolution: " + str(self.capture_width) + "x" + str(self.capture_height))
        print("[INFO]\tScreen Resolution: " + str(screenW) + "x" + str(screenH))
        print("[INFO]\tDisplay Resolution: " + str(self.dispW) + "x" + str(self.dispH))
        print("[INFO]\tRecording Resolution: " + str(self.recW) + "x" + str(self.recH))

    # Return string value for CSI camera
    def getCSIvalue(self): # __init__
        #return 'nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(self.flip)+' ! video/x-raw, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
        return 'nvarguscamerasrc !  video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=30/1 ! nvvidconv flip-method='+str(self.flip)+' ! video/x-raw, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
        #return 'nvarguscamerasrc !  video/x-raw(memory:NVMM), width=640, height=360, format=NV12, framerate=30/1 ! nvvidconv flip-method='+str(self.flip)+' ! video/x-raw, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
        #return 'nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(self.flip)+' ! video/x-raw, width='+str(self.dispW)+', height='+str(self.dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

    def captureFrame(self):
        ret, self.frame = self.Cap.read() # ret=True/False
        if not ret:
            print("[ERROR]\tCould not read image from camera.\n[ERROR]\tProgram terminated")
            quit()

    # Display captured frame - startX/startY: window's position value
    def displayFrame(self, startX=0, startY=0):
        cv2.namedWindow(self.cam_name, cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_NORMAL | cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.cam_name, self.dispW, self.dispH)
        cv2.imshow(self.cam_name, self.frame)
        cv2.moveWindow(self.cam_name, startX, startY)

    # Display any frame - startX/startY: window's position value
    #                   - frame_name:    Window's name (string)
    def displayFrameAny(self, frame_name, frame):
        cv2.namedWindow(frame_name, cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_NORMAL | cv2.WINDOW_NORMAL)
        cv2.resizeWindow(frame_name, self.dispW, self.dispH)
        cv2.imshow(frame_name, frame)

    # Save captured frame
    def saveFrame(self):
        timestamp = datetime.now()
        currentdate = timestamp.strftime("%Y-%m-%d")
        currenttime = timestamp.strftime("%H-%M-%S")
        cv2.imwrite("captures/img/"+self.cam_name+"_"+currentdate+"_"+currenttime+".jpg", self.frame)
        print("[INFO]\t"+self.cam_name+"'s image taken at "+currentdate+" "+currenttime)

    # Save any frame - frame_name: Window's name (string)
    #                - frame:      Input frame
    def saveFrameAny(self, frame_name, frame):
        timestamp = datetime.now()
        currentdate = timestamp.strftime("%Y-%m-%d")
        currenttime = timestamp.strftime("%H-%M-%S")
        cv2.imwrite("captures/img/"+frame_name+"_"+currentdate+"_"+currenttime+".jpg", frame)
        print("[INFO]\t"+self.cam_name+"'s image taken at "+currentdate+" "+currenttime)

    # Start recording
    def startRecording(self):
        if self.rec == True:
            print("[WARN]\t" + self.cam_name + " is currently recording")
        else:
            self.rec = True
            timestamp = datetime.now()
            currentdate = timestamp.strftime("%Y-%m-%d")
            currenttime = timestamp.strftime("%H-%M-%S")
            if self.Writer is None:
                (h, w) = self.frame.shape[:2]
                fps = 5
                self.Writer = cv2.VideoWriter("captures/vids/"+self.cam_name+"_"+currentdate+"_"+currenttime+".avi", self.fourcc, fps, (self.recW, self.recH), True)
            print("[INFO]\t"+self.cam_name+" recording started at "+currentdate+" "+currenttime)
            print("[INFO]\tRecording "+self.cam_name)

    # Stop recording
    def stopRecording(self):
        if self.rec == False:
            print("[WARN]\tNothing is currently recording")
        else:
            self.rec = False
            timestamp = datetime.now()
            currentdate = timestamp.strftime("%Y-%m-%d")
            currenttime = timestamp.strftime("%H-%M-%S")
            print("[INFO]\t"+self.cam_name+" recording stopped at "+currentdate+" "+currenttime)

    # Record self's frame
    def recordFrame(self):
        self.recording_frame = self.frame.copy()
        self.Writer.write(self.recording_frame)

    # Record any frame
    def recordFrameAny(self, frame):
        self.Writer.write(frame)

    # Stop capturing frame
    def stopCapturing(self):
        if self.Cap.isOpened():
            self.Cap.release()
        if self.Writer is not None:
            self.Writer.release()
        print("[INFO]\t" + self.cam_name + " disconnected")



    # ================= EXTRA FUNCTIONS =================
    # Output: live feed camera
    # Input: startX/startY - display position
    def liveFeed(self, startX, startY):
        print("[OPTS]\tAvailable options:")
        print("\tq - quit")
        print("\tp - take a screenshot")
        print("\tr - start recording")
        print("\ts - stop recording")
        while True:
            key = cv2.waitKey(1) & 0xFF
            self.captureFrame()
            self.displayFrame(startX, startY)
            if self.rec:
                self.recordFrame()
            if key == ord('q'):
                if self.rec:
                    self.stopRecording()
                break
            elif key == ord('p'):
                self.saveFrame()
            elif key == ord('r'):
                self.startRecording()
            elif key == ord('s'):
                self.stopRecording()

    # Finding the target (room number sign)
    # Conditions:
    def findTarget(self):
        (W, H) = (None, None)
        (newW, newH) = (320, 320)
        layerNames = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]
        net = cv2.dnn.readNet("drivers/east_detector.pb")

        print("[OPTS]\tAvailable options:")
        print("\tq - quit")
        print("\tp - take a screenshot")
        print("\tr - start recording")
        print("\ts - stop recording")
        while True:
            key = cv2.waitKey(1) & 0xFF

            self.captureFrame()

            temp_frame = self.frame.copy()
            disp_frame = self.frame.copy()

            (H, W) = temp_frame.shape[:2]
            rW = W / float(newW)
            rH = H / float(newH)

            temp_frame = cv2.resize(temp_frame, (newW, newH))

            blob = cv2.dnn.blobFromImage(temp_frame, 1.0, (newW, newH), (123.68, 116.78, 103.94), swapRB=True, crop=False)
            net.setInput(blob)
            (scores, geometry) = net.forward(layerNames)

            (rects, confidences) = self.decode_predictions(scores, geometry, 0.5)
            boxes = non_max_suppression(np.array(rects), probs=confidences)


            """
            for (startX, startY, endX, endY) in boxes:
                startX = int(startX * rW)
                startY = int(startY * rH)
                endX = int(endX * rW)
                endY = int(endY * rH)
                cv2.rectangle(disp_frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            """

            results = []
            for (startX, startY, endX, endY) in boxes:
                startX = int(startX * rW)
                startY = int(startY * rH)
                endX = int(endX * rW)
                endY = int(endY * rH)
        
                dX = int((endX - startX) * 0.0)
                dY = int((endY - startY) * 0.0)

                startX = max(0, startX - dX)
                startY = max(0, startY - dY)
                endX = min(W, endX + (dX * 2))
                endY = min(H, endY + (dY * 2))

                roi = disp_frame[startY:endY, startX:endX]
                config = ("-l eng --oem 1 --psm 7")
                text = pytesseract.image_to_string(roi, config=config)
                results.append(((startX, startY, endX, endY), text))

            results = sorted(results, key=lambda r:r[0][1])
            for ((startX, startY, endX, endY), text) in results:
                text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
                if text.isdigit():
                    cv2.rectangle(disp_frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                    cv2.putText(disp_frame, "TARGET LOCATED", (startX, startY - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0),2)
                    cv2.putText(disp_frame, "Maybe: "+text, (startX, endY + 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

            self.displayFrameAny("Detection Frame", disp_frame)
            if self.rec:
                self.recordFrameAny(disp_frame)
            if key == ord('q'):
                if self.rec:
                    self.stopRecording()
                break
            elif key == ord('p'):
                self.saveFrame()
            elif key == ord('r'):
                self.startRecording()
            elif key == ord('s'):
                self.stopRecording()

    def decode_predictions(self, scores, geometry, min_confidence):
        (numRows, numCols) = scores.shape[2:4]
        rects = []
        confidences = []
        for y in range(0, numRows):
            scoresData = scores[0, 0, y]
            xData0 = geometry[0, 0, y]
            xData1 = geometry[0, 1, y]
            xData2 = geometry[0, 2, y]
            xData3 = geometry[0, 3, y]
            anglesData = geometry[0, 4, y]
            for x in range(0, numCols):
                if scoresData[x] < min_confidence:
                    continue
                (offsetX, offsetY) = (x * 4.0, y * 4.0)

                angle = anglesData[x]
                cos = np.cos(angle)
                sin = np.sin(angle)

                h = xData0[x] + xData2[x]
                w = xData1[x] + xData3[x]

                endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
                endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
                startX = int(endX - w)
                startY = int(endY - h)

                rects.append((startX, startY, endX, endY))
                confidences.append(scoresData[x])
        return (rects, confidences)















            
