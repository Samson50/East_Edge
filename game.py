import pygame, sys, random, story, shelve
from pygame.locals import *
from menu import *
from interaction import *
from characters import *
from images import *
from pause import *

fpsClock = pygame.time.Clock()
FPS = 70
##surface = pygame.display.set_mode((300,300))

class Controller(object):
    def __init__(self):
        self.surface = pygame.display.set_mode((300,300))
        self.mode = "Menu"
        self.menu = Menu(self.surface, fpsClock)
        self.cadet = Player(player_pack,28,16)
        self.rooms = ROOMS
        self.room = ROOMS[0]
        self.width = 0
        self.fade_count = 0
        self.fade = fade.convert()
        self.cut_scene_counter = 0
        self.saves = self.load_saves()

    def run(self):
        while True:

            while self.mode == "Menu":
                self.mode = self.menu.run(fpsClock, self.cadet)
                fpsClock.tick(FPS)


    def intro(self):
        counter = 0
        current_image = sumgai_logo
        cx = 100
        cy = 100
        while (counter < 135):

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            if counter < 30:
                self.fade.set_alpha(255 - 255/29*counter)

            if counter == 30: self.fade.set_alpha(0)

            if counter > 74 and counter < 105:
                self.fade.set_alpha(255/29*(counter%75))

            if counter == 105:
                current_image = emblem
                cx = 2; cy = 16
                self.fade.set_alpha(255)

            if counter > 110:
                self.fade.set_alpha(255 - 255/29*(counter%110))

            counter += 1
            self.surface.blit(current_image,(cx,cy))
            self.surface.blit(self.fade,(0,0))
            fpsClock.tick(30)
            pygame.display.update()

    def load_saves(self):
        slot1 = shelve.open("saves/slot1")
        slot2 = shelve.open("saves/slot2")
        slot3 = shelve.open("saves/slot3")
        slots = [slot1, slot2, slot3]
        loads = [0, 0, 0]

        for slot in [0,1,2]:
            try:
                if slots[slot]["file"] == "no_save":
                    loads[slot] = 0
                else:
                    loads[slot] = 1
                slots[slot].close()
            except KeyError:
                slots[slot]["file"] = "no_save"
                slots[slot].close()
                loads[slot] = 0
        return loads





pygame.init()

pygame.display.set_icon(icon)
pygame.display.set_caption("East Edge")
#pygame.mixer.music.load("8-bit-Detective/detective.wav")
#pygame.mixer.music.play(-1,0.0)
#pygame.mixer.music.set_volume(0.1)
game = Controller()
#game.intro()
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
