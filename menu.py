import pygame, sys
from pygame.locals import *
from room_data import *
from images import *

class Menu:
    def __init__(self, surface):
        self.surface = surface
        self.menu = emblem
        self.play_button = play_button
        self.logo = logo

    def run(self):
        self.surface.fill((0,0,0))
        self.surface.blit(self.menu, (2, 16))
        self.surface.blit(self.logo, (0,0))
        self.surface.blit(self.play_button, (20,230))
        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if pygame.mouse.get_pressed()[0]:
            if mouse_x > 20 and mouse_x < 120 and mouse_y > 230 and mouse_y < 280:
                return "Moving"
            else:
                return "Menu"
        else:
            return "Menu"

    def start_game(self):
        #self.room = home_main
        #self.width = 13 #self.cadet.x = 0; self.cadet.y = 32
        # return room, x, and y
        return (sally_port, 160, 160)