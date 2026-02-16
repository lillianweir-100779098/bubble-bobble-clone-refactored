from src.game import Game, draw_status, draw_text
import utilities

class PauseScreen():
    def __init__(self, app):
        self.app = app
    
    def update(self, input_state):
        if input_state.esc_pressed:
            from src.screens.play import PlayScreen
            play_screen = PlayScreen(self.app)
            self.app.change_screen(play_screen)
    
    def draw(self, screen):
        utilities.game.draw(screen)
        screen.blit("dark", (0, 0))
        draw_text(screen, "PAUSED", 200)
        draw_status(screen)
