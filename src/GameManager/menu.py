import pygame
import random
from PYGUSES.pyguses.curses import Flicker
from PYGUSES.pyguses.form import Hline, Frame

class Menu():
    pass

class MainMenu():
    def __init__(self, curses, width, height, select_dict={0 : 'Demo', 1 : 'Quit'}):
        self.curses = curses
        self.width = width
        self.height = height
        self.select_dict = select_dict
        self.initialization()
    
    def initialization(self):
        self.window_center = (int(self.curses.win_width/2), int(self.curses.win_height/2))
        
        # Generate flicker
        self.flicker = Flicker(curses=self.curses, flick_type=1, interval=500)
        
        # Draw background
        self.draw_background()
        # Draw menu frame
        self.draw_frame()        
        # Menu selections
        self.sel_ind = 0
        self.draw_selection()
        self.draw_select_indicator()
        # Selection info.
        Hline(0, self.curses.win_width-1, self.curses.win_height-1, self.curses, char='/solid', foreground='navy', background='trans')
        message = '</up/w>: move up, </down/x>: move down, <s/Enter>: select, <ESC>: quit'
        self.curses.put_message(self.curses.win_width-1, self.curses.win_height-1, message, foreground='yellow', background='navy', auto=True, align='right')
           
        # Control flags
        pygame.mouse.set_visible(False)
        self.key_block = True
        self.enable = True
        self.mouse_pos = (0, 0)
        self.is_mouse_recorded = False
    
    def draw_background(self):
        # Draw background
        for i in range(self.curses.win_height - 1):
            for j in range(self.curses.win_width):
                h_ind = [0,11,12,13][random.randint(0, 3)]
                w_ind = random.randint(0, self.curses.image_array.shape[0] - 1)
                self.curses.put_char(j, i, self.curses.char_array[h_ind, w_ind], 'gray', 'trans')
    
    def draw_frame(self):
        # Draw menu frame
        Frame(self.window_center[0] - int(self.width/2), self.window_center[1] - int(self.height/2), self.width, self.height, self.curses, style=1, is_filled=True, char=' ', foreground='white', background='trans', frame_foreground='white', frame_background='trans')
        # Main Menu
        message = ' Main Menu '
        self.curses.put_message(self.window_center[0], self.window_center[1] - int(self.height/2), message, foreground='trans', background='white', auto=True, align='mid')
        
    def draw_selection(self, ind=None):
        if ind == None:
            # Selections
            for i in range(len(self.select_dict.keys())):
                message = self.select_dict[i]
                self.curses.put_message(self.window_center[0], self.window_center[1] - int(self.height/2) + (i + 1) * int(self.height/(len(self.select_dict.keys())+1)), message, foreground='white', background='trans', auto=True, align='mid')
        else:
            message = ' '*2 + self.select_dict[ind] + ' '*2
            self.curses.put_message(self.window_center[0], self.window_center[1] - int(self.height/2) + (ind + 1) * int(self.height/(len(self.select_dict.keys())+1)), message, foreground='white', background='trans', auto=True, align='mid')
   
    def selection(self, event):
        flag = None
        
        # Mouse event
        self.update_mouse()
        
        # Keyboard events
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_w or event.key == pygame.K_UP) and self.key_block:
                self.draw_selection(ind=self.sel_ind)
                self.sel_ind -= 1
                self.sel_ind %= len(self.select_dict.keys())
                self.draw_select_indicator()
                self.key_block = False
            if (event.key == pygame.K_x or event.key == pygame.K_DOWN) and self.key_block :
                self.draw_selection(ind=self.sel_ind)
                self.sel_ind += 1
                self.sel_ind %= len(self.select_dict.keys())
                self.draw_select_indicator()
                self.key_block = False
            if (event.key == pygame.K_s  or event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN) and self.key_block :
                flag = self.select()
                self.key_block = False
                
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_w or event.key == pygame.K_UP):
                self.key_block = True
            if (event.key == pygame.K_x or event.key == pygame.K_DOWN):
                self.key_block = True
            if (event.key == pygame.K_s  or event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN):
                self.key_block = True
        
        # Update flicker handler
        self.flicker.update()
        self.refresh_selected()
        return flag
    
    def draw_select_indicator(self):
        message = ' ' + self.select_dict[self.sel_ind] + ' '
        char_list = self.curses.get_char_list(message)
        # Coordinates
        label_x = self.window_center[0] - int(len(char_list)/2)
        label_y = self.window_center[1] - int(self.height/2) + (self.sel_ind + 1) * int(self.height/(len(self.select_dict.keys())+1))
        # Draw selected
        self.curses.put_char(label_x -1, label_y, '/Right', 'white', 'trans')
        self.curses.put_char(label_x + len(char_list), label_y, '/Left', 'white', 'trans')
            
    def refresh_selected(self):
        message = self.select_dict[self.sel_ind]
        char_list = self.curses.get_char_list(message)
        # Coordinates
        label_x = self.window_center[0] - int(len(char_list)/2)
        label_y = self.window_center[1] - int(self.height/2) + (self.sel_ind + 1) * int(self.height/(len(self.select_dict.keys())+1))
        
        for x in range(len(char_list)):
            self.curses.put_char(label_x + x, label_y, char_list[x], 'red', 'trans')
        for x in range(label_x, label_x + len(char_list)):
            self.flicker.refresh(x, label_y)
    
    def select(self):
        self.enable = False
        return self.select_dict[self.sel_ind]
    
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