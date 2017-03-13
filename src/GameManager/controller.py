import pygame

class Controller():
    def __init__(self, curses, enable=True, is_blocked=True):
        self.curses = curses
        self.enable = enable
        self.is_blocked = is_blocked
    
    def initialization(self):
        pass
    
    def update(self):
        pass

class MouseController(Controller):
    def __init__(self, curses, x=0, y=0, enable=True, is_blocked=True):
        super(MouseController, self).__init__(curses, enable, is_blocked)
        self.x = x
        self.y = y
        self.initialization()
    
    def initialization(self):
        self.is_mouse_recorded = False
        self.mouse_pos = (self.x, self.y)
    
    def update(self):
        if self.enable:
            self.update_mouse()
    
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

class KeyboardController(Controller):
    def __init__(self, curses, enable=True, is_blocked=True):
        super(KeyboardController, self).__init__(curses, enable, is_blocked)
        self.initialization()
        
    def initialization(self):
        self.key_blocked = True
    
    def update(self, event):
        if self.enable:
            self.update_keyboard(event)
    
    def update_keyboard(self, event):  
        self.pressed = None
        if self.is_blocked:            
            if event.type == pygame.KEYDOWN and self.key_blocked:
                self.pressed = pygame.key.get_pressed()
                self.key_blocked = False
            
            if event.type == pygame.KEYUP:
                self.key_blocked = True
        else:
            if event.type == pygame.KEYDOWN:
                self.pressed = pygame.key.get_pressed()                