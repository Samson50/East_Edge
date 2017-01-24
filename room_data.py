import pygame, sys
from pygame.locals import *
from character_data import *
from images import *
from pause import *


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

class Room_Manager:
    def __init__(self, room_list, fpsClock, surface):
        self.text_box = TextBox(surface)
        self.pause_menu = PauseMenu()
        self.fpsClock = fpsClock
        self.room_list = room_list
        self.room = room_list[0]
        self.direction = 0
        self.move_counter = 0
        self.tick = 0
        self.keys = []
        self.fade = fade.convert()

        ##== Externally Used Variables ==##
        self.text = []

    def change_rooms(self, cadet, ROOMS, surface):
        fade_count = 0
        while fade_count < 510:
            fade_count += 5
            if fade_count < 255:
                self.fade.set_alpha(fade_count)
            elif (fade_count == 255):
                self.move_counter = 0
                index = self.room.exits.index(((cadet.x + 139) / 32) + self.room.width * ((cadet.y + 139) / 32))
                story.current_room = self.room.adjacent[index]
                (cadet.x, cadet.y, burn) = self.room.entrance[index]
                self.room = self.room_list[story.current_room]

            elif (fade_count > 255 and fade_count < 510):
                self.fade.set_alpha(510 - fade_count)

            self.cheap_display(surface, cadet)
            surface.blit(self.fade, (0, 0))

            pygame.display.update()
            self.fpsClock.tick(70)


    def display(self, surface, cadet):
        surface.fill((0,0,0))
        surface.blit(self.room.background, (-cadet.x, -cadet.y+10))
        for img in self.room.back_obj:
            surface.blit(img[0], (img[1]-cadet.x, img[2]-cadet.y))
        for cdt in self.room.non_player_characters:
            surface.blit(cdt.show_base(),(cdt.x-cadet.x, cdt.y-cadet.y))
        cadet.show(surface)
        for cdt in self.room.non_player_characters:
            surface.blit(cdt.show_top(), (cdt.x-cadet.x, cdt.y-cadet.y))
        for img in self.room.fore_obj:
            surface.blit(img[0], (img[1]-cadet.x, img[2]-cadet.y))
        cadet.status(surface)
        pygame.display.update()

    def cheap_display(self, surface, cadet):
        surface.blit(self.room.background, (-cadet.x, -cadet.y + 10))
        for img in self.room.back_obj:
            surface.blit(img[0], (img[1] - cadet.x, img[2] - cadet.y))
        for cdt in self.room.non_player_characters:
            surface.blit(cdt.show_base(), (cdt.x - cadet.x, cdt.y - cadet.y))
        cadet.show(surface)
        for cdt in self.room.non_player_characters:
            surface.blit(cdt.show_top(), (cdt.x-cadet.x, cdt.y-cadet.y))
        for img in self.room.fore_obj:
            surface.blit(img[0], (img[1] - cadet.x, img[2] - cadet.y))
        cadet.status(surface)
        return surface


    def getEvents(self, cadet, fpsClock, FPS, surface):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return self.pause_menu.run(surface, cadet, pygame.transform.smoothscale(surface, (300,300)))

            if event.type == KEYDOWN and event.key == K_f:
                return self.action(cadet, fpsClock, FPS, surface)

            if event.type == KEYDOWN and event.key in [K_LEFT, K_DOWN, K_UP, K_RIGHT]:
                self.keys.insert(0, event.key)

            if event.type == KEYUP and event.key in [K_LEFT, K_DOWN, K_UP, K_RIGHT]:
                try:
                    self.keys.remove(event.key)
                except:
                    print "KEY ERROR"

        self.tick += 1
        self.tick %= 8

        if self.tick == 0 and self.move_counter == 0:
            if self.keys != []:
                if self.move_counter == 0:
                    self.move_counter = 16
                    self.direction = self.keys[0]
            else:
                self.direction = 0

        if self.move_counter != 0:
            self.move_counter -= 1
            self.move(cadet)
        else:
            cadet.pace = 0

        if ((cadet.x+139)/32+((cadet.y+139)/32)*self.room.width) in self.room.exits:
            self.keys = []
            self.direction = 0
            self.tick = 0
            self.move_counter = 0
            self.change_rooms(cadet, self.room_list, surface)

        return "Moving"

    def move(self, cadet):
        cadet.pace += 1
        if (self.direction == pygame.K_UP):
            cadet.move_up(self.room.width, self.room.bounds)
        if (self.direction == pygame.K_DOWN):
            cadet.move_down(self.room.width, self.room.bounds)
        if (self.direction == pygame.K_LEFT):
            cadet.move_left(self.room.width, self.room.bounds)
        if (self.direction == pygame.K_RIGHT):
            cadet.move_right(self.room.width, self.room.bounds)

    def action(self, cadet, fpsClock, FPS, surface):
        X = (cadet.x + 149) / 32
        Y = (cadet.y + 145) / 32
        if cadet.face == 0:
            if (X + (Y - 1) * self.room.width) in self.room.actionable:
                i = self.room.actionable.index(X + (Y - 1) * self.room.width)
                self.room.non_player_characters[i].look_at(cadet.face)
                surface = self.cheap_display(surface, cadet)
                pygame.display.update()
                return self.room.non_player_characters[i].talk_to(self.text_box, fpsClock, FPS, surface, cadet)
            else: return "Moving"

        elif cadet.face == 1:
            if (X + (Y + 1) * self.room.width) in self.room.actionable:
                i = self.room.actionable.index(X + (Y + 1) * self.room.width)
                self.room.non_player_characters[i].look_at(cadet.face)
                surface = self.cheap_display(surface, cadet)
                pygame.display.update()
                return self.room.non_player_characters[i].talk_to(self.text_box, fpsClock, FPS, surface, cadet)
            else: return "Moving"

        elif cadet.face == 2:
            if (X - 1 + Y * self.room.width) in self.room.actionable:
                i = self.room.actionable.index(X - 1 + Y * self.room.width)
                self.room.non_player_characters[i].look_at(cadet.face)
                surface = self.cheap_display(surface, cadet)
                pygame.display.update()
                return self.room.non_player_characters[i].talk_to(self.text_box, fpsClock, FPS, surface, cadet)
            else: return "Moving"

        elif cadet.face == 3:
            if (X + 1 + Y * self.room.width) in self.room.actionable:
                i = self.room.actionable.index(X + 1 + Y * self.room.width)
                self.room.non_player_characters[i].look_at(cadet.face)
                surface = self.cheap_display(surface, cadet)
                pygame.display.update()
                return self.room.non_player_characters[i].talk_to(self.text_box, fpsClock, FPS, surface, cadet)
            else: return "Moving"

        else:
            return "Moving"

    def npc_action(self, mode, fpsClock, cadet, surface):
        self.mode = mode
        while self.mode != "Moving" and self.mode != "Loading" and self.mode != "Quit":
            if self.mode == "Cut_Scene":
                self.cut_scene(fpsClock, 70, cadet, surface)
            if self.mode == "Talking":
                print "talking"
        return self.mode



    def cut_scene(self, fpsClock, FPS, cadet, surface):
        print "cutting"
        directions = cut_scenes[story.current_scene]
        cut_scene_counter = 0
        while self.mode == "Cut_Scene":
            # step is the individual section of the scene
            step = directions[0][cut_scene_counter]
            # each action is an instruction to be performed during that section
            for action in step.split(" "):

                ##== Move NPC Action ==##
                if action[0] == 'N':
                    change = action.split(":")
                    ## Move action
                    self.room.actionable[self.room.actionable.index(int(change[1]))] = int(change[2])
                    ## Move bound
                    del self.room.bounds[self.room.bounds.index(int(change[1]))]
                    self.room.bounds.append(int(change[2]))

                ##== Remove NPC from Room ==##
                if action[0] == 'R':
                    change = action.split(":")
                    # Delete actionable
                    del self.room.actionable[int(change[1])]
                    # Delete character
                    del self.room.non_player_characters[int(change[1])]
                    if len(change) == 3:
                        del self.room.bounds[self.room.bounds.index(int(change[2]))]

                ##== Move Player ==##
                if action[0] == 'M':
                    d = action.split(":")[1]
                    if (d == "d"):
                        cadet.move_down(self.room.width, self.room.bounds)
                    elif (d == "u"):
                        cadet.move_up(self.room.width, self.room.bounds)
                    elif (d == "r"):
                        cadet.move_right(self.room.width, self.room.bounds)
                    elif (d == "l"):
                        cadet.move_left(self.room.width, self.room.bounds)

                ##== Move NPC ==##
                if action[0] in ["0", "1", "2", "3", "4", "5"]:
                    direction = action.split(":")
                    if (direction[1] == 'r' or direction[1] == 'l' or direction[1] == 'u' or direction[1] == 'd'):
                        self.room.non_player_characters[int(direction[0])].move(direction[1])
                    if (direction[1] == 'f'):
                        self.room.non_player_characters[int(direction[0])].look_at(int(direction[2]))

                ##== Talk to NPC ==##
                if action[0] == 'T':
                    #TODO: Needs to be able to edit the current directions to effect cutscene follow on
                    #TODO: Also needs to be the last direction
                    direction = action.split(":")
                    self.mode = self.room.non_player_characters[int(direction[1])].talk_to(self.text_box, fpsClock, FPS, surface, cadet)


                ##== Change Rooms ==##
                if (action[0] == 'C'):
                    change = action.split(":")
                    while (self.fade_count < 510):
                        self.fade_count += 5
                        if (self.fade_count < 255):
                            self.fade.set_alpha(self.fade_count)
                        elif (self.fade_count == 255):
                            self.room = self.room_list[int(change[1])]
                            cadet.x = int(change[2])
                            cadet.y = int(change[3])
                        elif (self.fade_count > 255 and self.fade_count < 510):
                            self.fade.set_alpha(510 - self.fade_count)
                        self.cheap_display(surface, cadet)
                        surface.blit(self.fade, (0, 0))

                        pygame.display.update()
                        fpsClock.tick(FPS)

                    self.fade_count = 0

                ##== Do Things with Objects ==##
                if (action[0] == 'O'):
                    stuff = action.split(":")
                    if action[1] == 'F':
                        if action[2] == 'R':
                            del self.room.fore_obj[(int(stuff[1]))]

                            # if action[1] == 'B':

            cut_scene_counter += 1
            if cut_scene_counter >= len(directions[0]):  # make 32 class variable
                story.restore_steps += directions[1]
                self.mode = "Moving"

            self.display(surface, cadet)
            pygame.display.update()

            fpsClock.tick(FPS)
        return self.mode



hallway0 = Room(hallway,
           [[door_barracks,0,198],
            [door_barracks,0,486],
            [door_stairwell,160,134]],
           [[CCQ,32,128]],
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
           [NPC(cadet_npc,34,94,0,default_text)],
           [19],
            6)

barracks0 = Room(barracks_a,
           [[cadet_desk,31,92],
            [cadet_desk,192,92],
            [cadet_bed,38,220],
            [cadet_bed,198,220],
            [cadet_sink,224,288],
            [cadet_drawers,32,310]],
           [[cadet_bed_front,38,220],
            [cadet_bed_front,198,220],
            [cadet_drawers_front,32,310],
            [cadet_wardrobe_h,32,410],
            [cadet_wardrobe_h,96,410],
            [cadet_wardrobe_v,224,380]],
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
            [NPC(cadet_npc,34,128,0,default_text)],
            [37],
             9)

barracks1 = Room(barracks_b,
           [[cadet_desk,31,92],
            [cadet_desk,192,92],
            [cadet_bed,38,220],
            [cadet_bed,198,220],
            [cadet_sink,32,288],
            [exit_down,64,426]],
           [[cadet_bed_front,38,220],
            [cadet_bed_front,198,220]],
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
            [NPC(cadet_npc,34,128,1,default_text)],
             [37],
              9)

m2_stairwell = Room(stairwell,
             [[decal_m2,62,150]],
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

Mac_401 = Room(barracks_a,
           [[cadet_desk,31,92],
            [cadet_desk,192,92],
            [cadet_bed,38,220],
            [cadet_bed,198,220],
            [cadet_sink,224,288],
            [cadet_drawers,32,310]],
           [[cadet_bed_front,38,220],
            [cadet_bed_front,198,220],
            [cadet_drawers_front,32,310],
            [cadet_wardrobe_h,32,410],
            [cadet_wardrobe_h,96,410],
            [cadet_wardrobe_v,224,380]],
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

home_room = Room(home_player,
                 [[home_bed,288,256],
                  [home_tree,36,296]],
                 [[home_bed_front,288,256],
                  [home_tree_front,36,296]],
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

home_main0 = Room(home_main,
                 [[box,96,136]],
                 [[home_table_front,96,256],
                  [home_counter_front,32,160],
                  [home_stair_bit,279,111]],
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

m1_stairwell = Room(stairwell_ground,
             [[decal_m1,62,150]],
             [],
             [0, 1, 2, 3, 4, 5, 6,
              7, 8, 9,10,11,12,13,
             14,15,16,17,18,19,20,
             21,               27,
             28,               34,
             35,36,         40,41,
             42,               48,
             49,50,51,   53,54,55],
             [15,52],
             [[-10,-42,6],[118,-10,18],[118,-10,18]],
             [3, 7],
             [blocker_001,cadet_001,blocker_002],
             [36,15,40],
              7)

sally_port = Room(sally_port_img,
                  [],
                  [],
                  [0  ,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12 ,13, 14, 15, 16,
                    18,                                                             34,
                    36,                                                             52,
                    54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
                    72, 73, 74,                                             86, 87, 88,
                    90,     92, 93,                                    103,104,    106,
                   108,    110,111,                                    121,122,    124,
                   126,    128,129,130,                                139,140,    142,
                   144,    146,147,148,                                157,158,    160,
                   162,    164,165,                                    175,176,    178,
                   180,    182,183,                                    193,194,    196,
                   198,    200,201,                                    211,212,    214,
                   216,    218,                                            230,    232,
                   234,    236,237,238,239,240,241,242,243,244,245,246,247,248,249,250],
                  [62],
                  [[-42,54,7]],
                  [4],
                  [cadet_000, NPC(female_white_ginger,131,213,1,blocker_text),NPC(female_white_brown,131,245,0,blocker_text)],
                  [62,130,148],
                  18)

ROOMS = [Mac_401, hallway0, barracks1, m2_stairwell, m1_stairwell, home_room, home_main0, sally_port]