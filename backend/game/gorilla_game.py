import pygame
import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from game.base_game import BaseGame

class GorillaGame(BaseGame):
    def __init__(self):
        super().__init__("GORILLE DIMENSIONNEL - 2040")
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        # Configuration spécifique au gorille
        self.player = {
            'x': self.width // 2,
            'y': self.height - 100,
            'width': 80,
            'height': 100,
            'speed': 5,
            'jumping': False,
            'jump_power': 15,
            'gravity': 0.8,
            'velocity': 0
        }
        
        self.running = True
        self.clock = pygame.time.Clock()
        self.score = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.player['jumping']:
                    self.player['jumping'] = True
                    self.player['velocity'] = -self.player['jump_power']

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player['x'] -= self.player['speed']
        if keys[pygame.K_RIGHT]:
            self.player['x'] += self.player['speed']
            
        # Gestion du saut
        if self.player['jumping']:
            self.player['y'] += self.player['velocity']
            self.player['velocity'] += self.player['gravity']
            
            if self.player['y'] >= self.height - 100:
                self.player['y'] = self.height - 100
                self.player['jumping'] = False
                self.player['velocity'] = 0

    def render(self):
        self.screen.fill((100, 50, 50))  # Fond rouge foncé
        
        # Dessiner le gorille
        pygame.draw.rect(self.screen, (139, 69, 19),  # Marron
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
    game = GorillaGame()
    game.run() 