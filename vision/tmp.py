from camera import Camera
from calibrate import *
import cv2

cal = Calibrate()
def do_thing():
  c = Camera()

  while True:
    frame = cal.step(c.get_frame())
    cv2.circle(frame, (320,240), 5, (255,0,0), 1)
    cal.show_frame(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  c.close()
  cv2.destroyAllWindows()
