import pygame
from PYGUSES.pyguses.form import Hline, Frame

class Demo():
    
    def __init__(self, curses):
        self.curses = curses
        self.initialization()
    
    def initialization(self):
        self.is_init = False
        self.enable = False
        self.key_block = True
        self.is_mouse_recorded = False
    
    def init(self):
        # Draw Title
        Hline(0, self.curses.win_width-1, 0, self.curses, char='/solid', foreground='navy', background='trans')
        title = 'Demo: show all characters'
        char_list = self.curses.get_char_list(title)
        for x in range(len(char_list)):
            self.curses.put_char(x, 0, char_list[x], 'yellow', 'navy')
            
        # Draw info
        Hline(0, self.curses.win_width-1, self.curses.win_height-1, self.curses, char='/solid', foreground='navy', background='trans')
        info = '<BACKSPACE>: retrun'
        char_list = self.curses.get_char_list(info)
        for x in range(len(char_list)):
            self.curses.put_char(self.curses.win_width - len(char_list) + x, self.curses.win_height-1, char_list[x], 'yellow', 'navy')
        
        # Demo: show all characters
        self.show_character_sheet()
        
        # Demo form
        Frame(0, 8, 10, 8, self.curses, style=0, is_filled=False, char='/solid', foreground='white', background='trans', frame_foreground='white', frame_background='trans')
        
        # Set control flag
        self.is_init = True
        self.enable = True
    
    def update(self, event):
        # Mouse event
        self.update_mouse()        
        # Keyboard events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE  and self.key_block:
                self.enable = False
                self.key_block = False
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE:
                self.key_block = True
        
        return self.enable
    
    def update_mouse(self):
        # Mouse event
        self.mouse_pos = self.curses.get_mouse_pos()        
        if not self.is_mouse_recorded:
            self.mouse_temp_pos = self.mouse_pos
            self.mouse_temp = self.curses.get_cell(self.mouse_pos[0], self.mouse_pos[1]).copy()
            self.is_mouse_recorded = True
            
        if self.mouse_pos != self.mouse_temp_pos:
            self.curses.set_cell(self.mouse_temp_pos[0], self.mouse_temp_pos[1], self.mouse_temp)
            self.mouse_temp_pos = self.mouse_pos
            self.mouse_temp = self.curses.get_cell(self.mouse_pos[0], self.mouse_pos[1]).copy()
        
        temp = self.curses.get_cell(self.mouse_pos[0], self.mouse_pos[1]).copy()
        temp['foreground'] = 'maroon'
        temp['background'] = 'yellow'
        self.curses.set_cell(self.mouse_pos[0], self.mouse_pos[1], temp)
        
    def show_character_sheet(self):
        CL=[]
        for i in range(self.curses.char_array.shape[0]):
            for j in range(self.curses.char_array.shape[1]):
                CL.append(self.curses.char_array[i, j])
        message = ''.join(CL)
        self.curses.put_message(0, 1, message)        
        self.curses.put_message(1, 9, 'abcdefghijklmnopqrstuvwxyz' ,auto=True, align='left', box_x=1,box_y=8, box_width=8, box_height=6)
    