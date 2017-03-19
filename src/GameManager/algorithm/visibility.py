def basic_sight(graph, position, sight):
    # Set explored region
    graph.visible_state_grid[graph.visible_state_grid==1] = 2
    # Set visible region
    graph.visible_state_grid[max(position[1] - sight, 0) : min(position[1] + sight, graph.visible_state_grid.shape[0]),\
                             max(position[0] - sight, 0) : min(position[0] + sight, graph.visible_state_grid.shape[1])] = 1
    # Raycasting vision
