import pygame, sys
import characters
import story
from pygame.locals import *



##== Cut-Scenes ==##
m_o = [["00:d"]*16+["00:r"]*16+["00:d"]*48+["00:r"]*16+["00:d"]*32+["00:r"]*16+["C:2:64:56"],[]]
s_00 = [["M:d"]*17+["M:u"]+["00:d"]*16+["00:l"]*16+["00:f:2"]+["N:62:79"], []]
s_01 = [["M:r"]*16+["01:d"]*28+["01:r"]*16+["01:d"]*32+["01:l"]*18+["01:f:2"]+["N:13:37"], []]

cut_scenes = [m_o,s_00,s_01]


class TextBox:
    def __init__(self):
        self.text = []
        self.message = ["", "", "", ""]
        self.text_box = pygame.image.load("sprites/decal/textBox.png")
        self.font = pygame.font.Font(None, 20)
        self.message_marker = 0
        self.decision_marker = 0
        self.yes = pygame.image.load("sprites/decal/yes.png")
        self.no = pygame.image.load("sprites/decal/no.png")
        self.decision = pygame.image.load("sprites/decal/decision.png")

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
                    print story.current_scene
                    return "Cut_Scene"
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
                    else:
                        self.message[i] = text_block.text[self.message_marker]
                        self.message_marker += 1
        return "Talking"



