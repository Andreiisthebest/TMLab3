import pygame
from config import WHITE, GREEN, RED, SCREEN_WIDTH, SCREEN_HEIGHT


class GameOverScene:
    def __init__(self):
        self.font_large = None
        self.font_medium = None
        self.victory = False

    def on_enter(self, victory=False):
        self.victory = victory
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)

    def update(self, dt):
        if self.game.event_handler.keys.get(pygame.K_RETURN, False):
            self.game.change_scene("menu")

    def render(self, renderer):
        if self.victory:
            # Victory screen
            text = self.font_large.render("Level Completed!", True, GREEN)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            renderer.draw_text(text, text_rect)

            next_text = self.font_medium.render("Press Enter to continue", True, WHITE)
            next_rect = next_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            renderer.draw_text(next_text, next_rect)
        else:
            # Game over screen (can be used for failure cases)
            text = self.font_large.render("Game Over", True, RED)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            renderer.draw_text(text, text_rect)

            retry_text = self.font_medium.render("Press Enter to retry", True, WHITE)
            retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            renderer.draw_text(retry_text, retry_rect)