# Maze-Clearing
CSC3206 Artificial Intelligence Assignment
This is a Python implementation of a greedy maze-clearing algorithm that collects rubbish while moving towards the disposal rooms. The algorithm uses heuristics to estimate the cost to the closest disposal room or room with rubbish.

Table of Contents
- Overview
- Dependencies
- Usage
- Maze Representation
- Node Class
- Algorithm Description
- How to Run
- Sample Input and Output

Overview
The greedy maze-clearing algorithm is designed to navigate through a maze containing rooms with rubbish and disposal rooms. The objective is to collect all rubbish from rooms and reach the disposal rooms. The algorithm uses a greedy approach to choose the next move based on a heuristic that estimates the cost to the closest disposal room or room with rubbish.

Dependencies
This code relies on the following Python libraries:
- math
- numpy

Usage
You can use this code to simulate the navigation of an agent in a maze to collect rubbish and dispose of it. The agent's path will be determined by the greedy heuristic, which aims to minimise the distance to the closest disposal room or room with rubbish.

Maze Representation
The maze is represented as a 2D grid. Each grid cell is a room, and the rooms can have the following characteristics:
- (x, y): Axial coordinate of the room.
- rubbish_size: The amount of rubbish in the room (values: 1, 2, 3).
- rubbish_weight: The weight of the rubbish in the room (values: 0, 5, 10, 20, 30).
- disposal_room: Boolean value (True/False) indicating if the room is a disposal room.

Node Class
The Node class represents each room in the maze. It contains attributes such as coordinate, rubbish size, rubbish weight, disposal room status, children (neighboring rooms), and heuristic score.

Algorithm Description
The greedy algorithm follows these steps:

1. Initialize the maze and agent's starting position.
2. While there is rubbish in any room:
   a. Collect rubbish from the current room and update the bin capacity.
   b. Expand the current node and generate children nodes.
   c. Calculate heuristic scores for the children nodes based on the distance to the closest room with rubbish and disposal room.
   d. Choose the child node with the minimum heuristic score and move to that room.
3. If the current node is a disposal room and the bin is not empty, empty the bin.
4. Repeat steps 2 and 3 until all rubbish is collected and the agent reaches the disposal room.

How to Run
1. Make sure you have Python and the required dependencies installed.
2. Copy and paste the code into a Python script (e.g., maze_navigation.py).
3. Customise the maze dimensions, maximum bin capacity, disposal rooms, and rooms with rubbish as needed.
4. Run the script.

Sample Input and Output
To see the algorithm in action, use the provided sample input to navigate the maze and collect rubbish. The output will show the path taken by the agent, including the rooms visited and any disposal stops.
