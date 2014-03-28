import cv2
import numpy as np
import Image #require Python Imaging Library (PIL)

patternSize = (6,9)#interior number of corners, that is, points, where the black squares touch each other

cv2.namedWindow("w1", cv2.CV_WINDOW_AUTOSIZE)
camera_index = 0
capture = cv2.VideoCapture(camera_index)
c = cv2.waitKey(5000)#wait for the camera to be initialized


def repeat():
	global capture #declare as globals since we are assigning to them now
	global camera_index
	global frame
	ret, frame = capture.read()
	
	if ret:  		
		cv2.imshow("w1", frame)
		#convert to grayImage 
		#frameGray = cv2.CreateImage(cv2.GetSize(frame), cv2.IPL_DEPTH_8U, 1)
		#cv2.CvtColor(frame,frameGray,cv.CV_BGR2GRAY)
		
		found, corners = cv2.findChessboardCorners(frame, patternSize, cv2.cv.CV_CALIB_CB_ADAPTIVE_THRESH + cv2.cv.CV_CALIB_CB_NORMALIZE_IMAGE)
		if found:#if we found all the internal corners
			#Refines the corner locations
			cv2.FindCornerSubPix(frameGray,corners[1],(11,11),(-1,-1),(cv.CV_TERMCRIT_ITER | cv.CV_TERMCRIT_EPS, 10, 0.01))
			patternWasFound = corners[0]
			cv2.DrawChessboardCorners(frame, patternSize, corners[1], patternWasFound)
			cv2.ShowImage("w1",frame)
	c = cv2.waitKey(10)
while True:
	repeat()