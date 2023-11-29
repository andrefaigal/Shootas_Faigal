import pygame
import random
import time
import sys
from math import atan2

#the modules I created with functions and classes that I am importing:
from game_parameters import *
from bullets import Bullet, bullets
from monster import monsters
from zombie import zombies, Zombie
from player import Player
from utilities import draw_background, add_monsters, add_zombies, add_bullets

# initialize Pygame, it starts all of the game
pygame.init()

#display a caption on the game's display at the top
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shootas The Game")

#load the sound effects
music = pygame.mixer.Sound("../assets/sounds/music/onlymp3.to - Ultimate 8 bit Electro Gaming Music Mix 2020 Chiptune Music Mix-xb0cMDEyMzg-192k-1700502985.mp3")
pew = pygame.mixer.Sound("../assets/sounds/esert-eagle-gunshot.mp3")
hurt = pygame.mixer.Sound("../assets/sounds/hurt.wav")
ow = pygame.mixer.Sound("../assets/sounds/Kill Confirmed Sound Effect -Free Sound Effect Download.mp3")
gameover = pygame.mixer.Sound("../assets/sounds/game_over_voice___sound_effect_hd-sbz13HBSgxY-192k-1700518998.mp3")
sad = pygame.mixer.Sound("../assets/sounds/[Emotional Music] Ghibli Epic Songs Collection (128kbps).mp3")

#background music
pygame.mixer.Sound.play(music)

#set up the timer #from CHATGPT and initalizing pygame clock
clock = pygame.time.Clock()

# make a copy of the screen #what does this do???
background = screen.copy()
draw_background(background)

#buttons
play_button = pygame.image.load("../assets/sprites/start_btn.png").convert()
quit_button = pygame.image.load("../assets/sprites/exit_btn.png").convert()

new_size_play_button = pygame.transform.scale(play_button, (209.25,94.5))
new_size_quit_button = pygame.transform.scale(quit_button, (209.25,94.5))

play_button_rect = new_size_play_button.get_rect(center=(screen_width/2 , screen_height/2 -60))
quit_button_rect = new_size_quit_button.get_rect(center=(screen_width/2, screen_height/2 +60))

#heart stuff
life_icon = pygame.image.load("../assets/sprites/Individual Icons and Particles/minceraftheart.png")
life_icon.set_colorkey((0,0,0))

#initialize score and a custom font to display it
main_menu_font = pygame.font.Font("../assets/fonts/Minecraft-Regular.otf", 60)
gameover_font = pygame.font.Font("../assets/fonts/Minecraft-Regular.otf", 60)
score_font = pygame.font.Font("../assets/fonts/Minecraft-Regular.otf", 48)
time_font = pygame.font.Font("../assets/fonts/Minecraft-Regular.otf", 36)
angle = 0
score = 0

#add monsters and player
add_monsters(8)
add_zombies(5)
player = Player(screen_width / 2, screen_height/ 2)
player2 = Player(screen_width/2, screen_height/ 2 + 50)

def draw_welcome(screen):
    game_font = pygame.font.Font("../assets/fonts/Minecraft-Regular.otf",64)
    welcome_text = game_font.render("Welcome to Shootas", True, (255,255,255))
    screen.blit(welcome_text, (screen_width/ 2 - welcome_text.get_width() /2, screen_height/2 - welcome_text.get_height()/2))

    instructions_font = pygame.font.Font("../assets/fonts/Minecraft-Regular.otf", 30)
    instructions_text = instructions_font.render(f"Objective: Survive and don't let the enemies touch you.", True, (255,255,255))
    screen.blit(instructions_text, (screen_width - instructions_text.get_width(), screen_height - 200))

draw_mess = True

def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if play_button_rect.collidepoint(mouse_pos):
                        return
                    elif quit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

        screen.fill((139,0,0))
        screen.blit(new_size_play_button, play_button_rect)
        screen.blit(new_size_quit_button, quit_button_rect)
        pygame.display.flip()

main_menu()

def restart_game():
    global draw_mess, lives, score, player, player2, bullets, monsters, zombies

    draw_mess = True
    lives = num_lives
    score = 0

    monsters.remove()
    zombies.remove()

    # Add monsters and player
    add_monsters(8)
    add_zombies(5)
    player = Player(screen_width / 2, screen_height / 2)
    player2 = Player(screen_width / 2, screen_height / 2 + 50)

#main game loop
running = True
while running:

    lives = num_lives
    score = 0
    add_monsters(1)
    add_zombies(5)
    player = Player(screen_width / 2, screen_height / 2)

    #lives loop
    while lives > 0:
        # welcome screen
        if draw_mess:
            draw_mess = False

            # welcome message
            screen.fill((0,0,0))
            draw_welcome(screen)
            start_time = pygame.time.get_ticks()

            # update the display
            pygame.display.flip()
            time.sleep(10)

        for event in pygame.event.get(): #this is here to check if the button is pressed, so that is why it calls for the event

            #control player with arrow keys
            player.stop()
            player2.stop()

            if event.type == pygame.KEYDOWN:    #always start from no motion state
                if event.key == pygame.K_UP:    #move player up if event key is up
                    player.move_up()
                if event.key == pygame.K_DOWN:     #move player up if event key is down
                    player.move_down()
                if event.key == pygame.K_LEFT:  #move player up if event key is left
                    player.move_left()
                if event.key == pygame.K_RIGHT:     #move player up if event key is right
                    player.move_right()

                if event.key == pygame.K_w:
                    player2.move_up()
                if event.key == pygame.K_s:
                    player2.move_down()
                if event.key == pygame.K_a:
                    player2.move_left()
                if event.key == pygame.K_d:
                    player2.move_right()

            #shooting for player
            elif event.type == pygame.MOUSEBUTTONDOWN: #elif instead of if because this smoothens the code
                if pygame.mouse.get_pressed()[0]:
                    pygame.mixer.Sound.play(pew)
                    pos = player.rect.midright
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    angle = - atan2(mouse_y - player.y, mouse_x - player.x)
                    add_bullets(1, pos, angle)

        #calculate time
        running_time = (pygame.time.get_ticks() - start_time) //1000 # in seconds

        #update each monster direction, do it individually so they all don't go the same way
        for monster in monsters:
            direction = atan2(player.y - monster.y, player.x - monster.x)
            monster.update(direction)

        #check for collisions between player and zombies
        result = pygame.sprite.spritecollide(player, zombies, True)
        if result:
            lives -= len(result)
            # play hurt sound
            pygame.mixer.Sound.play(hurt)
            # add new zombie
            add_zombies(len(result))

        #check for collisions between player and monsters
        result = pygame.sprite.spritecollide(player, monsters, True)
        if result:
            lives -= len(result)
            #play hurt sound
            pygame.mixer.Sound.play(hurt)
            #add new fish
            add_monsters(len(result))

        #generating monsters
        for monster in monsters:
            if monster.rect.x < -monster.rect.width:
                monsters.remove(monster)
                add_monsters(1)

        # # adds the zombies
        # for __ in range(2):
        #     zombies.add(Zombie(random.randint(-screen_width, 0),
        #                        random.randint(tile_size, screen_height - tile_size)))

        #spawning in zombies
        for zombie in zombies:
            if zombie.rect.x > screen_width:
               zombies.remove(zombie)
               zombies.add(Zombie(random.randint(-screen_width, 0),
                                  random.randint(tile_size, screen_height - tile_size)))

        #bullet interaction with monsters and zombies
        for bullet in bullets:
            if bullet.rect.x > screen_width:
                bullets.remove(bullet)

            for monster in monsters:
                bullet_monster = pygame.sprite.spritecollide(bullet, monsters, True)
                if bullet_monster:
                    score += len(bullet_monster)
                    monsters.remove(monster)
                    add_monsters(1)
                    bullets.remove(bullet)
                    pygame.mixer.Sound.play(ow)

            for zombie in zombies:
                bullet_zombie = pygame.sprite.spritecollide(bullet, zombies, True)
                if bullet_zombie:
                    score += len(bullet_zombie)
                    zombies.remove(zombie)
                    add_zombies(1)
                    bullets.remove(bullet)
                    pygame.mixer.Sound.play(ow)

        # draw the background
        screen.blit(background, (0, 0))

        # draw the score in the upper left corner
        score_message = score_font.render(f"{score}", True, (255, 255, 240))
        screen.blit(score_message, (screen_width - score_message.get_width() - 10, 0))

        #draw the timer
        timer_text = time_font.render(f"{running_time}s", True, (255, 255, 240))
        screen.blit(timer_text, (10,10))

        # draw game objects
        player.draw(screen)
        player2.draw(screen)
        monsters.draw(screen)
        zombies.draw(screen)

        for bullet in bullets:
            bullet.draw_bullet(screen)

        # draw the lives in the lower left corner
        for life in range(lives):
            screen.blit(life_icon, (life* tile_size, screen_height - tile_size))

        #update display
        pygame.display.flip() #why do we put this here

        # update game objects
        player.update()
        player2.update()
        bullets.update()
        zombies.update()

        # Limit the frame rate
        clock.tick(60)

    screen.blit(background, (0,0))

    #show a game over message
    gameover_message = gameover_font.render("Game Over", True, (139,0,0))
    screen.blit(gameover_message, (screen_width/ 2 - gameover_message.get_width() / 2,
                          screen_height/2 - gameover_message.get_height() / 2 ))

    #show the final score
    score_text = score_font.render(f"Score: {score}", True, (0,0,0))
    screen.blit(score_text, (screen_width / 2 - score_text.get_width() / 2,
                             screen_height / 2 + gameover_message.get_height()))
    #time survived
    time_text = time_font.render(f"Time survived: {running_time}", True, (0,0,0))
    screen.blit(time_text, (screen_width/2 - time_text.get_width()/2, screen_height / 2 + gameover_message.get_height() + score_text.get_height()))

    quit_font = pygame.font.Font("../assets/fonts/HUSKYSTA.TTF", 20)
    quit_text = quit_font.render(f"Press 'Q' to quit", True, (255, 255, 240))
    screen.blit(quit_text, (screen_width - quit_text.get_width(), screen_height - 20))

    pygame.display.flip()

    if lives == 0:
        pygame.mixer.Sound.stop(music)
        pygame.mixer.Sound.play(gameover) and pygame.mixer.Sound.play(sad)

    #wait for user to exit the game
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    # Quit Pygame
                    pygame.quit()
                    sys.exit()

                elif event.key == pygame.K_r:
                    restart_game()