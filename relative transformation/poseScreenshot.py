import numpy as np
import cv2


# Loading from xml files and converting into numpy array

intrinsic = np.asarray(cv2.cv.Load("Intrinsics-Kinect.xml"),np.float64)
distortion = np.asarray(cv2.cv.Load("Distortion-Kinect.xml"),np.float64)

#intrinsic = np.asarray(cv2.cv.Load("Intrinsics.xml"),np.float64)
#distortion = np.asarray(cv2.cv.Load("Distortion.xml"),np.float64)


objectPoint1 = (0,0,0)
objectPoint2 = (189,0,0)
objectPoint3 = (0,119,0)
objectPoint4 = (189,119,0)

#creating nympy array 
#objectPoints = np.array([objectPoint1,objectPoint2,objectPoint3,objectPoint4],dtype=np.float) 
objectPoint = []
objectPoint.append(objectPoint1)
objectPoint.append(objectPoint2)
objectPoint.append(objectPoint3)
objectPoint.append(objectPoint4)
objectPoints = np.asarray(objectPoint,np.float64)



patternSize = (6,9)#interior number of corners, that is, points, where the black squares touch each other


img = cv2.imread('Images/kinect0.png')

#img = cv2.imread('Images/image0.jpg')
#convert to gray
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
found, corners = cv2.findChessboardCorners(img, patternSize, cv2.cv.CV_CALIB_CB_ADAPTIVE_THRESH + cv2.cv.CV_CALIB_CB_NORMALIZE_IMAGE)
if found:#if we found all the internal corners
	#Refines the corner locations			
	term = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1 )
	cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), term)

	#origin is at the bottom right (to match the kinect axes convention)
	imagePoint1 = int(corners[5][0][0]), int(corners[5][0][1])
	imagePoint2 = int(corners[53][0][0]), int(corners[53][0][1])
	imagePoint3 = int(corners[0][0][0]), int(corners[0][0][1])
	imagePoint4 = int(corners[48][0][0]), int(corners[48][0][1])

	cv2.circle(img,(imagePoint1[0], imagePoint1[1]), 3, (0,0,255))	
	#cv2.circle(img,(imagePoint2[0], imagePoint2[1]), 3, (0,0,255))	
	#cv2.circle(img,(imagePoint3[0], imagePoint3[1]), 3, (0,0,255))	
	#cv2.circle(img,(imagePoint4[0], imagePoint4[1]), 3, (0,0,255))	

			

	imagePoint = []
	imagePoint.append(imagePoint1)
	imagePoint.append(imagePoint2)
	imagePoint.append(imagePoint3)
	imagePoint.append(imagePoint4)

	imagePoints = np.asarray(imagePoint,np.float64)
			


	found,rvec,tvec = cv2.solvePnP(objectPoints, imagePoints, intrinsic, distortion)
	cameraRotation = cv2.Rodrigues(rvec)[0]
	#put in world coordinate
	cameraPosition = -np.matrix(cameraRotation).T * np.matrix(tvec)
	#z axe is inverted, I don't know why
	cameraPosition[2] = cameraPosition[2]*(-1)
	print cameraPosition


cv2.imshow('display image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
	

