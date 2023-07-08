from queue import PriorityQueue

def a_star(initial_node):
  frontier = PriorityQueue()
  # Create a dictionary to store the cost from the start to each node
  g_score = {initial_node: 0}
  # Create a dictionary to store the total estimated cost of each node
  f_score = {}
  #keeps track of the parent node for each explored node
  came_from = {}
  visited = []
  distance = {initial_node: 0}
  # add initial node to frontier
  frontier.put(initial_node)

  while not frontier.empty():
    current = frontier.get()
    # Check if the current node has already been visited
    if current in visited:
        continue
    # Mark the current node as visited
    visited.append(current)
    
    # Check if the current node is the goal
    if isgoal(current):
        # Reconstruct the path
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(initial_node)
        path.reverse()
        return path
    
    # Explore the neighbors of the current node
    for neighbour in current.neighbours:
        # Calculate the tentative g_score
        tentative_g_score = g_score[current] + distance(current, neighbour)

        if neighbour not in g_score or tentative_g_score < g_score[neighbour]:
            # Update the g_score and f_score
            g_score[neighbour] = tentative_g_score
            f_score[neighbour] = tentative_g_score + heuristic(neighbour, state_space, disposal_rooms)
            came_from[neighbour] = current

            # Push the neighbor into the frontier with its f_score as the priority
            frontier.put((f_score[neighbour], neighbour))
  # No path found
  return None



      

