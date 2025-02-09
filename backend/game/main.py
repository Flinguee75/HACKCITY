import pygame
import random
import sys

class MutationGame:
    def __init__(self, game_type="whale"):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.game_type = game_type
        
        # Titre différent selon le jeu
        titles = {
            "gorilla": "SAUVE LA FORÊT - 2040",
            "horse": "PROTÈGE LE CONGO - 2040",
            "whale": "NETTOIE L'OCÉAN - 2040"
        }
        pygame.display.set_caption(titles.get(game_type, "MUTATION GAME - 2040"))
        
        # Couleurs selon le type de jeu
        self.colors = {
            "gorilla": {"bg": (100, 50, 50), "player": (0, 255, 0)},
            "horse": {"bg": (50, 100, 50), "player": (200, 150, 50)},
            "whale": {"bg": (0, 0, 50), "player": (0, 100, 255)}
        }[game_type]

        # Configuration du joueur selon le type
        player_configs = {
            "gorilla": {"width": 60, "height": 80, "speed": 7},
            "horse": {"width": 70, "height": 50, "speed": 9},
            "whale": {"width": 80, "height": 40, "speed": 6}
        }[game_type]

        self.player_width = player_configs["width"]
        self.player_height = player_configs["height"]
        self.player_speed = player_configs["speed"]
        self.clock = pygame.time.Clock()
        self.running = True

        # Joueur (baleine)
        self.player_x = self.width // 2
        self.player_y = self.height - 80

        # Déchets radioactifs
        self.wastes = []
        self.waste_speed = 4
        self.spawn_timer = 0
        self.spawn_delay = 30

        # Score et texte
        self.score = 0
        self.font = pygame.font.Font(None, 36)

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

        # Mouvement du joueur
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.player_x > 0:
            self.player_x -= self.player_speed
        if keys[pygame.K_RIGHT] and self.player_x < self.width - self.player_width:
            self.player_x += self.player_speed

    def update(self):
        # Spawn des déchets
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_waste()
            self.spawn_timer = 0

        # Mise à jour des déchets
        for waste in self.wastes[:]:
            waste['y'] += self.waste_speed
            
            # Collision avec le joueur
            if (waste['y'] + waste['height'] > self.player_y and
                waste['x'] < self.player_x + self.player_width and
                waste['x'] + waste['width'] > self.player_x):
                self.wastes.remove(waste)
                self.score += 10
                # Augmenter la difficulté
                if self.score % 50 == 0:
                    self.waste_speed += 0.5
                    self.spawn_delay = max(10, self.spawn_delay - 2)

            # Suppression si hors écran
            elif waste['y'] > self.height:
                self.wastes.remove(waste)
                self.score -= 5

    def render(self):
        # Fond personnalisé
        self.screen.fill(self.colors["bg"])
        
        # Rendu du joueur selon le type
        if self.game_type == "whale":
            pygame.draw.ellipse(self.screen, self.colors["player"],
                            (self.player_x, self.player_y,
                             self.player_width, self.player_height))
        elif self.game_type == "horse":
            # Dessin simplifié d'un cheval
            pygame.draw.rect(self.screen, self.colors["player"],
                         (self.player_x, self.player_y,
                          self.player_width, self.player_height))
        else:  # gorilla
            # Dessin simplifié d'un gorille
            pygame.draw.rect(self.screen, self.colors["player"],
                         (self.player_x, self.player_y,
                          self.player_width, self.player_height))
        
        # Déchets radioactifs
        for waste in self.wastes:
            pygame.draw.rect(self.screen, (255, 0, 0),
                           (waste['x'], waste['y'],
                            waste['width'], waste['height']))

        # Score
        score_text = self.font.render(f'Déchets nettoyés: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        # Instructions
        if len(self.wastes) == 0:
            instructions = self.font.render('Guide la baleine avec ← → pour nettoyer l\'océan', 
                                         True, (255, 255, 255))
            self.screen.blit(instructions, (self.width//2 - 250, self.height//2))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

        pygame.quit() 