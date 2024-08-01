import os
from datetime import datetime

if not os.path.isdir("./logs"):
    try:
        os.mkdir("./logs")
    except OSError:
        print("Could not create logs directory")
    else:
        print("Created logs directory")

logfile = open("./logs/ALSETLogData.log","a")

if os.path.getsize("./logs/ALSETLogData.log")>0:
    logfile.write("\n")

view_size_sm = 2
view_size_lg = 3

# Simple check if two rectangles intersect
# Rectangles are a 4 tuple of (x, y, width, height)
def intersects(rect_a, rect_b):
  # separate data
  a_x, a_y, a_width, a_height = rect_a
  b_x, b_y, b_width, b_height = rect_b
  # verify intersections
  x_intersection = (a_x + a_width > b_x) and (b_x + b_width > a_x)
  y_intersection = (a_y + a_height > b_y) and (b_y + b_height > a_y)
  # return result
  return x_intersection and y_intersection


# Will return a list of the sensors that detect an obstacle
# ex: ["Front", "Right"]
def get_car_obstructions(car_bounds, obstacles):
  # local variables
  car_x, car_y, car_width, car_height = car_bounds
  car_center_x = car_x + car_width / 2
  car_center_y = car_y + car_height / 2
  # bounds calculation -- downwards y is positive
  front_bounds = (car_center_x - view_size_lg / 2, 
                 car_y - view_size_sm, 
                 view_size_lg,
                 view_size_sm)
  back_bounds = (car_center_x - view_size_lg / 2, 
                 car_y + car_height, 
                 view_size_lg,
                 view_size_sm)
  right_bounds = (car_x + car_width, 
                 car_center_y - view_size_lg / 2, 
                 view_size_sm,
                 view_size_lg)
  left_bounds = (car_x - view_size_sm, 
                 car_center_y - view_size_lg / 2, 
                 view_size_sm,
                 view_size_lg)
  # prepare result array 
  result = []
  
  # check intersections
  for obs in obstacles:
    if intersects(front_bounds, obs):
      result.append("Front")
    if intersects(back_bounds, obs):
      result.append("Back")
    if intersects(left_bounds, obs):
      result.append("Left")
    if intersects(right_bounds, obs):
      result.append("Right")
      
  return result


# Returns a string interpretation of a list of the obstacles
def obstructions_to_str(obstr_list):
  if (len(obstr_list) == 0):
    return "No obstructions around the car!"
  else:
    return str(obstr_list)

  

# returns if the path to the goal parking spot is clear 
# assuming car has been sufficiently lined up to the goal spot
def is_parking_path_clear(v):
  speed = v[0]
  car_bounds = v[1]
  goal_bounds = v[2]
  obstacles = v[3]
  car_x, car_y, car_width, car_height = car_bounds
  goal_x, goal_y, goal_width, goal_height = goal_bounds
  #check speed
  if(speed>10 or speed<0):
    logfile.write("["+datetime.now().strftime("%H:%M:%S")+ "] Parking failed due to invalid speed. \n")
    logfile.close()
    return "Invalid Speed"
  # calculate collective bounds
  min_x = min(car_x, goal_x)
  max_x = max(car_x + car_width, goal_x + goal_width)
  min_y = min(car_y, goal_y)
  max_y = max(car_y, goal_y)
  total_width = abs(max_x - min_x)
  total_height = abs(max_y - min_y)
  collective_bounds = (min_x, max_y, total_width, total_height)
  # check collisions for each obstacle --then return result
  for obs in obstacles:
    if intersects(collective_bounds, obs):
      return False
  return True


