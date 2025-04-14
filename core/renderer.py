# core/renderer.py
import pygame


class Renderer:
    """Handles rendering to the screen."""

    def __init__(self, screen):
        self.screen = screen
        self.fonts = {}

    def clear(self, color=(0, 0, 0)):
        """Clear the screen with a color."""
        self.screen.fill(color)

    def draw_rect(self, rect, color, width=0):
        """Draw a rectangle."""
        pygame.draw.rect(self.screen, color, rect, width)

    def draw_circle(self, center, radius, color, width=0):
        """Draw a circle."""
        pygame.draw.circle(self.screen, color, center, radius, width)

    def draw_line(self, start_pos, end_pos, color, width=1):
        """Draw a line."""
        pygame.draw.line(self.screen, color, start_pos, end_pos, width)

    def draw_text(self, text, font_size, color, position, centered=False):
        """Draw text on the screen."""
        font_key = f"size_{font_size}"
        if font_key not in self.fonts:
            self.fonts[font_key] = pygame.font.Font(None, font_size)

        font = self.fonts[font_key]
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()

        if centered:
            text_rect.center = position
        else:
            text_rect.topleft = position

        self.screen.blit(text_surface, text_rect)
        return text_rect

    def draw_image(self, image, position, centered=False):
        """Draw an image on the screen."""
        rect = image.get_rect()
        if centered:
            rect.center = position
        else:
            rect.topleft = position
        self.screen.blit(image, rect)
        return rect
