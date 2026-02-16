class App:
    def __init__(self):
        self.current_screen = None
    
    def change_screen(self, new_screen):
        self.current_screen = new_screen
    
    def update(self, input_state):
        if self.current_screen:
            self.current_screen.update(input_state)

    def draw(self, screen):
        if self.current_screen:
            self.current_screen.draw(screen)