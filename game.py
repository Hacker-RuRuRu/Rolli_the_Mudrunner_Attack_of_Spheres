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
        self.animation_offset = 0
        self.last_shot_time = 0
        self.shoot_cooldown = 750
    def player_movement(self):
        
        speed = 8
        dx = 0
        dy = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]: dy -= 1
        if keys[pygame.K_s]: dy += 1
        if keys[pygame.K_d]: dx += 1
        if keys[pygame.K_a]: dx -= 1
        #Diagonal Fix 
        if dy != 0 and dx != 0:
            dx *= 0.71
            dy *= 0.71

        self.rect.x += round(dx * speed)
        self.rect.y += round(dy * speed)

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if pygame.mouse.get_pressed()[0] or pygame.key.get_pressed()[pygame.K_SPACE]:
            if current_time - self.last_shot_time >= self.shoot_cooldown:
                print("pew")
                self.last_shot_time = current_time
                new_shot = player_shot(self.rect.centerx, self.rect.centery)
                player_shots.add(new_shot)

    def animation(self):
        self.frame_counter += 1
        if self.frame_counter == 5:
            self.animation_offset -= 2
        if self.frame_counter == 10:
            self.animation_offset = 0
            self.frame_counter = 0

    #Animations Rect vom Player Rect trennen damit Bewegung smooth bleibt
    def draw_custom(self):
        animation_rect = self.rect.copy()
        animation_rect.y += self.animation_offset
        screen.blit(self.image, animation_rect)

    def update(self):
        self.animation()
        self.player_movement()
        self.shoot()

class player_shot(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.shot = pygame.image.load('graphics/player/shot.png')
        self.image = self.shot
        self.rect = self.image.get_rect(midbottom = (x,y))
    
    def update(self):
        self.rect.y -= 12
        if self.rect.bottom < -40:
            self.kill()

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
player_shots = pygame.sprite.Group()

#Game Loop
while True:

    #Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill('lightblue')
    screen.blit(ground, (0,300))
    player.sprite.draw_custom()
    player.update()        
    cow.draw(screen)
    player_shots.draw(screen)
    player_shots.update()


    pygame.display.update()
    clock.tick(60)