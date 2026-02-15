from src.game import Game, draw_status
import utilities

class PlayScreen():
    def __init__(self, app):
        self.app = app
        
    def update(self, input_state):
        if utilities.game.player.lives < 0:
            utilities.game.play_sound("over")
            from src.screens.game_over import GameOverScreen
            game_over_screen = GameOverScreen(self.app)
            self.app.change_screen(game_over_screen)
        else:
            utilities.game.update(input_state)

    def draw(self, screen):
        utilities.game.draw(screen)
        draw_status(screen)