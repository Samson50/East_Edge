import pygame, sys
from pygame.locals import *
from characters import *

#   when entering room [-44,-256,6,12]
class Room:
    def __init__(self,background,back_obj,fore_obj,bounds,exits,entrance,adjacent,non_player_characters,actionable,width):
        self.background = background
        self.back_obj = back_obj
        self.fore_obj = fore_obj
        self.bounds = bounds
        self.exits = exits
        self.entrance = entrance
        self.adjacent = adjacent
        self.non_player_characters = non_player_characters
        self.actionable = actionable
        self.width = width

        ##== Externally Used Variables ==##
        self.text = []

    def change_rooms(self,x,y,ROOMS):
        index = self.exits.index(((x+139)/32)+self.width*((y+139)/32))
        new_room = ROOMS[self.adjacent[index]]
        positions = self.entrance[index]
        return  (new_room,positions[0],positions[1])

    def display(self, surface, cadet):

        surface.fill((0,0,0))

        surface.blit(self.background, (-cadet.x, -cadet.y+10))

        for img in self.back_obj:
            surface.blit(img[0], (img[1]-cadet.x, img[2]-cadet.y))

        for cdt in self.non_player_characters:
            surface.blit(cdt.show_base(),(cdt.x-cadet.x, cdt.y-cadet.y))

        cadet.show(surface)

        for cdt in self.non_player_characters:
            surface.blit(cdt.show_top(), (cdt.x-cadet.x, cdt.y-cadet.y))

        for img in self.fore_obj:
            surface.blit(img[0], (img[1]-cadet.x, img[2]-cadet.y))

        cadet.status(surface)

        pygame.display.update()

    def cheap_display(self, surface, cadet):
        surface.blit(self.background, (-cadet.x, -cadet.y + 10))

        for img in self.back_obj:
            surface.blit(img[0], (img[1] - cadet.x, img[2] - cadet.y))

        for cdt in self.non_player_characters:
            surface.blit(cdt.show_base(), (cdt.x - cadet.x, cdt.y - cadet.y))

        cadet.show(surface)

        for cdt in self.non_player_characters:
            surface.blit(cdt.show_top(), (cdt.x-cadet.x, cdt.y-cadet.y))

        for img in self.fore_obj:
            surface.blit(img[0], (img[1] - cadet.x, img[2] - cadet.y))

        cadet.status(surface)

        return surface


    def getEvents(self, cadet, text_box, fpsClock, FPS, surface):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_f:
                return self.action(cadet,text_box, fpsClock, FPS, surface)

        buttons = pygame.key.get_pressed()

        if buttons[pygame.K_UP] or buttons[pygame.K_DOWN] or buttons[pygame.K_LEFT] or buttons[pygame.K_RIGHT]:
            self.move(buttons, cadet)
        else: cadet.pace = 0

        if ((cadet.x+139)/32+((cadet.y+139)/32)*self.width) in self.exits:
            return "Changing_Rooms"

        return "Moving"

    def move(self, buttons, cadet):
        print cadet.x
        print cadet.y
        cadet.pace += 1
        if (buttons[pygame.K_UP]):
            cadet.move_up(self.width, self.bounds)

        if (buttons[pygame.K_DOWN]):
            cadet.move_down(self.width, self.bounds)

        if (buttons[pygame.K_LEFT]):
            cadet.move_left(self.width, self.bounds)

        if (buttons[pygame.K_RIGHT]):
            cadet.move_right(self.width, self.bounds)

    def action(self, cadet, text_box, fpsClock, FPS, surface):
        X = (cadet.x + 149) / 32
        Y = (cadet.y + 145) / 32
        if cadet.face == 0:
            if (X + (Y - 1) * self.width) in self.actionable:
                i = self.actionable.index(X + (Y - 1) * self.width)
                self.non_player_characters[i].look_at(cadet.face)
                surface = self.cheap_display(surface, cadet)
                pygame.display.update()
                return self.non_player_characters[i].talk_to(text_box, fpsClock, FPS, surface)

        elif cadet.face == 1:
            if (X + (Y + 1) * self.width) in self.actionable:
                i = self.actionable.index(X + (Y + 1) * self.width)
                self.non_player_characters[i].look_at(cadet.face)
                surface = self.cheap_display(surface, cadet)
                pygame.display.update()
                return self.non_player_characters[i].talk_to(text_box, fpsClock, FPS, surface)

        elif cadet.face == 2:
            if (X - 1 + Y * self.width) in self.actionable:
                i = self.actionable.index(X - 1 + Y * self.width)
                self.non_player_characters[i].look_at(cadet.face)
                surface = self.cheap_display(surface, cadet)
                pygame.display.update()
                return self.non_player_characters[i].talk_to(text_box, fpsClock, FPS, surface)

        elif cadet.face == 3:
            if (X + 1 + Y * self.width) in self.actionable:
                i = self.actionable.index(X + 1 + Y * self.width)
                self.non_player_characters[i].look_at(cadet.face)
                surface = self.cheap_display(surface, cadet)
                pygame.display.update()
                return self.non_player_characters[i].talk_to(text_box, fpsClock, FPS, surface)

        else:
            return "Moving"

hallway = Room(pygame.image.load("surfaces/CADET_hall.png"),
           [[pygame.image.load("sprites/objects/CADET_door.png"),0,198],
            [pygame.image.load("sprites/objects/CADET_door.png"),0,486],
            [pygame.image.load("sprites/objects/CADET_door_stair1.png"),160,134]],
           [[pygame.image.load("sprites/objects/CADET_CCQ.png"),32,128]],
           [0, 1, 2, 3, 4, 5,
            6, 7, 8, 9,10, 11,
            12,13,14,15,16,17,
            18,19,         23,
            24,25,26,
            30,            35,
                           41,
            42,            47,
            48,            53,
            54,            59,
            60,            65,
            66,            71,
            72,            77,
            78,            83,
            84,            89,
                           95,
            96,            101,
            102,           107,
         108,109,110,111,112,113],
           [36,90,29],
           [[54,262,9],[-74,262,9],[-104,22,6]],
           [0,2,3],     #next room index
           [NPC(SpritePack_NPC(cadet_NPC),34,94,0,default_text)],
           [19],
            6)

barracks0 = Room(pygame.image.load("surfaces/CADET_room_a.png"),
           [[pygame.image.load("sprites/objects/CADET_desk.png"),31,92],
            [pygame.image.load("sprites/objects/CADET_desk.png"),192,92],
            [pygame.image.load("sprites/objects/CADET_bed.png"),38,220],
            [pygame.image.load("sprites/objects/CADET_bed.png"),198,220],
            [pygame.image.load("sprites/objects/CADET_sink.png"),224,288],
            [pygame.image.load("sprites/objects/CADET_drawers.png"),32,310]],
           [[pygame.image.load("sprites/objects/CADET_bed_front.png"),38,220],
            [pygame.image.load("sprites/objects/CADET_bed_front.png"),198,220],
            [pygame.image.load("sprites/objects/CADET_drawers_front.png"),32,310],
            [pygame.image.load("sprites/objects/CADET_wardrobe.png"),32,410],
            [pygame.image.load("sprites/objects/CADET_wardrobe.png"),96,410],
            [pygame.image.load("sprites/objects/CADET_wardrobe_v.png"),224,380]],
           [0, 1, 2, 3, 4, 5, 6, 7, 8,
            9,                     17,
           18,19,20,21,22,23,24,25,26,
           27,28,29,         33,34,35,
           36,37,                  44,
           45,                     53,
           54,                     62,
           63,64,65,         69,70,71,
           72,73,74,         78,79,80,
           81,                  88,89,
           90,91,92,93,            98,
           99,                    107,
           108,               115,116,
        117,118,119,120,121,122,124,125],
            [123],
            [[-104,54,6]],
            [1],    #next room index
            [NPC(SpritePack_NPC(cadet_NPC),34,128,0,default_text)],
            [37],
             9)

barracks1 = Room(pygame.image.load("surfaces/CADET_room_b.png"),
           [[pygame.image.load("sprites/objects/CADET_desk.png"),31,92],
            [pygame.image.load("sprites/objects/CADET_desk.png"),192,92],
            [pygame.image.load("sprites/objects/CADET_bed.png"),38,220],
            [pygame.image.load("sprites/objects/CADET_bed.png"),198,220],
            [pygame.image.load("sprites/objects/CADET_sink_b.png"),32,288],
            [pygame.image.load("sprites/decal/exit_down.png"),64,426]],
           [[pygame.image.load("sprites/objects/CADET_bed_front.png"),38,220],
            [pygame.image.load("sprites/objects/CADET_bed_front.png"),198,220]],
           [0, 1, 2, 3, 4, 5, 6, 7, 8,
            9,                     17,
           18,19,20,21,22,23,24,25,26,
           27,28,29,         33,34,35,
           36,37,                  44,
           45,                     53,
           54,                     62,
           63,64,65,         69,70,71,
           72,73,74,         78,79,80,
           81,82,                  89,
           90,                     98,
           99,                    107,
           108,                   116,
        117,118,120,121,122,123,124,125],
            [119],
            [[-104,342,6]],
            [1],    #next room index
            [NPC(SpritePack_NPC(cadet_NPC),34,128,1,default_text)],
             [37],
              9)

m1_stairwell = Room(pygame.image.load("surfaces/CADET_stairwell_ground.png"),
             [[pygame.image.load("sprites/decal/M1.png"),62,150]],
             [],
             [0, 1, 2, 3, 4, 5,
              6, 7, 8, 9,10,11,
             12,13,14,15,16,17,
             18,            23,
             24,            29,
             30,31,      34,35,
             36,            41,
             42,43,      46,47],
             [13,44,45],
             [[-10,-42,6],[118,-10,18],[118,-10,18]],
             [3, 7, 7],
             [blocker_001,cadet_001,blocker_002],
             [31,13,34],
              6)

m2_stairwell = Room(pygame.image.load("surfaces/CADET_stairwell_working.png"),
             [[pygame.image.load("sprites/decal/M2.png"),62,150]],
             [],
             [0, 1, 2, 3, 4, 5,
              6, 7, 8, 9,10,11,
             12,13,14,15,   17,
             18,            23,
             24,            29,
                            35,
             36,            41,
             42,43,44,45,46,47],
             [30,16],
             [[20,-10,6],[-106,-42,6]],
             [1,4],
             [basic_blocker],
             [13],
              6)

Mac_401 = Room(pygame.image.load("surfaces/CADET_room_a.png"),
           [[pygame.image.load("sprites/objects/CADET_desk.png"),31,92],
            [pygame.image.load("sprites/objects/CADET_desk.png"),192,92],
            [pygame.image.load("sprites/objects/CADET_bed.png"),38,220],
            [pygame.image.load("sprites/objects/CADET_bed.png"),198,220],
            [pygame.image.load("sprites/objects/CADET_sink.png"),224,288],
            [pygame.image.load("sprites/objects/CADET_drawers.png"),32,310]],
           [[pygame.image.load("sprites/objects/CADET_bed_front.png"),38,220],
            [pygame.image.load("sprites/objects/CADET_bed_front.png"),198,220],
            [pygame.image.load("sprites/objects/CADET_drawers_front.png"),32,310],
            [pygame.image.load("sprites/objects/CADET_wardrobe.png"),32,410],
            [pygame.image.load("sprites/objects/CADET_wardrobe.png"),96,410],
            [pygame.image.load("sprites/objects/CADET_wardrobe_v.png"),224,380]],
           [0, 1, 2, 3, 4, 5, 6, 7, 8,
            9,                     17,
           18,19,20,21,22,23,24,25,26,
           27,28,29,         33,34,35,
           36,37,                  44,
           45,                     53,
           54,                     62,
           63,64,65,         69,70,71,
           72,73,74,         78,79,80,
           81,                  88,89,
           90,91,92,93,            98,
           99,                    107,
           108,               115,116,
        117,118,119,120,121,122,124,125],
            [123],
            [[-104,54,6]],
            [1],    #next room index
            [Blocker(34,128,1)],
            [37],
             9)

home_room = Room(pygame.image.load("surfaces/HOME_room.png"),
                 [[pygame.image.load("sprites/objects/HOME_bed.png"),288,256],
                  [pygame.image.load("sprites/objects/HOME_tree.png"),36,296]],
                 [[pygame.image.load("sprites/objects/HOME_bed_front.png"),288,256],
                  [pygame.image.load("sprites/objects/HOME_tree_front.png"),36,296]],
                 [0 ,1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10,11,
                  12,                              23,
                  24,25,26,27,28,29,30,31,32,33,34,35,
                  36,37,38,39,40,41,42,43,44,45,46,47,
                  48,49,50,51,52,               58,59,
                  60,                        69,70,71,
                  72,                              83,
                  84,                              95,
                  96,                      105,106,107,
                  108,                     117,118,119,
                  120,121,                         131,
            132,133,134,135,136,137,138,139,140,141,142,143],
                 [57],
                 [[176,-42,13]],
                 [6],
                 [],
                 [],
                 12)

home_main = Room(pygame.image.load("surfaces/HOME_main.png"),
                 [[pygame.image.load("sprites/objects/box.png"),96,136]],
                 [[pygame.image.load("sprites/objects/HOME_table.png"),96,256],
                  [pygame.image.load("sprites/objects/HOME_counter.png"),32,160],
                  [pygame.image.load("sprites/objects/stair_bit.png"),279,111]],
                 [0 ,1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10,11,12,
                  13,                                 25,
                  26,27,28,29,30,31,32,33,34,35,36,37,38,
                  39,40,41,42,   44,45,46,            51,
                  52,      55,      58,59,60,61,      64,
                  65,66,67,68,      71,72,            77,
                  78,                                 90,
                  91,                                 103,
                  104,      107,108,                  116,
                  117,      120,121,                  129,
                  130,                                142,
            143,144,145,146,147,148,149,150,151,152,153,154
                  ],
                 [47],
                 [[120,6,12]],
                 [5],
                 [],#mother_home],
                 [],#42],
                  13)

sally_port = Room(pygame.image.load("surfaces/sally_port.png"),
                  [],
                  [],
                  [0  ,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12 ,13, 14, 15, 16,
                    18,                                                             34,
                    36,                                                             52,
                    54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
                    72, 73, 74,                                             86, 87, 88,
                    90,     92, 93,                                    103,104,    106,
                   108,    110,111,                                    121,122,    124,
                   126,    128,129,                                    139,140,    142,
                   144,    146,147,                                    157,158,    160,
                   162,    164,165,                                    175,176,    178,
                   180,    182,183,                                    193,194,    196,
                   198,    200,201,                                    211,212,    214,
                   216,    218,                                            230,    232,
                   234,    236,237,238,239,240,241,242,243,244,245,246,247,248,249,250],
                  [62],
                  [[-54,56,6]],
                  [4],
                  [cadet_000],
                  [62],
                  18)

ROOMS = [Mac_401, hallway, barracks1, m2_stairwell, m1_stairwell, home_room, home_main, sally_port]