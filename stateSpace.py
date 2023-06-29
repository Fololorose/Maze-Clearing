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

#dummy class node
class Node:
    def __init__(self,y, x, rubbish):
        self.x = x 
        self.y = y
        self.rubbish = rubbish # 0/1
        self.neighbours = []

    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)
      
#transition model 
def transitionModel(node, action):
    #initialise node 
    child = Node(0, 2, 0)
    #fill in node with other parameters
    #key in coordinates
    if action == "N":
        child.x =  node.x - 2
        child.y = (node.y)
    elif action == "S":
        child.x = node.x + 2
        child.y = (node.y) 
    elif action == "NE":
        child.x = (node.x) + 1
        child.y = (node.y) - 1
    elif action == "SE":
        child.x = (node.x) + 1
        child.y = (node.y) + 1
    elif action == "SW":
        child.x = (node.x) - 1
        child.y = (node.y) + 1
    elif action == "NW":
        child.x = (node.x) - 1
        child.y = (node.y) - 1
    elif action == "clean":
        child.rubbish = 0
    return child

#state space: edit node attributes
def createStateSpace():
    #define size of the maze
    width = 9
    height = 7

    #list of possible actions
    actions = ['N', 'S', 'NE', 'SE', 'SW', 'NW']

    #create a dict to save the state space and transitions using axial coordinates as keys
    state_space = {}

    # put the range correctly :)
    for y in range(height):
        for x in range(width):
            if x % 2 == 0:
                if y % 2 == 0:
                    node = Node(y, x, 0)
                    state_space[(y, x)] = node
                    for action in actions:
                        neighbour = transitionModel(node, action)
                        if(-1 <neighbour.x <= width and -1 < neighbour.y <= height):
                            node.add_neighbour(neighbour) 
            else:
                if y % 2 != 0:
                    if x % 2 != 0:
                        node = Node(y, x, 0)
                        state_space[(y, x)] = node
                        for action in actions:
                            neighbour = transitionModel(node, action)
                            if(-1 <neighbour.x <= width and -1 < neighbour.y <= height):
                                node.add_neighbour(neighbour) 
                        
    #print out the state space
    for key in state_space:
        print(key, '->', state_space[key])
        # for neighbour in state_space[key].neighbours: 
        #     print("neighbour: " + str(neighbour.y) + "," + str(neighbour.x))

    

createStateSpace()

