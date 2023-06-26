class Node:
    def __init__(self, x,y, bin_size = 0, bin_weight = 0, rubbish_weight= 0, rubbish_size = 0, parent=None, action=None):
        self.x = x #x coordinate
        self.y = y #y coordinate
        self.bin_size = bin_size #0-5
        self.bin_weight = bin_weight #0-40
        self.rubbish_weight =  rubbish_weight #0/5/10/20/30
        self.rubbish_size = rubbish_size #1/2/3
        self.parent = parent
        self.action = action

        


