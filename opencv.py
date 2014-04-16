import cv2
import numpy as np

sypnosis = '''
USAGE: opencv.py [video_source]
video_source - can be a number to indicate a camera device
               or a movie file name
	       default is 0
press Esc to exit
'''
def resizeFrame(img, downscale = 2):
  minisize = (img.shape[1]/downscale,img.shape[0]/downscale)
  return cv2.resize(img, minisize)


def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)

def drawObjectFrame(img, half_width, half_height):
  h, w = img.shape[:2]
  hh , hw = h/2, w/2
  cv2.rectangle(img, (hw - half_width, hh - half_height),(hw + half_width, hh + half_height),(0,0,255),3)

def draw_flow(img, flow, step = 16):
  h, w = img.shape[:2]
  y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1)
  fx, fy = flow[y,x].T
  lines = np.vstack([x,y,x+fx*10,y+fy*10]).T.reshape(-1,2,2)
  lines = np.int32(lines + 0.5)
  vis = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
  cv2.polylines(vis, lines, 0, (0,0,225)) 
  for (x1,y1),(x2,y2) in lines:
    cv2.circle(vis, (x1,y1),1,(0,0,225),-1)
  return vis

def draw_hsv(flow):
  h, w = flow.shape[:2]
  fx, fy = flow[:,:,0], flow[:,:,1]
  ang = np.arctan2(fy, fx) + np.pi
  v = np.sqrt(fx*fx+fy*fy)
  hsv = np.zeros((h, w, 3), np.uint8)
  hsv[...,0] = ang*(180/np.pi/2)
  hsv[...,1] = 255
  hsv[...,2] = np.minimum(v*4, 255)
  bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
  return bgr

def warp_flow(img, flow):
  h, w = flow.shape[:2]
  flow = -flow
  flow[:,:,0] += np.arange(w)
  flow[:,:,1] += np.arange(h)[:,np.newaxis]
  res = cv2.remap(img, flow, None, cv2.INTER_LINEAR)
  return res


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
  img = resizeFrame(img)
  h, w = img.shape[:2]
  print "Frame size: ", h , "x" , w

  prevgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  show_hsv = False
  show_glitch = False
  cur_glitch = img.copy()
  
  while s:
    #drawObjectFrame(img,100,100)
    s, img = cam.read()
    img = resizeFrame(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(prevgray,gray,0.5,3,15,3,5,1.2,0)
    prevgray = gray
    
    cv2.imshow('flow', draw_flow(gray, flow))
    if show_hsv:
      cv2.imshow('flow HSV', draw_hsv(flow))
    if show_glitch:
      cur_glitch = warp_flow(cur_glitch, flow)
      cv2.imshow('glitch', cur_glitch)

    ch = 0xFF & cv2.waitKey(5)
    if ch == 27:
      break
    if ch == ord('1'):
      show_hsv = not show_hsv
      print 'HSV flow visualization is', ['off', 'on'][show_hsv]
    if ch == ord('2'):
      show_glitch = not show_glitch
      if show_glitch:
        cur_glitch = img.copy()
      print 'glitch is', ['off', 'on'][show_glitch]
    #end while


  print "Goodbye"
  cv2.destroyAllWindows()
