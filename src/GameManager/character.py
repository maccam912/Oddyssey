import pygame
from GameManager.algorithm.path_finding import a_star_algorithm
from GameManager.algorithm.visibility import raycasting_sight, bresenhams_line_algorithm

class Character():
    def __init__(self, x, y, char, foreground, background, graph, name, sight, health, is_blocked=True):
        self.x = x
        self.y = y
        self.char = char
        self.foreground = foreground
        self.background = background
        self.graph = graph
        self.name = name
        self.sight = sight
        self.health = health
        self.is_blocked = is_blocked
    
    def initialization(self):
        self.current_health = self.health
        self.move_cost = 0
        self.target = None
        self.base_damage = 1
        self.background = self.graph.tile_grid[self.y, self.x]['cell']['foreground']
    
    def path_finding(self, goal, screen=None, is_shown=False):
        path = a_star_algorithm(self.graph, self.get_pos(), goal)
        if path != None and is_shown:
            for node in path:
                if node != tuple(self.get_pos()) and node != tuple(goal):
                    screen.put_char(node[0], node[1], '/solid', 'aqua', 'transparent')
        return path
    
    def get_pos(self):
        return (self.x, self.y)    
    
    def draw(self, offset_x, offset_y, screen):
        if self.graph.visible_state_grid[self.y, self.x] == 1 and \
        self.x >= screen.x + offset_x and self.x < screen.x + screen.width + offset_x and self.y >= screen.y + offset_y and self.y < screen.y + screen.height + offset_y:
            screen.put_char(self.x - offset_x, self.y - offset_y, self.char, self.foreground, self.background)
        
    def update(self, keyboard_controller, message_screen):
        pass
    
    def is_grid_movable(self, graph, position):
        if graph.cost_grid[position[1], position[0]] == float('inf'):
            return False
        else:
            return True
    
    def check_character_list(self, position, character_type, character_list):
        for character in character_list:
            if position == character.get_pos() and character.__class__.__name__ == character_type and character.current_health > 0:
                self.target = character
                return True
        return False
    
    def attack(self, character, message_screen):
        character.current_health -= self.base_damage
        message_screen.add_message('%s dealed %d damage to %s.' %(self.name, self.base_damage, character.name), 'orange')
        if character.current_health <= 0:
            character.current_health = 0
            character.killed()
            message_screen.add_message('%s is killed.' %character.name, 'red')
            swap_indx = self.graph.character_list.index(character)
            self.graph.character_list[0], self.graph.character_list[swap_indx] = self.graph.character_list[swap_indx], self.graph.character_list[0]
            
    def killed(self):
        self.char = '%'
        self.foreground = 'red'
        if self.is_blocked:
            self.graph.cost_grid[self.y, self.x] = self.graph.tile_grid[self.y, self.x]['cost']
    
    def move(self, position):
        current_tile_cost = self.graph.cost_grid[self.y, self.x]
        self.move_cost += 1
        self.move_cost %= current_tile_cost
        if self.move_cost == 0:
            self.x = position[0]
            self.y = position[1]
    
class Player(Character):
    def __init__(self, x, y, char, foreground, background, graph, name, sight, health, is_blocked=True):
        super(Player, self).__init__(x, y, char, foreground, background, graph, name, sight, health, is_blocked)
        self.initialization()
        raycasting_sight(self.graph, self.get_pos(), self.sight)
    
    def update(self, keyboard_controller, message_screen):
        self.target = None
        if self.current_health > 0:
            self.background = self.graph.tile_grid[self.y, self.x]['cell']['foreground']
            # Nnbocked current position
            if self.is_blocked:
                self.graph.cost_grid[self.y, self.x] = self.graph.tile_grid[self.y, self.x]['cost']
        
            # Keyboard event
            self.update_keyboard(keyboard_controller, message_screen)
            # Mouse event
            raycasting_sight(self.graph, self.get_pos(), self.sight)
        
            # Blocked moved position
            if self.is_blocked:
                self.graph.cost_grid[self.y, self.x] = float('inf')
        
    def update_keyboard(self, keyboard_controller, message_screen):
        if keyboard_controller.pressed != None:
            if self.graph.border == 'fixed':
                if keyboard_controller.pressed[pygame.K_w] and self.y > 0:
                    self.keyboard_unit_controller((self.x, self.y - 1), message_screen)
                if keyboard_controller.pressed[pygame.K_x] and self.y < self.graph.height - 1:
                    self.keyboard_unit_controller((self.x, self.y + 1), message_screen)
                if keyboard_controller.pressed[pygame.K_a] and self.x > 0:
                    self.keyboard_unit_controller((self.x - 1, self.y), message_screen)
                if keyboard_controller.pressed[pygame.K_d] and self.x < self.graph.width - 1:
                    self.keyboard_unit_controller((self.x + 1, self.y), message_screen)
                if keyboard_controller.pressed[pygame.K_q] and self.y > 0 and self.x > 0:
                    self.keyboard_unit_controller((self.x - 1, self.y - 1), message_screen)
                if keyboard_controller.pressed[pygame.K_e] and self.x < self.graph.width - 1 and self.y > 0:
                    self.keyboard_unit_controller((self.x + 1, self.y - 1), message_screen)
                if keyboard_controller.pressed[pygame.K_c] and self.y < self.graph.height - 1 and self.x < self.graph.width - 1:
                    self.keyboard_unit_controller((self.x + 1, self.y + 1), message_screen)
                if keyboard_controller.pressed[pygame.K_z] and self.x > 0 and self.y < self.graph.height - 1:
                    self.keyboard_unit_controller((self.x - 1, self.y + 1), message_screen)
    
    def keyboard_unit_controller(self, to_position, message_screen):
        if self.check_character_list(to_position, 'Enemy', self.graph.character_list):
            # Attack
            self.attack(self.target, message_screen)
        elif self.check_character_list(to_position, 'NPC', self.graph.character_list):
            # Interact
            self.target.interact(message_screen)
        elif self.is_grid_movable(self.graph, to_position):
            # Move
            self.move(to_position)
    
    def killed(self):
        self.char = '/_face'
        self.foreground = 'red'
        if self.is_blocked:
            self.graph.cost_grid[self.y, self.x] = self.graph.tile_grid[self.y, self.x]['cost']
        
class Enemy(Character):
    def __init__(self, x, y, char, foreground, background, graph, name, sight, health, is_blocked=True):
        super(Enemy, self).__init__(x, y, char, foreground, background, graph, name, sight, health, is_blocked)
        self.initialization()
        
    def initialization(self):
        self.current_health = self.health
        self.move_cost = 0
        self.last_saw_position = None
        self.target = None
        self.player_path = None
        self.base_damage = 1
        self.background = self.graph.tile_grid[self.y, self.x]['cell']['foreground']
        
    def update(self, keyboard_controller, message_screen):
        if self.current_health > 0:
            self.background = self.graph.tile_grid[self.y, self.x]['cell']['foreground']
            
            # Nnbocked current position
            if self.is_blocked:
                self.graph.cost_grid[self.y, self.x] = self.graph.tile_grid[self.y, self.x]['cost']
            # Action
            if self.tracking_criteria_in_sight():
                # Tracking the player
                self.player_path = self.get_player_path()
                self.stategy_chase_player_to_death(self.player_path, message_screen)
            elif self.last_saw_position != None:
                # Track to the last saw position
                self.player_path = self.get_last_saw_path()
                self.stategy_chase_player_to_death(self.player_path, message_screen)
                
            # Blocked moved position
            if self.is_blocked:
                self.graph.cost_grid[self.y, self.x] = float('inf')
    
    def tracking_criteria_in_sight(self):
        line_of_sight = None
        for character in self.graph.character_list:
            if character.__class__.__name__ == 'Player':
                if character.current_health > 0:                    
                    line_of_sight = bresenhams_line_algorithm(self.get_pos(), character.get_pos())
                    break
        if line_of_sight != None:    
            if len(line_of_sight) > self.sight + 1:
                return False
            for node in line_of_sight:
                if self.graph.block_vision_grid[node[1], node[0]]:
                    return False
        return True                
    
    def stategy_chase_player_to_death(self, path, message_screen):                    
        if self.check_character_list(path[0], 'Player', self.graph.character_list):
            self.attack(self.target, message_screen)
        elif self.is_grid_movable(self.graph, path[0]):
            self.move((path[0][0], path[0][1]))
    
    def get_player_path(self):
        for character in self.graph.character_list:
            if character.__class__.__name__ == 'Player':
                if character.current_health > 0:
                    self.last_saw_position = character.get_pos()
                    if character.is_blocked:
                        self.graph.cost_grid[self.last_saw_position[1], self.last_saw_position[0]] = self.graph.tile_grid[self.last_saw_position[1], self.last_saw_position[0]]['cost']
                    path = self.path_finding(self.last_saw_position)
                    return path[1:]
                else:
                    return [self.get_pos()]
    
    def get_last_saw_path(self):
        path = self.path_finding(self.last_saw_position)
        if len(path) > 1:
            return path[1:]
        else:
            return [self.get_pos()]
                
class NPC(Character):
    def __init__(self, x, y, char, foreground, background, graph, name, sight, health, is_blocked=True):
        super(NPC, self).__init__(x, y, char, foreground, background, graph, name, sight, health, is_blocked)
        self.initialization()
        
    def update(self, keyboard_controller, message_screen):
        if self.current_health > 0:
            self.background = self.graph.tile_grid[self.y, self.x]['cell']['foreground']
            
            # Nnbocked current position
            if self.is_blocked:
                self.graph.cost_grid[self.y, self.x] = self.graph.tile_grid[self.y, self.x]['cost']
            
            # Action
            
            # Blocked moved position
            if self.is_blocked:
                self.graph.cost_grid[self.y, self.x] = float('inf')
    
    def interact(self, message_screen):
        message_screen.add_message('%s said: Hello, traveler!' %(self.name), 'wheat')
                