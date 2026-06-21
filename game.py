# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pygame
from sys import exit
import os
import cut_scenes as ct
from random import randint, choices, choice
import webbrowser
#Spiel aus jedem directory sauber Startbar ;)
os.chdir(os.path.dirname(__file__))

#Entity Klasse
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
        self.pew_sound = pygame.mixer.Sound('audio/pew.mp3')
        self.pew_sound.set_volume(0.1)
        self.pew = [self.pew_sound,self.pew_sound,self.pew_sound] #falls ich dazu komme unterschiedlich pitche für abwechslung zu erstellen
        #Fahren
        self.gas_sound = pygame.mixer.Sound('audio/engine_gas.mp3')
        self.idle_sound = pygame.mixer.Sound('audio/engine_idle.mp3')
        self.engine_channel = pygame.mixer.Channel(0) #channel damit beim gas geben sounds direkt wechseln wrumm wrumm
        self.engine_channel.set_volume(0.2)
        self.current_engine_state = 'idle' #state damit sounds nicht permanet neustarten
    def player_movement(self):
        speed = 15                     #einfaches anpassen
        dx = 0
        dy = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]: dy -= 1   
        if keys[pygame.K_s]: dy += 1
        if keys[pygame.K_d]: dx += 1
        if keys[pygame.K_a]: dx -= 1

        if dx != 0 or dy != 0 and not (dy > 0 and dx == 0):         #Sound wechsel über dx dy sehr elegant
            if self.current_engine_state != 'gas':
                self.engine_channel.play(self.gas_sound, loops=-1 , fade_ms= 200)
                self.engine_channel.set_volume(0.1)
                self.current_engine_state = 'gas'       #beste möglichkeit ansonsten noch komplexeres channel System damit gas sound nicht immer abhackt
        elif self.current_engine_state != 'idle':       #und bei längerem idle trotzdem auch wieder von vorne startet 
            self.engine_channel.play(self.idle_sound, loops=-1, fade_ms= 200)
            self.engine_channel.set_volume(0.2) 
            self.current_engine_state = 'idle'
       
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

    def engine_reset(self):
        self.engine_channel.stop()    #niemand will den rasenmäher ewig hören
    #Health Funktionen
    def damage(self):
        if self.health > 0:
            self.health -= 1
            breacktrough.play()
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
                game.state = 'game_over_breacktrough' #ich hätte game states im Manager halten sollen und hier einfach true zurückgeben 
    
    #man kann Schuss Taste gedrückt halten da key.get_pressed 
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if pygame.mouse.get_pressed()[0] or pygame.key.get_pressed()[pygame.K_SPACE]:
            if current_time - self.last_shot_time >= self.shoot_cooldown:
                self.last_shot_time = current_time
                new_shot = Player_Shot(self.rect.center)
                player_shots.add(new_shot)
                choice(self.pew).play()
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
        self.fuel_consumption = 0.07
        self.consumed_fuel = 0
    def update(self):
        self.fuel -= self.fuel_consumption
        self.consumed_fuel = self.max_fuel - self.fuel
        if self.fuel <= 0:
            game.state = 'game_over_fuel'

    def draw_fuel(self,screen):
        fuel_text_surf = pygame.font.SysFont(None,50).render('Fuel',True,'red')
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
        self.shot1 = pygame.transform.scale_by(pygame.image.load('graphics/player/shot1.png'),2)
        self.shot2 = pygame.transform.scale_by(pygame.image.load('graphics/player/shot2.png'),2)
        self.shot = [self.shot1,self.shot2]
        self.animation_index = 0
        self.image = self.shot[self.animation_index]
        self.rect = self.image.get_rect(midbottom = pos) 
    def animation(self):
        self.animation_index += 0.07
        if self.animation_index >= len(self.shot):
            self.animation_index = 0
        self.image = self.shot[int(self.animation_index)]

    def update(self):
        self.rect.y -= 16   
        self.animation()           #Shotspeed
        if self.rect.bottom < -40:
            self.kill()

class Milky_Sphere(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load('graphics/cow/milky_sphere.png').convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(midbottom = (960,210))
        self.muh = pygame.mixer.Sound('audio/Muh.mp3')
        self.muh.set_volume(0.2)
        #movment
        self.x = 960
        self.y = 210
        self.target_x = self.x
        self.speed = 2
        self.gravity = 0
        self.angle = 0
        self.flip = False
        #wachsen
        self.scale_factor = 0.2
        self.growth_rate = 2/60/60/4

    def auch_einfach_mal_muh_machen(self,boolean = False):    #boolean damit am Ende immer Muh
        if randint(0,2000) == randint(0,2000) or boolean:   #doppel randint genau so nötig wie die function ;) 
            self.muh.play()
            self.gravity = -10
            self.angle = randint(-45,45)  #jetzt dreht sie sich noch dähmlich es ist perfekt
            if self.flip: self.flip = False
            else: self.flip = True

    def move_randomly(self):
        if abs(self.x - self.target_x) < 5:
            self.target_x = randint(300,screen_widht -300)
        if self.x < self.target_x:
            self.x += self.speed
        elif self.x > self.target_x:
            self.x -= self.speed
        self.rect.x = self.x

    def apply_gravity(self):
        self.gravity += 0.5
        self.y += self.gravity    #ja die kuh hat gravität damit si beim muhen springen kann
        if self.y >= 210:
            self.y = 210

    def grow(self):
        self.scale_factor += self.growth_rate
        if self.scale_factor > 5: self.scale_factor = 5
        self.image = pygame.transform.rotozoom(self.original_image,self.angle, self.scale_factor)
        if self.flip: self.image = pygame.transform.flip(self.image,True,False) 
        self.rect = self.image.get_rect(midbottom =(self.x,self.y))        
        
    def update(self):
        self.auch_einfach_mal_muh_machen() 
        self.move_randomly()
        self.grow()
        self.apply_gravity()

class Planet_Storm(pygame.sprite.Sprite):
    def __init__(self,type,):
        super().__init__()
        self.speed = 5  
        self.type = type        # genereller Speed um Spiel einfacher zu balancen 
        #Animations Variablen
        self.angle = 0
        self.rotation_speed = choice([randint(-3, -2), randint(2, 3)])  #keine berecihe um 0 damit sich immer dreht

        if type == 'Mars':
            self.original_image = pygame.transform.scale_by(pygame.image.load('graphics/planets/Mars.png').convert_alpha(),0.5)
            self.speed = self.speed * 1
            self.health = 2
        if type == 'Saturn':
            self.original_image = pygame.transform.scale_by(pygame.image.load('graphics/planets/Saturn.png').convert_alpha(),0.7)
            self.speed = self.speed * 1
            self.health = 2
        if type == 'Pluto':
            self.original_image = pygame.transform.scale_by(pygame.image.load('graphics/planets/Pluto.png').convert_alpha(),0.3)
            self.speed = self.speed * 1.4    
            self.health = 1                     #Pluto soll schnell aber leicht zerstöbar sein
            self.rotation_speed = int(self.rotation_speed * 2.5)         #und sich etwas schneller drehen                                  
        if type == 'DeathStar': 
            self.original_image= pygame.image.load('graphics/planets/DeathStar.png').convert_alpha()
            self.speed = self.speed * 0.2
            self.health = 5
            self.rotation_speed = 0     #DeatStar soll einfach nur reinschweben
        self.image = self.original_image #original image damit rotozoom bild qualität nicht zunehmend verschlechtert    
        self.rect = self.image.get_rect(bottomleft = (randint(100,screen_widht - 420), -200))   #Platz an den Rändern für Benzin anzeige

    def animate(self):                                                                               
        self.angle = (self.angle + self.rotation_speed) % 360
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1.0)
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)

    def destroy(self):                              #schaden wenn planet bildschirm verlässt
        if self.rect.y >= screen_height + 200:
            player.sprite.damage()
            self.kill()
            
            
        
    def update(self):
        self.rect.y += self.speed
        self.animate()
        self.destroy()


# Collisionen
def collisions_shot():
    hits = pygame.sprite.groupcollide(planets, player_shots, False, True)
    
    for planet in hits:
        if planet.type == 'DeathStar':
            metal.play()
        else: hit.play()    
        planet.health -= len(hits[planet])  #potentiell kan ein planet von mehreren schüssen getroffen werden sollte aber eigentlich nicht vorkommen können 
        if planet.health <= 0:
            if planet.type == 'DeathStar':
                willhelm.play()
            else: explode.play()
            spawn_chance = 15 + (fuel.consumed_fuel * 0.9)   #gößere Chance bei niedrigem Benzin stand mehr Spielspannung Base chance 15%
            if randint(0,100) <= spawn_chance:
                jerrycans.add(JerryCan(planet.rect.center))
            planet.kill()

def pickup_jerry():
    if pygame.sprite.spritecollide(player.sprite, jerrycans, True):
        fuel_pickup.play()
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
            return True

    def draw(self, screen):
        width = 30                          #Diesmal mit Parametern damit einfacher anpassbar        
        height = 600 
        x = screen_widht - 80 - width       #Selber abstand zum Rand wie Fuelbar
        y = 400                             #Bündig mit Fuelbar    
        prog_text_surf = pygame.font.SysFont(None,50).render(f"{self.name}",True,(0, 191, 255))
        prog_text_rect = prog_text_surf.get_rect(center = (x + width/2 ,y - 20))
        background_rect= prog_text_rect.inflate(20, 10) 
        pygame.draw.rect(screen, (80, 80, 80), background_rect, border_radius=5)  #Von Fuel übernommen
        screen.blit(prog_text_surf,prog_text_rect)            
        pygame.draw.rect(screen, (60, 60, 60), (x, y, width, height))
        pygame.draw.rect(screen, (0, 191, 255), (x, y + height - self.progress * height, width, int(height * self.progress)))
        pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height), 3)

class GameState():

    def __init__(self,screen):
        self.state = 'intro'   
        self.screen = screen
        self.cut_scene1 = ct.CutScene1(screen) 
        self.dt = 0  
        self.jingleplayed = False #nutzbar für Victory und Gameover jingle
        self.end_start_time = 0  
        self.rick_rolled = False # :P
    def intro(self,events): 
        for event in events:           
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.sprite.reset_shoot()
                self.progressbar = ProgressBar(120,'Stage 1','End')   #durch self im scope des gesamten GameState
                pygame.mixer_music.play(-1)
                self.jingleplayed = False # zurücksetzen nach game over
                self.state = 'stage_1' 
                player.sprite.engine_channel.play(player.sprite.idle_sound, loops=-1)
                player.sprite.engine_channel.set_volume(0.2)  
        #Start screen mit controls  
        screen.fill('lightblue')
        wasd_surf = font50.render('W-A-S-D to MOVE',True,50)
        wasd_rect = wasd_surf.get_rect(center=(screen.get_width()//2,300))
        screen.blit(wasd_surf,wasd_rect)
        howshoot_surf = font50.render('|SPACE| to Shoot',True,50)
        howshoot_rect = howshoot_surf.get_rect(center=(screen.get_width()//2,400))
        screen.blit(howshoot_surf,howshoot_rect)
        start_surf = font50.render('Press |SPACE| to start',True,50)
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

        screen.fill('black')  #canvas reset um ghosting quellen zu erkennen (damit erkannt das boden 33 pixel zu klein)
        #Background
        ground.update()
        ground.draw(screen)
        screen.blit(sky, (0,0)) #Sky nach ground damit überdeckt
        screen.blit(horizon,(0,0))
        #sprites und co
        player.sprite.draw_custom()
        player.update()        
        cow.draw(screen)
        cow.update()
        player_shots.draw(screen)
        player_shots.update()
        planets.draw(screen)
        planets.update()
       
        jerrycans.draw(screen)
        jerrycans.update()

        #Gui
        fuel.update()
        fuel.draw_fuel(screen)
        self.progressbar.draw(screen)

        if self.progressbar.update(self.dt):
            self.state = 'End'
            pygame.mixer_music.fadeout(1500) #damit am ende nicht die ganze zeit music weiter leuft 
            cow.sprite.auch_einfach_mal_muh_machen(True) #Das wichtigste am Ende muss gemuht werden ^-^
            self.end_start_time = pygame.time.get_ticks()

    def game_over(self):
        planets.empty()
        jerrycans.empty() #wieso zum hänker habe ich die gruppe jerrycans gennant und nicht auch fuel
        fuel.fuel = fuel.max_fuel                           #Player resets
        player.sprite.health = player.sprite.max_health
        pygame.mixer_music.fadeout(1500)   
        pygame.mixer.stop()
       
    
    def game_over_fuel(self,events):
        if not self.jingleplayed:
            self.game_over()
            nofuel_jingle.play()
            self.jingleplayed = True 
        for event in events:           
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'intro'

        screen.fill('lightblue')        
        out_of_fuel_surf = font100.render('You ran out of fuel',True,'black')
        out_of_fuel_rect = out_of_fuel_surf.get_rect(center = (screen_widht/2,200))
        screen.blit(out_of_fuel_surf,out_of_fuel_rect)
        fuel_tip_surf = font70.render('Try destroying Planets to get Fuel drops',True,'black')
        fuel_tip_rect = fuel_tip_surf.get_rect(center = (screen_widht/2,500))
        screen.blit(fuel_tip_surf,fuel_tip_rect)
        restart_surf = font50.render('Press |SPACE| to return to Menu',True,50)
        restart_rect = restart_surf.get_rect(center=(screen.get_width()//2,800))
        screen.blit(restart_surf,restart_rect)

    def game_over_breacktrough(self,events):
        if not self.jingleplayed:
            self.game_over()
            breacktrough_jingle.play()
            self.jingleplayed = True
        for event in events:           
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'intro'
        screen.fill('lightblue')        
        breacktrough_surf = font50.render('The Lecturehall was crushed by Planets',True,'black')
        breacktrough_rect = breacktrough_surf.get_rect(center = (screen_widht/2,200))
        screen.blit(breacktrough_surf,breacktrough_rect)
        breacktrough_tip_surf = pygame.font.SysFont(None,20).render('Just so you know: Roli seems not to care, if his Car gets Hit by a Planet',True,'black')
        breacktrough_tip_rect = breacktrough_tip_surf.get_rect(center = (screen_widht/2,500))
        screen.blit(breacktrough_tip_surf,breacktrough_tip_rect)
        restart_surf = font70.render('Press |SPACE| to return to Menu',True,50)
        restart_rect = restart_surf.get_rect(center=(screen.get_width()//2,800))
        screen.blit(restart_surf,restart_rect)

    def end(self):
        if not self.jingleplayed:
            self.game_over()
            end_jingle.play()
            self.jingleplayed = True
        screen.fill('lightblue')
        thx_surf = font100.render('Thank you for Playing',True,'black')
        thx_rect = thx_surf.get_rect(center = (screen_widht/2,200))
        screen.blit(thx_surf,thx_rect)
        success_surf = font50.render('Did Roli manage to save everyone from the falling Planets?',True,'black')
        success_rect = success_surf.get_rect(center = (screen_widht/2,400))
        screen.blit(success_surf,success_rect)
        plans1_surf = pygame.font.SysFont(None,20).render('Will there ever bee a next Stage?',True,'black')
        plans1_rect = plans1_surf.get_rect(center = (screen_widht/2,900))
        screen.blit(plans1_surf,plans1_rect)
        plans2_surf = pygame.font.SysFont(None,20).render('Probaly not :(      Only if i have waaaaaay to much spare time or i ever start studying Gamedesign',True,'black')
        plans2_rect = plans2_surf.get_rect(center = (screen_widht/2,940))
        screen.blit(plans2_surf,plans2_rect)

        current_time = pygame.time.get_ticks()
        if current_time - self.end_start_time >= 10000 and not self.rick_rolled:
            webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')  
            self.rick_rolled = True

    def state_manager(self,events):
        #Game
        if self.state == 'intro':
            self.intro(events)
        if self.state == 'stage_1':
            self.stage_1(events)   
        #Game Overs    
        if self.state == 'game_over':
            self.game_over()
        if self.state == 'game_over_fuel':
            self.game_over_fuel(events) 
        if self.state == 'game_over_breacktrough':
            self.game_over_breacktrough(events)       
        #Victory Royal    
        if self.state == 'End':
            self.end()
        
#Background Klassen/Funktionen
class RunningGround:               #Für fahr Illusion 
    def __init__(self, ):
        self.image = pygame.image.load('graphics/background/ground.png').convert() 
        self.speed = 10 
        self.img_height = self.image.get_height() 
        self.y1 = 33                          #Boden ist 33 Pixel zu klein deswegem geht nicht einfach mit scrren_height 
        self.y2 = self.y1 - self.img_height    #y1 und y2 damit wenn ein boden durchgelaufen ist der zweite nachschieben kann

    def update(self):
        self.y1 += self.speed
        self.y2 += self.speed

        if self.y1 >= screen_height:    
            self.y1 = self.y2 - self.img_height  #sauber aneinander hängen
        if self.y2 >= screen_height:
            self.y2 = self.y1 - self.img_height

    def draw(self, surface):
        surface.blit(self.image, (0, self.y1))
        surface.blit(self.image, (0, self.y2))

def create_shadow(image):
    mask = pygame.mask.from_surface(image)
    shadow = mask.to_surface(setcolor=(58, 12, 3), unsetcolor=(0, 0, 0, 0)) #ich habe am ende einfach ein horizont png erstellnt :/
    return shadow

#Startups
pygame.init()
clock = pygame.time.Clock()
screen_widht = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_widht, screen_height), pygame.NOFRAME) #Skalliertes Noframe damit auch bei Windows der richtige Bildschirm gewählt wird 
pygame.display.set_caption('Roli_The_Mudrunner_AOS')  #ja das Fensterchen hat ein Nämchen
cut_scene = None
last_fps_print_time = 0
pygame.mixer_music.load('audio/background_music.mp3')  #mixer_music damit nicht volll in arbeitsspeicher geladen wird
pygame.mixer_music.set_volume(0.1)
#Background
sky = pygame.image.load('graphics/background/sky.png')
horizon = pygame.image.load('graphics/background/horizon.png')
#Font
font50 = pygame.font.Font('fonts/VCR_OSD_MONO_1.001.ttf',50)
font100 = pygame.font.Font('fonts/VCR_OSD_MONO_1.001.ttf',100)
font70 = pygame.font.Font('fonts/VCR_OSD_MONO_1.001.ttf',70)
font20 = pygame.font.Font('fonts/VCR_OSD_MONO_1.001.ttf',20)
#Sounds
hit = pygame.mixer.Sound('audio/hit.wav')
hit.set_volume(0.1)
metal = pygame.mixer.Sound('audio/metall_hit.mp3')
metal.set_volume(0.2)
explode = pygame.mixer.Sound('audio/explode.wav')
explode.set_volume(0.1)
fuel_pickup = pygame.mixer.Sound('audio/gas_pickup.mp3')
fuel_pickup.set_volume(0.2)
willhelm = pygame.mixer.Sound('audio/willhelm.mp3')
willhelm.set_volume(0.2)
breacktrough = pygame.mixer.Sound('audio/breacktrough.mp3')
breacktrough.set_volume(0.08)
end_jingle = pygame.mixer.Sound('audio/victory.mp3')
end_jingle.set_volume(0.2)
breacktrough_jingle = pygame.mixer.Sound('audio/gameover_breacktrough.mp3')
breacktrough_jingle.set_volume(0.2)
nofuel_jingle = pygame.mixer.Sound('audio/gameover_fuel.mp3')
nofuel_jingle.set_volume(0.1)
#Klassen initialisieren
fuel = Fuel()
game = GameState(screen)
ground = RunningGround()
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
        print(f"FPS: {int(clock.get_fps())}")       #festgestellt ich muss dt für Progress timer nutzen da keine smoothen 60 fps 
        last_fps_print_time = current_time          #ich habe nur mehr code hinzugefügt und nun leuft es wieder mit 60fps ?!?!
                                                    #Problematisch das manch balancing von der framrate abhängt (Fuelbar)