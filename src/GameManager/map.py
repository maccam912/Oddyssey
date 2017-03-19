import numpy as np

tiles = {
        'grass' : {'cell': {'char' : '.', 'foreground' : 'green', 'background' : 'transparent'},        'cost' : 1              ,'block_vision' : False},
        'wall'  : {'cell': {'char' : '/brick', 'foreground' : 'darkgray', 'background' : 'dimgray'},    'cost' : float('inf')   ,'block_vision' : True}
        }

class Map():
    def __init__(self, width, height, init_state='unexplored', border='fixed', file_path=None):
        self.width = width
        self.height = height
        self.init_state = init_state
        self.border = border
        self.file_path = file_path
        self.initialization()
        
    def initialization(self):
        self.tile_grid = self.load_tile_grid()
        self.cell_grid = self.get_cell_grid()
        self.cost_grid = self.get_cost_grid()
        self.block_vision_grid = self.get_block_vision_grid()
        
        # FOV Initialization
        self.visible_state_grid = self.get_visible_state_grid()
    
    def load_tile_grid(self):
        if self.file_path != None:
            # Load file
            int_grid = np.loadtxt(self.file_path, dtype=int)
            tile_grid = self.get_tile_grid_from_int_grid(int_grid)
            self.width = int_grid.shape[1]
            self.height = int_grid.shape[0]
        else:
            # Random terrain generation
            pass
        
        return tile_grid
    
    def get_tile_grid_from_int_grid(self, int_grid):
        tile_grid = np.empty([int_grid.shape[0], int_grid.shape[1]], dtype=dict)
        for i in range(int_grid.shape[0]):
            for j in range(int_grid.shape[1]):
                tile_grid[i, j] = tiles[list(tiles.keys())[int_grid[i, j]]]
        return tile_grid
    
    def get_cell_grid(self):
        cell_grid = np.empty([self.tile_grid.shape[0], self.tile_grid.shape[1]], dtype=dict)
        for i in range(self.tile_grid.shape[0]):
            for j in range(self.tile_grid.shape[1]):
                cell_grid[i, j] = self.tile_grid[i, j]['cell']
        return cell_grid
    
    def get_cost_grid(self):
        cost_grid = np.ones([self.tile_grid.shape[0], self.tile_grid.shape[1]], dtype=float)
        for i in range(self.tile_grid.shape[0]):
            for j in range(self.tile_grid.shape[1]):
                cost_grid[i, j] = self.tile_grid[i, j]['cost']
        return cost_grid
    
    def get_block_vision_grid(self):
        block_vision_grid = np.ones([self.tile_grid.shape[0], self.tile_grid.shape[1]], dtype=bool)
        for i in range(self.tile_grid.shape[0]):
            for j in range(self.tile_grid.shape[1]):
                block_vision_grid[i, j] = self.tile_grid[i, j]['block_vision']
        return block_vision_grid
    
    def get_visible_state_grid(self):
        if self.init_state == 'unexplored':
            visible_state_grid = np.zeros([self.tile_grid.shape[0], self.tile_grid.shape[1]], dtype=int)
        elif self.init_state == 'visible':
            visible_state_grid = np.ones([self.tile_grid.shape[0], self.tile_grid.shape[1]], dtype=int)
        elif self.init_state == 'explored':
            visible_state_grid = 2 * np.ones([self.tile_grid.shape[0], self.tile_grid.shape[1]], dtype=int)
        else:
            raise ValueError('Error: No matching state.')
        return visible_state_grid            
    
    def get_cell_section(self, x, y, width, height):
#        temp_section = self.cell_grid.T
#        section = temp_section[x : x + width, y : y + height].T
        section = self.get_cell_section_by_visibility(x, y, width, height)
        return section
    
    def get_cell_section_by_visibility(self, x, y, width, height):
        section = np.empty([min(height, self.visible_state_grid.shape[0]), min(width, self.visible_state_grid.shape[1])], dtype=dict)
        for i in range(x, min(x + width, self.visible_state_grid.shape[1])):
            for j in range(y, min(y + height, self.visible_state_grid.shape[0])):
                if self.visible_state_grid[j, i] == 0:
                    # State: unexplored
                    section[j, i] = {'char' : '/l1', 'foreground' : 'gray', 'background': 'transparent'}
                elif self.visible_state_grid[j, i] == 1:
                    # State: visible
                    section[j, i] = self.cell_grid[j, i].copy()
                elif self.visible_state_grid[j, i] == 2:
                    # State: explored
                    section[j, i] = self.cell_grid[j, i].copy()
                    section[j, i]['foreground'] = 'gray'
                    section[j, i]['background'] = 'transparent'
                else:
                    raise ValueError('Error: No matching state.')
        return section
    
    # For path finding algorithm    
    def get_neighbors(self, position):
        neighbors = []
        if self.border == 'fixed':
            if position[0] > 0 and position[0] < self.width - 1:
                if position[1] > 0 and position[1] < self.height - 1:
                    neighbors.append((position[0] - 1, position[1] - 1))
                    neighbors.append((position[0] - 1, position[1]))
                    neighbors.append((position[0] - 1, position[1] + 1))
                    neighbors.append((position[0] + 1, position[1] - 1))
                    neighbors.append((position[0] + 1, position[1]))
                    neighbors.append((position[0] + 1, position[1] + 1))
                    neighbors.append((position[0], position[1] - 1))
                    neighbors.append((position[0], position[1] + 1))
                elif position[1] == 0:
                    neighbors.append((position[0] - 1, position[1]))
                    neighbors.append((position[0] - 1, position[1] + 1))
                    neighbors.append((position[0] + 1, position[1]))
                    neighbors.append((position[0] + 1, position[1] + 1))
                    neighbors.append((position[0], position[1] + 1))
                elif position[1] == self.height - 1:
                    neighbors.append((position[0] - 1, position[1] - 1))
                    neighbors.append((position[0] - 1, position[1]))
                    neighbors.append((position[0] + 1, position[1] - 1))
                    neighbors.append((position[0] + 1, position[1]))
                    neighbors.append((position[0], position[1] - 1))
            elif position[0] == 0:
                if position[1] > 0 and position[1] < self.height - 1:
                    neighbors.append((position[0] + 1, position[1] - 1))
                    neighbors.append((position[0] + 1, position[1]))
                    neighbors.append((position[0] + 1, position[1] + 1))
                    neighbors.append((position[0], position[1] - 1))
                    neighbors.append((position[0], position[1] + 1))
                elif position[1] == 0:
                    neighbors.append((position[0] + 1, position[1]))
                    neighbors.append((position[0] + 1, position[1] + 1))
                    neighbors.append((position[0], position[1] + 1))
                elif position[1] == self.height - 1:
                    neighbors.append((position[0] + 1, position[1] - 1))
                    neighbors.append((position[0] + 1, position[1]))
                    neighbors.append((position[0], position[1] - 1))
            elif position[0] == self.width - 1:
                if position[1] > 0 and position[1] < self.height - 1:
                    neighbors.append((position[0] - 1, position[1] - 1))
                    neighbors.append((position[0] - 1, position[1]))
                    neighbors.append((position[0] - 1, position[1] + 1))
                    neighbors.append((position[0], position[1] - 1))
                    neighbors.append((position[0], position[1] + 1))
                elif position[1] == 0:
                    neighbors.append((position[0] - 1, position[1]))
                    neighbors.append((position[0] - 1, position[1] + 1))
                    neighbors.append((position[0], position[1] + 1))
                elif position[1] == self.height - 1:
                    neighbors.append((position[0] - 1, position[1] - 1))
                    neighbors.append((position[0] - 1, position[1]))
                    neighbors.append((position[0], position[1] - 1))
        
        # Remove impassable neighbors
        neighbors = [neighbor for neighbor in neighbors if self.get_cost_by_position(neighbor) != float('inf')]
                
        return neighbors
    
    def get_cost_by_position(self, position):
        cost = self.cost_grid[position[1], position[0]]
        return cost
    
    def cost(self, from_position, to_position):
        # Considers only the destination cost
        cost = self.get_cost_by_position(to_position)
        # Penalty on the diagonal directions
        if to_position == (from_position[0] - 1, from_position[1] - 1) or to_position == (from_position[0] - 1, from_position[1] + 1) \
        or to_position == (from_position[0] + 1, from_position[1] - 1) or to_position == (from_position[0] + 1, from_position[1] + 1):
            cost *= np.sqrt(2)            
        return cost