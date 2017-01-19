import pygame, sys, shelve, story
from pygame.locals import *
from characters import *
from images import *
from room_data import *


class Option():
    def __init__(self, image, x):
        self.image = image
        self.x = x

    def show(self, surface, y):
        surface.blit(self.image, (self.x, y))


class Save(Option):
    def __init__(self, x):
        Option.__init__(self, pause_img, x)
        self.decision = 0

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

    def run(self, cadet, surface):
        saving = True
        loads = self.load_saves()
        while saving:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_f:
                        self.save(cadet, self.decision)
                        saving = False
                    if event.key == K_UP:
                        self.decision -= 1
                        self.decision %= 3
                    if event.key == K_DOWN:
                        self.decision += 1
                        self.decision %= 3
                    if event.key == K_ESCAPE or event.key == K_d:
                        saving = False

            surface.blit(save_menu, (75, 75))
            for slot in [0,1,2]:
                surface.blit(save_slot, (85, 97+slot*42))
                if loads[slot] == 0:
                    surface.blit(save_empty, (90, 101+slot*42))
            surface.blit(save_select, (81, 93+self.decision*42))

            pygame.display.update()
        return "Pause"

    def save(self, cadet, decision):
        # save values
        slot = shelve.open(story.saves[decision])
        slot["file"] = "has-file"
        slot["restore"] = story.restore_steps
        slot["decisions"] = story.decisions
        slot["room"] = story.current_room
        slot["cdt-x"] = cadet.x
        slot["cdt-y"] = cadet.y
        slot.close()
        return "Pause"


class Pack(Option):
    def __init__(self, x):
        Option.__init__(self, pack_img, x)

    def run(self, cadet, surface):
        return "Pause"

class Quit(Option):
    def __init__(self, x):
        Option.__init__(self, quit_img, x)

    def run(self, cadet, surface):
        return "Quit"
        #pygame.quit()
        #sys.exit()


class PauseMenu():
    def __init__(self):
        self.options = [Save(250), Pack(250), Quit(250)]
        self.top = pause_top
        self.mid = pause_mid
        self.bottom = pause_bottom
        self.pointer = 0

    def get_events(self, cadet, surface):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    self.pointer += 1
                if event.key == K_UP:
                    self.pointer -= 1
                if event.key == K_ESCAPE:
                    return "Moving"
                if event.key == K_f:
                    return self.options[self.pointer].run(cadet, surface)
        self.pointer %= len(self.options)
        return "Pause"

    def show(self, surface, backdrop):
        surface.blit(backdrop, (0,0))
        surface.blit(self.top, (250,0))
        i = 0
        for option in self.options:
            surface.blit(self.mid, (250, 20+20*i))
            option.show(surface,20+i*20)
            i += 1
        surface.blit(self.bottom, (250,len(self.options)*20+20))
        surface.blit(pause_select, (250, 20+20*self.pointer))

        pygame.display.update()

    def run(self, surface, cadet, backdrop):
        mode = "Pause"
        while mode == "Pause":
            mode = self.get_events(cadet, surface)
            self.show(surface, backdrop)

        print mode
        return mode














