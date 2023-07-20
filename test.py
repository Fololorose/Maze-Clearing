from math import floor
import numpy as np

class Node:
  def __init__(self, x, y, rubbish_size = 0, rubbish_weight = 0, disposal_room = 0, h_score = 0):
    self.coordinate = (x, y) # Axial coordinate
    self.rubbish_size = rubbish_size # 1/2/3
    self.rubbish_weight =  rubbish_weight # 0/5/10/20/30
    self.disposal_room = disposal_room # True/False 
    self.children = []
    self.h_score = h_score

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

# def check_final_condition(child, current_bin_size, current_bin_weight):
#   if len(rooms_with_rubbish) == 0:
#     heuristic = closest_target_room(child, disposal_rooms, current_bin_size, current_bin_weight)
#   return heuristic

# Determine possible child nodes to become frontier
def expand_and_return_children(state_space, node, directions, current_bin_size, current_bin_weight):
  children = []
  for direction in directions.values():
    child = tuple(np.add(np.array(node.coordinate),np.array(direction)))
    for [x, y] in state_space:
      if child[0] == x and child[1] == y:
        children.append(Node(child[0], child[1]))
        children[-1].h_score = heuristics(state_space, children[-1], current_bin_size, current_bin_weight)
  return children

# Find the estimation cost to the closest disposal room or room with rubbish
def closest_target_room(child, target_rooms, current_bin_size, current_bin_weight):
  direct_distance = []
  temp_child_coordinate = child.coordinate + (z_coordinate(child.coordinate[0], child.coordinate[1]),)
  for target_room in target_rooms:
    if ((current_bin_size + target_room.rubbish_size) <= max_bin_size) and ((current_bin_weight + target_room.rubbish_weight) <= max_bin_weight):
      coordinates_subtract = []
      temp_target_room_coordinate = target_room.coordinate + (z_coordinate(target_room.coordinate[0], target_room.coordinate[1]),)
      for i in range(0, 3):
        coordinates_subtract.append(abs(temp_child_coordinate[i] - temp_target_room_coordinate[i]))
      direct_distance.append(max(coordinates_subtract))
    else:
      # If the bin size or bin weight exceeds the maximum, set direct_distance to a large value to discourage selecting this target
      direct_distance.append(float("inf"))
  return min(direct_distance)


# Heuristics euclidean distance
def heuristics(state_space, child, current_bin_size, current_bin_weight):
  # Retrieve the nodes with disposal room and the nodes with rubbish
  disposal_rooms = [node for node in state_space.values() if node.disposal_room]
  rooms_with_rubbish = [node for node in state_space.values() if node.rubbish_size != 0 or node.rubbish_weight != 0]
  if len(rooms_with_rubbish) == 0:
    heuristic1 = float("inf")
    heuristic2 = closest_target_room(child, disposal_rooms, current_bin_size, current_bin_weight)
  elif current_bin_size == 0:   
    heuristic1 = closest_target_room(child, rooms_with_rubbish, current_bin_size, current_bin_weight)
    heuristic2 = float("inf")
  else:
    heuristic1 = closest_target_room(child, rooms_with_rubbish, current_bin_size, current_bin_weight)
    heuristic2 = closest_target_room(child, disposal_rooms, current_bin_size, current_bin_weight)
  return min(heuristic1, heuristic2)


# Just for testing
def append_and_sort(frontier, child): 
  duplicated = False
  removed = False
  for i, f in enumerate(frontier):
    if child.coordinate == f.coordinate:
      duplicated = True
      if child.h_score <= f.h_score:
        del frontier[i]
        removed = True
        break
  if (not duplicated) or removed:
    insert_index = len(frontier)
    for i, f in enumerate(frontier):
      if child.h_score <= f.h_score:
        insert_index = i
        break
    frontier.insert(insert_index, child)
  return frontier

def greedy(state_space, rooms_with_rubbish, disposal_rooms, initial_node):
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
  explored = []
  frontier = []
  solution = []
  indices_to_remove = []
  current_bin_size = 0
  current_bin_weight = 0
    
  # Add initial node to frontier
  frontier.append(Node(initial_node[0], initial_node[1]))

  current_step = 0
  while not goal_achieved:
    current_node = state_space[frontier[0].coordinate]
    for i, room_with_rubbish in enumerate(rooms_with_rubbish):
      if current_node.coordinate == room_with_rubbish[0]:
        current_bin_size += current_node.rubbish_size
        current_bin_weight += current_node.rubbish_weight
        current_node.rubbish_size = 0
        current_node.rubbish_weight = 0
        indices_to_remove.append(i)

      # Remove the elements from rooms_with_rubbish using the collected indices
      for index in reversed(indices_to_remove):
        rooms_with_rubbish.pop(index)
        indices_to_remove.clear()
    
    for i, disposal_room in enumerate(disposal_rooms):
      if current_node.coordinate == disposal_room:
        current_bin_size = 0
        current_bin_weight = 0
        
    # Goal test at expansion
    if achieve_goal(current_node):
      goal_achieved = True
      solution.append(current_node.coordinate)
      break
    
    # Expand the first in the frontier
    children = expand_and_return_children(state_space, frontier[0], directions, current_bin_size, current_bin_weight)
    # Add children list to the expanded node
    frontier[0].add_children(children)
    # Add to the expanded node explored list
    explored.append(frontier[0])
    # Remove the expanded frontier from the frontier list
    current_expanded_node = frontier.pop(0)
    # Add the expanded node to the solution (optimal path)
    solution.append(current_expanded_node.coordinate)
    #print(*solution)
    # Add children to the frontier

    for child in children:
      # Check if a node was expanded or generated previously      
    #   if not(child.coordinate in [e.coordinate for e in explored]):
      frontier = append_and_sort(frontier, child)

    print("=" * 25, "Step:",current_step, "=" * 25)  
    print("\nCurrent position:", current_node.coordinate, "| Bin State:[",current_bin_size,"m³, ",current_bin_weight,"kg ]"  )
    remaining_rubbish_coordinates = [room[0] for room in rooms_with_rubbish]
    print("Rooms with Rubbish Left:", len(rooms_with_rubbish), "| Coordinates:", remaining_rubbish_coordinates)
    if current_node.coordinate in disposal_rooms:
        print("Bin moved to the disposal room.")
    elif current_node.rubbish_size or current_node.rubbish_weight:
        print("Bin collected rubbish in the room.")
    else:
        print("Bin moved to an empty room.")
    print("")
    print("-" * 50)  
    print("\nExplored: ", [e.coordinate for e in explored])
    print("Frontier: ", [(f.coordinate, f.h_score) for f in frontier])
    print("Children: ", [c.coordinate for c in children])
    print("")
    print("-" * 50)  
    print("\nSolution Path So Far: ", solution)
    print("")

    next_expanded_node = frontier.pop(0)
    frontier.clear()
    frontier.append(next_expanded_node)


    current_step += 1
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
      ((0, -5), 1, 10),
      ((1, -3), 3, 30),
      ((2, -3), 1, 5),
      ((3, -2), 1, 5),
      ((3, -5), 3, 5),
      ((4, -4), 2, 10),
      ((4, -6), 1, 20),
      ((6, -4), 2, 10),
      ((6, -7), 2, 5),
      ((7, -3), 1, 30),
      ((7, -6), 2, 20),
      ((8, -5), 3, 10)
  ]
    
  generate_maze(maze_height, maze_width, state_space) 
    
  initial_node = (0, 0)
    
  solution = greedy(state_space, rooms_with_rubbish, disposal_rooms, initial_node)
  print("=" * 50, "\nSolution:", solution)
  print("Path Cost:", len(solution))
    
