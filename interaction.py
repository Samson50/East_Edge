import pygame, sys
import characters
from pygame.locals import *



##== Cut-Scenes ==##
m_o = [["00:d"]*16+["00:r"]*16+["00:d"]*48+["00:r"]*16+["00:d"]*32+["00:r"]*16+["C:2:64,64"],[[0,42,123]]]

cut_scenes = [m_o]

class TextBox:
    def __init__(self, surface):
        self.surface = surface
        self.text = []
        self.message = ["", ""]
        self.text_box = pygame.image.load("surfaces/textbox.png")
        self.font = pygame.font.Font(None, 20)
        self.message_marker = 0
        self.decision_marker = 0
        self.yes = pygame.image.load("sprites/decal/yes.png")
        self.no = pygame.image.load("sprites/decal/no.png")
        self.decision = pygame.image.load("sprites/decal/decision.png")

    def getEvents(self, text):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_f:
                return self.update_message(text)

            if event.type == KEYDOWN and event.key == K_RIGHT:
                self.decision_marker += 1
            if event.type == KEYDOWN and event.key == K_LEFT:
                self.decision_marker -= 1
            self.decision_marker = self.decision_marker%2
        return "Talking"

    def draw_text(self, surface):
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
            surface.blit(self.yes,(56,225))
            surface.blit(self.no, (160,225))
            surface.blit(self.decision, (56+104*self.decision_marker,225))

        pygame.display.update()

    def update_message(self, text):
        if ("DCX" in self.message[1]):
            if ("CTS" in self.message[1]):
                if self.decision_marker == 0:
                    self.cut_scene_active = True
                    self.cut_scene_counter = 0
                    self.message = ["", ""]
                    return "Cut_Scene"
                    ##if self.message_marker >= len(self.text)-1:
                    ##    self.message_marker = 0
                    ##    self.message = ["",""]
                else:
                    self.message_marker = 0
                    self.message = ["", ""]
                    return "Moving"
            else:
                if (self.message_marker == len(text)):
                    self.message_marker = 0
                    self.message = ["", ""]
                    return "Moving"
                elif (self.message_marker == len(text)-1):
                    self.message[0] = text[self.message_marker]
                    self.message[1] = ""
                    self.message_marker += 1
                else:
                    self.message[0] = text[self.message_marker]
                    self.message_marker += 1
                    self.message[1] = text[self.message_marker]
                    self.message_marker += 1
                    return "Talking"
        else:
            if (self.message_marker == len(text)):
                self.message_marker = 0
                self.message = ["",""]
                return "Moving"
            elif (self.message_marker == len(text)-1):
                self.message[0] = text[self.message_marker]
                self.message[1] = ""
                self.message_marker += 1
                return "Talking"
            else:
                self.message[0] = text[self.message_marker]
                self.message_marker += 1
                self.message[1] = text[self.message_marker]
                self.message_marker += 1
                return "Talking"
