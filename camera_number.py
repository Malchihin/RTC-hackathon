from neronka import load_model, predict_digit, image
from picamera2 import Picamera2, Preview
from time import sleep
import cv2
import

def neronka_number():
    camera = Picamera2()
    camera.start_preview()
    camera.start()

    model = load_model()

    while True:
        img = camera.capture_array()
        img = image
        image
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.stop()
    camera.stop_preview()
    cv2.destroyAllWindows()     

neronka_number()