import pygame
from pygame.locals import *

class Cutscene:
    def __init__(self, surface, name, actions, NPCs, timer):
        self.surface = surface
        self.name = name
        self.act = actions
        self.NPCs = NPCs
        self.timer = timer
    def run(self):
        count = 0
        while (count < self.timer):
            for NPC in self.NPCs:
                NPC.cutscene(self.name)
                self.surface.blit(NPC.show(),NPC.position())
            pygame.display.update()
