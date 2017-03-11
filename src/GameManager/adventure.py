import pygame
from PYGUSES.pyguses.form import Frame

class Adventure():
    
    def __init__(self, curses):
        self.curses = curses
        self.initialization()
    
    def initialization(self):
        self.is_init = False
        self.enable = False
        self.key_block = True
        self.timer_enable = False
        self.is_mouse_recorded = False
    
    def init(self):
        # Initial setting
        self.window_center = (int(self.curses.win_width/2), int(self.curses.win_height/2))
        self.menu_size = (40,20)
        self.menu_enable = True
        self.timer = 0
        
        # Draw UI
#        bottom_h = 5
#        Frame(0, self.curses.win_height - bottom_h, self.curses.win_width, bottom_h, self.curses, style=1, is_filled=True, char=' ', foreground='white', background='trans', frame_foreground='teal', frame_background='trans')
#        self.curses.put_message(1, self.curses.win_height - bottom_h+1 , 'HP:', foreground='white', background='trans', auto=True, align='left', box_x=0, box_y=0, box_width=None, box_height=None)
#        self.curses.put_message(4, self.curses.win_height - bottom_h+1 , '/solid'*10+'/l3/l2/l1', foreground='red', background='trans', auto=True, align='left', box_x=0, box_y=0, box_width=None, box_height=None)
#        
#        self.curses.put_message(1, self.curses.win_height - bottom_h+2 , 'MP:', foreground='white', background='trans', auto=True, align='left', box_x=0, box_y=0, box_width=None, box_height=None)
#        self.curses.put_message(4, self.curses.win_height - bottom_h+2 , '/solid'*10+'/l3/l2/l1', foreground='blue', background='trans', auto=True, align='left', box_x=0, box_y=0, box_width=None, box_height=None)
        
        
        # Set control flag
        self.is_init = True
        self.enable = True
        self.timer_enable = True
    
    def update(self, event):
        # Gameloop
        if self.timer_enable:
                
            # Draw counter
            self.timer += 1
            message = '%04d' %self.timer
            self.curses.put_message(3, 0 , message[-4:], foreground='white', background='trans', auto=True, align='right', box_x=0, box_y=0, box_width=None, box_height=None)
        # Mouse event
        self.update_mouse()     
        # Keyboard events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and self.key_block:
                if self.menu_enable:
                    self.timer_enable = False
                    # Draw menu
                    self.draw_menu()
                else:
                    self.timer_enable = True
                    # Return cells in menu section
                    self.exit_menu()
                    
                self.menu_enable = not self.menu_enable
                self.key_block = False            
            
            if event.key == pygame.K_SPACE and self.key_block:
                if self.menu_enable:
                    self.timer_enable = not self.timer_enable                
                self.key_block = False 
        
        # Draw timer state
        message = 'PULSED'
        if self.timer_enable:
            self.curses.put_message(self.curses.win_width-2, self.curses.win_height-1, '/2Hbar'*len(message), foreground='teal', background='trans', auto=True, align='right')
        else:
            self.curses.put_message(self.curses.win_width-2, self.curses.win_height-1, message, foreground='white', background='trans', auto=True, align='right')
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.key_block = True
            if event.key == pygame.K_SPACE:
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
        
    def draw_menu(self):
        # Draw menu frame
        menu_x = self.window_center[0] - int(self.menu_size[0]/2)
        menu_y = self.window_center[1] - int(self.menu_size[1]/2)
        x = self.mouse_pos[0]
        y = self.mouse_pos[1]
        if x >= menu_x and x < menu_x + self.menu_size[0] and y >= menu_y and y < menu_y + self.menu_size[1]:
            self.curses.set_cell(x, y, self.mouse_temp)
            self.is_mouse_recorded = False
        self.menu_sec = self.curses.get_cell_section(menu_x, menu_y, self.menu_size[0], self.menu_size[1]).copy()
        Frame(self.window_center[0] - int(self.menu_size[0]/2), self.window_center[1] - int(self.menu_size[1]/2), self.menu_size[0], self.menu_size[1], self.curses, style=1, is_filled=True, char=' ', foreground='white', background='trans', frame_foreground='white', frame_background='trans')
        
    def exit_menu(self):
        menu_x = self.window_center[0] - int(self.menu_size[0]/2)
        menu_y = self.window_center[1] - int(self.menu_size[1]/2)
        x = self.mouse_pos[0]
        y = self.mouse_pos[1]
        self.curses.set_cell_section(self.window_center[0] - int(self.menu_size[0]/2), self.window_center[1] - int(self.menu_size[1]/2), self.menu_sec)
        if x >= menu_x and x < menu_x + self.menu_size[0] and y >= menu_y and y < menu_y + self.menu_size[1]:
            self.mouse_temp = self.curses.get_cell(self.mouse_pos[0],self.mouse_pos[1]).copy()
            