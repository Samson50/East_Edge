import pygame, sys, shelve
from pygame.locals import *
from room_data import *
from images import *

class Menu:
    def __init__(self, surface, fpsClock):
        self.mode = "Menu"
        self.room_manager = Room_Manager(ROOMS, fpsClock, surface)
        self.surface = surface
        self.menu = emblem
        self.logo = logo
        self.fade_white = fade_white.convert()
        self.decision = 0
        self.slots = 3
        self.saves = self.load_saves()
        self.files = ["saves/slot1","saves/slot2","saves/slot3"]

    def run(self, fpsClock, cadet):
        while self.mode == "Menu":
            self.surface.fill((0,0,0))
            self.surface.blit(self.menu, (2, 16))
            self.surface.blit(self.logo, (0,0))
            self.surface.blit(menu_select, (25+self.decision*140,225))
            self.decision %= 2
            self.surface.blit(menu_play, (30,230))
            self.surface.blit(menu_load, (170,230))
            (mouse_x, mouse_y) = pygame.mouse.get_pos()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_RIGHT:
                    self.decision += 1
                if event.type == KEYDOWN and event.key == K_LEFT:
                    self.decision -= 1
                if event.type == KEYDOWN and event.key == K_f:
                    if self.decision == 0:
                        self.fade_to_white(fpsClock)
                        self.mode = self.play_game(fpsClock, cadet)
                    if self.decision == 1:
                        self.mode = self.load_game(fpsClock, cadet)

        return self.mode

    def start_game(self):
        #self.room = home_main
        #self.width = 13 #self.cadet.x = 0; self.cadet.y = 32
        # return room, x, and y
        return (sally_port, 160, 160)

    def play_game(self, fpsClock, cadet):
        self.mode = "Moving"
        while self.mode == "Moving":
            self.mode = self.room_manager.getEvents(cadet, fpsClock, 70, self.surface)
            self.room_manager.display(self.surface, cadet)
            self.mode = self.room_manager.npc_action(self.mode,fpsClock,cadet,self.surface)
            fpsClock.tick(70)

    def load_game(self, fpsClock, cadet):
        self.mode = "Loading"
        while self.mode == "Loading":
            self.mode = self.run_load(fpsClock)
            fpsClock.tick(70)

        if self.mode == "Moving":
            (self.room_manager.room, cadet.x, cadet.y) = self.load_slot()
            return self.play_game(fpsClock, cadet)


    def run_load(self, fpsClock):
        self.surface.fill((0, 0, 0))
        for slot in range(0,self.slots):
            self.surface.blit(load_tile, (20, 20+90*slot))
            if self.saves[slot] == 0:
                self.surface.blit(empty_tile, (20, 20+90*slot))
        self.surface.blit(load_select, (19, 19+90*self.decision))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_d:
                self.mode = "Menu"
            if event.type == KEYDOWN and event.key == K_UP:
                self.decision -= 1
            if event.type == KEYDOWN and event.key == K_DOWN:
                self.decision += 1
            self.decision %= 3
            if event.type == KEYDOWN and event.key == K_f:
                self.mode = "Moving"

        return self.mode

    def fade_to_white(self, fpsClock):
        counter = 0

        while (counter < 30):
            self.fade_white.set_alpha((255/29)*counter)
            self.surface.blit(self.fade_white, (0,0))
            fpsClock.tick(30)
            pygame.display.update()
            counter += 1

    def load_slot(self):
        save = shelve.open(self.files[self.decision])
        if save["file"] == "no_save":
            print "defaults"
            story.decisions = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
            story.current_room = 7
            story.current_save = self.decision
            save.close()
            return (sally_port, 120, 86)

        else:
            story.restore_steps = save["restore"]
            for step in story.restore_steps:
                change = step.split(":")
                if change[0] == "N":
                    print "got it"
                    ## Move action
                    ROOMS[int(change[1])].non_player_characters[ROOMS[int(change[1])].actionable.index(int(change[2]))].x = int(change[4])
                    ROOMS[int(change[1])].non_player_characters[ROOMS[int(change[1])].actionable.index(int(change[2]))].y = int(change[5])
                    ROOMS[int(change[1])].actionable[ROOMS[int(change[1])].actionable.index(int(change[2]))] = int(change[3])
                    ## Move bound
                    del ROOMS[int(change[1])].bounds[ROOMS[int(change[1])].bounds.index(int(change[2]))]
                    ROOMS[int(change[1])].bounds.append(int(change[3]))
                if change[0] == "R":
                    del ROOMS[int(change[1])].non_player_characters[int(change[2])]
                    del ROOMS[int(change[1])].actionable[int(change[2])]
                    if len(change) == 4:
                        del ROOMS[int(change[1])].bounds[int(change[3])]
            story.decisions = save["decisions"]
            story.current_save = self.decision
            story.current_room = save["room"]
            ret = (ROOMS[save["room"]], save["cdt-x"], save["cdt-y"])
            save.close()
            return ret
    def load_saves(self):
        slot1 = shelve.open("saves/slot1")
        slot2 = shelve.open("saves/slot2")
        slot3 = shelve.open("saves/slot3")
        slots = [slot1, slot2, slot3]
        loads = [0, 0, 0]

        for slot in [0,1,2]:
            try:
                if slots[slot]["file"] == "no_save":
                    loads[slot] = 0
                else:
                    loads[slot] = 1
                slots[slot].close()
            except KeyError:
                slots[slot]["file"] = "no_save"
                slots[slot].close()
                loads[slot] = 0
        return loads


