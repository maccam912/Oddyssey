import pygame
import numpy as np
from PYGUSES.pyguses.form import Hline, Frame
from PYGUSES.pyguses.color import colornames

class Demo():
    
    def __init__(self, curses, keyboard_controller):
        self.curses = curses
        self.keyboard_controller = keyboard_controller
        self.initialization()
    
    def initialization(self):
        self.is_init = False
        self.enable = False
    
    def start(self):
        # Draw Title
        Hline(0, self.curses.win_width-1, 0, self.curses, char='█', foreground='navy', background='transparent')
        title = 'Demo: show all characters'
        char_list = self.curses.get_char_list(title)
        for x in range(len(char_list)):
            self.curses.put_char(x, 0, char_list[x], 'yellow', 'navy')
            
        # Draw info
        Hline(0, self.curses.win_width-1, self.curses.win_height-1, self.curses, char='█', foreground='navy', background='transparent')
        info = '<BACKSPACE>: retrun'
        char_list = self.curses.get_char_list(info)
        for x in range(len(char_list)):
            self.curses.put_char(self.curses.win_width - len(char_list) + x, self.curses.win_height-1, char_list[x], 'yellow', 'navy')
        
        # Demo: show all characters
        self.show_character_sheet()        
        # Demo form
        Frame(0, 8, 10, 8, self.curses, style=0, is_filled=False, char='█', foreground='white', background='transparent', frame_foreground='white', frame_background='transparent')
        
        self.show_all_colors()
        
        # Set control flag
        self.is_init = True
        self.enable = True
    
    def update(self):        
        # Keyboard events
        if self.keyboard_controller.pressed != None:
            if self.keyboard_controller.pressed[pygame.K_BACKSPACE]:
                self.enable = False
        
    def show_character_sheet(self):
        CL=[]
        for i in range(self.curses.char_array.shape[0]):
            for j in range(self.curses.char_array.shape[1]):
                CL.append(self.curses.char_array[i, j])
        message = ''.join(CL)
        self.curses.put_message(0, 1, message)        
        self.curses.put_message(1, 9, 'abcdefghijklmnopqrstuvwxyz' ,auto=True, align='left', box_x=1,box_y=8, box_width=8, box_height=6)
        self.curses.put_char(0, 5, 'š')
        self.curses.put_char(1, 5, 'š'.upper())
        
    def show_all_colors(self):
        color_num = len(colornames.keys())
        for i in range(color_num):
            y = int(np.floor(i / self.curses.win_width)) + 17
            x = i - int(int(np.floor(i / self.curses.win_width)) * self.curses.win_width)
            color = list(colornames.keys())[i]
            self.curses.put_char(x, y, char='█', foreground=color, background='transparent')