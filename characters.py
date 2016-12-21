import pygame, random
from pygame.locals import *
from images import *
from interaction import *
from item import *

choice_0 = [pygame.image.load("sprites/decal/choices/0.png"), pygame.image.load("sprites/decal/choices/1.png"),
            pygame.image.load("sprites/decal/choices/2.png"), pygame.image.load("sprites/decal/choices/3.png")]
choice_1 = [pygame.image.load("sprites/decal/choices/4.png"), pygame.image.load("sprites/decal/choices/5.png")]


class Player:
    def __init__(self, spritePack, x, y):
        self.sprites = spritePack
        self.status_bar = pygame.image.load("sprites/status/status_bar.png")
        self.health = 100
        self.max_health = 100
        self.morale = 100
        self.max_morale = 100
        self.strength = 10
        self.eloquence = 10
        self.x = x
        self.y = y
        self.face = 0
        self.pace = 0
        self.items = [Potion("sprites/items/potion.png")]

    def status(self, surface):
        surface.blit(self.status_bar, (0, 0))

    def show(self, surface):
        self.pace = self.pace % 32
        if self.pace < 8:
            surface.blit((self.sprites[(self.face * 3)]), (139, 127))
        elif self.pace < 16:
            surface.blit((self.sprites[self.face * 3 + 1]), (139, 127))
        elif self.pace < 24:
            surface.blit((self.sprites[(self.face * 3)]), (139, 127))
        else:
            surface.blit((self.sprites[self.face * 3 + 2]), (139, 127))

    def move_up(self, width, bounds):
        self.face = 0
        if ((self.x + 139) / 32 + ((self.y - 2 + 139) / 32) * width) not in bounds and (
                        (self.x + 167) / 32 + ((self.y - 2 + 139) / 32) * width) not in bounds:
            self.y -= 2

    def move_down(self, width, bounds):
        self.face = 1
        if ((self.x + 139) / 32 + ((self.y + 2 + 168) / 32) * width) not in bounds and (
                        (self.x + 167) / 32 + ((self.y + 2 + 168) / 32) * width) not in bounds:
            self.y += 2

    def move_left(self, width, bounds):
        self.face = 2
        if ((self.x - 2 + 136) / 32 + ((self.y + 139) / 32) * width) not in bounds and (
                        (self.x - 2 + 136) / 32 + ((self.y + 167) / 32) * width) not in bounds:
            self.x -= 2

    def move_right(self, width, bounds):
        self.face = 3
        if ((self.x + 2 + 168) / 32 + ((self.y + 167) / 32) * width) not in bounds and (
                        (self.x + 2 + 168) / 32 + ((self.y + 139) / 32) * width) not in bounds:
            self.x += 2


class NPC:
    def __init__(self, spritePack, x, y, face, text_block):
        self.sprites = spritePack
        self.x = x
        self.y = y
        self.stationary = True
        self.face = face
        self.pose = 0
        self.block = 14
        self.text_block = text_block
        self.just_moved = True
        self.jm_counter = 0
        self.action = False
        self.message = ["", "", "", ""]

    def show_base(self):
        if self.pose == 0:
            return self.sprites.get(0, self.face * 3)
        elif self.pose < 8:
            return self.sprites.get(0, self.face * 3 + 1)
        else:
            return self.sprites.get(0, self.face * 3 + 2)

    def show_top(self):
        return self.sprites.get(1, self.face)

    def move(self, direction):
        if (direction != "s"):
            self.pose += 1
            if direction == "d":
                self.y += 2
                self.face = 1
            if direction == "u":
                self.y -= 2
                self.face = 0
            if direction == "l":
                self.x -= 2
                self.face = 2
            if direction == "r":
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
                self.face = random.randint(0, 3)
                self.just_moved = True
            self.stationary = True

    def interaction(self):
        return self.text

    def talk_to(self, text_box, fpsClock, FPS, surface):
        if (story.decisions[self.text_block.result] != -1):
            print self.text_block.result
            print self.text_block.next_text[0].text
            self.text_block = self.text_block.next_text[story.decisions[self.text_block.result]]
        text_box.message = [self.text_block.text[0], self.text_block.text[1], self.text_block.text[2],
                            self.text_block.text[3]]
        text_box.message_marker = 4
        mode = "Talking"
        while (mode == "Talking"):
            if (story.decisions[self.text_block.result] != -1):
                self.text_block = self.text_block.next_text[story.decisions[self.text_block.result]]
                text_box.message = [self.text_block.text[0], self.text_block.text[1], self.text_block.text[2],
                                    self.text_block.text[3]]
                text_box.message_marker = 4
            mode = text_box.getEvents(self.text_block)
            text_box.draw_text(surface, self.text_block)
            fpsClock.tick(FPS)
        return mode

    def look_at(self, face):
        self.pose = 0
        if face == 0:
            self.face = 1
        elif face == 1:
            self.face = 0
        elif face == 2:
            self.face = 3
        else:
            self.face = 2


class Combatant(NPC):
    def __init__(self, spritePack, x, y, face, text_block):
        NPC.__init__(self, spritePack, x, y, face, text_block)
        # TODO: get name from init arg
        self.name = "Johnson"
        self.result = 2
        self.escape_chance = 0
        self.health = 100
        self.max_health = 100
        self.morale = 100
        self.max_morale = 100
        self.helped = 0
        self.help_needed = 2
        self.NCOR_effect = 1
        self.strength = 8
        self.eloquence = 7
        self.target = 0
        self.analyzed = 3

    def escape_chance(self):
        return 1


class TextBlock:
    def __init__(self, text, choices, result, next_text):
        self.text = text
        self.choices = choices
        self.result = result
        self.next_text = next_text


class Blocker(NPC):
    def __init__(self, x, y, f):
        NPC.__init__(self, cadet_npc, x, y, f, blocker_text)


ginger1 = female_white_ginger
brown1 = female_white_brown

default_text = TextBlock(["This is the first line",
                           "This is the second line",
                           "This is the third line",
                           "This is the last line"], [], -1, [])

text_000 = ["Jake! There are some serious regs",
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
            "DCX FLO",
            "",
            "",
            ##
            ""]
text_010 = ["Okay, man. That's your decision.",
            "You made it, now you have to",
            "stick to it. A good leader is true",
            "to themselves and isn't afraid",
            ##
            "to make unpopular decisions. The",
            "worst thing you can do is be",
            "fake. People can smell a fake",
            "leader from miles away.",
            ##
            "CTS 001",
            "",
            "",
            ""]

blocker_text = TextBlock(["Sorry, bro.",
                           "You can't go this way yet.",
                           "...",
                           "..."], [], -1, [])
basic_blocker = Blocker(32, 64, 1)

blocker_001 = NPC(cadet_npc, 30, 156, 3, blocker_text)
blocker_002 = NPC(cadet_npc, 162, 156, 2, blocker_text)

# mother_home = NPC(SpritePack(mother),96,96,["Hey, Jake",
#                                            "Are you excited?",
#                                            "Ready to go to West Point?",
#                                            "DCX CTS 000"])
text_D = ["What?", "What do you still want?", "", ""]
empty_res = TextBlock(text_D, [], -1, [])

cadet_000 = NPC(white_rh_npc, 258, 96, 1, TextBlock(text_000, choice_0, 0, [
    TextBlock(text_010, choice_0, -2, [empty_res]),
    TextBlock(text_010, choice_0, -2, [empty_res]),
    TextBlock(text_010, choice_0, -2, [empty_res]),
    TextBlock(text_010, choice_0, -2, [empty_res]),
]))

text_001 = ["Hey, word spreads fast here. I",
            "heard what you said to Steve. You",
            "seem like a cool guy. I'm not",
            "about to hassle someone like you.",
            ###
            "CTS 002",
            "",
            "",
            ""]

text_002 = ["Hey, things get around pretty",
            "quick here and I heard what you",
            "said to Steve outside. I get it.",
            "You want do do the \' right thing\'",
            ###
            "You're still full of Kewl-Aid from",
            "Beast. I know how you feel, wanting",
            "to make sure that everything is",
            "Done by the book.",
            ###
            "That's what this is, right?",
            "DCX FLO",
            "",
            "",
            ###
            ""]

text_003 = ["Hey, I heard you told Steve outside",
            "that you were going to give everyone",
            "boards... Obviously you were kidding.",
            "Nobody is that crazy, right?",
            ##
            "Nobody is that crazy, right?",
            "DCX FLO",
            "",
            "",
            ##
            ""]

text_301 = ["Dude... what the fuck...",
            "",
            "",
            "",
            ##
            "ATK 001",
            "",
            "",
            ""]

text_302 = ["",
            "",
            "",
            ""]

text_004 = ["Fourth", "", "", ""]

text_005 = ["*Sigh* Well... I'm not about to",
            "just let someone like you walk into",
            " my company area with an attitude",
            "like that.",
            ###
            "ATK 001",
            "",
            "",
            ""]

text_006 = ["Okay, cool. Just remember that",
            "you don't have to do everything",
            "by the book to be a good leader.",
            "It's about the people.",
            ##
            "CTS 002",
            "",
            "",
            ""]

# Create texts 007 - 009
text_007 = ["Morale response.",
            "",
            "",
            "",
            ##
            "CTS 002",
            "",
            "",
            ""]

text_008 = ["Leading response.",
            "",
            "",
            "",
            ##
            "CTS 002",
            "",
            "",
            ""]

text_009 = ["Fighting response.",
            "",
            "",
            "",
            ##
            "CTS 003",
            "",
            "",
            ""]

cadet_001 = Combatant(black_npc, 34, 64, 1, TextBlock(text_001, choice_0, 0, [
    TextBlock(text_001, [], 1, [empty_res]),
    TextBlock(text_002, choice_1, 1, [
        TextBlock(text_005, [], 2, [
            TextBlock(text_007, [], 3, [empty_res]),
            TextBlock(text_008, [], 3, [empty_res]),
            TextBlock(text_009, [], 3, [empty_res])
        ]),
        TextBlock(text_006, [], 2, [empty_res])
    ]),
    TextBlock(text_003, [
        TextBlock(text_301, [], 1, [empty_res]),
        TextBlock(text_302, [], 1, [empty_res])
    ], 1, [empty_res]),
    TextBlock(text_004, [], 1, [empty_res])
]))
