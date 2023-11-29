# a pygame sprite class for the player
import pygame
from game_parameters import *

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()

        #uploading the png picture of shooter as forward image
        self.forward_image = pygame.image.load("../assets/sprites/Individual Animations/Handgun1.png").convert()
        self.forward_image.set_colorkey((0,0,0))

        #makes player to move in directions up, down, left, right
        self.reverse_image = pygame.transform.flip(self.forward_image, True, False)
        self.up_image = pygame.transform.rotate(self.forward_image, 90)
        self.down_image = pygame.transform.rotate(self.forward_image, -90)
        self.image = self.forward_image
        self.rect = self.image.get_rect()
        # update the position of this object by setting the values of rect.x and rect.y
        self.x = x
        self.y = y
        self.x_velocity = 0
        self.y_velocity = 0
        self.rect.center = (x, y)

    def move_up(self):
        self.y_velocity = - player_speed
        self.image = self.up_image

    def move_down(self):
        self.y_velocity = player_speed
        self.image = self.down_image

    def move_left(self):
        self.x_velocity = -1 * player_speed
        self.image = self.reverse_image

    def move_right(self):
        self.x_velocity = player_speed
        self.image = self.forward_image

    def stop(self):
        self.x_velocity = 0
        self.y_velocity = 0

    def update(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        self.rect.x = self.x
        self.rect.y = self.y

        if self.x <= 0:     #boundaries just like chomp... gotta tweak this
            self.x = 0
        if self.x >= screen_width - tile_size:
            self.x = screen_width - tile_size
        if self.y <= 0:
            self.y = 0
        if self.y >= screen_height - tile_size:
            self.y = screen_height - tile_size

    def draw(self, screen):
        screen.blit(self.image, self.rect)