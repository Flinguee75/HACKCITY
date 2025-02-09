import os
import pygame
import random
import math
from enum import Enum
from game.base_game import BaseGame  # Assurez-vous que ce module est accessible

# --- Constantes Globales ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Couleurs
BLACK       = (0, 0, 0)
WHITE       = (255, 255, 255)
RED         = (255, 0, 0)
GREEN       = (0, 255, 0)
NEON_GREEN  = (57, 255, 20)
NEON_YELLOW = (229, 255, 20)

# Constantes du joueur
PLAYER_SPEED     = 5
PLAYER_JUMP_FORCE = -17
GRAVITY          = 0.8
MAX_HEARTS       = 6

# --- Énumération de l'état du jeu ---
class GameState(Enum):
    MENU      = 1
    PLAYING   = 2
    PAUSED    = 3
    GAME_OVER = 4
    WIN       = 5  # État de victoire

# --- Classes de sprites ---
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animation_frames = []
        self.animation_frames_flipped = []
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_delay = 5  # Mise à jour toutes les 5 ticks

        try:
            # Chargement des images horse0.png à horse7.png
            for i in range(8):
                img = pygame.image.load(os.path.join("assets", f"horse{i}.png")).convert_alpha()
                img = pygame.transform.scale(img, (150, 150))
                self.animation_frames.append(img)
                self.animation_frames_flipped.append(pygame.transform.flip(img, True, False))
            self.image = self.animation_frames[0]
            self.idle_image = self.image
            self.idle_image_flipped = self.animation_frames_flipped[0]
        except Exception as e:
            self.image = pygame.Surface((150, 150))
            self.image.fill(WHITE)
            print("Erreur lors du chargement des images du joueur :", e)
            self.idle_image = self.image
            self.idle_image_flipped = self.image
            self.animation_frames = [self.image]
            self.animation_frames_flipped = [self.image]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0
        self.velocity_x = 0  # Pour le knockback horizontal
        self.knockback_resistance = 0.8
        self.hearts = MAX_HEARTS
        self.special_meter = 0
        self.is_jumping = False
        self.facing_right = True
        self.attack_cooldown = 0
        self.special_cooldown = 0
        self.attack_damage = 10
        self.special_damage = 40
        self.invincibility_timer = 0
        self.hitbox = pygame.Rect(0, 0, 80, 50)

        # Chargement des sons
        try:
            self.splash_sound = pygame.mixer.Sound(os.path.join("assets", "splash.mp3"))
            self.neigh_sound = pygame.mixer.Sound(os.path.join("assets", "neigh.mp3"))
            self.punch_sound = pygame.mixer.Sound(os.path.join("assets", "punch.mp3"))
        except Exception as e:
            print("Erreur lors du chargement des sons du joueur :", e)
            self.splash_sound = self.neigh_sound = self.punch_sound = None

    def update(self):
        # Vérification vie
        if self.hearts <= 1:
            self.hearts = 0
            if self.game.game_state != GameState.GAME_OVER:
                self.game.game_state = GameState.GAME_OVER
                pygame.mixer.music.stop()
                if self.game.gameover_sound:
                    self.game.gameover_sound.play(0)
            return

        # Gravité et déplacement vertical
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Déplacement horizontal (knockback)
        if self.velocity_x != 0:
            new_x = self.rect.x + self.velocity_x
            if 0 <= new_x <= SCREEN_WIDTH - self.rect.width:
                self.rect.x = new_x
            else:
                self.velocity_x = 0
            self.velocity_x *= self.knockback_resistance
            if abs(self.velocity_x) < 0.1:
                self.velocity_x = 0

        # Gestion de la transparence en cas d'invincibilité
        if self.invincibility_timer > 0:
            self.image.set_alpha(128)
            self.invincibility_timer -= 1
        else:
            self.image.set_alpha(255)

        # Mise à jour de la hitbox
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.bottom = self.rect.bottom - 10

        # Collision avec les ennemis
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False,
                   collided=lambda x, y: y.rect.colliderect(x.hitbox))
        if hits and self.invincibility_timer <= 0:
            self.hearts -= 0.5
            self.invincibility_timer = 60
            if self.splash_sound:
                self.splash_sound.play()
            for enemy in hits:
                acid_effect = AcidEffect((self.rect.centerx + enemy.rect.centerx) // 2,
                                         self.hitbox.centery)
                self.game.effects.add(acid_effect)
                self.game.all_sprites.add(acid_effect)
            if self.hearts <= 0:
                self.hearts = 0
                self.game.game_state = GameState.GAME_OVER
            knockback_speed = 12
            if hits[0].rect.centerx < self.rect.centerx:
                self.velocity_x = knockback_speed
            else:
                self.velocity_x = -knockback_speed

        # Collision avec le sol
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0
            self.is_jumping = False

        # Cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.special_cooldown > 0:
            self.special_cooldown -= 1

        # Animation selon le mouvement
        keys = pygame.key.get_pressed()
        is_moving = keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]
        if is_moving:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_delay:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
                self.image = (self.animation_frames[self.current_frame] if self.facing_right 
                              else self.animation_frames_flipped[self.current_frame])
        else:
            self.image = self.idle_image if self.facing_right else self.idle_image_flipped

    def attack(self, enemies):
        if self.attack_cooldown <= 0:
            attack_range = pygame.Rect(
                self.rect.x - 20 if not self.facing_right else self.rect.right,
                self.rect.centery,
                40,
                self.rect.height / 2
            )
            for enemy in enemies:
                if attack_range.colliderect(enemy.rect):
                    enemy.take_damage(self.attack_damage)
                    if self.punch_sound:
                        self.punch_sound.play()
            self.attack_cooldown = 20

    def special_attack(self, enemies):
        if self.special_cooldown <= 0 and self.special_meter >= 50:
            attack_range = pygame.Rect(
                self.rect.x - 40 if not self.facing_right else self.rect.right,
                self.rect.centery - 10,
                80,
                self.rect.height / 2 + 20
            )
            for enemy in enemies:
                if attack_range.colliderect(enemy.rect):
                    enemy.take_damage(self.special_damage)
            self.special_meter = 0
            self.special_cooldown = 60

    def move(self, direction):
        new_x = self.rect.x + direction * PLAYER_SPEED
        if 0 <= new_x <= SCREEN_WIDTH - self.rect.width:
            self.rect.x = new_x
        self.facing_right = direction > 0

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = PLAYER_JUMP_FORCE
            self.is_jumping = True

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type):
        super().__init__()
        self.animation_frames = []
        self.animation_frames_flipped = []
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_delay = 5

        try:
            for i in range(8):
                img = pygame.image.load(os.path.join("assets", f"horse{i}.png")).convert_alpha()
                img = pygame.transform.scale(img, (120, 120))
                # Création d'une version "tintée" en vert
                tinted = pygame.Surface(img.get_size(), pygame.SRCALPHA)
                for x_pos in range(img.get_width()):
                    for y_pos in range(img.get_height()):
                        c = img.get_at((x_pos, y_pos))
                        tinted.set_at((x_pos, y_pos), (int(min(255, (255 - c.r) * 0.7)),
                                                       int(min(255, (255 - c.g) * 1.2)),
                                                       int(min(255, (255 - c.b) * 0.7)),
                                                       c.a))
                self.animation_frames.append(tinted)
                self.animation_frames_flipped.append(pygame.transform.flip(tinted, True, False))
            self.image = self.animation_frames[0]
            self.idle_image = self.image
            self.idle_image_flipped = self.animation_frames_flipped[0]
            self.facing_right = True
        except Exception as e:
            self.image = pygame.Surface((120, 120))
            self.image.fill(RED)
            print("Erreur lors du chargement des images ennemies :", e)
            self.idle_image = self.image
            self.idle_image_flipped = self.image
            self.animation_frames = [self.image]
            self.animation_frames_flipped = [self.image]

        self.enemy_type = enemy_type
        self.rect = self.image.get_rect()
        self.x = float(x)
        self.rect.x = x
        self.rect.y = y
        self.max_health = 100
        self.health = self.max_health
        self.speed = random.uniform(1, 2)

    def update(self, player):
        old_x = self.x
        if self.x < player.rect.x:
            self.x += self.speed
            self.facing_right = True
        else:
            self.x -= self.speed
            self.facing_right = False

        if abs(self.x - old_x) > 0.1:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_delay:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
                self.image = (self.animation_frames[self.current_frame] if self.facing_right 
                              else self.animation_frames_flipped[self.current_frame])
        else:
            self.image = self.idle_image if self.facing_right else self.idle_image_flipped

        self.rect.x = int(self.x)
        self.rect.bottom = SCREEN_HEIGHT

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

    def draw_health_bar(self, surface):
        bar_width = 80
        bar_height = 5
        ratio = self.health / self.max_health
        x = self.rect.centerx - bar_width / 2
        y = self.rect.y - 20
        pygame.draw.rect(surface, RED, (x, y, bar_width, bar_height))
        pygame.draw.rect(surface, GREEN, (x, y, bar_width * ratio, bar_height))

class AcidEffect(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animation_frames = []
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_delay = 5
        try:
            for i in range(3):
                img = pygame.image.load(os.path.join("assets", f"acid{i}.png")).convert_alpha()
                img = pygame.transform.scale(img, (60, 60))
                tinted = pygame.Surface(img.get_size(), pygame.SRCALPHA)
                for x_pos in range(img.get_width()):
                    for y_pos in range(img.get_height()):
                        c = img.get_at((x_pos, y_pos))
                        tinted.set_at((x_pos, y_pos), (int(c.r * 0.3),
                                                       int(c.g * 1.5),
                                                       int(c.b * 0.3),
                                                       c.a))
                self.animation_frames.append(tinted)
            self.image = self.animation_frames[0]
        except Exception as e:
            self.image = pygame.Surface((60, 60))
            self.image.fill((0, 255, 0))
            self.animation_frames = [self.image]
            print("Erreur lors du chargement des images d'acide :", e)
        self.rect = self.image.get_rect(center=(x, y))
        self.lifetime = 15

    def update(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_delay:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.current_frame]
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

class HeartDrop(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        try:
            img = pygame.image.load(os.path.join("assets", "heart.png")).convert_alpha()
            self.image = pygame.transform.scale(img, (30, 30))
        except Exception as e:
            self.image = pygame.Surface((30, 30))
            self.image.fill(RED)
            print("Erreur lors du chargement de l'image du cœur :", e)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = -50
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# --- Classe principale du jeu dérivée de BaseGame ---
class MutantHorseGame(BaseGame):
    def __init__(self):
        super().__init__("Mutant Horse: Last Survivor")
        # On définit ici la taille de la fenêtre si BaseGame ne le fait pas déjà
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT

        # État du jeu
        self.game_state = GameState.MENU

        # Groupes de sprites
        self.all_sprites   = pygame.sprite.Group()
        self.enemies       = pygame.sprite.Group()
        self.effects       = pygame.sprite.Group()
        self.heart_drops   = pygame.sprite.Group()

        # Timers de spawn
        self.heart_spawn_timer = 0
        self.heart_spawn_delay = 300
        self.heart_spawn_chance = 0.5

        self.player = None

        # Chargement du fond
        try:
            bg = pygame.image.load(os.path.join("assets", "background.png")).convert()
            self.background = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill(BLACK)
            print("Erreur lors du chargement du fond :", e)

        # Chargement des polices
        try:
            self.font_big = pygame.font.Font(os.path.join("assets", "pixel_font.ttf"), 74)
            self.font_small = pygame.font.Font(os.path.join("assets", "pixel_font.ttf"), 36)
        except Exception as e:
            print("Erreur lors du chargement de la police :", e)
            self.font_big = pygame.font.Font(None, 74)
            self.font_small = pygame.font.Font(None, 36)

        # Chargement de l'image du cœur
        try:
            heart_img = pygame.image.load(os.path.join("assets", "heart.png")).convert_alpha()
            self.heart_image = pygame.transform.scale(heart_img, (30, 30))
        except Exception as e:
            self.heart_image = pygame.Surface((30, 30))
            self.heart_image.fill(RED)
            print("Erreur lors du chargement de l'image du cœur :", e)

        # Sons et musique
        try:
            self.win_sound = pygame.mixer.Sound(os.path.join("assets", "gamewin.mp3"))
            self.gameover_sound = pygame.mixer.Sound(os.path.join("assets", "gameover.mp3"))
            pygame.mixer.music.load(os.path.join("assets", "song.mp3"))
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)
        except Exception as e:
            print("Erreur lors du chargement des sons :", e)
            self.win_sound = None
            self.gameover_sound = None

        # Images des contrôles
        try:
            wasd_img = pygame.image.load(os.path.join("assets", "wasd.png")).convert_alpha()
            arrows_img = pygame.image.load(os.path.join("assets", "arrows.png")).convert_alpha()
            self.wasd_image = pygame.transform.scale(wasd_img, (120, 80))
            self.arrows_image = pygame.transform.scale(arrows_img, (120, 80))
        except Exception as e:
            print("Erreur lors du chargement des images de contrôles :", e)
            self.wasd_image = self.arrows_image = None

    def start_game(self):
        # Réinitialisation des groupes
        self.all_sprites.empty()
        self.enemies.empty()
        self.effects.empty()
        self.heart_drops.empty()

        # Création du joueur
        player_x = 100
        self.player = Player(player_x, SCREEN_HEIGHT - 150)
        self.player.game = self
        self.all_sprites.add(self.player)

        self.spawn_enemies()

        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        self.game_state = GameState.PLAYING

    def spawn_enemies(self):
        positions = [
            (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 120),
            (SCREEN_WIDTH * 3 / 4, SCREEN_HEIGHT - 120),
            (SCREEN_WIDTH / 2 + 100, SCREEN_HEIGHT - 120)
        ]
        for pos in positions:
            enemy = Enemy(pos[0], pos[1], "normal")
            enemy.game = self
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

    def spawn_heart(self):
        x = random.randint(50, SCREEN_WIDTH - 50)
        heart = HeartDrop(x)
        self.heart_drops.add(heart)
        self.all_sprites.add(heart)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # Dans le menu, appuyer sur SPACE démarre la partie, Q quitte
                if self.game_state == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        self.start_game()
                    elif event.key == pygame.K_q:
                        self.running = False
                # Dans les états GAME_OVER ou WIN, SPACE ou R réinitialise
                elif self.game_state in (GameState.GAME_OVER, GameState.WIN):
                    if event.key in (pygame.K_SPACE, pygame.K_r):
                        self.__init__()
                    elif event.key == pygame.K_q:
                        self.running = False
                # En mode PLAYING
                else:
                    if event.key in (pygame.K_w, pygame.K_UP):
                        self.player.jump()
                    if event.key == pygame.K_e:
                        self.player.attack(self.enemies)
                    if event.key == pygame.K_q:
                        self.player.special_attack(self.enemies)
        # Gestion continue du déplacement
        if self.game_state == GameState.PLAYING:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.player.move(-1)
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.player.move(1)

    def update(self):
        if self.game_state == GameState.PLAYING:
            self.player.update()
            for enemy in self.enemies:
                enemy.update(self.player)
            self.effects.update()
            self.heart_drops.update()

            # Spawn de cœur
            self.heart_spawn_timer += 1
            if self.heart_spawn_timer >= self.heart_spawn_delay:
                self.heart_spawn_timer = 0
                if random.random() < self.heart_spawn_chance:
                    self.spawn_heart()

            # Collection de cœur
            collisions = pygame.sprite.spritecollide(self.player, self.heart_drops, True)
            for heart in collisions:
                if self.player.hearts < MAX_HEARTS:
                    self.player.hearts += 1
                    if self.player.neigh_sound:
                        self.player.neigh_sound.play()

            # Passage à l'état WIN si tous les ennemis sont éliminés
            if len(self.enemies) == 0:
                self.game_state = GameState.WIN
                pygame.mixer.music.stop()
                if self.win_sound:
                    self.win_sound.play(0)

    def render(self):
        # Affichage du fond
        self.screen.blit(self.background, (0, 0))
        # Affichage en fonction de l'état
        if self.game_state == GameState.MENU:
            self.draw_menu()
        elif self.game_state == GameState.GAME_OVER:
            self.draw_game_over()
        elif self.game_state == GameState.WIN:
            self.draw_win_screen()
        else:
            self.all_sprites.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw_health_bar(self.screen)
            self.draw_ui()
        pygame.display.flip()

    def draw_ui(self):
        # Affichage des cœurs
        for i in range(int(self.player.hearts)):
            self.screen.blit(self.heart_image, (10 + i * 35, 10))
        # Affichage de la jauge spéciale
        pygame.draw.rect(self.screen, NEON_GREEN, (10, 40, self.player.special_meter * 2, 10))

    def draw_menu(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        title = self.font_big.render("MUTANT HORSE", True, NEON_GREEN)
        subtitle = self.font_big.render("LAST SURVIVOR", True, NEON_YELLOW)
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100)))
        self.screen.blit(subtitle, subtitle.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20)))
        start = self.font_small.render("Press SPACE to Start", True, WHITE)
        quit_txt = self.font_small.render("Press Q to Quit", True, WHITE)
        self.screen.blit(start, start.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)))
        self.screen.blit(quit_txt, quit_txt.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 90)))
        # Affichage des images de contrôles (si chargées)
        attack = self.font_small.render("E to Attack", True, WHITE)
        if self.wasd_image and self.arrows_image:
            self.screen.blit(self.wasd_image, self.wasd_image.get_rect(center=(SCREEN_WIDTH/2 - 70, SCREEN_HEIGHT/2 + 150)))
            self.screen.blit(self.arrows_image, self.arrows_image.get_rect(center=(SCREEN_WIDTH/2 + 70, SCREEN_HEIGHT/2 + 150)))
        else:
            ctrl = self.font_small.render("WASD or Arrows to Move", True, WHITE)
            self.screen.blit(ctrl, ctrl.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 150)))
        self.screen.blit(attack, attack.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 220)))

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        over = self.font_big.render("GAME OVER", True, RED)
        restart = self.font_small.render("Press SPACE to Play Again", True, WHITE)
        quit_txt = self.font_small.render("Press Q to Quit", True, WHITE)
        self.screen.blit(over, over.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50)))
        self.screen.blit(restart, restart.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 30)))
        self.screen.blit(quit_txt, quit_txt.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 70)))

    def draw_win_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        win_txt = self.font_big.render("VICTORY!", True, NEON_GREEN)
        restart = self.font_small.render("Press SPACE to Play Again", True, WHITE)
        quit_txt = self.font_small.render("Press Q to Quit", True, WHITE)
        self.screen.blit(win_txt, win_txt.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50)))
        self.screen.blit(restart, restart.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 30)))
        self.screen.blit(quit_txt, quit_txt.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 70)))

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        pygame.quit()

# --- Exécution du jeu ---
if __name__ == "__main__":
    game = MutantHorseGame()
    game.run()
