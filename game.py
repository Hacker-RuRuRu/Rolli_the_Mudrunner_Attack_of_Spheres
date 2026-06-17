import pygame
from sys import exit
import os

#Spiel aus jedem directory sauber Startbar ;)
os.chdir(os.path.dirname(__file__))


class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.player_car = pygame.image.load('graphics/player/player_car.png').convert_alpha()
        self.image = self.player_car
        self.rect = self.image.get_rect(midbottom = (960,840))
        self.frame_counter = 0


    def animation(self):
        self.frame_counter += 1
        if self.frame_counter == 5:
            self.rect.y -= 2
        if self.frame_counter == 10:
            self.rect.y += 2
            self.frame_counter = 0

    def update(self):
        self.animation()

class Milky_Sphere(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.milky_sphere = pygame.image.load('graphics/cow/milky_sphere.png').convert_alpha()
        self.image = self.milky_sphere
        self.rect = self.image.get_rect(center = (960,200))
#Background
ground = pygame.image.load('graphics/background/ground.png')
 


#Starups
pygame.init()
clock = pygame.time.Clock()
#Skalliertes Vollbild ;)
screen = pygame.display.set_mode((1920,1080), pygame.NOFRAME | pygame.SCALED, display = 0)
pygame.display.set_caption('Roli_The_Mudrunner_AOS')


#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
cow = pygame.sprite.GroupSingle()
cow.add(Milky_Sphere())

#Game Loop
while True:

    #Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill('lightblue')
    screen.blit(ground, (0,300))
    player.draw(screen)
    player.update()        
    cow.draw(screen)

    pygame.display.update()
    clock.tick(60)