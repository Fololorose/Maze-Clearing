#the state space created is a dictionary with coordinates as keys and the node object as the value
#=================a visual representation====================
#   state_space = {
#   (0, 0) -> <__main__.Node object at 0x10f6243d0>
#   (0, 2) -> <__main__.Node object at 0x10f624490>
#   (0, 4) -> <__main__.Node object at 0x10f624580>
#                        .
#                        .
#                        .
#   }

from math import floor

class Node:
    def __init__(self, q, r, s, bin_size = 0, bin_weight = 0, rubbish_weight= 0, rubbish_size = 0, disposal_room=0, parent=None, action=None):
        self.cube = (q, r, s) #cube coordinate
        self.bin_size = bin_size #0-5 
        self.bin_weight = bin_weight #0-40
        self.rubbish_weight =  rubbish_weight #0/5/10/20/30
        self.rubbish_size = rubbish_size #1/2/3
        self.disposal_room = disposal_room #True/False 
        self.parent = parent
        self.action = action
        self.neighbours = []

    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)
 
#add two vectors together
def vectorAdd(cube1, cube2):
    new_cube = (cube1[0] + cube2[0], cube1[1] + cube2[1], cube1[2] + cube2[2])
    return new_cube

#transition model 
def transitionModel(node, action):
    #initialise node 
    child = Node(0, 0, 0, 0)
    #fill in node with other parameters
    #key in coordinates
    if action == "N":
        child.cube = vectorAdd(node.cube, get_cube_direction_vector("N"))
    elif action == "S":
        child.cube = vectorAdd(node.cube, get_cube_direction_vector("S"))
    elif action == "NE":
        child.cube = vectorAdd(node.cube, get_cube_direction_vector("NE"))
    elif action == "SE":
        child.cube = vectorAdd(node.cube, get_cube_direction_vector("SE"))
    elif action == "NW":
        child.cube = vectorAdd(node.cube, get_cube_direction_vector("NW"))
    elif action == "SW":
        child.cube = vectorAdd(node.cube, get_cube_direction_vector("SW"))
    return child

#get calculations given direction
def get_cube_direction_vector(direction):
    # (dq, dr, ds)
    if direction == "N":
        return (0, -1, +1)
    elif direction == "S":
        return (0, +1, -1)
    elif direction == "NE":
        return (+1, -1, 0)
    elif direction == "SE":
        return (+1, 0, -1)
    elif direction == "SW":
        return (-1, +1, 0)
    elif direction == "NW":
       return (-1, 0, +1)
    # elif action == "clean":
    #     child.rubbish = 0

#creates entire state space
def createStateSpace():
    #define size of the maze
    width = 9
    height = 6

    #list of possible actions
    actions = ['N', 'S', 'NE', 'SE', 'SW', 'NW']

    #create a dict to save the state space and transitions using axial coordinates as keys
    state_space = {}

    #formula to create the maze coordinates
    for q in range(0, width):
        q_offset = floor((q+1)/2)
        for r in range(0 - q_offset, height - q_offset):
            s = -q-r
            node = Node(q,r,s)
            state_space[(q,r,s)] = node
    
    #add neighbours to each node
    for key in state_space:
        for action in actions:
            neighbour = transitionModel(state_space[key], action)
            if neighbour.cube in state_space.keys():
                state_space[key].add_neighbour(neighbour)  
    
    #determine disposal rooms, rubbish size and weight of each rooms
    disposal_rooms = [(2, 4, -6), (5, -3, -2), (8, 1, -9)]
    room_assignments = [ #(room coordinates, weight, size)
        ((0, 5, -5), 10, 1),
        ((1, 2, -3), 30, 3),
        ((2, 1, -3), 5, 1),
        ((3, -1, -2), 5, 1),
        ((3, 2, -5), 5, 3),
        ((4, 0, -4), 10, 2),
        ((4, 2, -6), 20, 1),
        ((6, -2, -4), 10, 2),
        ((6, 1, -7), 5, 2),
        ((7, -4, -3), 30, 1),
        ((7, -1, -6), 20, 2),
        ((8, -3, -5), 10, 3)
    ]
    for room in disposal_rooms:
        state_space[room].disposal_room = True
        print(state_space[room].disposal_room)
        
    for room_coord, weight, size in room_assignments:
        state_space[room_coord].rubbish_weight = weight
        state_space[room_coord].size = size

    #print out the state space
    for key in state_space:
        print("node: " + str(state_space[key].cube))
        for neighbour in state_space[key].neighbours: 
           print("neighbour: " + str(neighbour.cube))

#run
createStateSpace()


