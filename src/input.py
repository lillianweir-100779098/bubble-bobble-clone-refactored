from pgzero.builtins import keyboard

class InputState:
    def __init__(self):
        self.left = False
        self.right = False
        self.jump_pressed = False
        self.fire_pressed = False
        self.fire_held = False

        self._prev_space = False
        self._prev_up = False
    
    def get_keyboard(self):
        space = keyboard.space
        up = keyboard.up
        
        self.fire_pressed = space and not self._prev_space
        self.jump_pressed = up and not self._prev_up
        
        self.left = keyboard.left
        self.right = keyboard.right
        self.fire_held = space
        
        self._prev_space = space
        self._prev_up = up
        
        return self