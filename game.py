import pygame, sys, random
from pygame.locals import *
from characters import *
from images import *
from display import *



class Controller(object):
    def __init__(self):
        self.surface = pygame.display.set_mode((300,300))
        self.display = Display(self.surface)
        self.fpsClock = pygame.time.Clock()
        self.FPS = (70)
        self.mode = "Menu"

    def run(self):
        while True:
            while self.mode == "Play":
                self.display.getEvents()
                self.display.display()
                self.fpsClock.tick(self.FPS)

            while self.mode == "Menu":
                self.mode = self.display.run_menu()
                if self.mode == "Play":
                    self.display.start_game()



pygame.init()
game = Controller()
game.run()
"""
class PLAYER:
    def __init__(self, spritePack):
        self.x = 0
        self.y = 0
        self.X = 0
        self.Y = 0
        self.sprites = spritePack

    def show(self):
        return (self.sprites[0])

    def position(self):
        return (self.x, self.y)

class NPC:
    def __init__(self, spritePack, x, y, type):
        self.sprite = spritePack
        self.x = x
        self.y = y
        self.type = type

    def move(self):
        if (self.type == 0):
            ## stationary
            return
        if (self.type == 1):
            ## small range
            return
        if (self.type == 2):
            ## roaming
            return
        if (self.type == 3):
            ## approach Player
            return

    def interact(self):
        ## what happens when player interacts
        return

class Image:
    def __init__(self, src = "surfaces/menu.png", X = 0, Y = 0):
        self.src = pygame.image.load(src)
        self.X = X
        self.Y = Y


class SpritePack:
    def __init__(self, spritesList):
        self.sprites = []
        for img in spritesList[1]:
            self.sprites.append(Image(spritesList[0][0]+img,0,0))
    def __getitem__(self, i):
        return self.sprites[i]

class Sprites(pygame.sprite.RenderUpdates):
    def sprites(self):
        return sorted(self.spritedict.keys(),
                      key=lambda sprite: getattr(sprite, "depth", 0))

class Display(object):
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.size = self.screen.get_width(), self.screen.get_height()
        self.windows = Sprites()
        self.clock = pygame.time.Clock()
        self.back = Image()
        self.mid  = []
        self.fore = []

    def display(self, cadet):
        self.screen.blit(self.back.src, (self.back.X, self.back.Y))
        for pic in self.mid:
            self.screen.blit(pic.src, (pic.X, pic.Y))
        self.screen.blit(cadet.show(), (cadet.position()))
        for pic in self.fore:
            self.screen.blit(pic.src, (pic.X, pic.Y))


    def newRoom(self, room):
        self.back = room.back
        self.mid  = room.mid
        self.fore = room.fore

    def update(self):
        self.windows.clear(self.screen, self.windows_background)
        self.windows.update()


class Room:
    def __init__(self, roomData):
        self.back = Image(roomData[0])
        self.mid  = []
        for pic in roomData[1]:
            self.mid.append(Image(pic))
        self.fore = []
        for pic in roomData[2]:
            self.fore.append(Image(pic))
        self.bounds = roomData[3]
        self.NPCs = roomData[4]
        self.width = roomData[5]

class Game(object):
    def __init__(self):
        self.display = Display()

    def run(self):
        self.running = True

        while self.running:
            self.display.update()
            self.display.tick()

CADET = PLAYER(SpritePack(cadet_male))
BACKGROUND = Display()
"""