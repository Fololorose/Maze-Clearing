
#goal check
def isgoal(node):
  if node.disposal_room and rooms_with_rubbish == 0: #need sum up total room with rubbish at beginning and update it for every action 
    return True
  else:
    return False

#heuristics euclidean distance

def heuristics(child, state_space, disposal_rooms):
  h = closestDisposalRoom(child, disposal_rooms) + closestRoomWithRubbish(child, state_space)
  return h
     
#find the estimation cost to closest disposal room 
def closestDisposalRoom(child, disposal_rooms):
  direct_distance = []
  for disposal_room in disposal_rooms:
    coordinates_substract = []
    for i in range(0, 3):
      coordinates_substract.append(abs(child.cube[i] - disposal_room[i]))
    direct_distance.append(max(coordinates_substract))
  return min(direct_distance)

#find the estimation cost to closest room with rubbish 
def closestRoomWithRubbish(child, state_space):
  rooms_with_rubbish = []
  for state_space in state_space:
    if state_space.rubbish_size > 0:
      rooms_with_rubbish.append(state_space)
  direct_distance = []
  for room_with_rubbish in rooms_with_rubbish:
    coordinates_substract = []
    for i in range(0, 3):
      coordinates_substract.append(abs(child.cube[i] - room_with_rubbish[i]))
    direct_distance.append(max(coordinates_substract))
  return min(direct_distance)