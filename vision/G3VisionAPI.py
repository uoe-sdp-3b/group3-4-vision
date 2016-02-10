from tracker import *
from camera import Camera

# Make dependent system use this: 
# sys.path.extend('~/git/group3-4-vision/vision') or similar
# import G3VisionAPI

def get_info():
  try:
    c = Camera()
  except:
    print "WARNING: Camera connection broken"

  frame = c.get_frame()

  colors = {}
  colors['yellow'] = (0,255,255)
  colors['light_blue'] = (255,255,0)
  colors['pink'] = (127,0,255)
  colors['green'] = (0,255,0)
  colors['red'] = (0,0,255)
  colors['blue'] = (255,0,0)

   
  #print "\nPossible team colors: yellow/light_blue\n"
  our_team_color = 'light_blue' # Change if needed!
  num_of_pink = 1 # Change if needed!
  ball_color = 'red' # Change if needed!

  # create our robot as object:
  our_robot = RobotTracker(our_team_color, int(num_of_pink))
  ball = BallTracker(ball_color)

  # convert string colors into GBR
  our_circle_color = colors[our_team_color]
  if our_team_color == 'yellow':
      opponent_circle_color = colors['light_blue']
  else :
      opponent_circle_color = colors['yellow']

  # assign colors and names to the robots
  if int(num_of_pink) == 1:
      our_letters = 'GREEN'
      our_col = colors['green']
      our_robot_color = 'green_robot'
      mate_letters = 'PINK'
      mate_col = colors['pink']
      our_mate_color = 'pink_robot' 
  else:
      our_letters = 'PINK'
      our_col = colors['pink']
      our_robot_color = 'pink_robot' 
      mate_letters = 'GREEN' 
      mate_col = colors['green']
      our_mate_color = 'green_robot'
      
      # Get stuff
      ball_center = ball.getBallCoordinates(frame)
      our_orientation, our_robot_center = our_robot.getRobotOrientation(frame, 'us', our_robot_color)
      our_mate_orientation, our_mate_center = our_robot.getRobotOrientation(frame, 'us', our_mate_color)
      pink_opponent_orientation, pink_opponent_center = our_robot.getRobotOrientation(frame, 'opponent', 'pink_robot')
      green_opponent_orientation, green_opponent_center = our_robot.getRobotOrientation(frame, 'opponent', 'green_robot')
      
  c.close()
  
  ball_coords = Tracker.transformCoordstoDecartes(ball_center)
  
  # 0.46 is the estimated pixel -> cm ratio
  return (ball_coords[0] * 0.46, ball_coords[1] * 0.46),  # x,y ball coordinatees in cm
         (our_robot_center[0] * 0.46, our_robot_center[1] * 0.46),   # x,y bot coordinates in cm
         our_orientation[1])                             # direction vector (not scaled to anything)
     
