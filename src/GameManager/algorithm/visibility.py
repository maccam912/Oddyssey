# https://sites.google.com/site/jicenospam/visibilitydetermination
# https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm

def raycasting_sight(graph, position, sight):
    # Set explored region
    graph.visible_state_grid[graph.visible_state_grid==1] = 2
    
    # Raycasting vision
    # Get ray destination
    end_of_sight = []
    for x in range(max(position[0] - sight, 0) + 1, min(position[0] + sight, graph.visible_state_grid.shape[1]) - 1):
        end_of_sight.append((x, max(position[1] - sight, 0)))
        end_of_sight.append((x, min(position[1] + sight, graph.visible_state_grid.shape[0]) - 1))
        
    for y in range(max(position[1] - sight, 0), min(position[1] + sight, graph.visible_state_grid.shape[0])):
        end_of_sight.append((max(position[0] - sight, 0), y))
        end_of_sight.append((min(position[0] + sight, graph.visible_state_grid.shape[1]) - 1, y))
    # Ray projection
    for end in end_of_sight:
        ray = bresenhams_line_algorithm(position, end)
        if ray[0] == position:
            for node in ray[1:]:
                if not graph.block_vision_grid[node[1], node[0]]:
                    graph.visible_state_grid[node[1], node[0]] = 1
                else:
                    graph.visible_state_grid[node[1], node[0]] = 1
                    break
        else:
            for node in list(reversed(ray))[1:]:
                if not graph.block_vision_grid[node[1], node[0]]:
                    graph.visible_state_grid[node[1], node[0]] = 1
                else:
                    graph.visible_state_grid[node[1], node[0]] = 1
                    break
    # Post-processing artifact killer
    for x in range(max(position[0] - sight, 0) + 1, min(position[0] + sight, graph.visible_state_grid.shape[1]) - 1):
        for y in range(max(position[1] - sight, 0) + 1, min(position[1] + sight, graph.visible_state_grid.shape[0]) - 1):
            if graph.visible_state_grid[y, x] == 1 and not graph.block_vision_grid[y, x]:
                # North-West region
                if x < position[0] and y < position[1]:
                    if graph.block_vision_grid[y - 1, x]:
                        graph.visible_state_grid[y - 1, x] = 1
                    if graph.block_vision_grid[y , x - 1]:
                        graph.visible_state_grid[y, x - 1] = 1
                # North-East region
                elif x > position[0] and y < position[1]:
                    if graph.block_vision_grid[y - 1, x]:
                        graph.visible_state_grid[y - 1, x] = 1
                    if graph.block_vision_grid[y , x + 1]:
                        graph.visible_state_grid[y, x + 1] = 1
                # South-West region
                elif x < position[0] and y > position[1]:
                    if graph.block_vision_grid[y + 1, x]:
                        graph.visible_state_grid[y + 1, x] = 1
                    if graph.block_vision_grid[y , x - 1]:
                        graph.visible_state_grid[y, x - 1] = 1
                # South-East region
                elif x > position[0] and y > position[1]:
                    if graph.block_vision_grid[y + 1, x]:
                        graph.visible_state_grid[y + 1, x] = 1
                    if graph.block_vision_grid[y , x + 1]:
                        graph.visible_state_grid[y, x + 1] = 1
                # Harizontal
                elif x == position[0]:
                    if graph.block_vision_grid[y, x + 1]:
                        graph.visible_state_grid[y, x + 1] = 1
                    if graph.block_vision_grid[y, x - 1]:
                        graph.visible_state_grid[y, x - 1] = 1
                # Vertical
                elif y == position[1]:
                    if graph.block_vision_grid[y + 1, x]:
                        graph.visible_state_grid[y + 1, x] = 1
                    if graph.block_vision_grid[y - 1, x]:
                        graph.visible_state_grid[y - 1, x] = 1
                        

def bresenhams_line_algorithm(start, end):
    line = []
    steep = abs(end[1] - start[1]) > abs(end[0] - start[0])
    if steep:
        start = (start[1], start[0])
        end = (end[1], end[0])
    if start[0] > end[0]:
        start, end = end, start
    dx = end[0] - start[0]
    dy = abs(end[1] - start[1])
    error = dx / 2
    y = start[1]
    if start[1] < end[1]:
        step = 1
    else:
        step = -1
    for x in range(start[0], end[0]+1):
        if steep:
            line.append((y, x))
        else:
            line.append((x, y))
        error -= dy
        if error < 0:
            y += step
            error += dx    
    return line