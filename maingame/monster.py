import pygame
import random
from math import cos,sin
from game_parameters import *

class Monster(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("../assets/sprites/Individual Animations/slime-monster-character-2-png.png").convert()
        self.image = pygame.transform.flip(self.image, True, False)
        size = self.image.get_size()
        new_size = (size[0] * .015, size[1] * .015)
        self.image = pygame.transform.scale(self.image, new_size)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.x =x
        self.y = y
        self.speed = random.uniform(monster_speed_min,monster_speed_max)
        self.rect.center = (x,y)

    def update(self, direction):
        self.x += self.speed * cos(direction)
        self.rect.x = self.x
        self.y +=  self.speed * sin(direction)
        self.rect.y = self.y
    def draw(self, screen):
        screen.blit(self.image, self.rect)

monsters = pygame.sprite.Group()