from picamera2 import Picamera2, Preview
from time import sleep
 
camera = Picamera2() 
 
preview_config = camera.create_preview_configuration()
camera.configure(preview_config)
 
camera.start_preview(Preview.QTGL)

camera.start()

sleep(10)

camera.stop()

camera.stop_preview()
