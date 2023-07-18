from math import floor
import numpy as np
import heapq

class Node:
  def __init__(self, x, y, rubbish_size = 0, rubbish_weight= 0, disposal_room=0, parent=None, action=None, f_score=0):
    self.coordinate = (x, y) # Axial coordinate
    self.rubbish_size = rubbish_size # 1/2/3
    self.rubbish_weight =  rubbish_weight # 0/5/10/20/30
    self.disposal_room = disposal_room # True/False 
    # self.parent = parent
    # self.action = action
    self.children = []
    self.f_score = f_score

  def add_children(self, children):
    self.children.extend(children)
        
# Compute the z coordinate
def z_coordinate(x, y):
  return - x - y # Constraint of x+y+z=0

# Generate maze with respective coordinates and characteristics
def generate_maze(height, width, state_space):
  # Formula to create the maze coordinates
  for x in range(0, width):
    x_offset = floor((x+1)/2)
    for z in range(0 - x_offset, height - x_offset):
      y = -x-z 
      disposal_room = (x, y) in disposal_rooms
      rubbish_size, rubbish_weight = find_rubbish_info(x, y)
      state_space[(x, y)] = Node(x, y, rubbish_size, rubbish_weight, disposal_room)

# Find rubbish info for a given coordinate
def find_rubbish_info(x, y):
  for room_info in rooms_with_rubbish:
    if (x, y) == room_info[0]:
      return room_info[1], room_info[2]
  return 0, 0

# Goal check
def achieve_goal(current_node):
  # Goal is achieved when the current node is a disposal room and all the rooms with rubbish have been cleared
  if current_node.disposal_room and len(rooms_with_rubbish) == 0:
    return True
  else:
    return False

# Determine possible child nodes to become frontier
def expand_and_return_children(current_node, directions):
  children = []
  for direction in directions.values():
    new_coordinate = tuple(np.add(np.array(current_node.coordinate),np.array(direction)))
    if new_coordinate in state_space:
      child = state_space[new_coordinate]
      children.append(child)
  return children

# Find the estimation cost to the closest disposal room or room with rubbish
def closest_target_room(child, target_rooms):
  direct_distance = []
  temp_child_coordinate = child.coordinate + (z_coordinate(child.coordinate[0], child.coordinate[1]),)
  for target_room in target_rooms:
    coordinates_substract = []
    temp_target_room_coordinate = target_room.coordinate + (z_coordinate(target_room.coordinate[0], target_room.coordinate[1]),)
    for i in range(0, 3):
      coordinates_substract.append(abs(temp_child_coordinate[i] - temp_target_room_coordinate[i]))
    direct_distance.append(max(coordinates_substract))
  return min(direct_distance)

# Heuristics euclidean distance
def heuristics(child, state_space):
  # Retrieve the nodes with disposal room and the nodes with rubbish
  disposal_rooms = [node for node in state_space.values() if node.disposal_room]
  rooms_with_rubbish = [node for node in state_space.values() if node.rubbish_size != 0 or node.rubbish_weight != 0]
  # Probably gonna implement weightage
  h_score = closest_target_room(child, disposal_rooms) + closest_target_room(child, rooms_with_rubbish) 
  return h_score

# Just for testing
def append_and_sort(current_node, frontier, child, g_score, f_score, came_from): 
  if child not in [i[1] for i in frontier]:
      came_from[child] = current_node
      g_score[child] = g_score[current_node] + 1
      f_score[child] = g_score[child] + heuristics(child, state_space)
      heapq.heappush(frontier, ((f_score[child], child.coordinate), child))
  return frontier

def a_star(initial_node):
  # Direction (only store manipulation of x and y)
  directions = {
    "N": (0, +1),
    "NE": (+1, 0),
    "SE": (+1, -1),
    "S": (0, -1),
    "SW": (-1, 0),
    "NW": (-1, +1),
  }
    
  goal_achieved = False
  frontier = []
  explored = []
  came_from = {}
  g_score = {initial_node: 0}
  f_score = {initial_node: heuristics(initial_node, state_space)}
    
  # Add initial node to frontier
  # frontier.append(initial_node)
  heapq.heappush(frontier, (f_score[initial_node], initial_node))
    
  while not goal_achieved:
    current_node = heapq.heappop(frontier)[1]
    # current_node = frontier[0]
    for room_with_rubbish in rooms_with_rubbish:
      if current_node.coordinate == room_with_rubbish[0]:
        current_node.rubbish_size = 0
        current_node.rubbish_weight = 0
      rooms_with_rubbish.remove(room_with_rubbish)
        
    # Goal test at expansion
    if achieve_goal(current_node):
      goal_achieved = True
      break
    
    # Expand the first in the frontier
    children = expand_and_return_children(current_node, directions)
    # Add children list to the expanded node
    current_node.add_children(children)
    # Add to the expanded node explored list
    explored.append(current_node)
    # # Remove the expanded frontier from the frontier list
    # del frontier[0]
    # Add children to the frontier
    for child in children:
      # Check if a node was expanded or generated previously
      if not (child.coordinate in [e.coordinate for e in explored]):       
        frontier = append_and_sort(current_node, frontier, child, g_score, f_score, came_from)
        
    print("Explored:", [e.coordinate for e in explored])
    print("Frontier:", [(f.coordinate, f_score[f]) for _, f in frontier])
    print("Children:", [c.coordinate for c in children])
    print("")
    
  solution = []
  while current_node in came_from:   
    solution.append(current_node)
    current_node = came_from[current_node]
  return solution

# Define state space (maze size, rubbish, disposal room)
if __name__ == "__main__":
    
  # Define the dimension of the maze, maximum bin capacity and initilise empty state_space
  maze_height = 6
  maze_width = 9
  max_bin_size = 5
  max_bin_weight = 40
  state_space = {}
    
  # Determine disposal rooms, rooms with rubbish including rubbish size & weight
  disposal_rooms = [(2, -6), (5, -2), (8, -9)] # (x,y)
  rooms_with_rubbish = [ #(x, y, rubbish_size, rubbish weight)
      ((0, 0), 1, 30),
      ((0, -5), 1, 10),
      ((1, -3), 3, 30),
      ((2, -3), 1, 5),
      ((3, -2), 1, 5),
      ((3, -5), 3, 5),
      ((4, -4), 2, 10),
      ((4, -6), 1, 20),
      ((6, -4), 2, 10),
      ((6, -7), 2, 5),
      ((7, -6), 2, 20),
      ((8, -5), 3, 10)
  ]
    
  generate_maze(maze_height, maze_width, state_space) 
    
  initial_node = state_space[(0, 0)]
    
  
    
  # # Print the state_space
  # for coordinate, node in state_space.items():
  #     print("Coordinate:", coordinate)
  #     print("Rubbish Size:", node.rubbish_size)
  #     print("Rubbish Weight:", node.rubbish_weight)
  #     print("Disposal Room:", node.disposal_room)
  #     print("---")
  
  solution  = a_star(initial_node)
  solution_coordinates = [node.coordinate for node in solution]
  print("Solution:", solution_coordinates)
  # print("Path Cost:", cost)
    
    
    
