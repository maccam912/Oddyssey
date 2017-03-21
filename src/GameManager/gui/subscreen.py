import numpy as np

class SubScreen():
    def __init__(self, x, y, width, height, curses):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.curses = curses
    
    def put_char(self, x, y, char=' ', foreground='white', background='transparent'):
        if x < self.width and x >= self.x and y < self.height and y >= self.y:
            self.curses.put_char(self.x + x, self.y + y, char, foreground, background)
        else:
            raise ValueError('Error: Out of SubScreen boundary.')
    
    def put_message(self, x, y , message, foreground='white', background='transparent', auto=True, align='left'):
        self.curses.put_message(self.x + x, self.y + y , message, foreground, background, auto, align, box_x=self.x, box_y=self.y, box_width=self.width, box_height=self.height)
        
    def fill_char(self, char=' ', foreground='white', background='transparent'):
        for i in range(self.x, self.x + self.width):
            for j in range(self.y, self.y + self.height):
                self.curses.put_char(i, j, char, foreground, background)                

class MessageScreen(SubScreen):
    def __init__(self, x, y, width, height, curses):
        super(MessageScreen, self).__init__(x, y, width, height, curses)
        self.initialization()
        
    def initialization(self):
        self.message_id = 1
        self.message_size = self.height
        self.message_storage = ['']*self.message_size
        self.color_storage = ['transparent']*self.message_size
        self.idx_storage = ['']*self.message_size
    
    def add_message(self, message, color='white'):
        idx = '[%d] '%(self.message_id)
        message = message
        self.message_id += 1
        self.message_storage.append(message)
        self.color_storage.append(color)
        self.idx_storage.append(idx)
        
        self.message_storage.pop(0)
        self.color_storage.pop(0)
        self.idx_storage.pop(0)
        
    def draw(self):
        self.fill_char()
        for i in range(len(self.message_storage)):
            self.put_message(0, i, self.idx_storage[i], foreground='white', background='transparent', auto=True, align='left')
            self.put_message(len(self.idx_storage[i]), i , self.message_storage[i], foreground=self.color_storage[i], background='transparent', auto=True, align='left')

class PlayerInfoScreen(SubScreen):
    def __init__(self, x, y, width, height, curses, player):
        super(PlayerInfoScreen, self).__init__(x, y, width, height, curses)
        self.player = player
        self.initialization()
        
    def initialization(self):
        self.full_health_bar_length = 15
        self.draw()
    
    def draw(self):
        # Draw background
        self.fill_char(char='/solid', foreground='peru', background='transparent')
        # Draw HP bar
        health = self.player.current_health
        interval = self.player.health / self.full_health_bar_length / 3
        level = int(np.ceil(health / interval))
        
        health_title = 'HP '
        if level % 3 == 0:
            remainder = ''
        else:
            remainder = '/l%d' % (level % 3)
        health_message = '/solid' * int((level - level%3)/3) + remainder
        self.put_message(0, 0, health_title, foreground='red', background='peru', auto=True, align='left')
        self.put_message(len(health_title), 0, ' '*self.full_health_bar_length, foreground='red', background='transparent', auto=True, align='left')
        self.put_message(len(health_title), 0, health_message, foreground='red', background='transparent', auto=True, align='left')
        