import numpy as np
import cv2


def getPose(device):
	if device == "Kinect":
		intrinsic = np.asarray(cv2.cv.Load("../Matrices/Intrinsics-Kinect.xml"),np.float64)
		distortion = np.asarray(cv2.cv.Load("../Matrices/Distortion-Kinect.xml"),np.float64)
		img = cv2.imread('Images/kinect0.png')
	else:
		intrinsic = np.asarray(cv2.cv.Load("../Matrices/Intrinsics-Webcam.xml"),np.float64)
		distortion = np.asarray(cv2.cv.Load("../Matrices/Distortion-Webcam.xml"),np.float64)
		img = cv2.imread('Images/image0.jpg')

	objectPoint1 = (0,0,0)
	objectPoint2 = (0.189,0,0)
	objectPoint3 = (0,0.119,0)
	objectPoint4 = (0.189,0.119,0)

	#creating nympy array 
	objectPoint = []
	objectPoint.append(objectPoint1)
	objectPoint.append(objectPoint2)
	objectPoint.append(objectPoint3)
	objectPoint.append(objectPoint4)
	objectPoints = np.asarray(objectPoint,np.float64)

	patternSize = (6,9)#interior number of corners, that is, points, where the black squares touch each other

	#convert to gray
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
	found, corners = cv2.findChessboardCorners(img, patternSize, cv2.cv.CV_CALIB_CB_ADAPTIVE_THRESH + cv2.cv.CV_CALIB_CB_NORMALIZE_IMAGE)
	if found:#if we found all the internal corners
		#Refines the corner locations			
		term = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1 )
		cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), term)

		#[point number][0 to get rid of square brackets][x][y]
		#origin is at the upper left corner
		imagePoint1 = (corners[48][0][0], corners[48][0][1])
		imagePoint2 = (corners[0][0][0], corners[0][0][1])
		imagePoint3 = (corners[53][0][0], corners[53][0][1])
		imagePoint4 = (corners[5][0][0], corners[5][0][1])


		cv2.circle(img,(imagePoint1[0], imagePoint1[1]), 3, (0,0,255))#world coordinates origin	
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
		
		#append R and T together
		RT = np.append(cameraRotation,tvec, axis=1)
		homogeneous = np.matrix("0,0,0,1")   
        RT = np.append(RT, homogeneous, axis = 0)
        return RT

	cv2.imshow('display image',img)
	cv2.waitKey(0)
	#cv2.destroyAllWindows()



RTKinect = getPose("Kinect")
RTWebcam = getPose("Webcam")

RT_Relative = np.linalg.inv(RTWebcam) * RTKinect


relativeRotation = np.matrix(RT_Relative[0:3,0:3])
relativePosition = np.matrix(RT_Relative[0:3,3:4])




print "relative position"
print relativePosition
print "relative rotation"
print relativeRotation

np.save("../Matrices/translation.npy",relativePosition)
np.save("../Matrices/rotation.npy", relativeRotation)
