import pygame
from GameManager.algorithm.path_finding import a_star_algorithm
from GameManager.algorithm.visibility import raycasting_sight

class Character():
    def __init__(self, x, y, char, foreground, background, sight):
        self.x = x
        self.y = y
        self.char = char
        self.foreground = foreground
        self.background = background
        self.sight = sight
    
    def path_finding(self, graph, goal, screen, is_shown=False):
        path = a_star_algorithm(graph, self.get_pos(), goal)
        if path != None and is_shown:
            for node in path:
                if node != tuple(self.get_pos()) and node != tuple(goal):
                    screen.put_char(node[0], node[1], '/solid', 'aqua', 'transparent')
        return path
    
    def get_pos(self):
        return (self.x, self.y)    
    
    def draw(self, screen):
        screen.put_char(self.x, self.y, self.char, self.foreground, self.background)
        
    def update(self, graph):
        pass
    
    def is_grid_movable(self, graph, position):
        if graph.cost_grid[position[1], position[0]] == float('inf'):
            return False
        else:
            return True
    
class Player(Character):
    def __init__(self, x, y, char, foreground, background, sight):
        super(Player, self).__init__(x, y, char, foreground, background, sight)
    
    def update(self, keyboard_controller, graph):
        # Keyboard event
        self.update_keyboard(keyboard_controller, graph)
        # Mouse event
        raycasting_sight(graph, self.get_pos(), self.sight)
        
    def update_keyboard(self, keyboard_controller, graph):
        if keyboard_controller.pressed != None:
            if graph.border == 'fixed':
                if keyboard_controller.pressed[pygame.K_w] and self.y > 0 \
                and self.is_grid_movable(graph, (self.x, self.y - 1)):
                    self.y -= 1
                if keyboard_controller.pressed[pygame.K_x] and self.y < graph.height - 1\
                and self.is_grid_movable(graph, (self.x, self.y + 1)):
                    self.y += 1
                if keyboard_controller.pressed[pygame.K_a] and self.x > 0\
                and self.is_grid_movable(graph, (self.x - 1, self.y)):
                    self.x -= 1
                if keyboard_controller.pressed[pygame.K_d] and self.x < graph.width - 1\
                and self.is_grid_movable(graph, (self.x + 1, self.y)):
                    self.x += 1
                if keyboard_controller.pressed[pygame.K_q] and self.y > 0 and self.x > 0\
                and self.is_grid_movable(graph, (self.x - 1, self.y - 1)):
                    self.x -= 1
                    self.y -= 1
                if keyboard_controller.pressed[pygame.K_e] and self.x < graph.width - 1 and self.y > 0\
                and self.is_grid_movable(graph, (self.x + 1, self.y - 1)):
                    self.x += 1
                    self.y -= 1
                if keyboard_controller.pressed[pygame.K_c] and self.y < graph.height - 1 and self.x < graph.width - 1\
                and self.is_grid_movable(graph, (self.x + 1, self.y + 1)):
                    self.x += 1
                    self.y += 1
                if keyboard_controller.pressed[pygame.K_z] and self.x > 0 and self.y < graph.height - 1\
                and self.is_grid_movable(graph, (self.x - 1, self.y + 1)):
                    self.x -= 1
                    self.y += 1
 