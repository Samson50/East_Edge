import pygame, sys, random, story
from pygame.locals import *
from menu import *
from interaction import *
from characters import *
from images import *

fpsClock = pygame.time.Clock()
FPS = 70
##surface = pygame.display.set_mode((300,300))

class Controller(object):
    def __init__(self):
        self.surface = pygame.display.set_mode((300,300))
        #self.fpsClock = pygame.time.Clock()
        #self.FPS = (70)
        self.mode = "Menu"
        self.text_box = TextBox()
        self.menu = Menu(self.surface)
        self.cadet = Player(player_pack,28,16)
        self.rooms = ROOMS
        self.room = ROOMS[0]
        self.combat = CombatBox()
        self.width = 0
        self.fade_count = 0
        self.fade = pygame.image.load("surfaces/fade.png").convert()
        self.cut_scene_counter = 0

    def run(self):
        while True:
            while self.mode == "Moving":
                self.mode = self.room.getEvents(self.cadet, self.text_box, fpsClock, FPS, self.surface)
                self.room.display(self.surface, self.cadet)
                fpsClock.tick(FPS)

            while self.mode == "Menu":
                self.mode = self.menu.run()
                if self.mode == "Moving":
                    (self.room, self.cadet.x, self.cadet.y) = self.menu.start_game()
                fpsClock.tick(FPS)

            while self.mode == "Changing_Rooms":
                self.fade_count += 5
                if (self.fade_count < 255):
                    self.fade.set_alpha(self.fade_count)
                elif (self.fade_count == 255):
                    (self.room, self.cadet.x, self.cadet.y) = self.room.change_rooms(self.cadet.x, self.cadet.y, self.rooms)
                elif (self.fade_count > 255 and self.fade_count < 510):
                    self.fade.set_alpha(510 - self.fade_count)
                else:
                    self.mode = "Moving"
                    self.fade_count = 0
                self.surface = self.room.cheap_display(self.surface, self.cadet)
                self.surface.blit(self.fade, (0, 0))

                pygame.display.update()
                fpsClock.tick(FPS)

            if self.mode == "Cut_Scene":
                directions = cut_scenes[story.current_scene]
                self.cut_scene_counter = 0
            while self.mode == "Cut_Scene":
                step = directions[0][self.cut_scene_counter]
                for action in step.split(" "):

                    ##== Move NPC Action ==##
                    if action[0] == 'N':
                        change = action.split(":")
                        ## Move action
                        self.room.actionable[self.room.actionable.index(int(change[1]))] = int(change[2])
                        ## Move bound
                        del self.room.bounds[self.room.bounds.index(int(change[1]))]
                        self.room.bounds.append(int(change[2]))

                    ##== Move Player ==##
                    if action[0] == 'M':
                        d = action.split(":")[1]
                        if (d == "d"): self.cadet.move_down(self.room.width, self.room.bounds)
                        elif (d == "u"): self.cadet.move_up(self.room.width, self.room.bounds)
                        elif (d == "r"): self.cadet.move_right(self.room.width, self.room.bounds)
                        elif (d == "l"): self.cadet.move_left(self.room.width, self.room.bounds)

                    ##== Move NPC ==##
                    if action[0] in ["0", "1", "2", "3", "4", "5"]:
                        direction = action.split(":")
                        if (direction[1] == 'r' or direction[1] == 'l' or direction[1] == 'u' or direction[1] == 'd'):
                            self.room.non_player_characters[int(direction[0])].move(direction[1])
                        if (direction[1] == 'f'):
                            self.room.non_player_characters[int(direction[0])].look_at(int(direction[2]))

                    ##== Change Rooms ==##
                    if (action[0] == 'C'):
                        change = action.split(":")
                        while(self.fade_count < 510):
                            self.fade_count += 5
                            if (self.fade_count < 255):
                                self.fade.set_alpha(self.fade_count)
                            elif (self.fade_count == 255):
                                self.room = self.rooms[int(change[1])]
                                self.cadet.x = int(change[2])
                                self.cadet.y = int(change[3])
                            elif (self.fade_count > 255 and self.fade_count < 510):
                                self.fade.set_alpha(510 - self.fade_count)
                            else:
                                cut_change = False
                            self.surface = self.room.cheap_display(self.surface, self.cadet)
                            self.surface.blit(self.fade, (0, 0))

                            pygame.display.update()
                            fpsClock.tick(FPS)

                        self.fade_count = 0

                    ##== Do Things with Objects ==##
                    if (action[0] == 'O'):
                        stuff = action.split(":")
                        if action[1] == 'F':
                            if action[2] == 'R':
                                del self.room.fore_obj[(int(stuff[1]))]

                        #if action[1] == 'B':


                self.cut_scene_counter += 1

                if self.cut_scene_counter >= len(directions[0]):  # make 32 class variable
                    for clean_up in directions[1]:
                        self.room.actionable[clean_up[0]] = clean_up[2]
                        self.room.bounds.remove(clean_up[1])
                        self.room.bounds.append(clean_up[2])
                    self.mode = "Moving"

                self.surface = self.room.cheap_display(self.surface, self.cadet)
                pygame.display.update()

                fpsClock.tick(FPS)

            ###
            self.combat.set_up(0, self.cadet)
            while self.mode == "Fighting":
                self.combat.get_events()
                self.combat.show(self.surface, self.cadet)



pygame.init()

pygame.display.set_icon(pygame.image.load("sprites/decal/icon.png"))
pygame.display.set_caption("East Edge")
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
