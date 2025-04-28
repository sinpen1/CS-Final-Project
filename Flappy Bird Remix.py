import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Start screen
Width, Height = 400, 600
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Flappy Bird Remix")
clock = pygame.time.Clock()

# Colors
SKY_BLUE = (135, 206, 235)
White = (255, 255, 255)
Black = (0, 0, 0)
Green = (0, 200, 0)

# Loading assets
bird_image = pygame.image.load("bird.png")
bird_image = pygame.transform.scale(bird_image, (50, 50))

# In game sounds
flap_sound = pygame.mixer.Sound("flap.mp3")
crash_sound = pygame.mixer.Sound("hit.mp3")

# Bird setup
bird = pygame.Rect(100, Height // 2, 50, 50)
bird_velocity = 0
gravity = 0.5
flap_power = -8

# Pipe setup
pipe_width = 60
pipe_gap = 150
pipe_speed = 3
pipes = []

def create_pipe():
    height = random.randint(100, 400)
    top_pipe = pygame.Rect(Width, 0, pipe_width, height)
    bottom_pipe = pygame.Rect(Width, height + pipe_gap, pipe_width, Height - (height + pipe_gap))
    return top_pipe, bottom_pipe

# Initial pipe
pipes.extend(create_pipe())

# Score
score = 0
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 28)

# Game logic statements
game_active = False
paused = False
game_over = False

# Main loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if not game_active and not game_over:
                    game_active = True
                elif game_over:
                    # Reset everything for restarting the game
                    bird.y = Height // 2
                    bird_velocity = 0
                    pipes = list(create_pipe())
                    score = 0
                    game_over = False
                    game_active = False
                if not paused and game_active:
                    bird_velocity = flap_power
                    flap_sound.play()
            if event.key == pygame.K_p and game_active and not game_over:
                paused = not paused  #pause/unpause

    if game_active and not paused and not game_over:
        # Bird movement
        bird_velocity += gravity
        bird.y += int(bird_velocity)

        # Move pipes
        for pipe in pipes:
            pipe.x -= pipe_speed

        # Creating new pipes
        if pipes[-1].x < 200:
            pipes.extend(create_pipe())

        # Remove old pipes/update score
        if pipes[0].x < -pipe_width:
            pipes.pop(0)
            pipes.pop(0)
            score += 1

        # Collision detection
        for pipe in pipes:
            if bird.colliderect(pipe):
                crash_sound.play()
                game_active = False
                game_over = True

        if bird.top <= 0 or bird.bottom >= Height:
            crash_sound.play()
            game_active = False
            game_over = True

    # Drawing
    screen.fill(SKY_BLUE)

    # Draw bird
    screen.blit(bird_image, bird)

    # Draw pipes
    for pipe in pipes:
        pygame.draw.rect(screen, Green, pipe)

    # Draw score
    score_text = font.render(f"Score: {score}", True, Black)
    screen.blit(score_text, (10, 10))

    # Screens
    if not game_active and not game_over:
        # Start screen
        box_width, box_height = 350, 200
        box_x, box_y = Width // 2 - box_width // 2, Height // 2 - box_height // 2
        pygame.draw.rect(screen, White, (box_x, box_y, box_width, box_height))
        pygame.draw.rect(screen, Black, (box_x, box_y, box_width, box_height), 3)

        title_text = font.render("Flappy Bird Remix", True, Black)
        creator_text = small_font.render("By Sinai P & Moe H", True, Black)
        up_text = small_font.render("Press UP to Play", True, Black)
        p_text = small_font.render("Press P to Pause/Unpause", True, Black)

        screen.blit(title_text, (Width // 2 - title_text.get_width() // 2, box_y + 10))
        screen.blit(creator_text, (Width // 2 - creator_text.get_width() // 2, box_y + 60))
        screen.blit(up_text, (Width // 2 - up_text.get_width() // 2, box_y + 100))
        screen.blit(p_text, (Width // 2 - p_text.get_width() // 2, box_y + 130))

    elif paused:
        pause_text = font.render("Paused - Press P", True, Black)
        screen.blit(pause_text, (Width // 2 - pause_text.get_width() // 2, Height // 2))

    elif game_over:
        # Game Over screen
        over_text = font.render("Game Over!", True, Black)
        restart_text = small_font.render("Press UP to Restart", True, Black)

        screen.blit(over_text, (Width // 2 - over_text.get_width() // 2, Height // 2 - 50))
        screen.blit(restart_text, (Width // 2 - restart_text.get_width() // 2, Height // 2 + 10))

    pygame.display.update()
    clock.tick(60)

