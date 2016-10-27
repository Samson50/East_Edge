import pygame, sys
import characters
import story
from pygame.locals import *
from images import *



##== Cut-Scenes ==##
m_o = [["00:d"]*16+["00:r"]*16+["00:d"]*48+["00:r"]*16+["00:d"]*32+["00:r"]*16+["C:2:64:56"],[]]
s_00 = [["M:d"]*17+["M:u"]+["00:d"]*16+["00:l"]*16+["00:f:2"]+["N:62:79"], []]
s_01 = [["M:r"]*16+["01:d"]*28+["01:r"]*16+["01:d"]*32+["01:l"]*18+["01:f:2"]+["N:13:37"], []]

cut_scenes = [m_o,s_00,s_01]


class TextBox:
    def __init__(self):
        self.text = []
        self.message = ["", "", "", ""]
        self.text_box = img_text_box
        self.font = pygame.font.Font(None, 20)
        self.message_marker = 0
        self.decision_marker = 0
        self.yes = img_yes
        self.no = img_no
        self.decision = img_decision

    def getEvents(self, text_block):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_f:
                return self.update_message(text_block)

            if event.type == KEYDOWN and event.key == K_RIGHT:
                self.decision_marker += 1
            if event.type == KEYDOWN and event.key == K_LEFT:
                self.decision_marker -= 1
            self.decision_marker = self.decision_marker%4
        return "Talking"

    def draw_text(self, surface, text_block):
        surface.blit(self.text_box, (10, 200))
        delta = 0
        if (not "DCX" in self.message[1]):
            for line in self.message:
                text_object = self.font.render(line, 1, (0,0,0))
                text_rect = text_object.get_rect()
                text_rect.topleft = (30,210+delta)
                delta += 20
                surface.blit(text_object, text_rect)
        else:
            text_object = self.font.render(self.message[0], 1, (0,0,0))
            text_rect = text_object.get_rect()
            text_rect.topleft = (30,210)
            surface.blit(text_object, text_rect)
            i = 0
            for choice in text_block.choices:
                surface.blit(choice, (15+(i%2)*140,230+(i/2)*30))
                i += 1
            surface.blit(self.decision, (50+140*(self.decision_marker%2),235+(self.decision_marker/2)*30))

        pygame.display.update()

    def update_message(self, text_block):
        for i in range(0,4):
            print self.message[i]
            if ("DCX" in self.message[i]):
                print "here"
                if ("CTX" in self.message[i]):
                    story.decisions[text_block.result] = self.decision_marker
                    story.current_scene = int(self.message[i].split(" ")[2])
                    self.message_marker = 0
                    self.message = ["","","",""]
                    return "Cut_Scene"
                elif ("FLO" in self.message[i]):
                    print "here"
                    story.decisions[text_block.result] = self.decision_marker
                    self.message_marker = 0
                    self.message = ["","","",""]
                    return "Talking"

                else:
                    story.decisions[text_block.result] = self.decision_marker
                    self.message_marker = 0
                    self.message = ["", "", "", ""]
                    return "Moving"

            else:
                if (self.message_marker == len(text_block.text)):
                    self.message_marker = 0
                    self.message = ["","","",""]
                    return "Moving"
                else:
                    if ("CTS" in text_block.text[self.message_marker]):
                        story.decisions[text_block.result] = 0
                        story.current_scene = int(text_block.text[self.message_marker].split(" ")[-1])
                        self.message_marker = 0
                        self.message = ["", "", "", ""]
                        return "Cut_Scene"
                    elif ("ATK" in text_block.text[self.message_marker]):
                        story.decisions[text_block.result] = 0
                        self.message_marker = 0
                        self.message = ["","","",""]
                        return "Fighting"
                    else:
                        self.message[i] = text_block.text[self.message_marker]
                        self.message_marker += 1
        return "Talking"


class Choice:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y

    def show(self, surface):
        surface.blit(self.image, (self.x, self.y))


class CombatBox:
    def __init__(self):
        self.background = combat_surface
        self.pointer = img_decision
        self.decision = 0
        self.level = 0
        self.i = 0; self.j = 0
        self.levels = [self.i, self.j]
        self.mode = "Fighting"
        self.choices = [Choice(choice_act,47,207),
                        Choice(choice_analyze,142,207),
                        Choice(choice_item,34,252),
                        Choice(choice_leave,170,252)]
        self.acts = [] #list of players action classes

    def set_up(self,opponent,cadet):
        cadet.face = 1
        cadet.pose = 9
        self.opponent = opponent
        self.mode = "Fighting"
        self.cadet = cadet
        self.items = cadet.items ## TODO add items to cadet class

    def analyze(self):
        print "working"

    def leave(self):
        print "working"

    def get_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_LEFT: self.decision -= 1
                if event.key == K_RIGHT: self.decision += 1

                if event.key == K_f:
                    if self.level == 0:
                        self.levels[self.level] = self.decision
                        self.level += 1

                    elif self.level == 1:
                        if self.levels[0] == 0:
                            self.acts[self.decision].run() ## TODO implement acts

                        if self.levels[0] == 1:
                            self.analyze()

                        if self.levels[0] == 2:
                            self.items[self.decision].run() ## TODO implement items

                        if self.levels[0] == 3:
                            self.leave()

                if event.key == K_d:
                    if self.level > 0 : self.level -= 1

        self.decision %= 4
        return self.mode

    def show(self, surface,cadet):
        surface.blit(self.background, (0,0))

        surface.blit(cadet.sprites[10], (20,150))

        if self.level == 0:
            for choice in self.choices:
                choice.show(surface)

        surface.blit(self.pointer, (47 + (self.decision%2)*142, 207 + (self.decision/2)*45))

        if self.level == 1:
            if self.levels[0] == 0:
                print "actions"

            if self.levels[0] == 2:
                print "items"

        pygame.display.update()



