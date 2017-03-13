import pygame
from PYGUSES.pyguses.form import Frame, Rect
from GameManager.menu import Menu

class Adventure():
    
    def __init__(self, curses, mouse_controller):
        self.curses = curses
        self.mouse_controller = mouse_controller
        self.initialization()
    
    def initialization(self):
        self.is_init = False
        self.enable = False
        self.key_block = True
        self.timer_enable = False
    
    def init(self):
        # Initial setting
        self.window_center = (int(self.curses.win_width/2), int(self.curses.win_height/2))
        self.menu_size = (40,20)
        self.menu_enable = False
        self.menu_init = False
        self.timer = 0
        
        # Draw static area
        Rect(0, 0, 50, 30,self.curses, is_filled=True, char='.', foreground='green', background='trans')
                
        
        # Exit menu
        self.select_dict = {0 : 'Exit to Main Menu', 1 : 'Exit Game'}
        self.menu_size = (40, 20)
        self.menu = Menu(self.curses, self.mouse_controller, int(self.curses.win_width/2 - self.menu_size[0]/2), int(self.curses.win_height/2 - self.menu_size[1]/2), self.menu_size[0], self.menu_size[1], self.select_dict, align='mid', flick_enable=True)
        
        # Draw UI
        bottom_h = 5
        Frame(0, self.curses.win_height - bottom_h, self.curses.win_width, bottom_h, self.curses, style=1, is_filled=True, char=' ', foreground='white', background='trans', frame_foreground='teal', frame_background='trans')
        self.curses.put_message(1, self.curses.win_height - bottom_h+1 , 'HP:', foreground='white', background='trans', auto=True, align='left', box_x=0, box_y=0, box_width=None, box_height=None)
        self.curses.put_message(4, self.curses.win_height - bottom_h+1 , '/solid'*10+'/l3/l2/l1', foreground='red', background='trans', auto=True, align='left', box_x=0, box_y=0, box_width=None, box_height=None)
        
        self.curses.put_message(1, self.curses.win_height - bottom_h+2 , 'MP:', foreground='white', background='trans', auto=True, align='left', box_x=0, box_y=0, box_width=None, box_height=None)
        self.curses.put_message(4, self.curses.win_height - bottom_h+2 , '/solid'*10+'/l3/l2/l1', foreground='blue', background='trans', auto=True, align='left', box_x=0, box_y=0, box_width=None, box_height=None)
        
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

        # Keyboard events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and self.key_block:
                self.menu_enable = not self.menu_enable
                self.key_block = False
                
            if event.key == pygame.K_SPACE and self.key_block:
                if not self.menu_enable:
                    self.timer_enable = not self.timer_enable                
                self.key_block = False
                
        if self.menu_enable:
            self.timer_enable = False
            # Draw menu
            if not self.menu_init:
                self.menu.initialization()
                self.menu_init = True
            flag = self.menu.update(event)
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
            self.curses.put_message(self.curses.win_width-2, self.curses.win_height-1, '/2Hbar'*len(message), foreground='teal', background='trans', auto=True, align='right')
        else:
            self.curses.put_message(self.curses.win_width-2, self.curses.win_height-1, message, foreground='white', background='trans', auto=True, align='right')
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.key_block = True
            if event.key == pygame.K_SPACE:
                self.key_block = True
        
        return self.enable