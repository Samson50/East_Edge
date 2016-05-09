import pygame, sys, time
from pygame.locals import *
from images import *
from characters import *
from room_data import *

class Display(object):
    def __init__(self,surface):
        self.screen = surface
        self.fade_count = 0
        self.fade = pygame.image.load("surfaces/fade.png").convert()
        pygame.display.set_caption('Game')
        self.rooms = ROOMS
        ##====Menu Elements====##
        self.menu = pygame.image.load("sprites/decal/emblem.png")
        self.mouse = pygame.image.load("sprites/decal/mouse.png")
        self.play_button = pygame.image.load("sprites/decal/play_button.png")

        ##====Room Elements====##
        self.room = home_main

        ##====Position Elements====##
        self.x = 28; self.y = 16
        self.X = 5; self.Y = 5; self.width = 9
        self.mode = "moving"; self.pace = 0; self.face = 1

        ##====Text Variables====##
        self.text = []; self.message = ["",""]; self.text_box = pygame.image.load("surfaces/textbox.png")
        self.font = pygame.font.Font(None, 20); self.message_marker = 0

        ##=====Dis is You======##
        self.cadet = Player(SpritePack(cadet_other),28,16)

    def display(self):

        self.screen.fill((0,0,0))

        self.screen.blit(self.room.background, (-self.cadet.x, -self.cadet.y+10))

        for img in self.room.back_obj:
            self.screen.blit(img[0], (img[1]-self.cadet.x, img[2]-self.cadet.y))

        for cdt in self.room.non_player_characters:
            self.screen.blit(cdt.show(),(cdt.x-self.cadet.x, cdt.y-self.cadet.y))

        self.screen.blit(self.cadet.show(self.pace), (139, 131))

        for img in self.room.fore_obj:
            self.screen.blit(img[0], (img[1]-self.cadet.x, img[2]-self.cadet.y))

        if self.mode == "changing_rooms":
            self.fade_count += 5
            if (self.fade_count == 510):
                self.mode = "moving"
                self.fade_count = 0
            elif (self.fade_count > 255):
                self.fade.set_alpha(510-self.fade_count)
            elif (self.fade_count == 255):
                (self.room,self.cadet.x,self.cadet.y,self.width) = self.room.change_rooms(self.cadet.x,self.cadet.y,self.width,self.rooms)
            elif (self.fade_count < 255):
                self.fade.set_alpha(self.fade_count)
            self.screen.blit(self.fade,(0,0))

        if self.mode == "talking":
            self.screen.blit(self.text_box,(10,200))
            self.draw_text()

        pygame.display.update()

    def getEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_f:
                self.action()

        buttons = pygame.key.get_pressed()
        if self.mode == "moving":
            if buttons[pygame.K_UP] or buttons[pygame.K_DOWN] or buttons[pygame.K_LEFT] or buttons[pygame.K_RIGHT]:
                self.move(buttons)
            else: self.pace = 0
            for guy in self.room.non_player_characters:
                guy.move()

        if ((self.cadet.x+139)/32+((self.cadet.y+139)/32)*self.width) in self.room.exits:
            self.mode = "changing_rooms"

    def move(self,buttons):

        if (buttons[pygame.K_UP]):
            self.cadet.move_up(self.width, self.room.bounds)

        if (buttons[pygame.K_DOWN]):
            self.cadet.move_down(self.width, self.room.bounds)

        if (buttons[pygame.K_LEFT]):
            self.cadet.move_left(self.width, self.room.bounds)

        if (buttons[pygame.K_RIGHT]):
            self.cadet.move_right(self.width, self.room.bounds)
        #print "(x,y): ("+str((self.cadet.x+139)/32)+","+str((self.cadet.y+139)/32)+")"
        #print "(x,y): ("+str(self.cadet.x)+","+str(self.cadet.y)+")"

        self.pace += 1
        if self.pace == 16: self.pace =0

    def action(self):
        if self.mode == "moving":
            X = (self.cadet.x+149)/32
            Y = (self.cadet.y+145)/32
            if self.cadet.face == 0:
                # print(str(X+(Y-1)*self.width))
                if (X+(Y-1)*self.width) in self.room.actionable:
                    self.mode = "talking"
                    i = self.room.actionable.index(X+(Y-1)*self.width)
                    self.room.non_player_characters[i].look_at(self.face)
                    self.text = self.room.non_player_characters[i].interaction()

            elif self.cadet.face == 1:
                if (X+(Y+1)*self.width) in self.room.actionable:
                    self.mode = "talking"
                    i = self.room.actionable.index(X+(Y+1)*self.width)
                    self.room.non_player_characters[i].look_at(self.face)
                    self.text = self.room.non_player_characters[i].interaction()
                    #self.update_message()

            elif self.cadet.face == 2:
                if (X-1+Y*self.width) in self.room.actionable:
                    self.mode = "talking"
                    i = self.room.actionable.index(X-1+Y*self.width)
                    self.room.non_player_characters[i].look_at(self.face)
                    self.text = self.room.non_player_characters[i].interaction()
                    #self.update_message()

            else:
                if (X+1+Y*self.width) in self.room.actionable:
                    self.mode = "talking"
                    i = self.room.actionable.index(X+1+Y*self.width)
                    self.room.non_player_characters[i].look_at(self.face)
                    self.text = self.room.non_player_characters[i].interaction()
                    #self.update_message()

        if self.mode == "talking":
            self.update_message()

    def draw_text(self):
        delta = 0
        for line in self.message:
            text_object = self.font.render(line, 1, (0,0,0))
            text_rect = text_object.get_rect()
            text_rect.topleft = (30,210+delta)
            delta += 20
            self.screen.blit(text_object, text_rect)

    def update_message(self):
        if (self.message_marker == len(self.text)):
            self.message_marker = 0
            self.mode = "moving"
        elif (self.message_marker == len(self.text)-1):
            self.message[0] = self.text[self.message_marker]
            self.message[1] = ""
            self.message_marker += 1
        else:
            self.message[0] = self.text[self.message_marker]
            self.message_marker += 1
            self.message[1] = self.text[self.message_marker]
            self.message_marker += 1

    def run_menu(self):
        self.screen.fill((0,0,0))

        self.screen.blit(self.menu, (2, 16))
        self.screen.blit(self.play_button, (25,225))

        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        #self.screen.blit(self.mouse, (mouse_x,mouse_y))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


        if pygame.mouse.get_pressed()[0]:
            if mouse_x > 25 and mouse_x < 125 and mouse_y > 225 and mouse_y < 275:
                return "Play"
            else:
                return "Menu"
        else:
            return "Menu"

    def start_game(self):
        self.room = home_main
        self.width = 13; self.cadet.x = 0; self.cadet.y = 32



