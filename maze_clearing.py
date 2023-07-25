from math import floor
import numpy as np

#node class to store properties of the room
class Node:
  def __init__(self, x, y, rubbish_size = 0, rubbish_weight = 0, is_disposal_room = 0, h_score = 0):
    self.coordinate = (x, y) # Axial coordinate
    self.rubbish_size = rubbish_size # 1/2/3
    self.rubbish_weight =  rubbish_weight # 0/5/10/20/30
    self.is_disposal_room = is_disposal_room # True/False 
    self.children = []
    self.h_score = h_score

  def add_children(self, children):
    self.children.extend(children)
        
# Compute the z coordinate
def z_coordinate(x, y):
  return - x - y


def generate_maze(height, width, state_space):
  # Formula to create the maze coordinates
  for x in range(0, width):
    x_offset = floor((x+1)/2)
    for z in range(0 - x_offset, height - x_offset):
      y = -x-z 
      #determine the DISPOSAL_ROOMS, rubbish info and put it as properties for the node
      is_disposal_room = (x, y) in DISPOSAL_ROOMS
      rubbish_size, rubbish_weight = find_rubbish_info(x, y)
      state_space[(x, y)] = Node(x, y, rubbish_size, rubbish_weight, is_disposal_room)


def find_rubbish_info(x, y):
  for room_info in ROOMS_WITH_RUBBISH:
    if (x, y) == room_info[0]:
      #returns rubbish information
      return room_info[1], room_info[2]
  return 0, 0

def achieved_goal(current_node):
  # Goal is achieved when the current node is a disposal room and all the rooms with rubbish have been cleared
  if current_node.is_disposal_room and len(ROOMS_WITH_RUBBISH) == 0:
    return True
  else:
    return False

# Expand children of the current node
def expand_and_return_children(state_space, node, current_bin_size, current_bin_weight):
  directions = {
    "N": (0, +1),
    "NE": (+1, 0),
    "SE": (+1, -1),
    "S": (0, -1),
    "SW": (-1, 0),
    "NW": (-1, +1),
  }
  children = []
  for direction in directions.values():
    child = tuple(np.add(np.array(node.coordinate),np.array(direction)))
    for [x, y] in state_space:
      if child[0] == x and child[1] == y:
        children.append(Node(child[0], child[1]))
        #calculate and set the h_score of the expanded node
        children[-1].h_score = heuristics(state_space, children[-1], current_bin_size, current_bin_weight)
  return children

#find the estimation cost to the closest disposal room or room with rubbish
def closest_target_room(child, target_rooms, current_bin_size, current_bin_weight):
  direct_distance = []
  temp_child_coordinate = child.coordinate + (z_coordinate(child.coordinate[0], child.coordinate[1]),)
  for target_room in target_rooms:
    #if current_bin_size and current_bin_weight can accommodate the current room
    if ((current_bin_size + target_room.rubbish_size) <= MAX_BIN_SIZE) and ((current_bin_weight + target_room.rubbish_weight) <= MAX_BIN_WEIGHT):
      #use the formula to calculate the euclidean distance from the child node to the targetted room
      coordinates_subtract = []
      temp_target_room_coordinate = target_room.coordinate + (z_coordinate(target_room.coordinate[0], target_room.coordinate[1]),)
      for i in range(0, 3):
        coordinates_subtract.append(abs(temp_child_coordinate[i] - temp_target_room_coordinate[i]))
      direct_distance.append(max(coordinates_subtract))
    #if the bin size or bin weight exceeds the maximum, set direct_distance to a large value to discourage selecting this target
    else:
      direct_distance.append(float("inf"))
  return min(direct_distance)


#heuristic1 calculates the h(n) to the nearest room with rubbish
#heuristic2 calculates the h(n) to the nearest disposal room
def heuristics(state_space, child, current_bin_size, current_bin_weight):
  #retrieve the nodes with disposal room and the nodes with rubbish
  DISPOSAL_ROOMS = [node for node in state_space.values() if node.is_disposal_room]
  ROOMS_WITH_RUBBISH = [node for node in state_space.values() if node.rubbish_size != 0 or node.rubbish_weight != 0]
  #if there are no more rooms with rubbish, then go straight to disposal rooms
  if len(ROOMS_WITH_RUBBISH) == 0:
    heuristic1 = float("inf")
    heuristic2 = closest_target_room(child, DISPOSAL_ROOMS, current_bin_size, current_bin_weight)
  #if there are no rubbish in the bin, go to rubbish rooms
  elif current_bin_size == 0:  
    heuristic1 = closest_target_room(child, ROOMS_WITH_RUBBISH, current_bin_size, current_bin_weight)
    heuristic2 = float("inf")
  #else decide find which one is the closest path 
  else:
    heuristic1 = closest_target_room(child, ROOMS_WITH_RUBBISH, current_bin_size, current_bin_weight)
    heuristic2 = closest_target_room(child, DISPOSAL_ROOMS, current_bin_size, current_bin_weight)
    #penalise if current bin is very little to prevent from going into disposal too early
    if(current_bin_size < MAX_BIN_SIZE/1.15): 
        heuristic2 += 5
  return min(heuristic1, heuristic2)


def append_and_sort(frontier, child): 
  duplicated = False
  removed = False
  for i, f in enumerate(frontier):
    #if child is in frontier
    if child.coordinate == f.coordinate:
      duplicated = True
      if child.h_score <= f.h_score:
        del frontier[i]
        removed = True
        break
  if (not duplicated) or removed:
    #add node to the back of the frontier
    insert_index = len(frontier)
    #if child node is nearer to goal
    for i, f in enumerate(frontier):
      if child.h_score <= f.h_score:
        insert_index = i
        break
    frontier.insert(insert_index, child)
  return frontier

def print_info(current_step, current_node, current_bin_size, current_bin_weight, remaining_rubbish_coordinates, explored, frontier, children, solution, has_rubbish):
    output = f"""
{'=' * 25} Step: {current_step} {'=' * 25}

Current position: {current_node.coordinate} | Bin State: [{current_bin_size} m³, {current_bin_weight} kg]
Rooms with Rubbish Left: {len(remaining_rubbish_coordinates)} | Coordinates: {remaining_rubbish_coordinates}
{'Bin moved to the disposal room.' if current_node.coordinate in DISPOSAL_ROOMS else 'Bin collected rubbish in the room.' if has_rubbish
 else 'Bin moved to an empty room.'}

{'-' * 60}

Explored: {[e.coordinate for e in explored]}
Frontier: {[(f.coordinate, f.h_score) for f in frontier]}
Children: {[c.coordinate for c in children]}

{'-' * 60}

Solution Path So Far: {solution}

"""
    print(output)

def greedy(state_space, ROOMS_WITH_RUBBISH, DISPOSAL_ROOMS, initial_node):
  goal_achieved = False
  explored = []
  frontier = []
  solution = []
  indices_to_remove = []
  current_bin_size = 0
  current_bin_weight = 0
    
  # Add initial node to frontier
  frontier.append(Node(initial_node[0], initial_node[1]))
  
  #while the ROOMS_WITH_RUBBISH are not cleared, continue
  has_rubbish=False
  current_step = 1
  while not goal_achieved:
    #set the current node as the frontier(sorted according to the the node's h_score)
    current_node = state_space[frontier[0].coordinate]
    #if it is a rubbish room add rubbish to Ronny's bin
    for i, room_with_rubbish in enumerate(ROOMS_WITH_RUBBISH):
      if current_node.coordinate == room_with_rubbish[0]:
        has_rubbish = True
        current_bin_size += current_node.rubbish_size
        current_bin_weight += current_node.rubbish_weight
        current_node.rubbish_size = 0
        current_node.rubbish_weight = 0
        indices_to_remove.append(i)

      #then remove the rubbish from the rooms 
      for index in reversed(indices_to_remove):
        ROOMS_WITH_RUBBISH.pop(index)
        indices_to_remove.clear()
    
    #if it is a disposal room then clear the rubbish
    for i, is_disposal_room in enumerate(DISPOSAL_ROOMS):
      if current_node.coordinate == is_disposal_room:
        current_bin_size = 0
        current_bin_weight = 0
        
    #check if all ROOMS_WITH_RUBBISH is cleared
    if achieved_goal(current_node):
      goal_achieved = True
      solution.append(current_node.coordinate)
      break
    
    #else expand the first node in the frontier
    children = expand_and_return_children(state_space, frontier[0], current_bin_size, current_bin_weight)
    # Add children list to the expanded node
    frontier[0].add_children(children)
    # Add to the expanded node explored list
    explored.append(frontier[0])
    # Remove the expanded frontier from the frontier list
    current_expanded_node = frontier.pop(0)
    # Add the expanded node to the solution (optimal path)
    solution.append(current_expanded_node.coordinate)
    # print(*solution)
    # Add children to the frontier
    for child in children:
      #decide on how to sort the frontier
      frontier = append_and_sort(frontier, child)
        
    print_info(current_step, current_node, current_bin_size, current_bin_weight, [room[0] for room in ROOMS_WITH_RUBBISH], explored, frontier, children, solution,has_rubbish)
    has_rubbish=False
    next_expanded_node = frontier.pop(0)
    frontier.clear()
    frontier.append(next_expanded_node)
    current_step += 1
  return solution


if __name__ == "__main__":
    
  #define the dimension of the maze, maximum bin capacity and initilise empty state_space
  MAZE_HEIGHT = 6
  MAX_WIDTH = 9
  MAX_BIN_SIZE = 5
  MAX_BIN_WEIGHT = 40
  state_space = {}
    
  #determine disposal rooms, rooms with rubbish including rubbish size & weight
  DISPOSAL_ROOMS = [(2, -6), (5, -2), (8, -9)] # (x,y)
  ROOMS_WITH_RUBBISH = [ #(x, y, rubbish_size, rubbish weight)
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
    
  generate_maze(MAZE_HEIGHT, MAX_WIDTH, state_space) 
    
  initial_node = (0, 0)
    
  solution = greedy(state_space, ROOMS_WITH_RUBBISH, DISPOSAL_ROOMS, initial_node)
  print("=" * 25, "FINAL SOLUTION", "=" * 25)
  print("Solution:", solution)
  print("Path Cost:", len(solution))
  print("")
    
