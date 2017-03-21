import time
import os 
import pygame
import configparser

from PYGUSES.pyguses.curses import Curses
from GameManager.gui.menu import MainMenu
from GameManager.demo import Demo
from GameManager.new_game import NewGame
from GameManager.controller import MouseController, KeyboardController

# system setting
os.environ['SDL_VIDEO_CENTERED'] = '1'

class Game():

    def __init__(self):
        self.initialization()

    def initialization(self):
        # Game config settings
        config = configparser.ConfigParser()
        config.read('config.ini')

        # [VERSION]
        game_title = config['VERSION']['title']
        game_ver = config['VERSION']['version']
        game_date = config['VERSION']['date']
        self.title = '%s --- %s(%s)'  %(game_title, game_ver, game_date)
        # [WINDOW]
        self.fps = int(config['WINDOW']['fps'])
        self.screen_width = int(config['WINDOW']['screen_width'])
        self.screen_height = int(config['WINDOW']['screen_height'])
        self.is_fullscreen = bool(int(config['WINDOW']['is_fullscreen']))
        self.icon_image_path = config['ASSETS']['icon_image_path']
        
        # Pygame initialization
        pygame.init()
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(self.title)
        pygame.display.set_icon(pygame.image.load(self.icon_image_path))
        self.done = False
        self.clock = pygame.time.Clock()        
        
        # Game initialization
        pygame.mouse.set_visible(False)
        
        self.curses = Curses(self.screen_width, self.screen_height, 'black')
        self.mouse_controller = MouseController(self.curses)
        self.keyboard_controller = KeyboardController(self.curses)
        
        self.select_dict = {0 : 'New Game', 1 : 'Demo', 2 : 'Quit'}
        menu_size = (40, 20)
        self.menu = MainMenu(self.curses, self.mouse_controller, self.keyboard_controller, int(self.curses.win_width/2 - menu_size[0]/2), int(self.curses.win_height/2 - menu_size[1]/2), menu_size[0], menu_size[1], \
                             self.select_dict, align='mid', flick_enable=True, indicator_enable=True, mouse_enable=True)
        
        self.demo = Demo(self.curses, self.keyboard_controller)        
        self.new_game = NewGame(self.curses, self.mouse_controller, self.keyboard_controller)
        
    def run(self):
         
        while not self.done:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
            
            t0 = time.time()
            # --- Game logic should go here
                        
            # Main Menu
            if self.menu.enable:
                flag = self.menu.update()
                if self.keyboard_controller.pressed != None or self.mouse_controller.pressed!=None:
                    # ESC pressed on main menu
                    if self.keyboard_controller.pressed != None:
                        is_exit = self.keyboard_controller.pressed[pygame.K_ESCAPE]
                    else:
                        is_exit = False
                    
                    # Game states
                    if flag == 'New Game':
                        self.curses.clear_window()
                        self.new_game.start()
                        self.mouse_controller.initialization()
                        self.keyboard_controller.initialization()
                    elif flag == 'Demo':
                        self.curses.clear_window()
                        self.demo.start()
                        self.mouse_controller.initialization()
                        self.keyboard_controller.initialization()
                    elif flag == 'Quit' or is_exit:
                        self.done = True
            
            # Game
            if self.new_game.enable:
                self.new_game.update(event)
            else:
                # Diable demo and reactivate main menu
                if not self.menu.enable and flag == 'New Game':
                    self.menu.initialization()
                    self.new_game.initialization()   
                    self.mouse_controller.initialization()

            # Demo
            if self.demo.enable:
                self.demo.update()
            else:
                # Diable demo and reactivate main menu
                if not self.menu.enable and flag == 'Demo':
                    self.menu.initialization()
                    self.demo.initialization()
                    self.mouse_controller.initialization()
            
            # Keyboard and mouse control
            self.keyboard_controller.update(event)
            self.mouse_controller.update()
            
            # Curses display
            self.screen.blit(self.curses.background, (0, 0))            
            self.screen.blit(self.curses.get_window_surface(), (0, 0))
            self.screen.blit(self.curses.foreground, (0, 0))
            
            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            
            # --- Limit to 60 frames per second
            self.clock.tick(self.fps)
        
            print('\rGame loop time elapsed: %.4f sec.' %(time.time() - t0), end='\r')

        # Close the window and quit.
        # If you forget this line, the program will 'hang'
        # on exit if running from IDLE.
        pygame.quit()
