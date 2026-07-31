#   load pygame library, random and os 
import pygame
import random
import os

#   intitialize pygame's modules
pygame.init()

#   initialize mixer which is responsible for all audio in the game
pygame.mixer.init()

#   creating game window
#   game window size 520 x 420 pixels
size=width,height=520,420

#   screen is the surface where we draw everything
screen=pygame.display.set_mode(size)
pygame.display.set_caption("Space Dodger")

#   loading and playing the music
pygame.mixer.music.load("sounds/space_sound.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1) # loops forever the music keeps playing until the game closes

crash_sound=pygame.mixer.Sound("sounds/crash.mp3") #    Sound is used for short effects
crash_sound.set_volume(0.7)
clock=pygame.time.Clock()
#l  oading the player image
#   convert_alpha() allows to preserve the transparency of image
player=pygame.image.load("images/player.png").convert_alpha()

player_width=64
player_height=64
player=pygame.transform.scale(player,(player_width,player_height))

#   player coordinates (In python coordinates starts from top left )
player_x=100   # increases to right
player_y=100   #increases downwards

speed=3 #   controls how much player moves each game-loop iteration

enemy=pygame.image.load("images/enemy.png").convert_alpha()
enemy_height=64
enemy_width=64

enemy=pygame.transform.scale(enemy,(enemy_width,enemy_height))

def create_enemies(count):
    enemies=[]
    for i in range(count): #  create 9 enemies
        enemy_x=random.randint(0,width-enemy_width)
        enemy_y=random.randint(-1200,-50)  #  negative y values are above the screen 
        enemies.append([enemy_x,enemy_y])
    return enemies

enemies=create_enemies(8)
print(enemies)
enemy_speed=5

white=255,255,255
running=True

game_over=False
font = pygame.font.Font(None,60)

#get highscore
def load_highscore():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt","r") as file:
            return int(file.read())
    return 0

#saving score
def save_highscore(highscore):
    with open("highscore.txt","w") as file:
        file.write(str(highscore))

# score 
score=0
highscore=load_highscore()
score_font=pygame.font.Font(None,36)
restart_font=pygame.font.Font(None,32)

restart_button=pygame.Rect(width//2-75,height//2+50,150,50)

# The main game loop
while running:

    # ---------------- EVENTS ----------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if game_over and restart_button.collidepoint(event.pos):

                # Reset game
                game_over = False
                score = 0
                crash_sound.stop()
                pygame.mixer.music.play(-1)
                player_x = (width-player_width)//2
                player_y = (height-player_height)//2

                enemies=create_enemies(8)


    # ---------------- GAME LOGIC ----------------

    if not game_over:
    
        # Player movement
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= speed

        if keys[pygame.K_RIGHT] and player_x < width - player_width:
            player_x += speed

        if keys[pygame.K_UP] and player_y > 0:
            player_y -= speed

        if keys[pygame.K_DOWN] and player_y < height - player_height:
            player_y += speed


        # Move enemies
        for enemy_pos in enemies:

            enemy_pos[1] += enemy_speed

            if enemy_pos[1] > height:

                score += 15

                enemy_pos[0] = random.randint(
                    0,
                    width - enemy_width
                )

                enemy_pos[1] = random.randint(-1200,-100)
        if score>=500:
            speed=5
            enemy_speed=7
        else:
            speed=3
            enemy_speed=5
        # Player collision rectangle
        player_rect = pygame.Rect(
            player_x + 15,
            player_y + 15,
            player_width - 30,
            player_height - 30
        )


        # Check collision with every enemy
        for enemy_pos in enemies:

            enemy_rect = pygame.Rect(
                enemy_pos[0] + 15,
                enemy_pos[1] + 15,
                enemy_width - 30,
                enemy_height - 30
            )

            if player_rect.colliderect(enemy_rect):
                crash_sound.play()
                game_over = True
                pygame.mixer.music.stop()
                if score>highscore:
                    highscore=score
                    save_highscore(highscore)


    # ---------------- DRAW ----------------

    screen.fill(white)

    # Draw player
    screen.blit(player, (player_x, player_y))

    # Draw enemies
    for enemy_pos in enemies:
        screen.blit(
            enemy,
            (enemy_pos[0], enemy_pos[1])
        )


    # Draw score
    score_text = score_font.render(
        f"Score: {score}",
        True,
        (0, 0, 0)
    )

    screen.blit(score_text, (10, 10))

    #Draw highscore
    highscore_text = score_font.render(
            f"High Score: {highscore}",
            True,
            (0, 0, 0)
        )
    
    screen.blit(highscore_text, (300, 10))
    

    # ---------------- GAME OVER ----------------

    if game_over:

        game_over_text = font.render(
            "GAME OVER",
            True,
            (255, 0, 0)
        )

        text_rect = game_over_text.get_rect(
            center=(width // 2, height // 2 - 30)
        )

        screen.blit(
            game_over_text,
            text_rect
        )


        # Draw restart button
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            restart_button
        )

        restart_text = restart_font.render(
            "RESTART",
            True,
            (255, 255, 255)
        )

        restart_text_rect = restart_text.get_rect(
            center=restart_button.center
        )

        screen.blit(
            restart_text,
            restart_text_rect
        )


    # Update display
    pygame.display.update()

    # Limit game to 60 FPS
    clock.tick(60)
pygame.quit()
