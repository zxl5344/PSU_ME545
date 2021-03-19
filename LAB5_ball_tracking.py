# import the necessary packages
from collections import deque
import numpy as np
import imutils
import cv2
import time
import matplotlib.pyplot as plt


# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

#get camera
camera = cv2.VideoCapture(0)



#Reading the time in the begining of the video.
start = time.time()

# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()
	
	#Reading The Current Time
	current_time = time.time() - start

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=1000)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		

		# only proceed if the radius meets a minimum size
		if (radius < 300) & (radius > 10 ) : 
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)		


			# otherwise, compute the thickness of the line and
			# draw the connecting lines
			thickness = 10
			cv2.line(frame, (500,400), (int(x),int(y)), (0, 0, 255), thickness)

           		 # display coordinate data
			font = cv2.FONT_HERSHEY_SIMPLEX
			cv2.putText(frame,str(int(x)) + ',' + str(int(y)) ,(int(x), int(y)), font, 1,(255,255,255),2)


	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		
		break


# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
