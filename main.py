from picamera2 import Picamera2, Preview
from time import sleep
import cv2
import cv2.aruco
 
camera = Picamera2()
 
preview_config = camera.create_preview_configuration()
camera.configure(preview_config)
 
camera.start_preview(Preview.QTGL)

camera.start()
camera_cv2 = camera.capture_array()
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
arucoParam = cv2.aruco.DetectorParameters()
arucoDetect = cv2.aruco.ArucoDetector(arucoDict,arucoParam)

robotID = 9
points = [[0,0]]

while True:
    _,img = camera.read(0)
    try:
        markerCornes, markerID, markerNo = arucoDetect.detectMarkers(cv2.cvtColor(img,cv2.COLOR_BGR2GRAY))
        if markerID is not None:
            if markerID == robotID:
                ID = str(markerID)
                cornes = markerCornes[0][0]
                cornes_x = int((cornes[0][0]+cornes[1][0]+cornes[2][0]+cornes[3][0]) / 4)
                cornes_y = int((cornes[0][1]+cornes[1][1]+cornes[2][1]+cornes[3][1]) / 4)
                #print(cornes_y)
                #print(cornes_x)
                print(str(markerID))
    except:points.clear()

    sleep(10)

    camera.stop()

camera.stop_preview()
