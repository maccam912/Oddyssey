import pygame
from GameManager.menu import Menu
from GameManager.subscreen import SubScreen
from GameManager.map import Map
from GameManager.character import Player, Enemy, NPC


class NewGame():
    
    def __init__(self, curses, mouse_controller, keyboard_controller, is_realtime=False):
        self.curses = curses
        self.mouse_controller = mouse_controller
        self.keyboard_controller = keyboard_controller
        self.is_realtime = is_realtime
        self.initialization()
    
    def initialization(self):
        self.is_init = False
        self.enable = False
        self.timer_enable = False
        self.character_update = False
    
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
        self.toolbar.fill_char('/solid', 'wheat', 'transparent')
        
        # Initialize game
        self.map = Map(0, 0, 'unexplored', 'fixed', '../assets/data/level/level_0.grid', [])
                
        # Set control flag
        self.is_init = True
        self.enable = True
        self.timer_enable = True
        
        # Game object initialization
        self.player = Player(2, 2, '/face', 'wheat', 'transparent', self.map, 'Hero', 15, 20)
        self.enemy = Enemy(21, 8, 'g', 'green', 'transparent', self.map, 'goblin', 15, 10)
        self.npc = NPC(13, 24, '/face', 'peru', 'transparent', self.map, 'farmer', 15, 10)
        
        self.map.character_list.append(self.enemy)
        self.map.character_list.append(self.npc)
        self.map.character_list.append(self.player)
        
    
    def update(self, event):
        if self.is_realtime:
                self.timer += 1
                
        if self.keyboard_controller.pressed != None:
            # Menu enable
            if self.keyboard_controller.pressed[pygame.K_ESCAPE]:
                self.menu_enable = not self.menu_enable
            # Timer control
            if self.keyboard_controller.pressed[pygame.K_SPACE]:
                if not self.menu_enable:
                    self.timer_enable = not self.timer_enable
        
        # Keyboard events
        if self.timer_enable:
            if self.keyboard_controller.pressed != None and not self.is_realtime and not self.keyboard_controller.pressed[pygame.K_SPACE]:
                self.timer += 1
                self.character_update = True
            
        if self.character_update:
            for character in self.map.character_list:
                character.update(self.keyboard_controller, self.subscreen)
            self.character_update = False
        
        # Display
        if self.timer_enable:
            # Draw grass tiles
            sec = self.map.get_cell_section(0, 0, self.subscreen.width, self.subscreen.height)
            self.curses.set_cell_section(0, 0, sec)
            
            for character in self.map.character_list:
                character.draw(self.subscreen)
            
            # Draw counter            
            message = '%04d' %self.timer
            self.subscreen.put_message(3, 0 , message[-4:], foreground='white', background='transparent', auto=True, align='right')
        
        # Menu control
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
            # Return cells within menu section
            if self.menu_init:
                self.timer_enable = True
                self.menu_init = False
                self.menu.exit_menu()
                    
        # Draw timer state
        message = 'PULSED'
        if self.timer_enable:
            self.curses.put_message(self.curses.win_width-2, self.curses.win_height-1, '/solid'*len(message), foreground='wheat', background='transparent', auto=True, align='right')
        else:
            self.curses.put_message(self.curses.win_width-2, self.curses.win_height-1, message, foreground='white', background='transparent', auto=True, align='right')

        
        return self.enable