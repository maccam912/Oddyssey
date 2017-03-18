import pygame
from GameManager.menu import Menu
from GameManager.subscreen import SubScreen
from GameManager.map import Map
from GameManager.ai import a_star_search, reconstruct_path

class NewGame():
    
    def __init__(self, curses, mouse_controller, keyboard_controller):
        self.curses = curses
        self.mouse_controller = mouse_controller
        self.keyboard_controller = keyboard_controller
        self.initialization()
    
    def initialization(self):
        self.is_init = False
        self.enable = False
        self.timer_enable = False
    
    def start(self):
        # Initial setting
        self.menu_size = (40,20)
        self.menu_enable = False
        self.menu_init = False
        self.timer = 0
        
        # Exit menu
        self.window_center = (int(self.curses.win_width/2), int(self.curses.win_height/2))
        self.select_dict = {0 : 'Exit to Main Menu', 1 : 'Exit Game'}
        self.menu_size = (40, 20)
        self.menu = Menu(self.curses, self.mouse_controller, self.keyboard_controller, int(self.curses.win_width/2 - self.menu_size[0]/2), int(self.curses.win_height/2 - self.menu_size[1]/2), self.menu_size[0], self.menu_size[1], \
                         self.select_dict, align='mid', flick_enable=False, indicator_enable=False, mouse_enable=True)
        
        # Draw UI
        
        if self.curses.screen_width > self.curses.screen_height:
            screen_size =int(3/4 * self.curses.screen_width / self.curses.cell_width)
            self.subscreen = SubScreen(0, 0, screen_size, self.curses.win_height, self.curses)
            self.toolbar = SubScreen(screen_size, 0, self.curses.win_width - screen_size, self.curses.win_height, self.curses)
        elif self.curses.screen_width < self.curses.screen_height:
            screen_size =int(3/4 * self.curses.screen_height / self.curses.cell_height)
            self.subscreen = SubScreen(0, 0, self.curses.win_width, screen_size, self.curses)
            self.toolbar = SubScreen(0, screen_size, self.curses.win_width, self.curses.win_height - screen_size, self.curses)
        else:
            raise ValueError('Error: Wrong resolution.')        
        self.toolbar.fill_char('/solid', 'teal', 'transparent')
        
        # Initialize game
        self.map = Map(0, 0, '../assets/data/level/level_0.grid')
                
        # Set control flag
        self.is_init = True
        self.enable = True
        self.timer_enable = True
        
        # Game object initialization
        self.player_pos = [2, 2]
        self.goal = [25, 15]
    
    def update(self, event):
        # Gameloop
        if self.timer_enable:
            # Draw grass tiles
            sec = self.map.get_cell_section(0, 0, self.subscreen.width, self.subscreen.height)
            self.curses.set_cell_section(0, 0, sec)
            
            self.subscreen.put_char(self.player_pos[0], self.player_pos[1], '/face', 'yellow', 'transparent')
            self.subscreen.put_char(self.goal[0], self.goal[1], '/_face', 'yellow', 'transparent')
            
            
            came_from, cost_so_far = a_star_search(self.map, self.player_pos, self.goal)
            path = reconstruct_path(came_from, self.player_pos, self.goal)
            for node in path:
                if node != tuple(self.player_pos) and node != tuple(self.goal):
                    self.subscreen.put_char(node[0], node[1], '/solid', 'yellow', 'transparent')
            
             # Draw counter
            self.timer += 1
            message = '%04d' %self.timer
            self.subscreen.put_message(3, 0 , message[-4:], foreground='white', background='transparent', auto=True, align='right')

        # Keyboard events
        if self.keyboard_controller.pressed != None:
            if self.keyboard_controller.pressed[pygame.K_ESCAPE]:
                self.menu_enable = not self.menu_enable
                
            if self.keyboard_controller.pressed[pygame.K_SPACE]:
                if not self.menu_enable:
                    self.timer_enable = not self.timer_enable                
                self.key_block = False
            
            if self.timer_enable:
                if self.keyboard_controller.pressed[pygame.K_w]:
                    self.player_pos[1] -= 1
                if self.keyboard_controller.pressed[pygame.K_x]:
                    self.player_pos[1] += 1
                if self.keyboard_controller.pressed[pygame.K_a]:
                    self.player_pos[0] -= 1
                if self.keyboard_controller.pressed[pygame.K_d]:
                    self.player_pos[0] += 1
                if self.keyboard_controller.pressed[pygame.K_q]:
                    self.player_pos[0] -= 1
                    self.player_pos[1] -= 1
                if self.keyboard_controller.pressed[pygame.K_e]:
                    self.player_pos[0] += 1
                    self.player_pos[1] -= 1
                if self.keyboard_controller.pressed[pygame.K_c]:
                    self.player_pos[0] += 1
                    self.player_pos[1] += 1
                if self.keyboard_controller.pressed[pygame.K_z]:
                    self.player_pos[0] -= 1
                    self.player_pos[1] += 1
                
        if self.menu_enable:
            self.timer_enable = False
            # Draw menu
            if not self.menu_init:
                self.menu.initialization()
                self.menu_init = True
            flag = self.menu.update()
            if flag == 'Exit to Main Menu':
                self.enable = False
            elif flag == 'Exit Game':
                pygame.quit()
        else:
            # Return cells in menu section
            if self.menu_init:
                self.timer_enable = True
                self.menu_init = False
                self.menu.exit_menu()
                    
        # Draw timer state
        message = 'PULSED'
        if self.timer_enable:
            self.curses.put_message(self.curses.win_width-2, self.curses.win_height-1, '/solid'*len(message), foreground='teal', background='transparent', auto=True, align='right')
        else:
            self.curses.put_message(self.curses.win_width-2, self.curses.win_height-1, message, foreground='white', background='transparent', auto=True, align='right')

        
        return self.enable