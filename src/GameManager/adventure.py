class Adventure():
    
    def __init__(self, curses):
        self.curses = curses
        self.initialization()
    
    def initialization(self):
        self.is_init = False
        self.enable = False
        self.key_block = True
        self.mouse_effect={}
    
    def init(self):
        # Initial setting
        
        # Set control flag
        self.is_init = True
        self.enable = True
    
    def update(self, event):
        # Gameloop
        
        # Mouse event
        if len(self.mouse_effect) != 0:
            self.curses.set_cell(self.mouse_pos[0], self.mouse_pos[1], self.mouse_effect)
        
        self.mouse_pos = self.curses.get_mouse_pos()
        self.mouse_effect = self.curses.get_cell(self.mouse_pos[0], self.mouse_pos[1]).copy()
        
        self.curses.get_cell(self.mouse_pos[0], self.mouse_pos[1])['foreground'] = 'maroon'
        self.curses.get_cell(self.mouse_pos[0], self.mouse_pos[1])['background'] = 'yellow'
        
        # Keyboard events
                
        return self.enable
        