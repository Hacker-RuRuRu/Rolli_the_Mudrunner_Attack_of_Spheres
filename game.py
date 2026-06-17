import pygame
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()



#Game Loop
while True:

    #Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()