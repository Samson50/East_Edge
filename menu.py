import pygame, sys, shelve
from pygame.locals import *
from room_data import *
from images import *

class Menu:
    def __init__(self, surface):
        self.surface = surface
        self.menu = emblem
        self.logo = logo
        self.fade_white = pygame.image.load("surfaces/fade_white.png").convert()
        self.decision = 0
        self.slots = 3
        self.files = ["saves/slot1","saves/slot2","saves/slot3"]

    def run(self, fpsClock):
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
                    return "Moving"
                if self.decision == 1:
                    return "Loading"

        if pygame.mouse.get_pressed()[0]:
            if menu_play.get_rect(topleft = (30,230)).collidepoint(mouse_x, mouse_y):
                self.fade_to_white(fpsClock)
                return "Moving"
            elif menu_load.get_rect(topleft = (170,230)).collidepoint(mouse_x,mouse_y):
                return "Loading"
            else:
                return "Menu"
        else:
            return "Menu"

    def start_game(self):
        #self.room = home_main
        #self.width = 13 #self.cadet.x = 0; self.cadet.y = 32
        # return room, x, and y
        return (sally_port, 160, 160)

    def run_load(self, fpsClock, slots):
        self.surface.fill((0, 0, 0))
        for slot in range(0,self.slots):
            self.surface.blit(load_tile, (20, 20+90*slot))
            if slots[slot] == 0:
                self.surface.blit(empty_tile, (20, 20+90*slot))
        self.surface.blit(load_select, (19, 19+90*self.decision))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_d:
                return "Menu"
            if event.type == KEYDOWN and event.key == K_UP:
                self.decision -= 1
            if event.type == KEYDOWN and event.key == K_DOWN:
                self.decision += 1
            self.decision %= 3
            if event.type == KEYDOWN and event.key == K_f:
                return "Moving"

        if pygame.mouse.get_pressed()[0]:
            return "Loading"

        else:
            return "Loading"

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
            story.decisions = save["decisions"]
            story.current_save = self.decision
            ret = (ROOMS[save["room"]], save["cdt-x"], save["cdt-y"])
            save.close()
            return ret


