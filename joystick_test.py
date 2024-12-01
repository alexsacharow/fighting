import pygame

# Initialize Pygame
pygame.init()

# Initialize the joystick module
pygame.joystick.init()

# Check for connected gamepads
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
for joystick in joysticks:
    joystick.init()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Assuming there's at least one connected joystick
    if len(joysticks) > 0:
        joystick = joysticks[0]  # Use the first joystick (player 1)

        # Loop through all buttons and check if any are pressed
        for button_id in range(joystick.get_numbuttons()):
            if joystick.get_button(button_id):  # If the button is pressed
                print(f"Button {button_id} pressed")

    pygame.time.delay(10)  # Delay to control frame rate

pygame.quit()
