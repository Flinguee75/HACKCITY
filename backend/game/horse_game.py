import pygame
import os
import sys
import random
from enum import Enum

# Initialiser Pygame au début du fichier
pygame.init()
pygame.font.init()  # Initialiser spécifiquement le module de police

# Ajouter le chemin parent au PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
assets_dir = os.path.join(os.path.dirname(__file__), "assets")
 

from base_game import BaseGame

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
NEON_GREEN = (57, 255, 20)
NEON_YELLOW = (229, 255, 20)

# Player Constants
PLAYER_SPEED = 5
PLAYER_JUMP_FORCE = -17
GRAVITY = 0.8
MAX_HEARTS = 6

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4
    WIN = 5  # Add new win state

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animation_frames = []
        self.animation_frames_flipped = []
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_delay = 5  # Update animation every 5 game ticks
        
        try:
            # Load all animation frames
            for i in range(8):  # horse0 to horse7
                original_image = pygame.image.load(os.path.join(assets_dir, f"horse{i}.png")).convert_alpha()
                scaled_image = pygame.transform.scale(original_image, (150, 150))
                self.animation_frames.append(scaled_image)
                # Create flipped version
                flipped_image = pygame.transform.flip(scaled_image, True, False)
                self.animation_frames_flipped.append(flipped_image)
            
            # Set initial image
            self.image = self.animation_frames[0]
            self.idle_image = self.animation_frames[0]  # Use first frame as idle
            self.idle_image_flipped = self.animation_frames_flipped[0]
        except:
            # Fallback to white rectangle if image loading fails
            self.image = pygame.Surface((150, 150))
            self.image.fill(WHITE)
            print("Could not load horse images. Please ensure horse0.png to horse7.png are in the assets folder.")
            self.idle_image = self.image
            self.idle_image_flipped = self.image
            self.animation_frames = [self.image]
            self.animation_frames_flipped = [self.image]
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0
        self.hearts = MAX_HEARTS
        self.special_meter = 0
        self.is_jumping = False
        self.facing_right = True
        self.attack_cooldown = 0
        self.special_cooldown = 0
        self.attack_damage = 10
        self.special_damage = 40
        self.invincibility_timer = 0
        self.velocity_x = 0  # Add horizontal velocity
        self.knockback_resistance = 0.8  # Resistance to slow down knockback
        self.hitbox = pygame.Rect(0, 0, 80, 50)  # Back to previous size
        
        # Load sounds
        try:
            self.splash_sound = pygame.mixer.Sound(os.path.join(assets_dir, "splash.mp3"))
            self.neigh_sound = pygame.mixer.Sound(os.path.join(assets_dir, "neigh.mp3"))
            self.punch_sound = pygame.mixer.Sound(os.path.join(assets_dir, "punch.mp3"))
        except:
            print("Could not load sound effects. Please ensure splash.mp3, neigh.mp3, and punch.mp3 are in the assets folder.")
            self.splash_sound = None
            self.neigh_sound = None
            self.punch_sound = None
        
    def update(self):
        # Check for game over at the start of update
        if self.hearts <= 1:
            self.hearts = 0
            if self.game.game_state != GameState.GAME_OVER:  # Only play sound when first entering game over state
                self.game.game_state = GameState.GAME_OVER
                # Stop background music and play game over sound once
                pygame.mixer.music.stop()
                if self.game.gameover_sound:
                    self.game.gameover_sound.play(0)  # 0 means play once
            return
        
        # Handle gravity
        self.velocity_y += GRAVITY
        
        # Move vertically
        self.rect.y += self.velocity_y
        
        # Handle horizontal knockback with boundary checks
        if self.velocity_x != 0:
            new_x = self.rect.x + self.velocity_x
            # Keep player within screen bounds during knockback
            if 0 <= new_x <= SCREEN_WIDTH - self.rect.width:
                self.rect.x = new_x
            else:
                # Stop knockback if it would push player out of bounds
                self.velocity_x = 0
            self.velocity_x *= self.knockback_resistance
            if abs(self.velocity_x) < 0.1:
                self.velocity_x = 0
        
        # Update player transparency based on invincibility
        if self.invincibility_timer > 0:
            self.image.set_alpha(128)
            self.invincibility_timer -= 1
        else:
            self.image.set_alpha(255)
        
        # Update hitbox position to lower part of sprite
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.bottom = self.rect.bottom - 10  # Back to previous position
        
        # Enemy collisions using hitbox instead of full sprite rect
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False, 
                                         collided=lambda x, y: y.rect.colliderect(x.hitbox))
        if hits and self.invincibility_timer <= 0:
            self.hearts -= 0.5
            self.invincibility_timer = 60
            
            # Play splash sound
            if self.splash_sound:
                self.splash_sound.play()
            
            # Create acid effect at point of impact
            for enemy in hits:
                acid_x = (self.rect.centerx + enemy.rect.centerx) // 2
                acid_y = self.hitbox.centery
                acid_effect = AcidEffect(acid_x, acid_y)
                self.game.effects.add(acid_effect)
                self.game.all_sprites.add(acid_effect)
            
            # Check for game over
            if self.hearts <= 0:
                self.hearts = 0
                self.game.game_state = GameState.GAME_OVER
            
            # Horizontal knockback only
            knockback_speed = 12
            if hits[0].rect.centerx < self.rect.centerx:
                self.velocity_x = knockback_speed
            else:
                self.velocity_x = -knockback_speed
        
        # Ground collision
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0
            self.is_jumping = False
            
        # Update cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.special_cooldown > 0:
            self.special_cooldown -= 1
        
        # Update animation if moving
        keys = pygame.key.get_pressed()
        is_moving = keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]
        
        if is_moving:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_delay:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
                if self.facing_right:
                    self.image = self.animation_frames[self.current_frame]
                else:
                    self.image = self.animation_frames_flipped[self.current_frame]
        else:
            # Use idle frame when not moving
            if self.facing_right:
                self.image = self.idle_image
            else:
                self.image = self.idle_image_flipped

    def attack(self, enemies):
        if self.attack_cooldown <= 0:
            attack_range = pygame.Rect(
                self.rect.x - 20 if not self.facing_right else self.rect.right,
                self.rect.centery,
                40,
                self.rect.height/2
            )
            for enemy in enemies:
                if attack_range.colliderect(enemy.rect):
                    enemy.take_damage(self.attack_damage)
                    # Play punch sound when hitting enemy
                    if self.punch_sound:
                        self.punch_sound.play()
            self.attack_cooldown = 20
            
    def special_attack(self, enemies):
        if self.special_cooldown <= 0 and self.special_meter >= 50:
            # Special attack range - also adjusted
            attack_range = pygame.Rect(
                self.rect.x - 40 if not self.facing_right else self.rect.right,
                self.rect.centery - 10,  # Slightly higher than normal attack
                80,  # Reduced from 100
                self.rect.height/2 + 20  # A bit taller than normal attack
            )
            for enemy in enemies:
                if attack_range.colliderect(enemy.rect):
                    enemy.take_damage(self.special_damage)
            self.special_meter = 0
            self.special_cooldown = 60

    def move(self, direction):
        new_x = self.rect.x + direction * PLAYER_SPEED
        # Keep player within screen bounds
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
        self.animation_delay = 5  # Update animation every 5 game ticks
        
        try:
            # Load all animation frames
            for i in range(8):  # horse0 to horse7
                original_image = pygame.image.load(os.path.join(assets_dir, f"horse{i}.png")).convert_alpha()
                scaled_image = pygame.transform.scale(original_image, (120, 120))
                
                # Create greenish version while preserving transparency
                negative_image = pygame.Surface(scaled_image.get_size(), pygame.SRCALPHA)
                for x_pos in range(scaled_image.get_width()):
                    for y_pos in range(scaled_image.get_height()):
                        color = scaled_image.get_at((x_pos, y_pos))
                        # Modify RGB values to create a green tint
                        green_r = min(255, (255 - color.r) * 0.7)  # Reduce red
                        green_g = min(255, (255 - color.g) * 1.2)  # Enhance green
                        green_b = min(255, (255 - color.b) * 0.7)  # Reduce blue
                        negative_image.set_at((x_pos, y_pos), 
                                            (int(green_r), int(green_g), int(green_b), color.a))
                
                self.animation_frames.append(negative_image)
                # Create flipped version
                flipped_image = pygame.transform.flip(negative_image, True, False)
                self.animation_frames_flipped.append(flipped_image)
            
            # Set initial image
            self.image = self.animation_frames[0]
            self.idle_image = self.animation_frames[0]
            self.idle_image_flipped = self.animation_frames_flipped[0]
            self.facing_right = True
        except:
            # Fallback to red rectangle if image loading fails
            self.image = pygame.Surface((120, 120))
            self.image.fill(RED)
            print("Could not load horse images. Please ensure horse0.png to horse7.png are in the assets folder.")
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
        # Store previous position to check if moving
        old_x = self.x
        
        # Basic enemy AI
        if self.x < player.rect.x:
            self.x += self.speed
            self.facing_right = True
        else:
            self.x -= self.speed
            self.facing_right = False

        # Update animation if moving
        is_moving = abs(self.x - old_x) > 0.1
        
        if is_moving:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_delay:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
                if self.facing_right:
                    self.image = self.animation_frames[self.current_frame]
                else:
                    self.image = self.animation_frames_flipped[self.current_frame]
        else:
            # Use idle frame when not moving
            if self.facing_right:
                self.image = self.idle_image
            else:
                self.image = self.idle_image_flipped

        self.rect.x = int(self.x)
        self.rect.bottom = SCREEN_HEIGHT

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            
    def draw_health_bar(self, screen):
        health_bar_width = 80  # Made wider to match larger enemy size
        health_bar_height = 5
        health_ratio = self.health / self.max_health
        
        # Center the health bar above the enemy
        bar_x = self.rect.centerx - health_bar_width/2
        bar_y = self.rect.y - 20  # Moved a bit higher above the enemy
        
        # Background (red)
        pygame.draw.rect(screen, RED, 
                        (bar_x, bar_y,
                         health_bar_width, health_bar_height))
        # Foreground (green)
        pygame.draw.rect(screen, GREEN,
                        (bar_x, bar_y,
                         health_bar_width * health_ratio, health_bar_height))

class AcidEffect(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animation_frames = []
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_delay = 5  # Speed of animation
        
        try:
            # Load acid animation frames
            for i in range(3):  # acid0 to acid2
                original_image = pygame.image.load(os.path.join(assets_dir, f"acid{i}.png")).convert_alpha()
                scaled_image = pygame.transform.scale(original_image, (60, 60))
                
                # Create green tinted version while preserving transparency
                green_image = pygame.Surface(scaled_image.get_size(), pygame.SRCALPHA)
                for x_pos in range(scaled_image.get_width()):
                    for y_pos in range(scaled_image.get_height()):
                        color = scaled_image.get_at((x_pos, y_pos))
                        # Modify RGB values to create a green tint
                        green_r = min(255, color.r * 0.3)  # Reduce red
                        green_g = min(255, color.g * 1.5)  # Enhance green
                        green_b = min(255, color.b * 0.3)  # Reduce blue
                        green_image.set_at((x_pos, y_pos), 
                                         (int(green_r), int(green_g), int(green_b), color.a))
                
                self.animation_frames.append(green_image)
            
            self.image = self.animation_frames[0]
        except:
            self.image = pygame.Surface((60, 60))
            self.image.fill((0, 255, 0))  # Green fallback
            self.animation_frames = [self.image]
            print("Could not load acid images. Please ensure acid0.png to acid2.png are in the assets folder.")
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.lifetime = 15  # How long the animation plays
        
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
            original_image = pygame.image.load(os.path.join(assets_dir, "heart.png")).convert_alpha()
            self.image = pygame.transform.scale(original_image, (30, 30))
        except:
            self.image = pygame.Surface((30, 30))
            self.image.fill(RED)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = -50  # Start above screen
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        # Remove if falls off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mutant Horse: Last Survivor")
        
        # Load and scale background
        try:
            original_bg = pygame.image.load(os.path.join(assets_dir, "background.png")).convert()
            self.background = pygame.transform.scale(original_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill(BLACK)
            print("Could not load background image. Please ensure 'background.png' is in the assets folder.")
        
        # Load pixel fonts
        try:
            self.font_big = pygame.font.Font(os.path.join(assets_dir, "pixel_font.ttf"), 74)
            self.font_small = pygame.font.Font(os.path.join(assets_dir, "pixel_font.ttf"), 36)
        except:
            print("Could not load pixel font. Using default font instead.")
            self.font_big = pygame.font.Font(None, 74)
            self.font_small = pygame.font.Font(None, 36)
        
        self.clock = pygame.time.Clock()
        self.game_state = GameState.MENU
        
        # Initialize sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()
        self.heart_drops = pygame.sprite.Group()
        
        self.heart_spawn_timer = 0
        self.heart_spawn_delay = 300
        self.heart_spawn_chance = 0.5
        
        # Don't create player and enemies yet
        self.player = None

        # Load heart image
        try:
            heart_image = pygame.image.load(os.path.join(assets_dir, "heart.png")).convert_alpha()
            self.heart_image = pygame.transform.scale(heart_image, (30, 30))  # Scale heart to appropriate size
        except:
            self.heart_image = pygame.Surface((30, 30))
            self.heart_image.fill(RED)
            print("Could not load heart image. Please ensure heart.png is in the assets folder.")

        # Load sounds
        try:
            self.win_sound = pygame.mixer.Sound(os.path.join(assets_dir, "gamewin.mp3"))
            self.gameover_sound = pygame.mixer.Sound(os.path.join(assets_dir, "gameover.mp3"))
            # Load and play background music
            pygame.mixer.music.load(os.path.join(assets_dir, "song.mp3"))
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            pygame.mixer.music.set_volume(0.5)  # Set music volume to 50%
        except:
            print("Could not load sound effects. Please ensure gamewin.mp3, gameover.mp3, and song.mp3 are in the assets folder.")
            self.win_sound = None
            self.gameover_sound = None

        # Load control images
        try:
            wasd_image = pygame.image.load(os.path.join(assets_dir, "wasd.png")).convert_alpha()
            arrows_image = pygame.image.load(os.path.join(assets_dir, "arrows.png")).convert_alpha()
            self.wasd_image = pygame.transform.scale(wasd_image, (120, 80))  # Adjust size as needed
            self.arrows_image = pygame.transform.scale(arrows_image, (120, 80))  # Adjust size as needed
        except:
            print("Could not load control images. Please ensure wasd.png and arrows.png are in the assets folder.")
            self.wasd_image = None
            self.arrows_image = None

    def start_game(self):
        # Stop any currently playing sounds
        if self.win_sound:
            self.win_sound.stop()
        if self.gameover_sound:
            self.gameover_sound.stop()
            
        # Clear all sprites
        self.all_sprites.empty()
        self.enemies.empty()
        self.effects.empty()
        self.heart_drops.empty()
        
        # Create player
        player_x = 100
        self.player = Player(player_x, SCREEN_HEIGHT - 150)
        self.player.game = self
        self.all_sprites.add(self.player)
        
        # Spawn enemies
        self.spawn_enemies()
        
        # Start music
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def spawn_enemies(self):
        # Spread enemies on right half of screen (after center)
        enemy_positions = [
            (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 120),    # Rightmost enemy
            (SCREEN_WIDTH * 3/4, SCREEN_HEIGHT - 120),    # Right middle enemy
            (SCREEN_WIDTH/2 + 100, SCREEN_HEIGHT - 120)   # Just past center enemy
        ]

        for position in enemy_positions:    
            enemy = Enemy(position[0], position[1], "normal")
            enemy.game = self
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return False
                
            if event.type == pygame.KEYDOWN:
                if self.game_state == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        self.start_game()  # Create player and enemies when starting
                        self.game_state = GameState.PLAYING
                    elif event.key == pygame.K_q:
                        return False
                elif self.game_state == GameState.GAME_OVER or self.game_state == GameState.WIN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_r:
                        self.__init__()  # Reset to menu state
                        self.game_state = GameState.MENU
                    elif event.key == pygame.K_q:
                        return False
                else:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.player.jump()
                    if event.key == pygame.K_e:  # Normal attack
                        self.player.attack(self.enemies)
                    if event.key == pygame.K_q:  # Special attack
                        self.player.special_attack(self.enemies)
            
        # Only process movement if playing
        if self.game_state == GameState.PLAYING:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.player.move(-1)
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.player.move(1)
            
        return True
        
    def update(self):
        if self.game_state == GameState.PLAYING:
            self.player.update()
            for enemy in self.enemies:
                enemy.update(self.player)
            self.effects.update()
            self.heart_drops.update()
            
            # Heart powerup spawning
            self.heart_spawn_timer += 1
            if self.heart_spawn_timer >= self.heart_spawn_delay:
                self.heart_spawn_timer = 0
                if random.random() < self.heart_spawn_chance:
                    self.spawn_heart()
            
            # Check heart collection
            heart_collisions = pygame.sprite.spritecollide(self.player, self.heart_drops, True)
            for heart in heart_collisions:
                if self.player.hearts < MAX_HEARTS:
                    self.player.hearts += 1
                    # Play neigh sound when collecting heart
                    if self.player.neigh_sound:
                        self.player.neigh_sound.play()
            
            # Check if all enemies are defeated
            if len(self.enemies) == 0:
                self.game_state = GameState.WIN
                # Stop background music and play win sound once
                pygame.mixer.music.stop()
                if self.win_sound:
                    self.win_sound.play(0)

    def draw(self):
        # Draw background first
        self.screen.blit(self.background, (0, 0))
        
        if self.game_state == GameState.MENU:
            self.draw_menu()
        elif self.game_state == GameState.GAME_OVER:
            self.draw_game_over()
        elif self.game_state == GameState.WIN:
            self.draw_win_screen()
        else:
            # Draw gameplay elements
            self.all_sprites.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw_health_bar(self.screen)
            self.draw_ui()
            
        pygame.display.flip()
        
    def draw_ui(self):
        # Draw hearts using heart image
        for i in range(int(self.player.hearts)):
            self.screen.blit(self.heart_image, (10 + i * 35, 10))  # Slightly more spacing between hearts
            
        # Draw special meter
        pygame.draw.rect(self.screen, NEON_GREEN, 
                        (10, 40, self.player.special_meter * 2, 10))
        
    def draw_menu(self):
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # Draw title
        title_text = self.font_big.render("MUTANT HORSE", True, NEON_GREEN)
        subtitle_text = self.font_big.render("LAST SURVIVOR", True, NEON_YELLOW)
        
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 20))
        
        self.screen.blit(title_text, title_rect)
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw instructions
        start_text = self.font_small.render("Press SPACE to Start", True, WHITE)
        quit_text = self.font_small.render("Press Q to Quit", True, WHITE)
        attack_text = self.font_small.render("E to Attack", True, WHITE)
        
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 90))
        attack_rect = attack_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 220))  # Changed from 190 to 220
        
        # Draw control images
        if self.wasd_image and self.arrows_image:
            wasd_rect = self.wasd_image.get_rect(center=(SCREEN_WIDTH/2 - 70, SCREEN_HEIGHT/2 + 150))
            arrows_rect = self.arrows_image.get_rect(center=(SCREEN_WIDTH/2 + 70, SCREEN_HEIGHT/2 + 150))
            self.screen.blit(self.wasd_image, wasd_rect)
            self.screen.blit(self.arrows_image, arrows_rect)
            self.screen.blit(attack_text, attack_rect)
        else:
            # Fallback to text if images not loaded
            controls_text = self.font_small.render("WASD or Arrows to Move", True, WHITE)
            controls_rect = controls_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 150))
            self.screen.blit(controls_text, controls_rect)
            self.screen.blit(attack_text, attack_rect)
        
        self.screen.blit(start_text, start_rect)
        self.screen.blit(quit_text, quit_rect)

    def draw_game_over(self):
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # Draw "GAME OVER" text
        game_over_text = self.font_big.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        # Draw instructions
        restart_text = self.font_small.render("Press SPACE to Play Again", True, WHITE)  # Changed from R to SPACE
        quit_text = self.font_small.render("Press Q to Quit", True, WHITE)
        
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 30))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 70))
        
        self.screen.blit(restart_text, restart_rect)
        self.screen.blit(quit_text, quit_rect)

    def draw_win_screen(self):
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # Draw "VICTORY!" text
        win_text = self.font_big.render("VICTORY!", True, NEON_GREEN)
        text_rect = win_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        self.screen.blit(win_text, text_rect)
        
        # Draw instructions
        restart_text = self.font_small.render("Press SPACE to Play Again", True, WHITE)  # Changed from R to SPACE
        quit_text = self.font_small.render("Press Q to Quit", True, WHITE)
        
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 30))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 70))
        
        self.screen.blit(restart_text, restart_rect)
        self.screen.blit(quit_text, quit_rect)

    def spawn_heart(self):
        x = random.randint(50, SCREEN_WIDTH - 50)  # Random x position
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
    game = Game()
    game.run()