import pygame, random
from pygame.locals import *
from images import *
from interaction import *

choice_0 = [pygame.image.load("sprites/decal/choices/0.png"),pygame.image.load("sprites/decal/choices/1.png"),pygame.image.load("sprites/decal/choices/2.png"),pygame.image.load("sprites/decal/choices/3.png")]

#cadet_male = [["sprites/character_packs/cadet_male/"],['b-s.png','b-l.png','b-r.png',   # back = 0
#                                                      'f-s.png','f-l.png','f-r.png',    # front= 1
#                                                      'l-s.png','l-l.png','l-r.png',    # left = 2
#                                                      'r-s.png','r-l.png','r-r.png']]  # right= 3

cadet_other = [["sprites/character_packs/cadet_other/"],['b-s.png','b-l.png','b-r.png',   # back = 0
                                                      'f-s.png','f-l.png','f-r.png',    # front= 1
                                                      'l-s.png','l-l.png','l-r.png',    # left = 2
                                                      'r-s.png','r-l.png','r-r.png']]

cadet_NPC = [["sprites/character_packs/cadet_other/"],['b-s.png','b-l.png','b-r.png',   # back = 0
                                                      'f-s.png','f-l.png','f-r.png',    # front= 1
                                                      'l-s.png','l-l.png','l-r.png',    # left = 2
                                                      'r-s.png','r-l.png','r-r.png'],  # right= 3
                                                     ['b.png','f.png','l.png','r.png']]

#mother = [["sprites/character_packs/mother/"],['b-s.png','b-l.png','b-r.png',   # back = 0
#                                                      'f-s.png','f-l.png','f-r.png',    # front= 1
#                                                      'l-s.png','l-l.png','l-r.png',    # left = 2
#                                                      'r-s.png','r-l.png','r-r.png']]

class SpritePack_NPC:
    def __init__(self, spritesList):
        self.sprites = [[],[]]
        for img in spritesList[1]:
            self.sprites[0].append(pygame.image.load(spritesList[0][0]+img))
        for img in spritesList[2]:
            self.sprites[1].append(pygame.image.load(spritesList[0][0]+"front/"+img))
    def get(self, j, i):
        return self.sprites[j][i]

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
        self.status_bar = pygame.image.load("sprites/status/status_bar.png")
        self.health = 100
        self.x = x
        self.y = y
        self.face = 0
        self.pace = 0

    def status(self, surface):
        surface.blit(self.status_bar, (0, 0))

    def show(self, surface):
        self.pace = self.pace%32
        if self.pace < 8:
            surface.blit((self.sprites[(self.face*3)]), (139, 127))
        elif (self.pace < 16):
            surface.blit((self.sprites[self.face*3+1]), (139, 127))
        elif (self.pace < 24):
            surface.blit((self.sprites[(self.face*3)]), (139, 127))
        else:
            surface.blit((self.sprites[self.face*3+2]), (139, 127))

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

# TODO: Add Current_TEXT int and next_TEXT list
class NPC:
    def __init__(self, spritePack, x, y, face, text_block):
        self.sprites = spritePack
        self.x = x; self.y = y
        self.stationary = True
        self.face = face; self.pose = 0
        self.block = 14
        self.text_block = text_block
        self.just_moved = True; self.jm_counter = 0
        self.action = False
        self.message = ["","","",""]

    def show_base(self):
        if self.pose == 0:
            return (self.sprites.get(0, (self.face*3)))
        elif (self.pose < 8):
            return (self.sprites.get(0, (self.face*3+1)))
        else:
            return (self.sprites.get(0,self.face*3+2))

    def show_top(self):
        return self.sprites.get(1, self.face)

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

    def talk_to(self, text_box, fpsClock, FPS, surface):
        if (story.decisions[self.text_block.result] != -1):
            self.text_block = self.text_block.next_text[story.decisions[self.text_block.result]]
        text_box.message = [self.text_block.text[0], self.text_block.text[1], self.text_block.text[2], self.text_block.text[3]]
        text_box.message_marker = 4
        mode = "Talking"
        while (mode=="Talking"):
            mode = text_box.getEvents(self.text_block)
            text_box.draw_text(surface, self.text_block)
            fpsClock.tick(FPS)
        return mode

    def look_at(self,face):
        self.pose = 0
        if face == 0: self.face  = 1
        elif face == 1: self.face = 0
        elif face == 2: self.face = 3
        else: self.face = 2




text_000    = ["Jake! There are some serious regs",
               "violations going down in the",
               "barracks! I know you're just a",
               "plebe, but some day, you will be a",
               ##
               "leader! You will have graduated",
               "from East Edge! The greatest",
               "academy in the entire world!",
               "",
               ##
               "So, how will you handle it?",
               "DCX CTX 001",
               "",
               "",
               ##
               ""]

class Text_Block:
    def __init__(self, text, choices, result, next_text):
        self.text = text
        self.choices = choices
        self.result = result
        self.next_text = next_text

default_text = Text_Block(["This is the first line",
                           "This is the second line",
                           "This is the third line",
                           "This is the last line"],[],-1,[])

class Blocker(NPC):
    def __init__(self, x, y, f):
        NPC.__init__(self, SpritePack_NPC(cadet_NPC),x,y,f,blocker_text)

blocker_text = Text_Block(["Sorry, bro.",
                          "You can't go this way yet.",
                          "...",
                          "..."], [],-1,[])
basic_blocker = Blocker(32,64,1)

blocker_001 = NPC(SpritePack_NPC(cadet_NPC),30,156,3,blocker_text)
blocker_002 = NPC(SpritePack_NPC(cadet_NPC),130,156,2,blocker_text)

#mother_home = NPC(SpritePack(mother),96,96,["Hey, Jake",
#                                            "Are you excited?",
#                                            "Ready to go to West Point?",
#                                            "DCX CTS 000"])
text_D = ["What?","What do you still want?","",""]
empty_res = Text_Block(text_D,[],-1,[])

cadet_000 = NPC(SpritePack_NPC(cadet_NPC),258,96,1,Text_Block(text_000,choice_0,0,[empty_res,empty_res,empty_res,empty_res]))

text_001 = ["Hey, word spreads fast here. I",
            "heard what you said to Steve. You",
            "seem like a cool guy. I'm not",
            "about to hassle someone like you.",
            ###
            "CTS 002",
            "",
            "",
            ""]

text_002 = ["Second","","",""]
text_003 = ["Third","","",""]
text_004 = ["Fourth","","",""]

cadet_001 = NPC(SpritePack_NPC(cadet_NPC),34,64,1,Text_Block(text_001,choice_0,0,[
                                                            Text_Block(text_001,[],1,[empty_res]),
                                                            Text_Block(text_002,[],1,[empty_res]),
                                                            Text_Block(text_003,[],1,[empty_res]),
                                                            Text_Block(text_004,[],1,[empty_res])]))