class SubScreen():
    def __init__(self, x, y, width, height, curses):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.curses = curses
    
    def put_char(self, x, y, char=' ', foreground='white', background='trans'):
        if x < self.width and x >= self.x and y < self.height and y >= self.y:
            self.curses.put_char(self.x + x, self.y + y, char, foreground, background)
        else:
            raise ValueError('Error: Out of SubScreen boundary.')
    
    def put_message(self, x, y , message, foreground='white', background='trans', auto=True, align='left'):
        self.curses.put_message(self.x + x, self.y + y , message, foreground, background, auto, align, box_x=self.x, box_y=self.y, box_width=self.width, box_height=self.height)
        
    def fill_char(self, char=' ', foreground='white', background='trans'):
        for i in range(self.x, self.x + self.width):
            for j in range(self.y, self.y + self.height):
                self.curses.put_char(i, j, char, foreground, background)