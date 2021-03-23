# import the necessary packages
from collections import deque
import numpy as np
import imutils
import cv2
import time
import string 
import serial
from gpiozero import Servo
from time import sleep


#serial bud rate
ser = serial.Serial('/dev/ttyACM0',9600)
ser.flush()

'''
for i in range(0,10):

	ser.write(chr(255))
	sleep(0.1)
'''

ser.flush()
angle = 90
# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (120, 240, 240)

#get camera
camera = cv2.VideoCapture(0)
camera.set(4,480)
camera.set(4,360)

start_time = time.time

# keep looping

while True:

	# grab the current frame
	(grabbed, frame) = camera.read()
	

	# resize the frame, blur it, and convert it to the HSV
	# color space
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		

		# only proceed if the radius meets a minimum size
		if (radius < 300) & (radius > 10 ) : 
			# draw the circle on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)		


			# otherwise, compute the thickness of the line and
			# draw the connecting lines
			thickness = 10
			cv2.line(frame, (310,240), (int(x),int(y)), (0, 0, 255), thickness)

           		 # display coordinate data
			font = cv2.FONT_HERSHEY_SIMPLEX
			
			angle = int(np.arctan(-(x-310)/302.22)*180/3.14+90)
			cv2.putText(frame,str(int(x)) + ',' + str(int(y)) ,(int(x), int(y)), font, 1,(255,255,255),2)
			


	# show the frame to our screen
	cv2.imshow("Frame", frame)
	print(angle)
	ser.write(chr(angle))
	line = ser.readline().decode('utf-8').rstrip()
	print('Arduino'+line)

	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		
		break


# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
