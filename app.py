#!/usr/bin/env python
from flask import Flask, render_template, Response
import cv2
import thread

from collections import deque
import numpy as np
import argparse
import imutils
# import cv2
import time

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template

import random

xframe = None
ws = None

class WSSerial(object):
    def __init__(self):
        self.no_connected = True
        class WSHandler(tornado.websocket.WebSocketHandler):
            def check_origin(self, origin):
                return True

            def open(self):
                global weight
                weight.connection = self
                weight.no_connected = False
                print 'ESP connection opened...'

            def on_message(self, message):
                print 'ESP received:', message

            def on_close(self):
                print 'ESP connection closed...'

        application = tornado.web.Application([
            (r'/', WSHandler)
        ])

        global weight
        weight = self

        def someFunc():
            application.listen(8100)
            tornado.ioloop.IOLoop.instance().start()

        thread.start_new_thread(someFunc, ())

    def write(self, chr):
        print 'write'
        self.connection.write_message(chr)


def ProcessingStream():
    global xframe
    global ws
    print "ProcessingStream start"
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-b", "--buffer", type=int, default=32,
    	help="max buffer size")
    args = vars(ap.parse_args())
    # define the lower and upper boundaries of the "green"
    # ball in the HSV color space
    greenLower = (29, 86, 6)
    greenUpper = (64, 255, 255)

    # initialize the list of tracked points, the frame counter,
    # and the coordinate deltas
    pts = deque(maxlen=args["buffer"])
    counter = 0
    (dX, dY) = (0, 0)
    direction = ""

    # camera = cv2.VideoCapture("http://192.168.100.11:9090/stream/video.mjpeg")
    camera = cv2.VideoCapture("http://195.67.26.73/mjpg/video.mjpg")

    # keep looping
    while True:
        # if random.randrange(10) == 3:
        #     print "AAAAAAAAAAAAAAAA"
        #     ws.write("aa")
    	# grab the current frame
    	(grabbed, frame) = camera.read()

    	# if we are viewing a video and we did not grab a frame,
    	# then we have reached the end of the video
    	if not grabbed:
    		break

    	# resize the frame, blur it, and convert it to the HSV
    	# color space
    	frame = imutils.resize(frame, width=600)
    	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
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
    		if radius > 10:
    			# draw the circle and centroid on the frame,
    			# then update the list of tracked points
    			cv2.circle(frame, (int(x), int(y)), int(radius),
    				(0, 255, 255), 2)
    			cv2.circle(frame, center, 5, (0, 0, 255), -1)
    			pts.appendleft(center)

    	# loop over the set of tracked points
    	for i in np.arange(1, len(pts)):
    		# if either of the tracked points are None, ignore
    		# them
    		if pts[i - 1] is None or pts[i] is None:
    			continue

    		# check to see if enough points have been accumulated in
    		# the buffer
    		try:
    		    puts_minus_10 = pts[-10]
    		except IndexError:
    		    puts_minus_10 = None
    		if counter >= 10 and i == 1 and puts_minus_10 is not None:
    			# compute the difference between the x and y
    			# coordinates and re-initialize the direction
    			# text variables
    			dX = pts[-10][0] - pts[i][0]
    			dY = pts[-10][1] - pts[i][1]
    			(dirX, dirY) = ("", "")

    			# ensure there is significant movement in the
    			# x-direction
    			if np.abs(dX) > 20:
    				dirX = "East" if np.sign(dX) == 1 else "West"

    			# ensure there is significant movement in the
    			# y-direction
    			if np.abs(dY) > 20:
    				dirY = "North" if np.sign(dY) == 1 else "South"

    			# handle when both directions are non-empty
    			if dirX != "" and dirY != "":
    				direction = "{}-{}".format(dirY, dirX)

    			# otherwise, only one direction is non-empty
    			else:
    				direction = dirX if dirX != "" else dirY

    		# otherwise, compute the thickness of the line and
    		# draw the connecting lines
    		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
    		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    	# show the movement deltas and the direction of movement on
    	# the frame
    	cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
    		0.65, (0, 0, 255), 3)
    	cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
    		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
    		0.35, (0, 0, 255), 1)

		# show the frame to our screen and increment the frame counter
        xframe = cv2.imencode('.jpg', frame)[1].tostring()
    	key = cv2.waitKey(1) & 0xFF
    	counter += 1

    	# if the 'q' key is pressed, stop the loop
    	if key == ord("q"):
    		break

    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()


thread.start_new_thread(ProcessingStream, ())
ws = WSSerial()

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    """Video streaming generator function."""
    while True:
        if xframe is None:
            # xframe = None
            break

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + xframe + b'\r\n')
        time.sleep(50.0/1000.0)


@app.route('/stream')
def stream():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=5000)
