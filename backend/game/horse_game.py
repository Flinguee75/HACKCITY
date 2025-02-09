# Similaire à gorilla_game.py mais avec des mécaniques de course 
import pygame
import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from game.base_game import BaseGame

class HorseGame(BaseGame):
    def __init__(self):
        super().__init__("CHEVAL PHILOSOPHE - 2040")
        
        # Configuration spécifique au cheval
        self.player = {
            'x': self.width // 2,
            'y': self.height - 100,
            'width': 70,
            'height': 50,
            'speed': 9
        }
        
        self.score = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player['x'] -= self.player['speed']
        if keys[pygame.K_RIGHT]:
            self.player['x'] += self.player['speed']

    def render(self):
        self.screen.fill((50, 100, 50))  # Fond vert foncé
        
        # Dessiner le cheval
        pygame.draw.rect(self.screen, (200, 150, 50),
                        (self.player['x'], self.player['y'],
                         self.player['width'], self.player['height']))
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    game = HorseGame()
    game.run() 