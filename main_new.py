import pygame
import os
import threading
from pygame import mixer
from fighter import Fighter
# Initialize the joystick module
pygame.joystick.init()

# Function to draw background
def draw_bg(bg):
    # Scale original background image to game window size
    scaled_bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# Function to draw text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Function for drawing fighter health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))
    
# Function for drawing buttons in menu
def draw_menu_buttons(cursor):
    pygame.draw.rect(screen, YELLOW, (SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 + 150, 300, 50))
    pygame.draw.rect(screen, YELLOW, (SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 + 50, 300, 50))
    pygame.draw.rect(screen, YELLOW, (SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 - 50, 300, 50))
    pygame.draw.rect(screen, (200, 200, 200), (SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 - 150, 300, 50))
    pygame.draw.polygon(screen, WHITE, [[SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 - 150 + (100 * cursor)], [SCREEN_WIDTH / 2 - 160, SCREEN_HEIGHT / 2 - 125 + (100 * cursor)], [SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 - 100 + (100 * cursor)]])
    draw_text("FIGHTING GAME", pygame.font.Font("assets/fonts/turok.ttf", 100), RED, SCREEN_WIDTH / 2 - 300, 30)
    draw_text("Play", buttons_font, RED, SCREEN_WIDTH / 2 - 30, SCREEN_HEIGHT / 2 - 150)
    draw_text("Play DEMO", buttons_font, RED, SCREEN_WIDTH / 2 - 70, SCREEN_HEIGHT / 2 - 50)
    draw_text("Settings", buttons_font, RED, SCREEN_WIDTH / 2 - 65, SCREEN_HEIGHT / 2 + 50)
    draw_text("Quit game", buttons_font, RED, SCREEN_WIDTH / 2 - 70, SCREEN_HEIGHT / 2 + 150)

def draw_settings_buttons(cursor):
    pygame.draw.rect(screen, YELLOW, (SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 + 50, 300, 50))
    pygame.draw.rect(screen, (200, 200, 200), (SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 - 50, 300, 50))
    pygame.draw.rect(screen, YELLOW, (SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 - 150, 300, 50))
    pygame.draw.polygon(screen, WHITE, [[SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 - 150 + (100 * cursor)], [SCREEN_WIDTH / 2 - 160, SCREEN_HEIGHT / 2 - 125 + (100 * cursor)], [SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 - 100 + (100 * cursor)]])
    draw_text("SETTINGS", pygame.font.Font("assets/fonts/turok.ttf", 100), RED, SCREEN_WIDTH / 2 - 200, 30)
    draw_text("Change BG", buttons_font, RED, SCREEN_WIDTH / 2 - 70, SCREEN_HEIGHT / 2 - 150)
    draw_text("Sound settings", buttons_font, RED, SCREEN_WIDTH / 2 - 120, SCREEN_HEIGHT / 2 - 50)
    draw_text("Back", buttons_font, RED, SCREEN_WIDTH / 2 - 30, SCREEN_HEIGHT / 2 + 50)

# Function to get a list of music files from a folder
def get_music_files(folder_path):
    music_files = []
    for file in os.listdir(folder_path):
        if file.endswith(('.mp3', '.wav', '.ogg')):
            music_files.append(os.path.join(folder_path, file))
    return music_files

# Function to play music files in a loop
def play_music_files(music_files):
    while True:
        for music_file in music_files:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

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
sword_fx = pygame.mixer.Sound("assets/audio/sword.mp3")
sword_fx.set_volume(0.5)
hit_fx = pygame.mixer.Sound("assets/audio/hit.mp3")
hit_fx.set_volume(0.5)

# Get the list of music files
music_files = get_music_files('assets/music')

# Start playing music files in a separate thread
music_thread = threading.Thread(target=play_music_files, args=(music_files,))
music_thread.daemon = True
music_thread.start()

# Load background
bg_image1 = pygame.image.load("assets/pic/bg/bg_final.png").convert_alpha()
bg_image2 = pygame.image.load("assets/pic/bg/bg_test.png").convert_alpha()
bg = [bg_image1, bg_image2]


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
buttons_font = pygame.font.Font("assets/fonts/turok.ttf", 35)

# Create two instances of fighters
fighter_1 = Fighter(1, 300, SCREEN_HEIGHT - 230, False, HERO1_DATA, hero1_sheet, HERO1_ANIMATION_FRAMES, sword_fx, hit_fx)
fighter_2 = Fighter(2, SCREEN_WIDTH - 300, SCREEN_HEIGHT - 230, True, HERO2_DATA, hero2_sheet, HERO2_ANIMATION_FRAMES, sword_fx, hit_fx)

# Define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # Player scores [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# Menu state variables
pause = False
settings = False
menu = True
button = 0
current_bg = 0

# Game loop
IS_RUNNING = True
while IS_RUNNING:
    
    clock.tick(FPS)

    # Draw background
    draw_bg(bg[current_bg])

    # Main menu logic
    if menu:
        if not settings:
            pause = False
            draw_menu_buttons(button)
            # Event handler
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if button == 0:
                        pass
                    if button == 1:
                        menu = False
                        button = 0
                    if button == 2:
                        settings = True
                        button = 0
                    if button == 3:
                        IS_RUNNING = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    if button < 3:
                        button += 1
                    else:
                        button = 0
                if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                    if button > 0:
                        button -= 1
                    else:
                        button = 3
                if event.type == pygame.QUIT:
                    IS_RUNNING = False
        # Settings menu logic
        if settings:
            pause = False
            draw_settings_buttons(button)
            # Settings event handler
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # Loop through backgrounds
                    if button == 0:
                        if current_bg < len(bg) - 1:
                            current_bg += 1
                        else:
                            current_bg = 0
                    # Inactive button
                    if button == 1:
                        pass
                    # Return button
                    if button == 2:
                        settings = False
                        button = 0
                # Cursor logic
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    if button < 2:
                        button += 1
                    else:
                        button = 0
                if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                    if button > 0:
                        button -= 1
                    else:
                        button = 2
                if event.type == pygame.QUIT:
                    IS_RUNNING = False

    else:
        # Show player stats
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, (SCREEN_WIDTH - 420), 20)
        draw_text("P1: " + str(score[0]) + " rounds won", score_font, RED, 20, 60)
        draw_text("P2: " + str(score[1]) + " rounds won", score_font, RED, (SCREEN_WIDTH - 420), 60)

        # Freeze main loop if paused
        if pause:
            
            draw_text("Press P to play", score_font, RED, SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 50)
            draw_text("Press R to reset", score_font, RED, SCREEN_WIDTH / 2 - 110, SCREEN_HEIGHT / 2)
            draw_text("Press Q to quit", score_font, RED, SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 50)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    # Recreate instances of fighters
                    fighter_1 = Fighter(1, 300, SCREEN_HEIGHT - 230, False, HERO1_DATA, hero1_sheet, HERO1_ANIMATION_FRAMES, sword_fx, hit_fx)
                    fighter_2 = Fighter(2, SCREEN_WIDTH - 300, SCREEN_HEIGHT - 230, True, HERO2_DATA, hero2_sheet, HERO2_ANIMATION_FRAMES, sword_fx, hit_fx)
                    intro_count = 3
                    score[0] = score[1] = 0
                    pause = False
                if event.type == event.type == pygame.KEYDOWN and event.key == pygame.K_p or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pause = not pause
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    # Reset score and quit to main menu
                    score[0] = score[1] = 0
                    menu = True
                if event.type == pygame.QUIT:
                    IS_RUNNING = False


        if not pause:

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


        # Draw fighters
            fighter_1.draw(screen)
            fighter_2.draw(screen)

        # Event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        IS_RUNNING = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        pause = not pause

    # Update display
    pygame.display.update()

# Exit pygame
pygame.quit()