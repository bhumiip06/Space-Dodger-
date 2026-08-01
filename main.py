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
pygame.mixer.music.load("sounds/space_sound.ogg")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1) # loops forever the music keeps playing until the game closes

crash_sound=pygame.mixer.Sound("sounds/crash.ogg") #    Sound is used for short effects
crash_sound.set_volume(0.7)
clock=pygame.time.Clock()
#l  oading the player image
#   convert_alpha() allows to preserve the transparency of image
player=pygame.image.load("images/player.png").convert_alpha()

player_width=64
player_height=64
player=pygame.transform.scale(player,(player_width,player_height))

#   player coordinates (In python coordinates starts from top left )
player_x=(width-player_width)//2   # increases to right
player_y=(height-player_height)//2   #increases downwards

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
show_menu=True
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

restart_button=pygame.Rect(width//2-75,height//2+80,150,50)

#Draw astart button
start_button=pygame.Rect(width//2-75,height//2+30,150,55)

title_font=pygame.font.Font(None,70)
menu_font=pygame.font.Font(None,32)

background=pygame.image.load("images/background.png").convert()
background=pygame.transform.scale(background,(width,height))

# The main game loop
while running:

    # ---------------- EVENTS ----------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if show_menu and start_button.collidepoint(event.pos):
                show_menu=False
            if game_over and restart_button.collidepoint(event.pos):

                # Reset game
                game_over = False
                score = 0
                speed=3
                enemy_speed=5
                crash_sound.stop()
                pygame.mixer.music.play(-1)
                player_x = (width-player_width)//2
                player_y = (height-player_height)//2

                enemies=create_enemies(8)

    
    # ---------------- GAME LOGIC ----------------

    if not game_over and not show_menu:
    
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
        enemy_speed=5+score//300
        enemy_speed=min(enemy_speed,10)
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

    
    screen.blit(background,(0,0))

    if show_menu:
        title=title_font.render("SPACE DODGER", True,(0,0,150))
        title_rect=title.get_rect(center=(width//2,80))
        screen.blit(title,title_rect)

        text1=menu_font.render("Use Arrow keys to move", True,white)
        text2=menu_font.render("Avoid Enemy Spaceships",True,white)

        screen.blit(text1,(110,150))
        screen.blit(text2,(95,190))

        pygame.draw.rect(screen,(0,150,0),start_button)
        start_text=menu_font.render("START",True, (255,255,255))

        start_rect=start_text.get_rect(center=start_button.center)
        screen.blit(start_text,start_rect)
    else:

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
            white
        )

        screen.blit(score_text, (10, 10))

    #Draw highscore
        highscore_text = score_font.render(
            f"High Score: {highscore}",
            True,
            white
        )
    
        screen.blit(highscore_text, (300, 10))
    

    # ---------------- GAME OVER ----------------

        if game_over:

            # adding dark overlay 
            # Create a semi-transparent black overlay
            # This darkens the screen so the Game Over text is easier to read
            overlay=pygame.Surface((width,height))
            overlay.set_alpha(170)  #   transparency
            overlay.fill((0,0,0))
            screen.blit(overlay,(0,0))

            #create game over text
            game_over_text = font.render(
                "GAME OVER",
                True,
                (255, 0, 0)
            )

            #position the text near the top center of the screen 
            text_rect = game_over_text.get_rect(
                center=(width // 2, height // 2 - 70)
            )

            #display the game over text
            screen.blit(
                game_over_text,
                text_rect
            )

            final_score=restart_font.render(f"Final Score:{score}",True,white)

            final_rect=final_score.get_rect(center=(width//2,height//2))
            screen.blit(final_score,final_rect)

            best_score = restart_font.render(
                f"High Score: {highscore}",
                True,
                white
            )

            best_rect = best_score.get_rect(
                center=(width//2, height//2+30)
            )

            screen.blit(best_score, best_rect)

        # Draw restart button
            pygame.draw.rect(
                screen,
                (40, 40, 40),
                restart_button,
                border_radius=12
            )
            pygame.draw.rect(screen,white,restart_button,2,border_radius=12)
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
