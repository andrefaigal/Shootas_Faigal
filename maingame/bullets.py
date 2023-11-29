import pygame
from math import cos, sin
from game_parameters import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, bullet_width, bullet_height) #want to make it into an image
        self.x = x
        self.y = y
        self.angle = angle

    def update(self):
        """Move the bullet up the screen."""
        # Update the position of the bullet.
        self.x += bullet_speed * cos(self.angle)
        self.y -= bullet_speed * sin(self.angle)

        # Update the rect position.
        self.rect.x, self.rect.y = self.x, self.y

    def draw_bullet(self, screen):
        """Draw the bullet to the screen."""
        # pygame.draw.rect(screen, BULLET_COLOR, self.rect)
        pygame.draw.circle(screen, bullet_color, self.rect.center, 10)


bullets = pygame.sprite.Group()


#     def __init__(self, x, y, angle):
#         super().__init__()
#
#         # uploading the png picture of orange fish as forward image
#         self.forward_image = pygame.image.load("../assets/sprites/Individual Icons and Particles/Bullet.png").convert()
#         self.forward_image.set_colorkey((0, 0, 0))
#
#         # makes orange fish to move opposite direction
#         self.reverse_image = pygame.transform.flip(self.forward_image, True, False)
#         self.up_image = pygame.transform.rotate(self.forward_image, 90)
#         self.down_image = pygame.transform.rotate(self.forward_image, -90)
#
#         size = self.forward_image.get_size()
#         new_size = (size[0] * .02, size[1] * .02)
#         self.forward_image = pygame.transform.scale(self.forward_image, new_size)
#
#         #create a bullet rect at (0,0) and then set correct position
#
#         self.x = x
#         self.y = y
#         self.angle = angle #chatGPT
#
#     def update(self):
#
#         #update the position of the bullet
#         self.x += bullet_speed * cos(self.angle)
#         self.y -= bullet_speed * sin(self.angle)
#
#         #update the rect position
#         self.forward_image.x, self.forward_image.y = self.x,self.y ##maybe its in this??
#
#     # def shoot_right(self):
#     #     self.x += bullet_speed
#     #
#     # def shoot_left(self):
#     #     self.x += - bullet_speed
#     #
#     # def shoot_up(self):
#     #     self.y +=bullet_speed
#     # def shoot_down(self):
#     #     self.y += - bullet_speed
#
#     def draw_bullet(self, screen):
#         """draw the bullet to the screen"""
#         screen.blit(self.forward_image, self.rect)
#
