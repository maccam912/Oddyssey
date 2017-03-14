import pygame
import random
from PYGUSES.pyguses.curses import Flicker
from PYGUSES.pyguses.form import Hline, Frame

class Menu():
    
    def __init__(self, curses, mouse_controller, keyboard_controller, x, y, width, height, select_dict, align='mid', flick_enable=True):
        self.curses = curses
        self.mouse_controller = mouse_controller
        self.keyboard_controller = keyboard_controller
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.select_dict = select_dict
        self.align = align
        self.flick_enable = flick_enable
    
    def initialization(self):
        self.sel_ind = 0
        self.window_center = (int(self.curses.win_width/2), int(self.curses.win_height/2))
        self.enable = True
        
        self.draw_frame()
        self.draw_selection()
        self.draw_select_indicator()
        if self.flick_enable:
            self.flicker = Flicker(curses=self.curses, flick_type=1, interval=500)        
        
        
    def draw_frame(self, style=0, title=None):
        if self.mouse_controller.mouse_pos[0] >= self.x and self.mouse_controller.mouse_pos[0] < self.x + self.width and self.mouse_controller.mouse_pos[1] >= self.y and self.mouse_controller.mouse_pos[1] < self.y + self.height:
            self.curses.set_cell(self.mouse_controller.mouse_pos[0], self.mouse_controller.mouse_pos[1], self.mouse_controller.mouse_temp)
            self.mouse_controller.is_mouse_recorded = False
        self.menu_sec = self.curses.get_cell_section(self.x, self.y, self.width, self.height).copy()
        # Draw menu frame
        Frame(self.x, self.y, self.width, self.height, self.curses, style=style, is_filled=True, char=' ', foreground='white', background='trans', frame_foreground='white', frame_background='trans')
        # Main Menu
        if title != None:
            self.curses.put_message(self.window_center[0], self.window_center[1] - int(self.height/2), title, foreground='trans', background='white', auto=True, align='mid')
    
    def exit_menu(self):
        self.curses.set_cell_section(self.x, self.y, self.menu_sec)
        if self.mouse_controller.mouse_pos[0] >= self.x and self.mouse_controller.mouse_pos[0] < self.x + self.width and self.mouse_controller.mouse_pos[1] >= self.y and self.mouse_controller.mouse_pos[1] < self.y + self.height:
            self.mouse_controller.mouse_temp = self.curses.get_cell(self.mouse_controller.mouse_pos[0], self.mouse_controller.mouse_pos[1]).copy()
    
    def draw_selection(self, ind=None):
        if self.align == 'mid':
            label_x = self.window_center[0]
            label_align = 'mid'
        
        if ind == None:
            # Selections
            for i in range(len(self.select_dict.keys())):
                message = self.select_dict[i]
                self.curses.put_message(label_x, self.window_center[1] - int(self.height/2) + (i + 1) * int(self.height/(len(self.select_dict.keys())+1)), message, foreground='white', background='trans', auto=True, align=label_align)
        else:
            message = ' '*2 + self.select_dict[ind] + ' '*2
            self.curses.put_message(label_x, self.window_center[1] - int(self.height/2) + (ind + 1) * int(self.height/(len(self.select_dict.keys())+1)), message, foreground='white', background='trans', auto=True, align=label_align)
    
    def draw_select_indicator(self):
        message = ' ' + self.select_dict[self.sel_ind] + ' '
        char_list = self.curses.get_char_list(message)
        # Coordinates
        if self.align == 'mid':
            label_x = self.window_center[0] - int(len(char_list)/2)
            label_y = self.window_center[1] - int(self.height/2) + (self.sel_ind + 1) * int(self.height/(len(self.select_dict.keys())+1))
        # Draw selected
        self.curses.put_char(label_x -1, label_y, '/Right', 'white', 'trans')
        self.curses.put_char(label_x + len(char_list), label_y, '/Left', 'white', 'trans')
    
    def update(self):
        # Keyboard event
        flag = self.update_keyboard()
        # Update flicker handler
        if self.flick_enable:
            self.flicker.update()
        self.refresh_selected()        
        return flag
    
    def update_keyboard(self):
        flag = None
        if self.keyboard_controller.pressed != None:
            if self.keyboard_controller.pressed[pygame.K_w] or self.keyboard_controller.pressed[pygame.K_UP]:
                self.draw_selection(ind=self.sel_ind)
                self.sel_ind -= 1
                self.sel_ind %= len(self.select_dict.keys())
                self.draw_select_indicator()
            if self.keyboard_controller.pressed[pygame.K_x] or self.keyboard_controller.pressed[pygame.K_DOWN]:
                self.draw_selection(ind=self.sel_ind)
                self.sel_ind += 1
                self.sel_ind %= len(self.select_dict.keys())
                self.draw_select_indicator()
            if self.keyboard_controller.pressed[pygame.K_s] or self.keyboard_controller.pressed[ pygame.K_KP_ENTER] or self.keyboard_controller.pressed[ pygame.K_RETURN]:
                flag = self.select()
        return flag
    
    def select(self):
        self.enable = False
        return self.select_dict[self.sel_ind]
    
    def refresh_selected(self):
        message = self.select_dict[self.sel_ind]
        char_list = self.curses.get_char_list(message)
        # Coordinates
        if self.align == 'mid':
            label_x = self.window_center[0] - int(len(char_list)/2)
            label_y = self.window_center[1] - int(self.height/2) + (self.sel_ind + 1) * int(self.height/(len(self.select_dict.keys())+1))
        for x in range(len(char_list)):
            self.curses.put_char(label_x + x, label_y, char_list[x], 'red', 'trans')
            
        if self.flick_enable:
            for x in range(label_x, label_x + len(char_list)):
                self.flicker.refresh(x, label_y)
            
class MainMenu(Menu):
    def __init__(self, curses, mouse_controller, keyboard_controller, x, y, width, height, select_dict, align='mid', flick_enable=False):
        super(MainMenu, self).__init__(curses, mouse_controller, keyboard_controller, x, y, width, height, select_dict, align, flick_enable)
        self.initialization()
    
    def initialization(self):
        pygame.mouse.set_visible(False)
        
        self.sel_ind = 0
        self.mouse_pos = (0, 0)
        self.window_center = (int(self.curses.win_width/2), int(self.curses.win_height/2))
        self.key_block = True
        self.enable = True
        self.is_mouse_recorded = False
        
        self.draw_UI()
                
        self.draw_frame(title=' Main Menu ')
        self.draw_selection()
        self.draw_select_indicator()
        if self.flick_enable:
            self.flicker = Flicker(curses=self.curses, flick_type=1, interval=500)
            
    def draw_UI(self):
        # Draw background
        self.draw_background()
        # Selection info.
        Hline(0, self.curses.win_width-1, self.curses.win_height-1, self.curses, char='/solid', foreground='navy', background='trans')
        message = '</up/w>: move up, </down/x>: move down, <s/Enter>: select, <ESC>: quit'
        self.curses.put_message(self.curses.win_width-1, self.curses.win_height-1, message, foreground='yellow', background='navy', auto=True, align='right')
    
    def draw_background(self):
        # Draw background
        for i in range(self.curses.win_height - 1):
            for j in range(self.curses.win_width):
                h_ind = [0,11,12,13][random.randint(0, 3)]
                w_ind = random.randint(0, self.curses.image_array.shape[0] - 1)
                self.curses.put_char(j, i, self.curses.char_array[h_ind, w_ind], 'gray', 'trans')