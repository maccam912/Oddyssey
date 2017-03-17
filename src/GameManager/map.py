import numpy as np

tiles = {
        'grass' : {'cell': {'char' : '.', 'foreground' : 'green', 'background' : 'transparent'},        'passable' : True},
        'wall'  : {'cell': {'char' : '/brick', 'foreground' : 'darkgray', 'background' : 'dimgray'},    'passable' : False}
        }

class Map():
    def __init__(self, width, height, file_path=None):
        self.width = width
        self.height = height
        self.file_path = file_path
        self.initialization()
        
    def initialization(self):
        self.tile_grid = self.load_tile_grid()
        self.cell_grid = self.get_cell_grid()
        self.path_grid = self.get_path_grid()
    
    def load_tile_grid(self):
        if self.file_path != None:
            # Load file
            int_grid = np.loadtxt(self.file_path, dtype=int)
            tile_grid = self.get_tile_grid_from_int_grid(int_grid)
            self.width = int_grid.shape[1]
            self.height = int_grid.shape[0]
        else:
            # Terrain generation
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
    
    def get_path_grid(self):
        path_grid = np.ones([self.tile_grid.shape[0], self.tile_grid.shape[1]], dtype=bool)
        for i in range(self.tile_grid.shape[0]):
            for j in range(self.tile_grid.shape[1]):
                if not self.tile_grid[i, j]['passable']:
                    path_grid[i, j] = False
        return path_grid
    
    def get_cell_section(self, x, y, width, height):
        temp_section = self.cell_grid.T
        section = temp_section[x : x + width, y : y + height].T
        return section