import pygame, sys
from pygame.locals import *
from room_data import *

class Menu:
    def __init__(self, surface):
        self.surface = surface
        self.menu = pygame.image.load("sprites/decal/emblem.png")
        self.play_button = pygame.image.load("sprites/decal/play_button.png")

    def run(self):
        self.surface.fill((0,0,0))

        self.surface.blit(self.menu, (2, 16))
        self.surface.blit(self.play_button, (25,225))

        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


        if pygame.mouse.get_pressed()[0]:
            if mouse_x > 25 and mouse_x < 125 and mouse_y > 225 and mouse_y < 275:
                return "Moving"
            else:
                return "Menu"
        else:
            return "Menu"

    def start_game(self):
        #self.room = home_main
        #self.width = 13 #self.cadet.x = 0; self.cadet.y = 32
        # return room, x, and y
        return (home_main, 0, 32)