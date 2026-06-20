import pygame
from sys import exit
import os
import cut_scenes as ct
from random import randint, choices
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
        
        #Leben
        self.health = 3
        self.max_health = 3
        self.heart_image = pygame.transform.scale_by(pygame.image.load('graphics/assets/heart.png'), 2)
        # Schiesen
        self.last_shot_time = 0   
        self.shoot_cooldown = 500

    def player_movement(self):
        speed = 15                     #einfaches anpassen
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
    #Health Funktionen
    def damage(self):
        if self.health > 0:
            self.health -= 1

    def heal(self):                         #falls ich eine mechanic einbaue die Leben gibt
        if self.health < self.max_health:
            self.health += 1

    def draw_health(self):
        for i in range(self.max_health):
            heart_rect = self.heart_image.get_rect(midbottom = (160, 1000 - i * 80))   #bottom rect damit bündig mid fuelbar abschließt 
            if i < self.health: self.heart_image.set_alpha(255)
            else:  self.heart_image.set_alpha(70)       # halb dursichtige herzen (kommt von ki ich wollte ursprünglich einfach nur graue herzen 
            screen.blit(self.heart_image,heart_rect)    # dahinter setzen und habe methode gesucht ohne ein neues bild laden zu müssen)

    def die(self):
        if self.health <= 0:
                game.state = 'game_over'
    #man kann Schuss Taste gedrückt halten da key.get_pressed 

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if pygame.mouse.get_pressed()[0] or pygame.key.get_pressed()[pygame.K_SPACE]:
            if current_time - self.last_shot_time >= self.shoot_cooldown:
                self.last_shot_time = current_time
                new_shot = Player_Shot(self.rect.center)
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
        self.die()
        self.draw_health()

class Fuel():
    def __init__(self):
        self.max_fuel = 100       
        self.fuel = 100           
        self.fuel_consumption = 0.1
        self.consumed_fuel = 0
    def update(self):
        self.fuel -= self.fuel_consumption
        self.consumed_fuel = self.max_fuel - self.fuel
        if self.fuel <= 0:
            game.state = 'game_over'

    def draw_fuel(self,screen):
        fuel_text_surf = font50.render('Fuel',True,'red')
        fuel_text_rect = fuel_text_surf.get_rect(center = (95,380))
        background_rect= fuel_text_rect.inflate(20, 10) 
        pygame.draw.rect(screen, (80, 80, 80), background_rect, border_radius=5)  #Backround damit fuel lesbar leicht abgerundet
        screen.blit(fuel_text_surf,fuel_text_rect)
        pygame.draw.rect(screen, (60, 60, 60), (80, 400, 30, 600))
        bar_color = (255, 0, 0) if self.fuel < 30 else (0, 255, 0) #rot wenn benzinstand niedrig
        pygame.draw.rect(screen, bar_color, (80, 400 + self.consumed_fuel * 6, 30,600 - int(self.consumed_fuel * 6))) #int da sonst lästiger 1 Pixel grauer streifen
        pygame.draw.rect(screen, (0, 0, 0), (80, 400, 30, 600), 3)

class JerryCan(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.jerrycan = pygame.transform.scale_by(pygame.image.load('graphics/assets/BenzinKanister.png'),0.5)
        self.image = self.jerrycan
        self.rect = self.image.get_rect(center = pos)
    def update(self):
        self.rect.y += 5            #Fallspeed
        if self.rect.top > screen_height + 100:
            self.kill()
                                       
class Player_Shot(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.shot = pygame.image.load('graphics/player/shot.png')
        self.image = self.shot
        self.rect = self.image.get_rect(midbottom = pos) 
    def update(self):
        self.rect.y -= 16              #Shotspeed
        if self.rect.bottom < -40:
            self.kill()

class Milky_Sphere(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.milky_sphere = pygame.image.load('graphics/cow/milky_sphere.png').convert_alpha()
        self.image = self.milky_sphere
        self.rect = self.image.get_rect(center = (960,200))

class Planet_Storm(pygame.sprite.Sprite):
    def __init__(self,type,):
        super().__init__()
        self.speed = 5  
        self.type = type        # genereller Speed um Spiel einfacher zu balancen 
        
        if type == 'Mars':
            self.image = pygame.image.load('graphics/planets/Mars.png').convert_alpha()
            self.speed = self.speed * 1
            self.health = 2
        if type == 'Saturn':
            self.image = pygame.image.load('graphics/planets/Saturn.png').convert_alpha()
            self.speed = self.speed * 1
            self.health = 2
        if type == 'Pluto':
            self.image = pygame.transform.scale_by(pygame.image.load('graphics/planets/Pluto.png').convert_alpha(),0.2)
            self.speed = self.speed * 1.4    
            self.health = 1                                               #Pluto soll schnell aber leicht zerstöbar sein
        if type == 'DeathStar': 
            self.image = pygame.image.load('graphics/planets/DeathStar.png').convert_alpha()
            self.speed = self.speed * 0.2
            self.health = 5
        self.rect = self.image.get_rect(bottomleft = (randint(100,screen_widht - 420), -200))   #Platz an den Rändern für Benzin anzeige
        
    def destroy(self):                              #schaden wenn planet bildschirm verlässt
        if self.rect.y >= screen_height + 200:
            player.sprite.damage()
            self.kill()
            
            
        
    def update(self):
        self.rect.y += self.speed
        self.destroy()


# Collisionen
def collisions_shot():
    hits = pygame.sprite.groupcollide(planets, player_shots, False, True)
    
    for planet in hits:
        planet.health -= len(hits[planet])  #potentiell kan ein planet von mehreren schüssen getroffen werden sollte aber eigentlich nicht vorkommen können 
        if planet.health <= 0:
            spawn_chance = 15 + (fuel.consumed_fuel * 0.9)   #gößere Chance bei niedrigem Benzin stand mehr Spielspannung Base chance 15%
            if randint(0,100) <= spawn_chance:
                jerrycans.add(JerryCan(planet.rect.center))
            planet.kill()

def pickup_jerry():
    if pygame.sprite.spritecollide(player.sprite, jerrycans, True):
        fuel.fuel += 20
        if fuel.fuel >= fuel.max_fuel:
            fuel.fuel = fuel.max_fuel    #fuel nicht über max
                     

      
        
        
#Game Managing Klassen  
class ProgressBar:
    def __init__(self, duration, name, next_state):
        self.end_time = duration * 1000     # Dauer von Sekunden in Millisekunden (z.B. 200 * 1000)
        self.current_time = 0
        self.progress = 0.0                 
        self.name = name
        self.next_state = next_state

    def update(self, dt):             
        if self.current_time < self.end_time:
            self.current_time += dt                         #dt damit unabhängig von FPS
            self.progress = self.current_time / self.end_time
        else:
            self.progress = 1.0
            game.state = self.next_state 

    def draw(self, screen):
        width = 30                          #Diesmal mit Parametern damit einfacher anpassbar        
        height = 600 
        x = screen_widht - 80 - width       #Selber abstand zum Rand wie Fuelbar
        y = 400                             #Bündig mit Fuelbar                
        pygame.draw.rect(screen, (60, 60, 60), (x, y, width, height))
        pygame.draw.rect(screen, (0, 191, 255), (x, y + height - self.progress * height, width, int(height * self.progress)))
        pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height), 3)
class GameState():

    def __init__(self,screen):
        self.state = 'intro'   
        self.screen = screen
        self.cut_scene1 = ct.CutScene1(screen) 
        self.dt = 0  
    def intro(self,events): 
        for event in events:           
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.progressbar = ProgressBar(120,'Stage 1','End')   #durch self im scope des gesamten GameState
                self.state = 'stage_1' 
        #Start screen mit controls  
        screen.fill('lightblue')
        wasd_surf = font50.render('WASD to MOVE',True,50)
        wasd_rect = wasd_surf.get_rect(center=(screen.get_width()//2,300))
        screen.blit(wasd_surf,wasd_rect)
        howshoot_surf = font50.render('SPACE to Shoot',True,50)
        howshoot_rect = howshoot_surf.get_rect(center=(screen.get_width()//2,400))
        screen.blit(howshoot_surf,howshoot_rect)
        start_surf = font50.render('Press SPACE to start',True,50)
        start_rect = start_surf.get_rect(center=(screen.get_width()//2,600))
        screen.blit(start_surf,start_rect)
        
         
    def stage_1(self,events):
        for event in events:           
            if event.type == planet_timer:
                planets.add(Planet_Storm(choices(['Mars', 'Saturn', 'Pluto', 'DeathStar'], weights=[35, 35, 20, 10])[0]))  
                progress_modifier = self.progressbar.progress * 900   #Gewichtet auswahl damit Pluto und DeathStar etwas seltener
                planet_modifier = len(planets.sprites()) * (150 - self.progressbar.progress*150)
                min_time = int(1500 - progress_modifier + planet_modifier) 
                max_time = int(3000 - progress_modifier + planet_modifier)  
                pygame.time.set_timer(planet_timer,randint(min_time,max_time))  #dynamische Spawnzeit schneller mit Progress langsamer wenn zu viele Planeten
        #collisions    
        collisions_shot()    
        pickup_jerry()

        #Background
        screen.fill('lightblue')
        screen.blit(ground, (0,300))
        #sprites und co
        player.sprite.draw_custom()
        player.update()        
        cow.draw(screen)
        player_shots.draw(screen)
        player_shots.update()
        planets.draw(screen)
        planets.update()
       
        jerrycans.draw(screen)
        jerrycans.update()

        #Gui
        fuel.update()
        fuel.draw_fuel(screen)
        self.progressbar.update(self.dt)
        self.progressbar.draw(screen)
    def game_over(self):
        planets.empty()
        fuel.fuel = fuel.max_fuel                           #Player resets
        player.sprite.health = player.sprite.max_health   
        self.state = 'intro'

    def end(self):
        screen.fill('lightblue')
        thx_surf = font100.render('Thank you for Playing',True,'black')
        thx_rect = thx_surf.get_rect(center = (screen_widht/2,200))
        screen.blit(thx_surf,thx_rect)
        success_surf = font70.render('Did Roli manage to save everyone from the falling Planets?',True,'black')
        success_rect = success_surf.get_rect(center = (screen_widht/2,400))
        screen.blit(success_surf,success_rect)
        plans1_surf = font20.render('Will there ever bee a next Stage?',True,'black')
        plans1_rect = plans1_surf.get_rect(center = (screen_widht/2,900))
        screen.blit(plans1_surf,plans1_rect)
        plans2_surf = font20.render('Probaly not :(      Only if i have waaaaaay to much spare time or i ever start studying Gamedesign',True,'black')
        plans2_rect = plans2_surf.get_rect(center = (screen_widht/2,940))
        screen.blit(plans2_surf,plans2_rect)
    def state_manager(self,events):
        if self.state == 'intro':
            self.intro(events)
        if self.state == 'stage_1':
            self.stage_1(events)   
        if self.state == 'game_over':
            self.game_over()
        if self.state == 'End':
            self.end()
#Background
ground = pygame.image.load('graphics/background/ground.png')
 
 


#Startups
pygame.init()
clock = pygame.time.Clock()
screen_widht = 1920
screen_height = 1080
cut_scene = None
last_fps_print_time = 0
#Font
font50 = pygame.font.SysFont(None,50)
font100 = pygame.font.SysFont(None,100)
font70 = pygame.font.SysFont(None,70)
font20 = pygame.font.SysFont(None,20)
#Skalliertes Noframe damit auch bei Windows der richtige Bildschirm gewählt wird 
screen = pygame.display.set_mode((screen_widht, screen_height), pygame.NOFRAME)
pygame.display.set_caption('Roli_The_Mudrunner_AOS')

#Klassen initialisieren
fuel = Fuel()
game = GameState(screen)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
cow = pygame.sprite.GroupSingle()
cow.add(Milky_Sphere())
player_shots = pygame.sprite.Group()
planets = pygame.sprite.Group()
jerrycans = pygame.sprite.Group()

#Timer
planet_timer = pygame.USEREVENT + 1
pygame.time.set_timer(planet_timer,1000)

#Game Loop
while True:
    #Gamestate unabhängige Events  (vielleicht noch Pausescreen)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    #Updates
    game.state_manager(events)
    pygame.display.update()
    dt = clock.tick(60)
    game.dt = dt   #dt abfangen und weiterleiten damit echtzeit berechnung der progressbar
    current_time = pygame.time.get_ticks()
    if current_time - last_fps_print_time >= 500:  
        print(f"FPS: {int(clock.get_fps())}")       #festgestellt ich muss dt für Progress timer nuten da keine smoothen 60 fps
        last_fps_print_time = current_time