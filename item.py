import pygame, sys, random
from pygame.locals import *

class Item:
    def __init__(self, icon):
        self.icon = pygame.image.load(icon)

    def show(self, surface, x, y):
        surface.blit(self.icon, (x,y))

class Potion(Item):
    def __init__(self, icon):
        Item.__init__(self, icon)

    def run(self, cadet, opponent):
        cadet.health += 10
        cadet.health  = min(cadet.health,cadet.max_health)









