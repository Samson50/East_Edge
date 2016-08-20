import pygame, random
from pygame.locals import *
from images import *

cadet_male = [["sprites/character_packs/cadet_male/"],['b-s.png','b-l.png','b-r.png',   # back = 0
                                                      'f-s.png','f-l.png','f-r.png',    # front= 1
                                                      'l-s.png','l-l.png','l-r.png',    # left = 2
                                                      'r-s.png','r-l.png','r-r.png']]  # right= 3

cadet_other = [["sprites/character_packs/cadet_other/"],['b-s.png','b-l.png','b-r.png',   # back = 0
                                                      'f-s.png','f-l.png','f-r.png',    # front= 1
                                                      'l-s.png','l-l.png','l-r.png',    # left = 2
                                                      'r-s.png','r-l.png','r-r.png']]  # right= 3

mother = [["sprites/character_packs/mother/"],['b-s.png','b-l.png','b-r.png',   # back = 0
                                                      'f-s.png','f-l.png','f-r.png',    # front= 1
                                                      'l-s.png','l-l.png','l-r.png',    # left = 2
                                                      'r-s.png','r-l.png','r-r.png']]

class SpritePack:
    def __init__(self, spritesList):
        self.sprites = []
        for img in spritesList[1]:
            self.sprites.append(pygame.image.load(spritesList[0][0]+img))
    def __getitem__(self, i):
        return self.sprites[i]

class Player:
    def __init__(self, spritePack, x, y):
        self.sprites = spritePack
        self.health = 100
        self.x = x
        self.y = y
        self.face = 0
        self.pace = 0

    def show(self):
        self.pace = self.pace%16
        if self.pace == 0:
            return (self.sprites[(self.face*3)])
        elif (self.pace < 8):
            return (self.sprites[(self.face*3+1)])
        else:
            return (self.sprites[self.face*3+2])

    def move_up(self, width, bounds):
        self.face = 0
        if ((self.x+139)/32+((self.y-2+139)/32)*width) not in bounds and ((self.x+167)/32+((self.y-2+139)/32)*width) not in bounds:
                self.y -= 2
    def move_down(self, width, bounds):
        self.face = 1
        if ((self.x+139)/32+((self.y+2+167)/32)*width) not in bounds and ((self.x+167)/32+((self.y+2+167)/32)*width) not in bounds:
            self.y += 2
    def move_left(self, width, bounds):
        self.face = 2
        if ((self.x-2+139)/32+((self.y+139)/32)*width) not in bounds and ((self.x-2+139)/32+((self.y+167)/32)*width) not in bounds:
            self.x -= 2
    def move_right(self, width, bounds):
        self.face = 3
        if ((self.x+2+167)/32+((self.y+167)/32)*width) not in bounds and ((self.x+2+167)/32+((self.y+139)/32)*width) not in bounds:
            self.x += 2


class NPC:
    def __init__(self, spritePack, x, y, text):
        self.sprites = spritePack
        self.x = x; self.y = y
        self.stationary = True
        self.face = 0; self.pose = 0
        self.block = 14
        self.text = text
        self.just_moved = True; self.jm_counter = 0
        self.action = False

    def show(self):
        if self.pose == 0:
            return (self.sprites[(self.face*3)])
        elif (self.pose < 8):
            return (self.sprites[(self.face*3+1)])
        else:
            return (self.sprites[self.face*3+2])

    def move(self,direction):
        if (direction != "s"):
            self.pose += 1
            if (direction == "d"):
                self.y += 2
                self.face = 1
            if (direction == "u"):
                self.y -= 2
                self.face = 0
            if (direction == "l"):
                self.x -= 2
                self.face = 2
            if (direction == "r"):
                self.x += 2
                self.face = 3
            self.pose = self.pose % 16
        else:
            if self.just_moved:
                self.jm_counter += 1
                if self.jm_counter > 100:
                    self.just_moved = False
                    self.jm_counter = 0
            else:
                self.face = random.randint(0,3)
                self.just_moved = True
            self.stationary = True

    def interaction(self):
        return self.text

    def look_at(self,face):
        if face == 0: self.face  = 1
        elif face == 1: self.face = 0
        elif face == 2: self.face = 3
        else: self.face = 2


default_text = ["This is the first line",
                "This is the second line",
                "This is the third line",
                "This is the last line"]

basic_blocker = NPC(SpritePack(cadet_other),32,64,["Sorry, bro.",
                                                   "You can't go this way yet."])

mother_home = NPC(SpritePack(mother),96,96,["Hey, Jake",
                                            "Are you excited?",
                                            "Ready to go to West Point?",
                                            "DCX CTS 000"])

