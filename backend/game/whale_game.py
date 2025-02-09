# Le jeu existant de la baleine, déplacé depuis main.py 
import pygame
import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from game.base_game import BaseGame

class WhaleGame(BaseGame):
    def __init__(self):
        super().__init__("NETTOIE L'OCÉAN - 2040")
        
        # Configuration spécifique à la baleine
        
        self.player = {
            'x': self.width // 2,
            'y': self.height - 80,
            'width': 80,
            'height': 40,
            'speed': 6
        }
        
        self.wastes = []
        self.waste_speed = 4
        self.spawn_timer = 0
        self.spawn_delay = 30
        self.score = 0
        
    def spawn_waste(self):
        waste = {
            'x': random.randint(0, self.width - 30),
            'y': -30,
            'width': 30,
            'height': 30
        }
        self.wastes.append(waste)

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
            
        # Spawn et mise à jour des déchets
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_waste()
            self.spawn_timer = 0

        for waste in self.wastes[:]:
            waste['y'] += self.waste_speed
            if (waste['y'] + waste['height'] > self.player['y'] and
                waste['x'] < self.player['x'] + self.player['width'] and
                waste['x'] + waste['width'] > self.player['x']):
                self.wastes.remove(waste)
                self.score += 10

    def render(self):
        self.screen.fill((0, 0, 50))  # Fond bleu foncé
        
        # Dessiner la baleine
        pygame.draw.ellipse(self.screen, (0, 100, 255),
                          (self.player['x'], self.player['y'],
                           self.player['width'], self.player['height']))
        
        # Dessiner les déchets
        for waste in self.wastes:
            pygame.draw.rect(self.screen, (255, 0, 0),
                           (waste['x'], waste['y'],
                            waste['width'], waste['height']))
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    game = WhaleGame()
    game.run() 