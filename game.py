import pygame
from sys import exit
import os
import cut_scenes as ct
from random import randint, choice
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
        speed = 12
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
        #Spieler auf Spielfläche gefangen
        if self.rect.right > screen_widht: self.rect.right = screen_widht
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.bottom> screen_height: self.rect.bottom = screen_height
        if self.rect.top < 0: self.rect.top = 0 
    #man kann Schuss Taste gedrückt halten da key.get_pressed 
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if pygame.mouse.get_pressed()[0] or pygame.key.get_pressed()[pygame.K_SPACE]:
            if current_time - self.last_shot_time >= self.shoot_cooldown:
                self.last_shot_time = current_time
                new_shot = Player_Shot(self.rect.centerx, self.rect.centery)
                player_shots.add(new_shot)
    #damit bei cutscene skips nicht geschssen wird
    def reset_shoot(self):
        self.last_shot_time = pygame.time.get_ticks()
                    
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

class Player_Shot(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.shot = pygame.image.load('graphics/player/shot.png')
        self.image = self.shot
        self.rect = self.image.get_rect(midbottom = (x,y))
    def update(self):
        shot_speed = 16
        self.rect.y -= shot_speed
        if self.rect.bottom < -40:
            self.kill()

class Milky_Sphere(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.milky_sphere = pygame.image.load('graphics/cow/milky_sphere.png').convert_alpha()
        self.image = self.milky_sphere
        self.rect = self.image.get_rect(center = (960,200))

class Planet_Storm(pygame.sprite.Sprite):
    def __init__(self,type,lane_x):
        super().__init__()
        self.speed = 10  
        self.type = type        # genereller Speed um Spiel einfacher zu balancen 
        
        if type == 'Mars':
            self.image = pygame.image.load('graphics/planets/Mars.png').convert_alpha()
            self.speed = self.speed * 1
            self.health = 3
        if type == 'Saturn':
            self.image = pygame.image.load('graphics/planets/Saturn.png').convert_alpha()
            self.speed = self.speed * 1
            self.health = 3
        if type == 'Pluto':
            self.image = pygame.image.load('graphics/planets/Pluto.png').convert_alpha()
            self.speed = self.speed * 1.4    
            self.health = 1                                               #Pluto soll schnell aber leicht zerstöbar sein
        if type == 'DeathStar': 
            self.image = pygame.image.load('graphics/planets/DeathStar.png').convert_alpha()
            self.speed = self.speed * 0.8
            self.health = 6
        self.rect = self.image.get_rect(center = (lane_x, 0))
        
    def destroy(self):
        if self.rect.y >= screen_height + 300 :
            game.state = 'game_over'
        
    def update(self):
        self.rect.y += self.speed
        self.destroy()

def collisions_shot():
    hits = pygame.sprite.groupcollide(planets, player_shots, False, True)
    
    for planet in hits:
        if planet.type != 'DeathStar':          #Todes Stern soll unzerstörbar sein
            planet.health -= len(hits[planet])  #potentiell kan ein planet von mehreren schüssen getroffen werden sollte aber eigentlich nich vorkommen
        if planet.health <= 0:
            planet.kill()    
      
        
        
        
     

class GameState():

    def __init__(self,screen):
        self.state = 'intro'   
        self.screen = screen
        self.cut_scene1 = ct.CutScene1(screen)
        self.lanes = [i * 320 + 160 for i in range(6)]  # Planeten lanes so kontruiert das es keinen Deadspot gibt wo sich der Player verstecken könnte
        self.lane_cooldowns = {lane: randint(100,3000) for lane in self.lanes}
    def intro(self,events): 
        for event in events:           
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'stage_1' 
        #Start screen mit controls  
        screen.fill('lightblue')
        wasd_surf = pygame.font.SysFont(None,50).render('WASD to MOVE',None,50)
        wasd_rect = wasd_surf.get_rect(center=(screen.get_width()//2,300))
        screen.blit(wasd_surf,wasd_rect)
        howshoot_surf = pygame.font.SysFont(None,50).render('SPACE to Shoot',None,50)
        howshoot_rect = howshoot_surf.get_rect(center=(screen.get_width()//2,400))
        screen.blit(howshoot_surf,howshoot_rect)
        start_surf = pygame.font.SysFont(None,50).render('Press SPACE to start',None,50)
        start_rect = start_surf.get_rect(center=(screen.get_width()//2,600))
        screen.blit(start_surf,start_rect)
        
         
    def stage_1(self,events):
        current_time = pygame.time.get_ticks()
        for lane in self.lanes:
            if current_time > self.lane_cooldowns[lane]:
                planets.add(Planet_Storm(choice(['Mars', 'Saturn', 'Pluto', 'DeathStar']), lane))
                self.lane_cooldowns[lane] = current_time + randint(1000, 3000)
            
        collisions_shot()    

        screen.fill('lightblue')
        screen.blit(ground, (0,300))
        player.sprite.draw_custom()
        player.update()        
        cow.draw(screen)
        player_shots.draw(screen)
        player_shots.update()
        planets.draw(screen)
        planets.update()

    def game_over(self):
        planets.empty()
        self.state = 'intro'

    def state_manager(self,events):
        if self.state == 'intro':
            self.intro(events)
        if self.state == 'stage_1':
            self.stage_1(events)   
        if self.state == 'game_over':
            self.game_over()

#Background
ground = pygame.image.load('graphics/background/ground.png')
 
 


#Startups
pygame.init()
clock = pygame.time.Clock()

screen_widht = 1920
screen_height = 1080
cut_scene = None
#Skalliertes Noframe damit auch bei Windows der richtige Bildschirm gewählt wird 
screen = pygame.display.set_mode((screen_widht, screen_height), pygame.NOFRAME | pygame.SCALED, display = 0)
pygame.display.set_caption('Roli_The_Mudrunner_AOS')



game = GameState(screen)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
cow = pygame.sprite.GroupSingle()
cow.add(Milky_Sphere())
player_shots = pygame.sprite.Group()
planets = pygame.sprite.Group()
#Game Loop
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    #Updates
    game.state_manager(events)
    pygame.display.update()
    clock.tick(60)