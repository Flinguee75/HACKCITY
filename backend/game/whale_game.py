import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("La Baleine Nettoyeuse")
assets_dir = os.path.join(os.path.dirname(__file__), "assets")

# Load and scale background images
background_images = []
CROP_TOP = 50  # Amount to crop from top to remove watermark
for i in range(35):  # 0 to 34
    image_path = os.path.join(assets_dir, f'c6fc0db3-6bfe-4668-bbfb-57aebb0cfcfa-{i}.png')
    img = pygame.image.load(image_path)
    # Scale image taller to allow for cropping
    scaled_width = WINDOW_WIDTH
    scaled_height = WINDOW_HEIGHT + CROP_TOP
    img = pygame.transform.scale(img, (scaled_width, scaled_height))
    # Create final surface and position image to hide top watermark
    final_img = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    final_img.blit(img, (0, -CROP_TOP))  # Shift image up to hide top watermark
    background_images.append(final_img)

# Add back animation settings
current_bg = 0
ANIMATION_SPEED = 6  # Changed from 2 to 6 (slower animation)
animation_timer = 0

# Cube properties
CUBE_SIZE = 150  # Decreased from 200 to 150 for slightly smaller whale
cube_x = WINDOW_WIDTH // 2 - CUBE_SIZE // 2
cube_y = WINDOW_HEIGHT - CUBE_SIZE - 10
CUBE_SPEED = 5

# Load whale animation images
whale_images = []
for i in range(14):  # 0 to 13
    image_path = os.path.join(assets_dir, f'31fa092b-3405-4ace-be12-e31959272deb-{i}.png')
    img = pygame.image.load(image_path)
    img = pygame.transform.scale(img, (CUBE_SIZE, CUBE_SIZE))
    whale_images.append(img)

# Add whale animation settings
current_whale = 0
WHALE_ANIMATION_SPEED = 2  # Changed from 3 to 2 for faster animation
whale_animation_timer = 0
is_moving = False  # Track if the whale is moving

# After the whale animation settings, add direction tracking
facing_right = True  # Track which way the whale is facing

# Falling cube properties
FALLING_CUBE_SIZE = 45  # Increased from 35 to 45 for slightly bigger trash
MIN_FALLING_SPEED = 2
MAX_FALLING_SPEED = 3.5
falling_cubes = []

# Load and scale trash images
trash_images = []
for i in range(1, 4):  # Load garbage1, garbage2, garbage3
    img = pygame.image.load(os.path.join(assets_dir, f'garbage{i}.png'))
    img = pygame.transform.scale(img, (FALLING_CUBE_SIZE, FALLING_CUBE_SIZE))
    trash_images.append(img)

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Game loop
running = True
clock = pygame.time.Clock()
spawn_timer = 0
SPAWN_INTERVAL = 60  # Frames between spawning new cubes

# After the game variables, add counter
trash_collected = 0
trash_missed = 0
MAX_CHANCES = 10  # Maximum number of trash that can be missed
MAX_DARKNESS = 180  # Maximum darkness level (0-255)
DARKNESS_PER_MISS = MAX_DARKNESS // MAX_CHANCES  # Darkness increase per missed trash
DARKNESS_PER_TRASH = 3  # How much darkness each collected trash adds to whale
pollution_overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
pollution_overlay.fill((0, 0, 0))  # Black overlay for ocean

# Move font loading outside the game loop (near the top with other initializations)
font = pygame.font.Font('assets/pixel_font.ttf', 36)

# After pygame.init(), add sound loading
game_over_sound = pygame.mixer.Sound(os.path.join(assets_dir, 'gameover.mp3'))
collect_sound = pygame.mixer.Sound(os.path.join(assets_dir, 'whale.mp3'))
splash_sound = pygame.mixer.Sound(os.path.join(assets_dir, 'plouk.mp3'))

# Load and start background music
pygame.mixer.music.load(os.path.join(assets_dir, 'whale_song.mp3'))
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

# Optimize whale darkening by pre-calculating surfaces
def create_darkened_whale(whale_img, darkness):
    darkened = whale_img.copy()
    # Create a surface for darkening
    dark_surface = pygame.Surface(whale_img.get_size(), pygame.SRCALPHA)
    # Use a more subtle darkening effect that preserves transparency
    dark_surface.fill((darkness, darkness, darkness, 0))
    darkened.blit(dark_surface, (0, 0), special_flags=pygame.BLEND_RGB_SUB)
    return darkened

# Pre-calculate darkened whale images (after loading whale images)
MAX_DARKNESS_LEVELS = 60  # Number of darkness levels to pre-calculate
darkened_whale_cache = []  # Change to list instead of dict
for darkness in range(0, MAX_DARKNESS + 1, 3):  # Step by 3 to reduce memory usage
    darkened_frames = []
    for img in whale_images:
        darkened = create_darkened_whale(img, darkness)
        darkened_frames.append(darkened)
    darkened_whale_cache.append(darkened_frames)

# Load heart image
heart_image = pygame.image.load(os.path.join(assets_dir, 'heart.png'))  # Ensure the heart image is in the assets folder
heart_image = pygame.transform.scale(heart_image, (30, 30))  # Scale the heart image to a suitable size

def reset_game():
    global trash_collected, trash_missed, falling_cubes, cube_x
    trash_collected = 0
    trash_missed = 0
    falling_cubes = []
    cube_x = WINDOW_WIDTH // 2 - CUBE_SIZE // 2
    # Restart background music when game resets
    pygame.mixer.music.play(-1)

def show_game_over_screen():
    # Stop background music during game over screen
    pygame.mixer.music.stop()
    
    waiting = True
    game_over_sound.play()
    
    while waiting:
        # Create semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        
        # Render all text
        game_over_font = pygame.font.Font('assets/pixel_font.ttf', 72)
        menu_font = pygame.font.Font('assets/pixel_font.ttf', 36)
        
        game_over_text = game_over_font.render('PARTIE TERMINÉE', True, (255, 0, 0))
        score_text = menu_font.render(f'Déchets ramassés: {trash_collected}', True, (255, 255, 255))
        replay_text = menu_font.render('Appuyez sur ESPACE pour rejouer', True, (255, 255, 255))
        quit_text = menu_font.render('Appuyez sur Q pour quitter', True, (255, 255, 255))
        
        # Position all text
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 100))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        replay_rect = replay_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 80))
        quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 130))
        
        # Draw all text
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(replay_text, replay_rect)
        screen.blit(quit_text, quit_rect)
        
        pygame.display.flip()
        
        # Handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()
                    return True
                if event.key == pygame.K_q:
                    return False
        
        clock.tick(60)
    
    return False

def show_start_screen():
    # Load and scale background images for the start screen
    background_images = []
    CROP_TOP = 50  # Amount to crop from top to remove watermark
    for i in range(35):  # 0 to 34
        image_path = os.path.join(assets_dir, f'c6fc0db3-6bfe-4668-bbfb-57aebb0cfcfa-{i}.png')
        img = pygame.image.load(image_path)
        # Scale image taller to allow for cropping
        scaled_width = WINDOW_WIDTH
        scaled_height = WINDOW_HEIGHT + CROP_TOP
        img = pygame.transform.scale(img, (scaled_width, scaled_height))
        # Create final surface and position image to hide top watermark
        final_img = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        final_img.blit(img, (0, -CROP_TOP))  # Shift image up to hide top watermark
        background_images.append(final_img)

    # Draw the first background image
    screen.blit(background_images[0], (0, 0))  # Display the first frame of the background

    # Create semi-transparent overlay
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    screen.blit(overlay, (0, 0))
    
    # Render title text
    title_font = pygame.font.Font('assets/pixel_font.ttf', 72)
    title_text = title_font.render('La Baleine Nettoyeuse', True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50))
    
    # Render instructions
    instructions_font = pygame.font.Font('assets/pixel_font.ttf', 36)
    instructions_text = instructions_font.render('Appuyez sur ESPACE pour commencer', True, (255, 255, 255))
    instructions_rect = instructions_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50))
    
    # Load control images without scaling
    wasd_image = pygame.image.load('assets/wasd.png')  # Load original size
    arrows_image = pygame.image.load('assets/arrows.png')  # Load original size
    
    # Position control images side by side
    wasd_rect = wasd_image.get_rect(center=(WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 120))
    arrows_rect = arrows_image.get_rect(center=(WINDOW_WIDTH / 2 + 100, WINDOW_HEIGHT / 2 + 120))
    
    # Draw everything
    screen.blit(overlay, (0, 0))
    screen.blit(title_text, title_rect)
    screen.blit(instructions_text, instructions_rect)
    screen.blit(wasd_image, wasd_rect)
    screen.blit(arrows_image, arrows_rect)
    
    pygame.display.flip()
    
    # Wait for space to start
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

# Show the start screen before the game loop
show_start_screen()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement and animation handling
    keys = pygame.key.get_pressed()
    is_moving = False  # Reset movement state
    
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and cube_x > 0:
        cube_x -= CUBE_SPEED
        facing_right = False
        is_moving = True
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and cube_x < WINDOW_WIDTH - CUBE_SIZE:
        cube_x += CUBE_SPEED
        facing_right = True
        is_moving = True

    # Update whale animation (always animate)
    whale_animation_timer += 1
    if whale_animation_timer >= WHALE_ANIMATION_SPEED:
        whale_animation_timer = 0
        current_whale = (current_whale + 1) % len(whale_images)

    # Spawn new falling cubes
    spawn_timer += 1
    if spawn_timer >= SPAWN_INTERVAL:
        spawn_timer = 0
        new_cube_x = random.randint(0, WINDOW_WIDTH - FALLING_CUBE_SIZE)
        # Add random image index and random speed to the cube data
        random_speed = random.uniform(MIN_FALLING_SPEED, MAX_FALLING_SPEED)
        falling_cubes.append([new_cube_x, -FALLING_CUBE_SIZE, random.randint(0, 2), random_speed])

    # Update falling cubes positions and check collisions
    for cube in falling_cubes[:]:
        cube[1] += cube[3]
        
        # Check collision with player cube
        if (cube_x < cube[0] + FALLING_CUBE_SIZE and
            cube_x + CUBE_SIZE > cube[0] and
            cube_y < cube[1] + FALLING_CUBE_SIZE and
            cube_y + CUBE_SIZE > cube[1]):
            falling_cubes.remove(cube)
            trash_collected += 1
            collect_sound.play()  # Play whale sound when collecting trash
        # Remove cubes that fall off screen and count as missed
        elif cube[1] > WINDOW_HEIGHT:
            falling_cubes.remove(cube)
            trash_missed += 1
            splash_sound.play()  # Play splash sound when trash hits water

    # Update background animation
    animation_timer += 1
    if animation_timer >= ANIMATION_SPEED:
        animation_timer = 0
        current_bg = (current_bg + 1) % len(background_images)

    # Draw everything
    # Draw background
    screen.blit(background_images[current_bg], (0, 0))

    # Apply ocean pollution based on missed trash (scaled to 10 chances)
    ocean_darkness = min(trash_missed * DARKNESS_PER_MISS, MAX_DARKNESS)
    pollution_overlay.set_alpha(ocean_darkness)
    screen.blit(pollution_overlay, (0, 0))

    # Draw the whale with darkness based on collected trash
    darkness_index = min(trash_collected * DARKNESS_PER_TRASH, MAX_DARKNESS) // 3
    darkened_whale = darkened_whale_cache[darkness_index][current_whale]
    
    if not facing_right:
        darkened_whale = pygame.transform.flip(darkened_whale, True, False)
    
    screen.blit(darkened_whale, (cube_x, cube_y))

    # Draw falling trash
    for cube in falling_cubes:
        screen.blit(trash_images[cube[2]], (cube[0], cube[1]))

    # Draw counters
    # Draw trash counter
    counter_text = font.render(f'Déchets: {trash_collected}', True, (255, 255, 255))
    screen.blit(counter_text, (20, 20))
    
    # Draw chances counter
    chances_left = MAX_CHANCES - trash_missed
    chances_text = font.render(f'Chances: {chances_left}', True, (255, 255, 255))
    screen.blit(chances_text, (20, 60))  # Position below trash counter

    # Draw hearts for chances
    for i in range(MAX_CHANCES):
        if i < MAX_CHANCES - trash_missed:  # Only draw hearts for remaining chances
            screen.blit(heart_image, (20 + i * 35, 100))  # Adjust position as needed

    # Update the display
    pygame.display.flip()

    # Control game speed
    clock.tick(60)

    # Optional: End game if all chances are used
    if trash_missed >= MAX_CHANCES:
        if not show_game_over_screen():
            running = False
        else:
            continue

# Quit the game
pygame.quit()
