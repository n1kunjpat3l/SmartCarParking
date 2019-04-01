# Import required Python libraries
import time
import os
import RPi.GPIO as GPIO
import sys

#import classify_image
# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Define GPIO to use on Pi
GPIO_TRIGGER = 4
GPIO_ECHO    = 17

print ("\nStarting the Sensor to measure distance change..")
vehicleStatus = sys.argv[1]
# Set pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo
# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)

# Allow module to settle
time.sleep(0.5)

# Distance in cm from sensor to the surface
fixedDistance = 32




while (True):
	# Send 10us pulse to trigger
	GPIO.output(GPIO_TRIGGER, True)
	time.sleep(1.0)
	GPIO.output(GPIO_TRIGGER, False)
	start = time.time()

	while GPIO.input(GPIO_ECHO)==0:
		start = time.time()

	while GPIO.input(GPIO_ECHO)==1:
		stop = time.time()

	# Calculate pulse length
	elapsed = stop-start

	# Distance pulse travelled in that time is time
	# multiplied by the speed of sound (cm/s)
	distance = elapsed * 34300

	# That was the distance there and back so halve the value
	distance = distance / 2
	
	distance=round(distance)

	print ("\nDistance : " + str(distance))
	if distance < fixedDistance-2:
		print (" Distance change detected. Triggering camera...")
		from camera import cameraTrigger
		cameraTrigger()
		os.system("python test.py "+vehicleStatus)
		
		
		
	else:
		print ("No distance change: camera not triggered...")
	

# Reset GPIO settings
GPIO.cleanup()