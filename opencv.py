import cv2

def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)

img = cv2.imread("/home/teo/musette.jpg")
grey = cv2.imread("/home/teo/musette.jpg",0)

##Run Threshold on image to make it black and white
ret, thresh = cv2.threshold(grey,100,200,cv2.THRESH_BINARY)

##Use houghcircles to determine centre of circle
circles = cv2.HoughCircles(thresh,cv2.cv.CV_HOUGH_GRADIENT,1,75,param1=50,param2=13,minRadius=0,maxRadius=175)
for i in circles[0,:]:
    #draw the outer circle
    cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
    #draw the centre of the circle
    cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow("matza", img)
cv2.waitKey(0)

cv2.imshow("thresh", thresh)
cv2.waitKey(0)


cam = cv2.VideoCapture(0)
s, img = cam.read()

winName = "Movement Indicator"
cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)

# Read three images first:
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

while s:
  cv2.imshow( winName,img )
  s, img = cam.read()

  #cv2.imshow( winName, diffImg(t_minus, t, t_plus) )

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
