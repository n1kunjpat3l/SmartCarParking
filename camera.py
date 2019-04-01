import datetime
from picamera import PiCamera
from time import *
camera = PiCamera()
#now= datetime.datetime.now()
#imageUrl='/home/pi/carparking/Images/Image_'+str(now)+'.jpg'
imageUrl='/home/pi/carparking/images/image.jpg'


def cameraTrigger():
        
	camera.start_preview()
	sleep(1)
	camera.capture(imageUrl)
	camera.stop_preview()
	print("  Image captured...")


