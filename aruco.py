from picamera2 import Picamera2, Preview
from time import sleep
import cv2
import cv2.aruco


camera = Picamera2()

camera.start_preview()

camera.start()

arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_100)
arucoParam = cv2.aruco.DetectorParameters()
arucoDetect = cv2.aruco.ArucoDetector(arucoDict, arucoParam)

robotID = 9
points = [[0, 0]]


while True:
    try:
        img = camera.capture_array()
        markerCorners, markerIDs, _ = arucoDetect.detectMarkers(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
        if markerIDs is not None:
            for i, markerID in enumerate(markerIDs):
                if markerID[0] == robotID:
                    corners = markerCorners[i][0]
                    corners_x = int((corners[0][0] + corners[1][0] + corners[2][0] + corners[3][0]) / 4)
                    corners_y = int((corners[0][1] + corners[1][1] + corners[2][1] + corners[3][1]) / 4)
                    print(f"Marker ID: {markerID[0]}, Center: ({corners_x}, {corners_y})")
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except:points.clear()

camera.stop()
camera.stop_preview()
cv2.destroyAllWindows()
