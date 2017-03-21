import heapq

# http://theory.stanford.edu/~amitp/GameProgramming/
# https://en.wikipedia.org/wiki/A*_search_algorithm
# https://www.youtube.com/watch?v=KNXfSOx4eEE

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]
    
def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_algorithm(graph, start, goal):
    start = tuple(start)
    goal = tuple(goal)
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            return reconstruct_path(came_from, start, goal)
        
        for next in graph.get_neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current
                         
    # Return None when there is no path                         
    return None

def reconstruct_path(came_from, start, goal):
    start = tuple(start)
    goal = tuple(goal)
    
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
#    path.append(start) # optional
    path.reverse() # optional
    return path