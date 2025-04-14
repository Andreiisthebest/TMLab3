import pygame


class EventHandler:
    def __init__(self):
        self.quit = False
        self.keys = {}
        self.mouse_pos = (0, 0)
        self.mouse_buttons = {
            "left": False,
            "middle": False,
            "right": False,
            "wheel_up": False,
            "wheel_down": False
        }
        self.events = []
        self.text_input = ""
        self.text_input_active = False

    def process_events(self):
        """Process all pygame events"""
        self.mouse_buttons["wheel_up"] = False
        self.mouse_buttons["wheel_down"] = False
        self.events = []
        self.text_input = ""

        for event in pygame.event.get():
            self.events.append(event)

            if event.type == pygame.QUIT:
                self.quit = True

            # Keyboard events
            elif event.type == pygame.KEYDOWN:
                self.keys[event.key] = True
                if self.text_input_active:
                    if event.key == pygame.K_BACKSPACE:
                        self.text_input = self.text_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.text_input_active = False
                    elif event.unicode.isprintable():
                        self.text_input += event.unicode

            elif event.type == pygame.KEYUP:
                self.keys[event.key] = False

            # Mouse events
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_buttons["left"] = True
                elif event.button == 2:
                    self.mouse_buttons["middle"] = True
                elif event.button == 3:
                    self.mouse_buttons["right"] = True
                elif event.button == 4:
                    self.mouse_buttons["wheel_up"] = True
                elif event.button == 5:
                    self.mouse_buttons["wheel_down"] = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_buttons["left"] = False
                elif event.button == 2:
                    self.mouse_buttons["middle"] = False
                elif event.button == 3:
                    self.mouse_buttons["right"] = False

    def is_key_pressed(self, key):
        """Check if a specific key is pressed"""
        return self.keys.get(key, False)

    def is_key_just_pressed(self, key, previous_keys):
        """Check if a key was just pressed this frame"""
        return self.keys.get(key, False) and not previous_keys.get(key, False)

    def get_mouse_pos(self):
        """Get current mouse position"""
        return self.mouse_pos

    def is_mouse_clicked(self, button="left"):
        """Check if mouse button was clicked"""
        return self.mouse_buttons.get(button, False)

    def start_text_input(self):
        """Start capturing text input"""
        self.text_input_active = True
        self.text_input = ""

    def stop_text_input(self):
        """Stop capturing text input"""
        self.text_input_active = False