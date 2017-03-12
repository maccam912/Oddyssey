import time
import os 
import pygame
import configparser

from PYGUSES.pyguses.curses import Curses
from GameManager.menu import MainMenu
from GameManager.demo import Demo
from GameManager.adventure import Adventure

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
        self.curses = Curses(self.screen_width, self.screen_height, 'black')
        self.select_dict = {0 : 'A New Adventure', 1 : 'Demo', 2 : 'Quit'}
        menu_size = (40, 20)
        self.menu = MainMenu(self.curses, int(self.curses.win_width/2 - menu_size[0]/2), int(self.curses.win_height/2 - menu_size[1]/2), menu_size[0], menu_size[1], self.select_dict, align='mid', flick_enable=True)
        self.demo = Demo(self.curses)
        self.adventure = Adventure(self.curses)
        
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
                flag = self.menu.update(event)
                if flag == 'Quit' or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.done = True
                elif flag == 'A New Adventure':
                    self.curses.clear_window()
                    self.adventure.init()
                elif flag == 'Demo':
                    self.curses.clear_window()
                    self.demo.init()
            
            # Game
            if self.adventure.enable:
                self.adventure.update(event)
            else:
                # Diable demo and reactivate main menu
                if not self.menu.enable and flag == 'A New Adventure':
                    self.menu.initialization()
                    self.adventure.initialization()                    
            # Demo
            if self.demo.enable:
                self.demo.update(event)
            else:
                # Diable demo and reactivate main menu
                if not self.menu.enable and flag == 'Demo':
                    self.menu.initialization()
                    self.demo.initialization()
                    
            # Curses display
            self.screen.blit(self.curses.background, (0, 0))            
            self.screen.blit(self.curses.get_window_surface(), (0, 0))
                                
            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            
            # --- Limit to 60 frames per second
            self.clock.tick(self.fps)
        
            print('\rGame loop time elapsed: %.4f sec.' %(time.time() - t0), end='\r')

        # Close the window and quit.
        # If you forget this line, the program will 'hang'
        # on exit if running from IDLE.
        pygame.quit()
