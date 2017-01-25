import pygame, random
from pygame.locals import *
from images import *
from interaction import *
from item import *

choice_0 = [choice_000, choice_001,
            choice_002, choice_003]
choice_1 = [choice_004, choice_005]


class Player:
    def __init__(self, spritePack, x, y):
        self.sprites = spritePack
        self.status_bar = status_bar
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
        self.items = [Potion(potion)]

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
        if self.pose < 8:
            return self.sprites.get(0, self.face * 3)
        elif self.pose < 16:
            return self.sprites.get(0, self.face * 3 + 1)
        elif self.pose < 24:
            return self.sprites.get(0, self.face * 3)
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
            self.pose %= 32
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
        return "Yeah, I have no idea what this is uspposed to do" #self.text

    def talk_to(self, text_box, fpsClock, FPS, surface, cadet):
        backdrop = pygame.transform.smoothscale(surface, (300,300))
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
                text_box.current_pointer = 0
            mode = text_box.getEvents(self.text_block, cadet)
            text_box.draw_text(surface, self.text_block, backdrop)
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

default_text = TextBlock(["This is the first line",
                           "This is the second line",
                           "This is the third line",
                           "This is the last line"], [], -1, [])

blocker_text = TextBlock(["Sorry, bro.",
                           "You can't go this way yet.",
                           "...",
                           "..."], [], -1, [])

class Blocker(NPC):
    def __init__(self, x, y, f):
        NPC.__init__(self, cadet_npc, x, y, f, blocker_text)




