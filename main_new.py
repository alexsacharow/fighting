import pygame
from pygame import mixer
from fighter import Fighter


# Function to draw background
def draw_bg():
    # Scale original background image to game window size
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))


# Function to draw text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)  # Convert text to image
    screen.blit(img, (x, y))


# Function for drawing fighter health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))  # Adjust health bar based on ratio of health


mixer.init()
pygame.init()

# Create game window
SCREEN_WIDTH = 1700
SCREEN_HEIGHT = 940

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Fighting Game")

# Set framerate
clock = pygame.time.Clock()
FPS = 60

# Define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Load music and sounds
pygame.mixer.music.load("assets/audio/music.mp3")
sword_fx = pygame.mixer.Sound("assets/audio/sword.mp3")
sword_fx.set_volume(0.5)
hit_fx = pygame.mixer.Sound("assets/audio/hit.mp3")
hit_fx.set_volume(0.5)
# pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1, 0.0, 10)

# Load background
bg_image = pygame.image.load("assets/pic/bg/bg_final.png").convert_alpha()

# Define fighter variables
HERO1_SIZE = 200.25
HERO1_SCALE = 4
HERO1_OFFSET = [87, 84]
HERO1_DATA = [HERO1_SIZE, HERO1_SCALE, HERO1_OFFSET]
HERO2_SIZE = 200.25
HERO2_SCALE = 4
HERO2_OFFSET = [84, 90]
HERO2_DATA = [HERO2_SIZE, HERO2_SCALE, HERO2_OFFSET]

# Load spritesheets
hero1_sheet = pygame.image.load("assets/pic/hero1/Sprites/hero1.png").convert_alpha()
hero2_sheet = pygame.image.load("assets/pic/hero2/Sprites/hero2.png").convert_alpha()

# Define number of frames of each animation
HERO1_ANIMATION_FRAMES = [8, 8, 2, 6, 6, 4, 6]
HERO2_ANIMATION_FRAMES = [4, 8, 2, 4, 4, 3, 7]

# Define font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)
victory_font = pygame.font.Font("assets/fonts/turok.ttf", 70)

# Create two instances of fighters
fighter_1 = Fighter(1, 300, SCREEN_HEIGHT - 230, False, HERO1_DATA, hero1_sheet, HERO1_ANIMATION_FRAMES, sword_fx, hit_fx)
fighter_2 = Fighter(2, SCREEN_WIDTH - 300, SCREEN_HEIGHT - 230, True, HERO2_DATA, hero2_sheet, HERO2_ANIMATION_FRAMES, sword_fx, hit_fx)

# Define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # Player scores [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# Game loop
IS_RUNNING = True
while IS_RUNNING:
    clock.tick(FPS)

    # Draw background
    draw_bg()

    # Show player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, (SCREEN_WIDTH - 420), 20)
    draw_text("P1: " + str(score[0]) + " rounds won", score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]) + " rounds won", score_font, RED, (SCREEN_WIDTH - 420), 60)

    # Update countdown
    if intro_count <= 0:
        # Move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        # Display countdown timer
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT / 4)

        # Update countdown timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
            print(intro_count)

    # Update fighters
    fighter_1.update()
    fighter_2.update()

    # Draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # Check for player defeat
    if not round_over:
        if not fighter_1.alive:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif not fighter_2.alive:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        # Display win text
        draw_text("Player {} Wins!".format(1 if fighter_1.alive else 2), victory_font, RED, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 4)
        # Additional logic for handling end of the round
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            # Recreate instances of fighters
            fighter_1 = Fighter(1, 300, SCREEN_HEIGHT - 230, False, HERO1_DATA, hero1_sheet, HERO1_ANIMATION_FRAMES, sword_fx, hit_fx)
            fighter_2 = Fighter(2, SCREEN_WIDTH - 300, SCREEN_HEIGHT - 230, True, HERO2_DATA, hero2_sheet, HERO2_ANIMATION_FRAMES, sword_fx, hit_fx)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            IS_RUNNING = False

    # Update display
    pygame.display.update()

# Exit pygame
pygame.quit()
