# import the necessary packagesr
import argparser
import datetimer
import imutilsr
import timer
import cv2r
import subprocess as spr
import os.pathr
r
#Initialize variablesr
FFMPEG_BIN = "ffmpeg" # on Linux ans Mac OSr
#FFMPEG_BIN = "ffmpeg.exe" # on Windowsr
r
# construct the argument parser and parse the argumentsr
ap = argparse.ArgumentParser()r
ap.add_argument("-v", "--video", help="path to the video file")r
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")r
args = vars(ap.parse_args())r
r
# if the video argument is None, then we are reading from webcamr
if args.get("video", None) is None:r
	camera = cv2.VideoCapture(0)r
	time.sleep(0.25)r
r
# otherwise, we are reading from a video filer
else:r
	camera = cv2.VideoCapture(args["video"])r
r
# initialize the first frame in the video streamr
firstFrame = Noner
r
#set first framer
while True:r
	(grabbed, frame) = camera.read()r
r
	if not grabbed:r
		break #change to exit programr
r
	# resize the frame, convert it to grayscale, and blur itr
	frame = imutils.resize(frame, width=500)r
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)r
	gray = cv2.GaussianBlur(gray, (21, 21), 0)r
r
	#add help text (press a to accept)r
	text = "help"r
	cv2.putText(frame, "Press 'a' key to accept".format(text), (10, 20),r
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)r
r
	cv2.imshow("Select Background", frame)r
	#time.sleep(1)r
r
	key = cv2.waitKey(1) & 0xFFr
r
	# if the `a` key is pressed, accept the intitial frame and break loopr
	if key == ord("a"):r
		firstFrame = grayr
		cv2.destroyWindow("Select Background")r
		breakr
r
#store video from the frames captured.r
#fps = camera.get(CV_CAP_PROP_FPS)r
height, width, channels = frame.shaper
fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')r
#fourcc = cv2.VideoWriter_fourcc(*'XVID')r
vw = cv2.VideoWriter("spy.avi", fourcc, 20, (width,height), 0)  #[, isColor]])r
r
if not vw:r
    print "!!! Failed VideoWriter: invalid parameters"r
    sys.exit(1)r
r
# loop over the frames of the videor
while True:r
	# grab the current frame and initialize the occupied/unoccupiedr
	# textr
	(grabbed, frame) = camera.read()r
	text = "Not Recording"r
r
	# if the frame could not be grabbed, then we have reached the endr
	# of the videor
	if not grabbed:r
		breakr
r
	# resize the frame, convert it to grayscale, and blur itr
	frame = imutils.resize(frame, width=500)r
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)r
	gray = cv2.GaussianBlur(gray, (21, 21), 0)r
		r
r
	# compute the absolute difference between the current frame andr
	# first framer
	frameDelta = cv2.absdiff(firstFrame, gray)r
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]r
r
	# dilate the thresholded image to fill in holes, then find contoursr
	# on thresholded imager
	thresh = cv2.dilate(thresh, None, iterations=2)r
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,r
		cv2.CHAIN_APPROX_SIMPLE)r
r
	# loop over the contoursr
	for c in cnts:r
		# if the contour is too small, ignore itr
		if cv2.contourArea(c) < args["min_area"]:r
			continuer
r
		# compute the bounding box for the contour, draw it on the frame,r
		# and update the textr
		#####(x, y, w, h) = cv2.boundingRect(c)r
		#####cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)r
		text = "Recording"r
r
		#store the framer
		#vw.write(frame)r
r
	# draw the text and timestamp on the framer
	cv2.putText(frame, "Status: {}".format(text), (10, 20),r
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)r
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),r
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)r
r
	#store the framer
	if text == "Recording":r
		#vw.write(frame)r
		#ffmpeg -i ./outimg/depth%d.png -vcodec png depth.movr
		#store frame as image on disk.r
		#sp.call( ["ffmpeg", "-i", "frame.png", "-vcodec png depth.mov"])r
		cv2.imwrite("frame.bmp", frame)r
r
		time.sleep(0.15)r
r
		if os.path.isfile("depth.mov") is False:r
r
			#use frame to create videor
			sp.call( ["ffmpeg", "-i", "frame.bmp", "-vcodec", "png", "depth.mov"])r
			#print "depth.mov created"r
r
		else:r
			sp.call( ["ffmpeg", "-i", "frame.bmp", "-vcodec", "png", "depth1.mov"])r
			#print "depth1.mov created"r
			#concat two videosr
			#cat INPUT1.avi INPUT2.avi > MERGEDFILE.avir
			#ffmpeg -i concat:"input1|input2" -codec copy outputr
			#ffmpeg -f concat -i mylist.txt -c copy outputr
			#sp.call( ["ffmpeg", "-i", "\"concat:depth1.mov|depth.mov\"", "-codec", "copy", "output"])r
			sp.call( ["ffmpeg", "-f", "concat","-i", "mylist.txt","-c", "copy", "depth.mov" , "-y"])r
			sp.call(["rm", "depth1.mov"])r
r
		#delete temporary image created from framer
		sp.call(["rm", "frame.bmp"])r
r
	# show the frame and record if the user presses a keyr
	#cv2.imshow("Security Feed", frame)r
	#cv2.imshow("Thresh", thresh)r
	cv2.imshow("Frame Delta", frameDelta)r
	key = cv2.waitKey(1) & 0xFFr
r
	# if the `q` key is pressed, break from the lopr
	if key == ord("q"):r
		breakr
	r
r
# cleanup the camera and close any open windowsr
vw.release()r
camera.release()r
cv2.destroyAllWindows()r
