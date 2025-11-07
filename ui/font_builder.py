import pygame

class FontBuilder:
    def __init__(self, font_path):
        print(f"Trying to access file `{font_path}`")
        try:
            with open(font_path, "r"):
                pass
        except FileNotFoundError:
            print("Error: font not found")
            font_path = None

        # Fonts
        self.very_small = pygame.font.Font(font_path, 16)
        self.small = pygame.font.Font(font_path, 24)
        self.medium = pygame.font.Font(font_path, 32)
        self.big = pygame.font.Font(font_path, 48)