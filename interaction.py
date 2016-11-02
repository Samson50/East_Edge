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
        self.font = pygame.font.Font(None, 20)
        self.text_box = img_text_box
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
            if ("DCX" in self.message[i]):
                if ("CTX" in self.message[i]):
                    story.decisions[text_block.result] = self.decision_marker
                    story.current_scene = int(self.message[i].split(" ")[2])
                    self.message_marker = 0
                    self.message = ["","","",""]
                    return "Cut_Scene"
                elif ("FLO" in self.message[i]):
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
                        story.opponent = int(text_block.text[self.message_marker].split(" ")[1])
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

class Attack(Choice):
    def __init__(self):
        Choice.__init__(self,act_attack, 79-act_attack.get_width()/2, 207)

    def run(self,opponent):
        print "ATTACK!!!"


class NCOR(Choice):
    def __init__(self):
        Choice.__init__(self, act_NCOR, 213-act_NCOR.get_width()/2, 207)

    def run(self,opponent):
        print "YOU ARE BAD!!!"


class Lead(Choice):
    def __init__(self):
        Choice.__init__(self, act_lead, 79-act_lead.get_width()/2, 252)

    def run(self,opponent):
        print "Inspired!!!"


class Help(Choice):
    def __init__(self):
        Choice.__init__(self, act_help, 213-act_help.get_width()/2, 252)

    def run(self,opponent):
        print "Empathy :)"


class CombatBox:
    def __init__(self):
        self.background = combat_surface
        self.pointer = combat_decision
        self.decision = 0
        self.level = 0
        self.i = 0; self.j = 0
        self.levels = [self.i, self.j]
        self.mode = "Fighting"
        self.display_mode = "choose"
        self.response = [[],[]]
        self.choices = [Choice(choice_act,47,207),
                        Choice(choice_analyze,142,207),
                        Choice(choice_item,34,252),
                        Choice(choice_leave,170,252)]
        self.acts = [Attack(),NCOR(),Lead(),Help()] #list of players action classes
        self.text_box = combat_text
        self.text = []
        self.message = ["", "", "", ""]
        self.message_marker = 0
        self.font = pygame.font.Font(None, 20)
        self.temp_items = []

    def set_up(self,opponent,cadet):
        cadet.face = 1
        cadet.pose = 9
        self.opponent = opponent
        self.opponent.look_at(0)
        self.mode = "Fighting"
        self.cadet = cadet
        self.items = cadet.items ## TODO add items to cadet class

    def analyze(self):
        first = [0,["You take a moment and try to","analyze the situation","",""]]
        first += [[],["You notice some thing","","","","ATE"]]
        return first

    def leave(self):
        ## Generate Randomly
        escape = 0
        if escape < self.opponent.escape_chance:
            return [0,["You try to leave","","",""],[],["You leave the opponent confused.","","","","ATE"]]
        else:
            return [0,["You try to leave...","","",""],[],["But you can't get away that easily!","","","","ATE"]]

    def update_message(self):
        if self.response[0] == 0:
            if self.text == []: self.text = self.response[1]
        else:
            if self.text == []: self.text = self.response[3]
        for i in range(0, 4):
            if self.message_marker == len(self.text):
                self.message_marker = 0
                self.text = []
                self.message = ["","","",""]
                self.response[0] += 1
                break
            else:
                if ("ATE" in self.text[self.message_marker]):
                    self.display_mode = "choose"
                    self.message_marker = 0
                    self.text = []
                    self.message = ["","","",""]
                    self.level = 0
                    self.decision = 0
                    break
                else:
                    self.message[i] = self.text[self.message_marker]
                    self.message_marker += 1


    def get_events(self,surface):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_LEFT: self.decision -= 1
                if event.key == K_RIGHT: self.decision += 1

                if event.key == K_f:
                    if self.display_mode == "choose":
                        if self.level == 0:
                            ## Analyze
                            if self.decision == 1:
                                self.response = self.analyze()
                                self.display_mode = "action"
                                self.update_message()
                            ## Leave
                            if self.decision == 3:
                                self.response = self.leave()
                                self.display_mode = "action"
                                self.update_message()

                            else:
                                self.levels[self.level] = self.decision
                                self.level += 1
                                self.decision = 0

                        elif self.level == 1:
                            ## ACT
                            if self.levels[0] == 0:
                                self.response = self.acts[self.decision].run(self.opponent)
                                self.display_mode = "action"
                                self.update_message()
                            ## Items
                            if self.levels[0] == 2:
                                self.response = self.items[self.decision].run()
                                self.display_mode = "action"
                                self.update_message()

                    elif self.display_mode == "action":
                        if self.response[0] == 0 or self.response[0] == 2:
                            self.update_message()
                        if self.response[0] == 1:
                            self.response[0] += 1

                if event.key == K_d:
                    if self.level > 0 : self.level -= 1
                    self.decision = 0

        self.decision %= 4
        return self.mode

    def show(self, surface,cadet):
        surface.blit(self.background, (0,0))

        if self.display_mode == "choose":
            surface.blit(cadet.sprites[10], (55,110))

            surface.blit(self.opponent.show_base(), (155,110))

            if self.level == 0:
                surface.blit(self.pointer, (14 + (self.decision % 2) * 137, 198 + (self.decision / 2) * 45))
                for choice in self.choices:
                    choice.show(surface)

            if self.level == 1:
                if self.levels[0] == 0:
                    surface.blit(self.pointer, (14 + (self.decision % 2) * 137, 198 + (self.decision / 2) * 45))
                    for action in self.acts:
                        action.show(surface)

                if self.levels[0] == 2:
                    surface.blit(img_items, (12,196))
                    surface.blit(item_decision, (15 + (self.decision % 8) * 34, 206 + (self.decision / 8) * 34))
                    for item in range(0,len(self.items)):
                        self.items[item].show(surface,15+(item%8)*34,199+(item/8)*34)



        if self.display_mode == "action":
            if self.response[0] == 0:
                surface.blit(self.text_box, (4,188))
                delta = 0
                for line in self.message:
                    text_object = self.font.render(line, 1, (255, 255, 255))
                    text_rect = text_object.get_rect()
                    text_rect.topleft = (30, 210 + delta)
                    delta += 20
                    surface.blit(text_object, text_rect)

            elif self.response[0] == 1:
                print "parse self.response[2]"
                self.response[0] = 2
                self.update_message()

            elif self.response[0] == 2:
                surface.blit(self.text_box, (4, 188))
                delta = 0
                for line in self.message:
                    text_object = self.font.render(line, 1, (255, 255, 255))
                    text_rect = text_object.get_rect()
                    text_rect.topleft = (30, 210 + delta)
                    delta += 20
                    surface.blit(text_object, text_rect)

        print self.response[0]

        pygame.display.update()



