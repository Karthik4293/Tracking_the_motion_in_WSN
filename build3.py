from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import io
import picamera as cam

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))



# allow the camera to warmup
time.sleep(0.1)



def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh

def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)

def text ( img, rects):        
    font = cv2.FONT_HERSHEY_SIMPLEX  
    for x, y, w, h in rects:
        print x,y
        if (y > 40 ):
           cv2.putText(img,'East',(1,130), font, 1, (255,0,0), 3)
        elif ( y < 30):
           cv2.putText(img,'West',(1,130), font, 1, (255,0,0), 3)
        else :
           cv2.putText(img,'within ROI',(1,130), font, 1, (255,0,0), 3)
      
         
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
  # grab the raw NumPy array representing the image, then initialize the timestamp
  # and occupied/unoccupied text
  image = frame.array
  
  cv2.imwrite('image.jpg' , image)
  img = cv2.imread('image.jpg', cv2.IMREAD_COLOR)

  hog = cv2.HOGDescriptor()
  hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

  winStride = (8,8)
  padding = (32,32)
  
  found,w=hog.detectMultiScale(img, winStride=winStride, padding=padding, scale=1.05)
  
  draw_detections(img,found)
  text (img, found)
  cv2.imshow('feed',img)


  
  ch = 0xFF & cv2.waitKey(1)
  if ch == 27:
        break

  rawCapture.truncate(0)






    
