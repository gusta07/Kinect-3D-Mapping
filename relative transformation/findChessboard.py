import cv2

patternSize = (6,9)#interior number of corners, that is, points, where the black squares touch each other
chessboardImage = cv2.imread("chessboard.png",cv2.cv.CV_LOAD_IMAGE_GRAYSCALE)
found, corners = cv2.findChessboardCorners(chessboardImage, patternSize, cv2.cv.CV_CALIB_CB_ADAPTIVE_THRESH + cv2.cv.CV_CALIB_CB_NORMALIZE_IMAGE)
if found:#if we found all the internal corners
	#Refines the corner locations
	cv2.cornerSubPix(chessboardImage,corners,(11,11),(-1,-1),(cv2.cv.CV_TERMCRIT_ITER | cv2.cv.CV_TERMCRIT_EPS, 10, 0.01))

	
	#show the image during an interval of 2000 milliseconds (or before if a key was pressed)
	cv2.drawChessboardCorners(chessboardImage, patternSize, corners, found)
	cv2.imshow("win2",chessboardImage)
	print corners
	cv2.waitKey(20000)


