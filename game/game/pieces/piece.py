import pygame
import os
import sys

class Piece:
    SIZE = 80

    def __init__(self, row, col, color):
        """
        Base class for all chess pieces.

        Args:
            row (int): Board row position
            col (int): Board column position
            color (str): "white" or "black"
        """
        self.row = row
        self.col = col
        self.color = color

        piece_name = self.__class__.__name__.lower()
        filename = f"{piece_name}_{color}.png"

        # Get the correct path for both development and PyInstaller
        path = self.get_resource_path(filename)
        
        try:
            self.image = pygame.image.load(path)
            self.image = pygame.transform.scale(self.image, (self.SIZE, self.SIZE))
        except FileNotFoundError:
            print(f"ERROR: Could not find image at {path}")
            # Create a fallback colored rectangle
            self.image = pygame.Surface((self.SIZE, self.SIZE))
            self.image.fill((255, 0, 255))  # Magenta = missing

    def get_resource_path(self, filename):
        """Get absolute path to resource, works for dev and for PyInstaller"""
        # Check if we're running as a PyInstaller bundle
        if getattr(sys, 'frozen', False):
            # Running in a PyInstaller bundle
            base_path = sys._MEIPASS
            print(f"PyInstaller mode - base path: {base_path}")
        else:
            # Running in normal development mode
            # Go up from game/pieces/ to project root (4 levels)
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            print(f"Development mode - base path: {base_path}")
        
        # Construct the full path to the image
        full_path = os.path.join(base_path, "assets", "pieces", filename)
        print(f"Looking for image: {full_path}")
        print(f"File exists: {os.path.exists(full_path)}")
        
        return full_path

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))