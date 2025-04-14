import pygame
from config import UI_COLOR, UI_ACCENT, WHITE, GREEN, SCREEN_WIDTH, SCREEN_HEIGHT


class MenuScene:
    def __init__(self):
        self.buttons = []
        self.title_font = None
        self.button_font = None
        self.selected_button = 0

    def on_enter(self):
        # Initialize fonts
        self.title_font = pygame.font.Font(None, 72)
        self.button_font = pygame.font.Font(None, 48)

        # Create menu buttons
        button_width = 300
        button_height = 60
        start_x = SCREEN_WIDTH // 2 - button_width // 2

        self.buttons = [
            {"rect": pygame.Rect(start_x, 250, button_width, button_height), "text": "Play", "action": "play"},
            {"rect": pygame.Rect(start_x, 330, button_width, button_height), "text": "Load Game", "action": "load"},
            {"rect": pygame.Rect(start_x, 410, button_width, button_height), "text": "Settings", "action": "settings"},
            {"rect": pygame.Rect(start_x, 490, button_width, button_height), "text": "Quit", "action": "quit"}
        ]

    def update(self, dt):
        # Handle keyboard navigation
        events = self.game.event_handler.events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_button = (self.selected_button + 1) % len(self.buttons)
                elif event.key == pygame.K_UP:
                    self.selected_button = (self.selected_button - 1) % len(self.buttons)
                elif event.key == pygame.K_RETURN:
                    self.handle_action(self.buttons[self.selected_button]["action"])

            # Mouse selection
            elif event.type == pygame.MOUSEMOTION:
                for i, button in enumerate(self.buttons):
                    if button["rect"].collidepoint(event.pos):
                        self.selected_button = i

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:
                    if button["rect"].collidepoint(event.pos):
                        self.handle_action(button["action"])

    def handle_action(self, action):
        if action == "play":
            self.game.change_scene("gameplay", level=self.game.player_data["current_level"])
        elif action == "load":
            # Implement load game functionality
            pass
        elif action == "settings":
            # Implement settings menu
            pass
        elif action == "quit":
            self.game.event_handler.quit = True

    def render(self, renderer):
        # Draw title
        title_text = self.title_font.render("Rail Building Tycoon", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        renderer.draw_text_surface(title_text, title_rect)

        # Draw buttons
        for i, button in enumerate(self.buttons):
            color = UI_ACCENT if i == self.selected_button else UI_COLOR
            renderer.draw_rect(color, button["rect"], border_radius=10)

            text_surf = self.button_font.render(button["text"], True, WHITE)
            text_rect = text_surf.get_rect(center=button["rect"].center)
            renderer.draw_text_surface(text_surf, text_rect)