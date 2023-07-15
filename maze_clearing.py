from math import floor

class Node:
    def __init__(self, x, y, rubbish_size = 0, rubbish_weight= 0, disposal_room=0, parent=None, action=None):
        self.cube = (x, y) #axial coordinate
        # self.bin_size = bin_size #0-5 
        # self.bin_weight = bin_weight #0-40
        self.rubbish_size = rubbish_size #1/2/3
        self.rubbish_weight =  rubbish_weight #0/5/10/20/30
        self.disposal_room = disposal_room #True/False 
        self.parent = parent
        self.action = action
        self.children = []

    def add_children(self, children):
        self.children.extend(children)
        
# compute the z coordinate
def z_coordinate(x, y):
    return -x-y # constraint of x+y+z=0

# direction (only store manipulation of x and y)
directions = {
    "N": (0, +1),
    "NE": (+1, 0),
    "SE": (+1, -1),
    "S": (0, -1),
    "SW": (-1, 0),
    "NW": (-1, +1),
}

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

def a_star():
    pass

# Define state space (maze size, rubbish, disposal room)
if __name__ == "__main__":
    
    # Define the dimension of the maze & initilise empty state_space
    maze_height = 6
    maze_width = 9
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
    
    # Print the state_space
    for coordinate, node in state_space.items():
        print("Coordinate:", coordinate)
        print("Rubbish Size:", node.rubbish_size)
        print("Rubbish Weight:", node.rubbish_weight)
        print("Disposal Room:", node.disposal_room)
        print("---")

    
    