from src.game import Game, draw_status
import utilities

class GameOverScreen():
    def __init__(self, app):
        self.app = app
    
    def update(self, input_state):
        if input_state.fire_pressed:
            from src.screens.menu import MenuScreen
            menu_screen = MenuScreen(self.app)
            self.app.change_screen(menu_screen)
            utilities.game = Game()
    
    def draw(self, screen):
        utilities.game.draw(screen)
        draw_status(screen)
        screen.blit("over", (0, 0))