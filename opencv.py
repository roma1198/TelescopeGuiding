import cv2
import numpy as np

sypnosis = '''
USAGE: opencv.py [video_source]
video_source - can be a number to indicate a camera device
               or a movie file name
	       default is 0
press Esc to exit
'''

def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)

def drawObjectFrame(img, half_width, half_height):
  h, w = img.shape[:2]
  hh , hw = h/2, w/2
  cv2.rectangle(img, (hw - half_width, hh - half_height),(hw + half_width, hh + half_height),(255,0,0),3)


if __name__ == '__main__':
  import sys
  print "Using OpenCV version " + cv2.__version__
  print sypnosis
  try: source = sys.argv[1]
  except: source = 0

  cam = cv2.VideoCapture(source)

  if cam is None or not cam.isOpened():
    print 'Error: unable to open video source: ', source
    sys.exit(1)

  s, img = cam.read()
  h, w = img.shape[:2]
  print h , "x" , w

  if s:
    winName = "Movement Indicator"
    cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)
    cv2.imshow( winName, img )

  # Read three images first:
  #t_minus = cv2.cvtColor(cam.read()[1],cv2.COLOR_RGB2GRAY)
  #t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
  #t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

  while s:
    drawObjectFrame(img,100,100)
    cv2.imshow( winName,img )
    s, img = cam.read()
    #img = diffImg(t_minus, t, t_plus)
    #drawObjectFrame(img,10,10)
    #cv2.imshow( winName, img )

    # Read next image
    #t_minus = t
    #t = t_plus
    #t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

    key = cv2.waitKey(10)
    if key == 27:
      cv2.destroyWindow(winName)
      break

  print "Goodbye"
  cv2.destroyAllWindows()
