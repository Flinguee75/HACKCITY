# Cheval Mutant : Dernier Survivant (Édition 2D Fighter)
import os
import pygame
import random
import math
from enum import Enum


# Initialiser Pygame
pygame.init()


# Constantes du jeu
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
VERT_NÉON = (57, 255, 20)
JAUNE_NÉON = (229, 255, 20)

# Constantes du joueur
VITESSE_JOUEUR = 5
FORCE_SAUT_JOUEUR = -17
GRAVITÉ = 0.8
MAX_CŒURS = 6
assets_dir = os.path.join(os.path.dirname(__file__), "assets")

class ÉtatJeu(Enum):
    MENU = 1
    JOUANT = 2
    PAUSE = 3
    GAME_OVER = 4
    GAGNER = 5  # Ajouter un nouvel état de victoire

class Joueur(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames_animation = []
        self.frames_animation_flippés = []
        self.frame_actuel = 0
        self.timer_animation = 0
        self.délai_animation = 5  # Mettre à jour l'animation tous les 5 ticks de jeu
        
        try:
            # Charger tous les frames d'animation pour le gorille
            for i in range(6):  # gorilla0 à gorilla5
                image_originale = pygame.image.load(os.path.join(assets_dir, f"1c055ac5-8583-4a90-8103-4cc3cec64249-{i}.png")).convert_alpha()
                image_redimensionnée = pygame.transform.scale(image_originale, (150, 150))
                self.frames_animation.append(image_redimensionnée)
                # Créer la version flippée
                image_flippée = pygame.transform.flip(image_redimensionnée, True, False)
                self.frames_animation_flippés.append(image_flippée)
            
            # Définir l'image initiale
            self.image = self.frames_animation[0]
            self.image_idle = self.frames_animation[0]  # Utiliser le premier frame comme idle
            self.image_idle_flippée = self.frames_animation_flippés[0]
        except:
            # Retour à un rectangle blanc si le chargement de l'image échoue
            self.image = pygame.Surface((150, 150))
            self.image.fill(BLANC)
            print("Impossible de charger les images de gorille. Veuillez vous assurer que 1c055ac5-8583-4a90-8103-4cc3cec64249-0.png à 1c055ac5-8583-4a90-8103-4cc3cec64249-5.png sont dans le dossier assets.")
            self.image_idle = self.image
            self.image_idle_flippée = self.image
            self.frames_animation = [self.image]
            self.frames_animation_flippés = [self.image]
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vitesse_y = 0
        self.cœurs = MAX_CŒURS
        self.mètre_spécial = 0
        self.est_sautant = False
        self.facing_right = True
        self.cooldown_attaque = 0
        self.cooldown_spécial = 0
        self.dégâts_attaque = 10
        self.dégâts_spéciaux = 40
        self.timer_invincibilité = 0
        self.vitesse_x = 0  # Ajouter la vitesse horizontale
        self.résistance_contre_coup = 0.8  # Résistance pour ralentir le recul
        self.hitbox = pygame.Rect(0, 0, 80, 50)  # Retour à la taille précédente
        
    def update(self):
        # Vérifier si le jeu est terminé au début de la mise à jour
        if self.cœurs <= 1:
            self.cœurs = 0
            if self.jeu.etat_jeu != ÉtatJeu.GAME_OVER:  # Ne jouer le son que lors de l'entrée dans l'état de game over
                self.jeu.etat_jeu = ÉtatJeu.GAME_OVER
                # Arrêter la musique de fond et jouer le son de game over une fois
                pygame.mixer.music.stop()
                if self.jeu.gameover_sound:
                    self.jeu.gameover_sound.play(0)  # 0 signifie jouer une fois
            return
        
        # Gérer la gravité
        self.vitesse_y += GRAVITÉ
        
        # Déplacer verticalement
        self.rect.y += self.vitesse_y
        
        # Gérer le recul horizontal avec vérifications de limites
        if self.vitesse_x != 0:
            new_x = self.rect.x + self.vitesse_x
            # Garder le joueur dans les limites de l'écran pendant le recul
            if 0 <= new_x <= SCREEN_WIDTH - self.rect.width:
                self.rect.x = new_x
            else:
                # Arrêter le recul s'il pousse le joueur hors des limites
                self.vitesse_x = 0
            self.vitesse_x *= self.résistance_contre_coup
            if abs(self.vitesse_x) < 0.1:
                self.vitesse_x = 0
        
        # Mettre à jour la transparence du joueur en fonction de l'invincibilité
        if self.timer_invincibilité > 0:
            self.image.set_alpha(128)
            self.timer_invincibilité -= 1
        else:
            self.image.set_alpha(255)
        
        # Mettre à jour la position de la hitbox en bas du sprite
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.bottom = self.rect.bottom - 10  # Retour à la position précédente
        
        # Collisions avec les ennemis en utilisant la hitbox au lieu du rectangle complet du sprite
        hits = pygame.sprite.spritecollide(self, self.jeu.enemies, False, 
                                         collided=lambda x, y: y.rect.colliderect(x.hitbox))
        if hits and self.timer_invincibilité <= 0:
            self.cœurs -= 0.5
            self.timer_invincibilité = 60
        
        # Collision avec le sol
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.vitesse_y = 0
            self.est_sautant = False
        
        # Mettre à jour les cooldowns
        if self.cooldown_attaque > 0:
            self.cooldown_attaque -= 1
        if self.cooldown_spécial > 0:
            self.cooldown_spécial -= 1
        
        # Mettre à jour l'animation si en mouvement
        keys = pygame.key.get_pressed()
        is_moving = keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]
        
        if is_moving:
            self.timer_animation += 1
            if self.timer_animation >= self.délai_animation:
                self.timer_animation = 0
                self.frame_actuel = (self.frame_actuel + 1) % len(self.frames_animation)
                if self.facing_right:
                    self.image = self.frames_animation[self.frame_actuel]
                else:
                    self.image = self.frames_animation_flippés[self.frame_actuel]
        else:
            # Utiliser le frame idle quand pas en mouvement
            if self.facing_right:
                self.image = self.image_idle_flippée
            else:
                self.image = self.image_idle

    def attack(self, enemies):
        if self.cooldown_attaque <= 0:
            attack_range = pygame.Rect(
                self.rect.x - 20 if not self.facing_right else self.rect.right,
                self.rect.centery,
                40,
                self.rect.height/2
            )
            for enemy in enemies:
                if attack_range.colliderect(enemy.rect):
                    enemy.take_damage(self.dégâts_attaque)
            self.cooldown_attaque = 20
            
    def special_attack(self, enemies):
        if self.cooldown_spécial <= 0 and self.mètre_spécial >= 50:
            # Plage d'attaque spéciale - également ajustée
            attack_range = pygame.Rect(
                self.rect.x - 40 if not self.facing_right else self.rect.right,
                self.rect.centery - 10,  # Légèrement plus haut que l'attaque normale
                80,  # Réduit de 100
                self.rect.height/2 + 20  # Un peu plus haut que l'attaque normale
            )
            for enemy in enemies:
                if attack_range.colliderect(enemy.rect):
                    enemy.take_damage(self.dégâts_spéciaux)
            self.mètre_spécial = 0
            self.cooldown_spécial = 60

    def move(self, direction):
        new_x = self.rect.x + direction * VITESSE_JOUEUR
        # Garder le joueur dans les limites de l'écran
        if 0 <= new_x <= SCREEN_WIDTH - self.rect.width:
            self.rect.x = new_x
        # Déterminer la direction à laquelle le gorille fait face
        self.facing_right = direction > 0  # Si direction est positive, il fait face à droite
        
    def jump(self):
        if not self.est_sautant:
            self.vitesse_y = FORCE_SAUT_JOUEUR
            self.est_sautant = True
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type):
        super().__init__()
        self.frames_animation = []
        self.frames_animation_flippés = []
        self.frame_actuel = 0
        self.timer_animation = 0
        self.délai_animation = 5  # Mettre à jour l'animation tous les 5 ticks de jeu
        
        try:
            # Charger tous les frames d'animation pour le feu
            for i in range(10):  # fire0 à fire9
                image_originale = pygame.image.load(os.path.join(assets_dir, f"b8ffca12-b021-4c92-9ab7-50a655146262-{i}.png")).convert_alpha()
                image_redimensionnée = pygame.transform.scale(image_originale, (150, 150))
                self.frames_animation.append(image_redimensionnée)
                # Créer la version flippée
                image_flippée = pygame.transform.flip(image_redimensionnée, True, False)
                self.frames_animation_flippés.append(image_flippée)
            
            # Définir l'image initiale
            self.image = self.frames_animation[0]
        except:
            # Retour à un rectangle rouge si le chargement de l'image échoue
            self.image = pygame.Surface((150, 150))
            self.image.fill(ROUGE)
            print("Impossible de charger les images de feu. Veuillez vous assurer que b8ffca12-b021-4c92-9ab7-50a655146262-0.png à b8ffca12-b021-4c92-9ab7-50a655146262-9.png sont dans le dossier assets.")
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vitesse_y = 0
        self.vitesse_x = random.choice([-2, 2])  # Vitesse de déplacement aléatoire
        self.health = 100  # Points de vie de l'ennemi

    def update(self, player):
        # Logique de mouvement de l'ennemi
        self.rect.x += self.vitesse_x
        
        # Changer de direction si l'ennemi atteint le bord de l'écran
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.vitesse_x *= -1  # Inverser la direction
        
        # Mettre à jour l'animation
        self.timer_animation += 1
        if self.timer_animation >= self.délai_animation:
            self.timer_animation = 0
            self.frame_actuel = (self.frame_actuel + 1) % len(self.frames_animation)
            self.image = self.frames_animation[self.frame_actuel]

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()  # Supprimer l'ennemi s'il n'a plus de points de vie
            
    def draw_health_bar(self, screen):
        health_bar_width = 80  # Élargi pour correspondre à la taille plus grande de l'ennemi
        health_bar_height = 5
        health_ratio = self.health / 100
        
        # Centrer la barre de santé au-dessus de l'ennemi
        bar_x = self.rect.centerx - health_bar_width/2
        bar_y = self.rect.y - 20  # Déplacé un peu plus haut au-dessus de l'ennemi
        
        # Fond (rouge)
        pygame.draw.rect(screen, ROUGE, 
                        (bar_x, bar_y,
                         health_bar_width, health_bar_height))
        # Avant-plan (vert)
        pygame.draw.rect(screen, VERT,
                        (bar_x, bar_y,
                         health_bar_width * health_ratio, health_bar_height))

class AcidEffect(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames_animation = []
        self.frame_actuel = 0
        self.timer_animation = 0
        self.délai_animation = 5  # Vitesse de l'animation
        
        try:
            # Charger les frames d'animation d'acide
            for i in range(3):  # acide0 à acide2
                image_originale = pygame.image.load(os.path.join(assets_dir, f"acid{i}.png")).convert_alpha()
                image_redimensionnée = pygame.transform.scale(image_originale, (60, 60))
                
                # Créer une version verdâtre tout en préservant la transparence
                green_image = pygame.Surface(image_redimensionnée.get_size(), pygame.SRCALPHA)
                for x_pos in range(image_redimensionnée.get_width()):
                    for y_pos in range(image_redimensionnée.get_height()):
                        color = image_redimensionnée.get_at((x_pos, y_pos))
                        # Modifier les valeurs RGB pour créer une teinte verte
                        green_r = min(255, color.r * 0.3)  # Réduire le rouge
                        green_g = min(255, color.g * 1.5)  # Améliorer le vert
                        green_b = min(255, color.b * 0.3)  # Réduire le bleu
                        green_image.set_at((x_pos, y_pos), 
                                         (int(green_r), int(green_g), int(green_b), color.a))
                
                self.frames_animation.append(green_image)
            
            self.image = self.frames_animation[0]
        except:
            self.image = pygame.Surface((60, 60))
            self.image.fill((0, 255, 0))  # Vert de secours
            self.frames_animation = [self.image]
            print("Impossible de charger les images d'acide. Veuillez vous assurer que acid0.png à acid2.png sont dans le dossier assets.")
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.lifetime = 15  # Durée de l'animation
        
    def update(self):
        self.timer_animation += 1
        if self.timer_animation >= self.délai_animation:
            self.timer_animation = 0
            self.frame_actuel = (self.frame_actuel + 1) % len(self.frames_animation)
            self.image = self.frames_animation[self.frame_actuel]
            
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

class HeartDrop(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        try:
            image_originale = pygame.image.load(os.path.join(assets_dir, "heart.png")).convert_alpha()
            self.image = pygame.transform.scale(image_originale, (30, 30))
        except:
            self.image = pygame.Surface((30, 30))
            self.image.fill(ROUGE)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = -50  # Commencer au-dessus de l'écran
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        # Supprimer si tombe hors de l'écran
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Jeu:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cheval Mutant : Dernier Survivant")
        
        # Charger et redimensionner l'arrière-plan
        try:
            image_originale_bg = pygame.image.load(os.path.join(assets_dir, "fireforest.png")).convert()
            self.background = pygame.transform.scale(image_originale_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill(NOIR)
            print("Impossible de charger l'image d'arrière-plan. Veuillez vous assurer que 'fireforest.png' est dans le dossier assets.")
        
        # Charger les polices pixel
        try:
            self.font_big = pygame.font.Font(os.path.join(assets_dir, "pixel_font.ttf"), 74)
            self.font_small = pygame.font.Font(os.path.join(assets_dir, "pixel_font.ttf"), 36)
        except:
            print("Impossible de charger la police pixel. Utilisation de la police par défaut à la place.")
            self.font_big = pygame.font.Font(None, 74)
            self.font_small = pygame.font.Font(None, 36)
        
        self.clock = pygame.time.Clock()
        self.etat_jeu = ÉtatJeu.MENU
        
        # Initialiser les groupes de sprites
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()
        self.heart_drops = pygame.sprite.Group()
        
        self.heart_spawn_timer = 0
        self.heart_spawn_delay = 300
        self.heart_spawn_chance = 0.5
        
        # Ne pas créer le joueur et les ennemis encore
        self.player = None

        # Charger l'image de cœur
        try:
            heart_image = pygame.image.load(os.path.join(assets_dir, "heart.png")).convert_alpha()
            self.heart_image = pygame.transform.scale(heart_image, (30, 30))  # Redimensionner le cœur à une taille appropriée
        except:
            self.heart_image = pygame.Surface((30, 30))
            self.heart_image.fill(ROUGE)
            print("Impossible de charger l'image de cœur. Veuillez vous assurer que heart.png est dans le dossier assets.")

        # Charger les sons
        try:
            self.win_sound = pygame.mixer.Sound(os.path.join(assets_dir, "gamewin.mp3"))
            self.gameover_sound = pygame.mixer.Sound(os.path.join(assets_dir, "gameover.mp3"))
            # Charger et jouer la musique de fond
            pygame.mixer.music.load(os.path.join(assets_dir, "song.mp3"))
            pygame.mixer.music.play(-1)  # -1 signifie boucle indéfiniment
            pygame.mixer.music.set_volume(0.5)  # Régler le volume de la musique à 50%
        except:
            print("Impossible de charger les effets sonores. Veuillez vous assurer que gamewin.mp3, gameover.mp3 et song.mp3 sont dans le dossier assets.")
            self.win_sound = None
            self.gameover_sound = None

        # Charger les images de contrôle
        try:
            wasd_image = pygame.image.load(os.path.join(assets_dir, "wasd.png")).convert_alpha()
            arrows_image = pygame.image.load(os.path.join(assets_dir, "arrows.png")).convert_alpha()
            self.wasd_image = wasd_image  # Garder la taille d'origine
            self.arrows_image = arrows_image  # Garder la taille d'origine
        except:
            print("Impossible de charger les images de contrôle. Veuillez vous assurer que wasd.png et arrows.png sont dans le dossier assets.")
            self.wasd_image = None
            self.arrows_image = None

    def start_game(self):
        # Arrêter tous les sons actuellement joués
        if self.win_sound:
            self.win_sound.stop()
        if self.gameover_sound:
            self.gameover_sound.stop()
            
        # Effacer tous les sprites
        self.all_sprites.empty()
        self.enemies.empty()
        self.effects.empty()
        self.heart_drops.empty()
        
        # Créer le joueur
        player_x = 100
        self.player = Joueur(player_x, SCREEN_HEIGHT - 150)
        self.player.jeu = self
        self.all_sprites.add(self.player)
        
        # Faire apparaître les ennemis
        self.spawn_enemies()
        
        # Démarrer la musique
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def spawn_enemies(self):
        # Répartir les ennemis sur la moitié droite de l'écran (après le centre)
        enemy_positions = [
            (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 120),    # Ennemi le plus à droite
            (SCREEN_WIDTH * 3/4, SCREEN_HEIGHT - 120),    # Ennemi au milieu à droite
            (SCREEN_WIDTH/2 + 100, SCREEN_HEIGHT - 120)   # Ennemi juste après le centre
        ]

        for position in enemy_positions:    
            enemy = Enemy(position[0], position[1], "fire")  # Créer un ennemi de type feu
            enemy.jeu = self
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return False
                
            if event.type == pygame.KEYDOWN:
                if self.etat_jeu == ÉtatJeu.MENU:
                    if event.key == pygame.K_SPACE:
                        self.start_game()  # Créer le joueur et les ennemis lors du démarrage
                        self.etat_jeu = ÉtatJeu.JOUANT
                    elif event.key == pygame.K_q:
                        return False
                elif self.etat_jeu == ÉtatJeu.GAME_OVER or self.etat_jeu == ÉtatJeu.GAGNER:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_r:
                        self.__init__()  # Réinitialiser à l'état du menu
                        self.etat_jeu = ÉtatJeu.MENU
                    elif event.key == pygame.K_q:
                        return False
                else:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.player.jump()
                    if event.key == pygame.K_e:  # Attaque normale
                        self.player.attack(self.enemies)
                    if event.key == pygame.K_q:  # Attaque spéciale
                        self.player.special_attack(self.enemies)
            
        # Ne traiter le mouvement que si en train de jouer
        if self.etat_jeu == ÉtatJeu.JOUANT:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.player.move(-1)
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.player.move(1)
            
        return True
        
    def update(self):
        if self.etat_jeu == ÉtatJeu.JOUANT:
            self.player.update()
            for enemy in self.enemies:
                enemy.update(self.player)
            self.effects.update()
            self.heart_drops.update()
            
            # Apparition de cœurs
            self.heart_spawn_timer += 1
            if self.heart_spawn_timer >= self.heart_spawn_delay:
                self.heart_spawn_timer = 0
                if random.random() < self.heart_spawn_chance:
                    self.spawn_heart()
            
            # Vérifier la collecte de cœurs
            heart_collisions = pygame.sprite.spritecollide(self.player, self.heart_drops, True)
            for heart in heart_collisions:
                if self.player.cœurs < MAX_CŒURS:
                    self.player.cœurs += 1
            
            # Vérifier si tous les ennemis sont vaincus
            if len(self.enemies) == 0:
                self.etat_jeu = ÉtatJeu.GAGNER
                # Arrêter la musique de fond et jouer le son de victoire une fois
                pygame.mixer.music.stop()
                if self.win_sound:
                    self.win_sound.play(0)

    def draw(self):
        # Draw the background first
        self.screen.blit(self.background, (0, 0))  # Draw the background at the top-left corner
        
        if self.etat_jeu == ÉtatJeu.MENU:
            self.draw_menu()
        elif self.etat_jeu == ÉtatJeu.GAME_OVER:
            self.draw_game_over()
        elif self.etat_jeu == ÉtatJeu.GAGNER:
            self.draw_win_screen()
        else:
            # Draw game elements
            self.all_sprites.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw_health_bar(self.screen)
            self.draw_ui()
            
        pygame.display.flip()
        
    def draw_ui(self):
        # Dessiner les cœurs en utilisant l'image de cœur
        for i in range(int(self.player.cœurs)):
            self.screen.blit(self.heart_image, (10 + i * 35, 10))  # Un peu plus d'espacement entre les cœurs
            
        # Dessiner le mètre spécial
        pygame.draw.rect(self.screen, VERT_NÉON, 
                        (10, 40, self.player.mètre_spécial * 2, 10))
        
    def draw_menu(self):
        # Créer un overlay semi-transparent
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # Dessiner le titre
        title_text = self.font_big.render("CHEVAL MUTANT", True, VERT_NÉON)
        subtitle_text = self.font_big.render("DERNIER SURVIVANT", True, JAUNE_NÉON)
        
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 20))
        
        self.screen.blit(title_text, title_rect)
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Dessiner les instructions
        start_text = self.font_small.render("Appuyez sur ESPACE pour commencer", True, BLANC)
        quit_text = self.font_small.render("Appuyez sur Q pour quitter", True, BLANC)
        attack_text = self.font_small.render("E pour attaquer", True, BLANC)
        
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 90))
        attack_rect = attack_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 220))  # Changer de 190 à 220
        
        # Dessiner les images de contrôle
        if self.wasd_image and self.arrows_image:
            wasd_rect = self.wasd_image.get_rect(center=(SCREEN_WIDTH/2 - 70, SCREEN_HEIGHT/2 + 150))
            arrows_rect = self.arrows_image.get_rect(center=(SCREEN_WIDTH/2 + 70, SCREEN_HEIGHT/2 + 150))
            self.screen.blit(self.wasd_image, wasd_rect)
            self.screen.blit(self.arrows_image, arrows_rect)
            self.screen.blit(attack_text, attack_rect)
        else:
            # Retour à du texte si les images ne sont pas chargées
            controls_text = self.font_small.render("WASD ou Flèches pour se déplacer", True, BLANC)
            controls_rect = controls_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 150))
            self.screen.blit(controls_text, controls_rect)
            self.screen.blit(attack_text, attack_rect)
        
        self.screen.blit(start_text, start_rect)
        self.screen.blit(quit_text, quit_rect)

    def draw_game_over(self):
        # Créer un overlay semi-transparent
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # Dessiner le texte "GAME OVER"
        game_over_text = self.font_big.render("PARTIE TERMINÉE", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        # Dessiner les instructions
        restart_text = self.font_small.render("Appuyez sur ESPACE pour rejouer", True, BLANC)  # Changer de R à ESPACE
        quit_text = self.font_small.render("Appuyez sur Q pour quitter", True, BLANC)
        
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 30))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 70))
        
        self.screen.blit(restart_text, restart_rect)
        self.screen.blit(quit_text, quit_rect)

    def draw_win_screen(self):
        # Créer un overlay semi-transparent
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # Dessiner le texte "VICTOIRE !"
        win_text = self.font_big.render("VICTOIRE !", True, VERT_NÉON)
        text_rect = win_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        self.screen.blit(win_text, text_rect)
        
        # Dessiner les instructions
        restart_text = self.font_small.render("Appuyez sur ESPACE pour rejouer", True, BLANC)  # Changer de R à ESPACE
        quit_text = self.font_small.render("Appuyez sur Q pour quitter", True, BLANC)
        
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 30))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 70))
        
        self.screen.blit(restart_text, restart_rect)
        self.screen.blit(quit_text, quit_rect)

    def spawn_heart(self):
        x = random.randint(50, SCREEN_WIDTH - 50)  # Position x aléatoire
        heart = HeartDrop(x)
        self.heart_drops.add(heart)
        self.all_sprites.add(heart)

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()

if __name__ == "__main__":
    jeu = Jeu()
    jeu.run()
