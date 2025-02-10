from neronka_proverka import neronka
from picamera2 import Picamera2, Preview
from time import sleep
import cv2

camera = Picamera2()

camera.start_preview()

camera.start()

while True:
    img = camera.capture_array()
    image_path = neronka(img)

    cv2.imshow("Image", image_path.squeeze().numpy())
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.stop()
camera.stop_preview()
cv2.destroyAllWindows()
