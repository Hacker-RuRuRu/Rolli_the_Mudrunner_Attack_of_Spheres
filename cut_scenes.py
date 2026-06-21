

#Hier liegen die Treume meines versuchs einen Cutscenesmanagers so bauen
#damals war ich noch nicht sehr geübt im umgang mit der Gameloop und wie man mit ihr Zeit und updates verwaltet :(



import pygame

def animate_text(screen, text, size , color, x, y, font_path, start_time):      
    
    font = pygame.font.Font(font_path, size)
    
    char_timer = pygame.time.get_ticks() - start_time
    chars_to_show = int(char_timer // 50)
                                                        #text erscheint wie getippt auf bildschirm
    animated_text = text[0:chars_to_show] 

    text_surface = font.render(animated_text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

    return chars_to_show >= len(text)     #true wenn text vorbei sonst false 

def animate_box(screen,side,box_y,character_surf=None):
    
    master_surface = pygame.Surface((screen.get_width(), 400))
    master_surface.fill((0,0,0))
    if character_surf is not None:
        master_surface.blit(character_surf,(screen.get_width()//8, 200))  #sprech boxen am oberen und unterem bildschirm rand + Icon einblendung
    master_rect = master_surface.get_rect(bottomleft = (0,0))
    if side == "top":
        
        screen.blit(master_surface,(master_rect.x,box_y))
            
class CutScene1:

    def __init__(self, screen):
        
    
        self.active = True
        self.step = 0
        self.text = {
            1 : "Roli: Whats that on the Horizon?",
            2 : "Roli: From my Scanners i would say its aproximatly a Milk filled Sphere",
            3 : "????: MUUHHH...MUUHH!!!! Muhh",
            4 : "Tanslatesystem activated",
            5 : "Cow : HOW DARE YOU CALL ME SPHERE?! IM CLEARLY A COW!!!",
            6 : "Cow : Im going to beat some Manners into your pattern recognizing brain!",
            7 : "Roli: I cant let any of these Planets hit my Students!"     #Vorstellen es wird auf dem Beamer gespielt und Roli verdeidigt den Hörsaal 
        }
        self.skip_timer = 0
        self.screen = screen
        self.top_box_y = -400
        self.bottom_box_y = screen.get_height()

    def skip(self,events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.step +=1
    
    def hard_skip(self,events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.skip_timer = pygame.time.get_ticks()
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                if pygame.time.get_ticks - self.skip_timer > 5000:
                    self.active = False       
    
    
    def update(self,events):

        self.skip(events)  
        self.hard_skip(events)
        if self.active:
            if self.step == 0:  
                if self.top_box_y < 400: 
                    animate_box(self.screen, "top" ,self.bottom_box_y)
                    self.bottom_box_y += 8
                


   

  