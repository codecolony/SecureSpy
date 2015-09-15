# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
import subprocess as sp
import os.path

#Initialize variables
#FFMPEG_BIN = "ffmpeg" # on Linux ans Mac OS
FFMPEG_BIN = "ffmpeg\\bin\\ffmpeg.exe" # on Windows

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
ap.add_argument("-c", "--enable-compression", type=int, default=1, help="enable compression or disable it")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	camera = cv2.VideoCapture(1)
	time.sleep(0.25)

# otherwise, we are reading from a video file
else:
	camera = cv2.VideoCapture(args["video"])

# initialize the first frame in the video stream
firstFrame = None

#set first frame
while True:
	(grabbed, frame) = camera.read()

	if not grabbed:
		break #change to exit program

	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	#add help text (press a to accept)
	text = "help"
	cv2.putText(frame, "Press 'a' key to accept".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

	cv2.imshow("Select Background", frame)
	#time.sleep(1)

	key = cv2.waitKey(1) & 0xFF

	# if the `a` key is pressed, accept the intitial frame and break loop
	if key == ord("a"):
		firstFrame = gray
		cv2.destroyWindow("Select Background")
		break

#store video from the frames captured.
#fps = camera.get(CV_CAP_PROP_FPS)
height, width, channels = frame.shape
#fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
vw = cv2.VideoWriter("spy.avi", -1, 20, (width,height), 1)  #[, isColor]])

if not vw:
    print "!!! Failed VideoWriter: invalid parameters"
    sys.exit(1)

# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	(grabbed, frame) = camera.read()
	text = "Not Recording"

	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if not grabbed:
		break

	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
		

	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 100, 255, cv2.THRESH_BINARY)[1]

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < args["min_area"] * 5:
			continue

		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		#####(x, y, w, h) = cv2.boundingRect(c)
		#####cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Recording"

		#store the frame
		#vw.write(frame)

	# draw the text and timestamp on the frame
	cv2.putText(frame, "Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

	#store the frame
	if text == "Recording":
		#store the frame
		if args["enable_compression"] == 0:
			vw.write(frame)
		else:
			#ffmpeg -i ./outimg/depth%d.png -vcodec png depth.mov
			#store frame as image on disk.
			#sp.call( ["ffmpeg", "-i", "frame.png", "-vcodec png depth.mov"])
			cv2.imwrite("frame.bmp", frame)
	
			time.sleep(0.15)
	
			if os.path.isfile("depth.mov") is False:
	
				#use frame to create video
				sp.call( [FFMPEG_BIN, "-i", "frame.bmp", "-vcodec", "png", "depth.mov"])
				#print "depth.mov created"
	
			else:
				sp.call( [FFMPEG_BIN, "-i", "frame.bmp", "-vcodec", "png", "depth1.mov"])
				#print "depth1.mov created"
				#concat two videos
				#cat INPUT1.avi INPUT2.avi > MERGEDFILE.avi
				#ffmpeg -i concat:"input1|input2" -codec copy output
				#ffmpeg -f concat -i mylist.txt -c copy output
				#sp.call( ["ffmpeg", "-i", "\"concat:depth1.mov|depth.mov\"", "-codec", "copy", "output"])
				sp.call( [FFMPEG_BIN, "-f", "concat","-i", "mylist.txt","-c", "copy", "depth.mov" , "-y"])
				sp.call(["del", "depth1.mov"])
	
			#delete temporary image created from frame
			sp.call(["del", "frame.bmp"])

	# show the frame and record if the user presses a key
	cv2.imshow("Security Feed", frame)
	#cv2.imshow("Thresh", thresh)
	#cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break
	

# cleanup the camera and close any open windows
vw.release()
camera.release()
cv2.destroyAllWindows()
# =======
# # import the necessary packages
# import argparse
# import datetime
# import imutils
# import time
# import cv2

# # construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video", help="path to the video file")
# ap.add_argument("-a", "--min-area", type=int, default=640, help="minimum area size")
# args = vars(ap.parse_args())

# # if the video argument is None, then we are reading from webcam
# if args.get("video", None) is None:
# 	camera = cv2.VideoCapture(0)
# 	time.sleep(0.25)

# # otherwise, we are reading from a video file
# else:
# 	camera = cv2.VideoCapture(args["video"])

# # initialize the first frame in the video stream
# firstFrame = None

# #set first frame
# while True:
# 	(grabbed, frame) = camera.read()

# 	if not grabbed:
# 		break #change to exit program

# 	# resize the frame, convert it to grayscale, and blur it
# 	frame = imutils.resize(frame, width=500)
# 	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# 	gray = cv2.GaussianBlur(gray, (21, 21), 0)

# 	#add help text (press a to accept)
# 	text = "help"
# 	cv2.putText(frame, "Press 'a' key to accept".format(text), (10, 20),
# 		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# 	cv2.imshow("Select Background", frame)
# 	#time.sleep(1)

# 	key = cv2.waitKey(1) & 0xFF

# 	# if the `a` key is pressed, accept the intitial frame and break loop
# 	if key == ord("a"):
# 		firstFrame = gray
# 		cv2.destroyWindow("Select Background")
# 		break

# #store video from the frames captured.
# #fps = camera.get(CV_CAP_PROP_FPS)
# height, width, channels = frame.shape
# #fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
# fourcc = cv2.VideoWriter_fourcc(*'MPEG')
# vw = cv2.VideoWriter("spy.avi", -1, 20, (width,height), 1)  #[, isColor]])

# if not vw:
#     print "!!! Failed VideoWriter: invalid parameters"
#     sys.exit(1)

# # loop over the frames of the video
# while True:
# 	# grab the current frame and initialize the occupied/unoccupied
# 	# text
# 	(grabbed, frame) = camera.read()
# 	text = "Not Recording"

# 	# if the frame could not be grabbed, then we have reached the end
# 	# of the video
# 	if not grabbed:
# 		break

# 	# resize the frame, convert it to grayscale, and blur it
# 	frame = imutils.resize(frame, width=500)
# 	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# 	gray = cv2.GaussianBlur(gray, (21, 21), 0)
		

# 	# compute the absolute difference between the current frame and
# 	# first frame
# 	frameDelta = cv2.absdiff(firstFrame, gray)
# 	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

# 	# dilate the thresholded image to fill in holes, then find contours
# 	# on thresholded image
# 	thresh = cv2.dilate(thresh, None, iterations=2)
# 	(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
# 		cv2.CHAIN_APPROX_SIMPLE)

# 	# loop over the contours
# 	for c in cnts:
# 		# if the contour is too small, ignore it
# 		if cv2.contourArea(c) < args["min_area"]:
# 			text = "Not Recording"
# 			continue

# 		# compute the bounding box for the contour, draw it on the frame,
# 		# and update the text
# 		#####(x, y, w, h) = cv2.boundingRect(c)
# 		#####cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
# 		text = "Recording"

# 		#store the frame
# 		#vw.write(frame)

# 	# draw the text and timestamp on the frame
# 	cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
# 		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
# 	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
# 		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
	
# 	if text == "Recording":
# 		#store the frame
# 		vw.write(frame)

# 	# show the frame and record if the user presses a key
# 	cv2.imshow("Security Feed", frame)
# 	#####cv2.imshow("Thresh", thresh)
# 	#####cv2.imshow("Frame Delta", frameDelta)
# 	key = cv2.waitKey(1) & 0xFF

# 	# if the `q` key is pressed, break from the loop
# 	if key == ord("q"):
# 		break
	

# # cleanup the camera and close any open windows
# vw.release()
# camera.release()
# cv2.destroyAllWindows()

# >>>>>>> b69abf603727d414e126c4c442086aa524b04b81
