import pygame
from config import BACKGROUND_COLOR


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font_cache = {}  # For caching loaded fonts

    def clear(self):
        """Clear the screen with background color"""
        self.screen.fill(BACKGROUND_COLOR)

    def present(self):
        """Update the display"""
        pygame.display.flip()

    def draw_text(self, text, size, color, x, y, font_name=None):
        """Draw text to the screen with optional font caching"""
        font_key = f"{font_name}_{size}" if font_name else f"default_{size}"

        if font_key not in self.font_cache:
            if font_name:
                try:
                    font = pygame.font.Font(f"assets/fonts/{font_name}.ttf", size)
                except:
                    font = pygame.font.SysFont(font_name, size)
            else:
                font = pygame.font.SysFont(None, size)
            self.font_cache[font_key] = font

        text_surface = self.font_cache[font_key].render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def draw_text_surface(self, text_surface, position):
        """Alternative method to draw a pre-rendered text surface"""
        self.screen.blit(text_surface, position)

    def draw_rect(self, color, rect, width=0, border_radius=0):
        """Draw a rectangle with optional border radius"""
        pygame.draw.rect(self.screen, color, rect, width, border_radius)

    def draw_image(self, image, position, area=None, special_flags=0):
        """Draw an image at the specified position"""
        self.screen.blit(image, position, area, special_flags)

    def draw_circle(self, color, center, radius, width=0):
        """Draw a circle"""
        pygame.draw.circle(self.screen, color, center, radius, width)

    def draw_line(self, color, start_pos, end_pos, width=1):
        """Draw a line"""
        pygame.draw.line(self.screen, color, start_pos, end_pos, width)